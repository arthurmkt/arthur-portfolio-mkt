#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Escopos e números de um vídeo, por cena — base do /editar-video.

Uso:
  python escopos.py VIDEO [-o PASTA] [--limiar 10] [--amostra 5] [--cenas 0-3.2,3.2-8]
                          [--sdr] [--pele x,y,w,h]

Saídas em PASTA (padrão: <video>_diag/):
  diagnostico.json  — números por cena (signalstats + medidas próprias)
  diagnostico.md    — tabela legível + alertas com a regra e a fonte
  folha_escopos.png — por cena: quadro do meio | waveform Y | parade RGB | vectorscope c/ linha de pele | histograma

Os escopos são desenhados aqui a partir dos valores Y'CbCr do quadro (não do PNG convertido),
então mostram os códigos reais do arquivo. As referências de cada limite estão em LIMITES.
"""
import argparse
import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Limites — cada número com a fonte. Valores em código 8 bits (10 bits = x4).
# ---------------------------------------------------------------------------
LIMITES = {
    "preto_nominal": 16,      # ITU-R BT.709-6, Parte 2, item 6.10 (quantização: preto = 16, branco = 235, croma 16–240, 8 bits)
    "branco_nominal": 235,    # idem
    "croma_min": 16,
    "croma_max": 240,
    # EBU R103 v3.0 (maio/2020), Tabela 1: faixa preferida 5–246 (8 bits) / 20–984 (10 bits) para Y e para R, G, B;
    # total 1–254. Só é "fora do gamut" se mais de 1% da área da imagem sair da faixa preferida (medida filtrada).
    # A versão de 2000 (Y -1%..103%, RGB -5%..105%) foi substituída; ainda aparece em specs antigas.
    "ebu_y_min": 5,
    "ebu_y_max": 246,
    "ebu_rgb_min_pct": (5 - 16) / 219 * 100,    # = -5,0%
    "ebu_rgb_max_pct": (246 - 16) / 219 * 100,  # = 105,0%
    # Linha de tom de pele (eixo I do NTSC) a 123° no vectorscope — Van Hurkman, Color Correction Handbook;
    # Adobe "Skin Tone Line" no Vectorscope YUV do Lumetri. Faixa de tolerância: ver referencias/pele.md.
    "pele_angulo": 123.0,
    # EBU R103 v3.0: tolera até 1% da área fora da faixa preferida.
    "area_fora_pct": 1.0,
    # Máscara de pele estimada: Cb 77–127, Cr 133–173 (Chai & Ngan, IEEE TCSVT 1999). Heurística: pega madeira,
    # laranja e bege também. Serve para conferir, não para decidir sozinha.
    "pele_cb": (77, 127),
    "pele_cr": (133, 173),
}

KR, KB = 0.2126, 0.0722  # BT.709 (ITU-R BT.709-6, Parte 1, item 3.2)
KG = 1 - KR - KB

FONT_PATHS = ["/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Helvetica.ttc",  # macOS
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "C:/Windows/Fonts/arial.ttf"]  # Linux, Windows


def fonte(tam):
    for p in FONT_PATHS:
        if os.path.exists(p):
            return ImageFont.truetype(p, tam)
    return ImageFont.load_default()


# ---------------------------------------------------------------------------
# ffprobe / extração
# ---------------------------------------------------------------------------
def probe(video):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height,pix_fmt,r_frame_rate,avg_frame_rate,color_range,color_space,color_transfer,"
         "color_primaries,bits_per_raw_sample:stream_side_data=rotation:format=duration",
         "-of", "json", str(video)], capture_output=True, text=True, check=True).stdout
    d = json.loads(out)
    s = d["streams"][0]
    num, den = s.get("avg_frame_rate", s["r_frame_rate"]).split("/")
    fps = float(num) / float(den) if float(den) else 30.0
    pf = s.get("pix_fmt", "")
    bits = 10 if ("10" in pf or "p010" in pf) else (12 if "12" in pf else 8)
    rot = 0
    for sd in s.get("side_data_list", []) or []:
        if "rotation" in sd:
            rot = int(sd["rotation"])
    return {
        "largura": s["width"], "altura": s["height"], "pix_fmt": pf, "bits": bits, "fps": round(fps, 3),
        "duracao": float(d["format"]["duration"]), "range": s.get("color_range", "unknown"),
        "matriz": s.get("color_space", "unknown"), "transferencia": s.get("color_transfer", "unknown"),
        "primarias": s.get("color_primaries", "unknown"), "rotacao": rot,
    }


# Medido 05/11/2026 em patches HLG sintéticos: cinza 18% → 43,4% SDR, branco ref. 75% HLG → 88,6%, 100% HLG → 99,1%.
# A cadeia antiga (npl=100) punha o cinza 18% em 58% (médios/pele claros demais). Ref.: ITU-R BT.2408, BT.2446.
TONEMAP_HLG = "zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:param=0.7:desat=0:peak=4.926,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"


def eh_hdr(info):
    return info["transferencia"] in ("arib-std-b67", "smpte2084")


def extrair_quadro_ycbcr(video, t, largura=480, pre=None):
    """Quadro em t como arrays float Y, Cb, Cr em escala de código 8 bits (sem conversão de faixa)."""
    vf = []
    if pre:
        vf.append(pre)
    if largura:
        vf.append(f"scale={largura}:-2:flags=area")
    vf.append("format=yuv444p16le")
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1",
           "-vf", ",".join(vf), "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    arr = np.frombuffer(raw, dtype="<u2").astype(np.float32) / 256.0
    n = arr.size // 3
    if largura:
        w = largura
    else:
        w = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                "stream=width", "-of", "csv=p=0", str(video)],
                               capture_output=True, text=True).stdout.strip().split(",")[0])
    h = n // w
    arr = arr[: 3 * w * h].reshape(3, h, w)
    return arr[0], arr[1], arr[2]


def ycbcr_para_rgb_pct(Y, Cb, Cr):
    """Y'CbCr faixa limitada (8 bits) → R'G'B' em % (0 = preto 16, 100 = branco 235). BT.709."""
    y = (Y - 16.0) / 219.0
    cb = (Cb - 128.0) / 224.0
    cr = (Cr - 128.0) / 224.0
    r = y + 2 * (1 - KR) * cr
    b = y + 2 * (1 - KB) * cb
    g = (y - KR * r - KB * b) / KG
    return r * 100, g * 100, b * 100


# ---------------------------------------------------------------------------
# Passada única: cortes (scdet em baixa resolução) + signalstats (amostrado, resolução cheia)
# ---------------------------------------------------------------------------
def analisar(video, pasta, limiar=10.0, amostra=5.0, pre=None):
    pasta.mkdir(parents=True, exist_ok=True)
    pre_f = (pre + ",") if pre else ""
    fc = (f"[0:v]{pre_f}split=2[a][b];"
          f"[a]scale=320:-2,scdet=t={limiar},metadata=mode=print:key=lavfi.scd.time:file=cortes.txt[oa];"
          f"[b]fps={amostra},signalstats=stat=brng,metadata=mode=print:file=stats.txt[ob]")
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(Path(video).resolve()), "-filter_complex", fc,
           "-map", "[oa]", "-f", "null", "-", "-map", "[ob]", "-f", "null", "-"]
    subprocess.run(cmd, cwd=pasta, check=True)

    cortes = []
    txt = (pasta / "cortes.txt").read_text(encoding="utf-8", errors="ignore") if (pasta / "cortes.txt").exists() else ""
    for m in re.finditer(r"lavfi\.scd\.time=([\d.]+)", txt):
        cortes.append(float(m.group(1)))

    quadros = []
    atual = None
    for linha in (pasta / "stats.txt").read_text(encoding="utf-8", errors="ignore").splitlines():
        m = re.match(r"frame:\d+\s+pts:\d+\s+pts_time:([\d.]+)", linha)
        if m:
            atual = {"t": float(m.group(1))}
            quadros.append(atual)
            continue
        m = re.match(r"lavfi\.signalstats\.(\w+)=([-+\d.eE]+)", linha)
        if m and atual is not None:
            atual[m.group(1)] = float(m.group(2))
    return sorted(set(round(c, 3) for c in cortes)), quadros


def agrupar_cortes(cortes, janela=0.3):
    """scdet marca vários quadros seguidos num mesmo corte/transição; fica o primeiro de cada grupo."""
    grupos = []
    for c in sorted(cortes):
        if grupos and c - grupos[-1][-1] <= janela:
            grupos[-1].append(c)
        else:
            grupos.append([c])
    return [g[0] for g in grupos]


def montar_cenas(cortes, duracao, minimo=0.4):
    cortes = agrupar_cortes(cortes)
    pts = [0.0] + [c for c in cortes if minimo < c < duracao - minimo] + [duracao]
    cenas = []
    for a, b in zip(pts, pts[1:]):
        if b - a >= minimo:
            cenas.append((round(a, 3), round(b, 3)))
    return cenas


def agregar(quadros, a, b, escala):
    q = [x for x in quadros if a <= x["t"] < b] or [min(quadros, key=lambda x: abs(x["t"] - (a + b) / 2))]
    def col(k):
        return np.array([x.get(k, np.nan) for x in q], dtype=float)
    s = escala
    r = {
        "quadros_medidos": len(q),
        "YMIN": float(np.nanmin(col("YMIN")) / s), "YLOW": float(np.nanmean(col("YLOW")) / s),
        "YAVG": float(np.nanmean(col("YAVG")) / s), "YHIGH": float(np.nanmean(col("YHIGH")) / s),
        "YMAX": float(np.nanmax(col("YMAX")) / s),
        "UAVG": float(np.nanmean(col("UAVG")) / s), "VAVG": float(np.nanmean(col("VAVG")) / s),
        "SATAVG": float(np.nanmean(col("SATAVG")) / s), "SATHIGH": float(np.nanmean(col("SATHIGH")) / s),
        "SATMAX": float(np.nanmax(col("SATMAX")) / s),
        "HUEMED": float(np.nanmedian(col("HUEMED"))),
        "BRNG_pct": float(np.nanmean(col("BRNG")) * 100) if "BRNG" in q[0] else None,
    }
    return {k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items()}


def pct(y):
    return (y - 16) / 219 * 100


# ---------------------------------------------------------------------------
# Medidas sobre o quadro (escopos numéricos)
# ---------------------------------------------------------------------------
def medidas_quadro(Y, Cb, Cr, regiao_pele=None):
    R, G, B = ycbcr_para_rgb_pct(Y, Cb, Cr)
    yflat = Y.ravel()
    ordem = np.argsort(yflat)
    n = yflat.size
    k = max(1, n // 20)
    alto = ordem[-k:]
    baixo = ordem[:k]
    rf, gf, bf = R.ravel(), G.ravel(), B.ravel()
    fora_rgb = ((R < LIMITES["ebu_rgb_min_pct"]) | (R > LIMITES["ebu_rgb_max_pct"]) |
                (G < LIMITES["ebu_rgb_min_pct"]) | (G > LIMITES["ebu_rgb_max_pct"]) |
                (B < LIMITES["ebu_rgb_min_pct"]) | (B > LIMITES["ebu_rgb_max_pct"]))
    m = {
        # Preto/branco efetivos: percentis 0,1% e 99,9% (ignora pixel isolado de ruído/nitidez)
        "Y_p01": round(float(np.percentile(yflat, 0.1)), 1),
        "Y_p999": round(float(np.percentile(yflat, 99.9)), 1),
        "Y_fora_16_235_pct": round(float(((yflat < 16) | (yflat > 235)).mean() * 100), 3),
        # Equilíbrio nas altas e nas baixas: neutro = R≈G≈B (parade alinhado). Diferença em pontos de %.
        "altas_RGB": [round(float(rf[alto].mean()), 1), round(float(gf[alto].mean()), 1), round(float(bf[alto].mean()), 1)],
        "baixas_RGB": [round(float(rf[baixo].mean()), 1), round(float(gf[baixo].mean()), 1), round(float(bf[baixo].mean()), 1)],
        "fora_gamut_rgb_pct": round(float(fora_rgb.mean() * 100), 2),
    }
    # Pele
    cbp, crp = LIMITES["pele_cb"], LIMITES["pele_cr"]
    if regiao_pele:
        h, w = Y.shape
        x, y, ww, hh = regiao_pele
        sl = (slice(int(y * h), int((y + hh) * h)), slice(int(x * w), int((x + ww) * w)))
        mask = np.zeros_like(Y, dtype=bool)
        mask[sl] = True
        origem = "região informada"
    else:
        mask = (Cb >= cbp[0]) & (Cb <= cbp[1]) & (Cr >= crp[0]) & (Cr <= crp[1]) & (Y > 40) & (Y < 230)
        origem = "máscara estimada Chai & Ngan (confira no quadro)"
    frac = float(mask.mean())
    if frac > 0.003:
        u = Cb[mask] - 128
        v = Cr[mask] - 128
        ang = np.degrees(np.arctan2(v, u)) % 360
        sat = np.hypot(u, v)
        m["pele"] = {
            "origem": origem, "area_pct": round(frac * 100, 1),
            "angulo_mediano": round(float(np.median(ang)), 1),
            "desvio_da_linha": round(float(np.median(ang) - LIMITES["pele_angulo"]), 1),
            "croma_mediana": round(float(np.median(sat)), 1),
            "Y_mediano_pct": round(float(pct(np.median(Y[mask]))), 1),
        }
    else:
        m["pele"] = None
    return m


# ---------------------------------------------------------------------------
# Desenho dos escopos (numpy → PIL)
# ---------------------------------------------------------------------------
H_SCOPE = 256


def _wave(canal, alt=H_SCOPE, larg=None, vmin=0.0, vmax=255.0, cor=(255, 255, 255)):
    h, w = canal.shape
    larg = larg or w
    xs = (np.arange(w) * larg // w)
    xs = np.broadcast_to(xs, (h, w)).ravel()
    ys = np.clip(((canal.ravel() - vmin) / (vmax - vmin) * (alt - 1)).astype(int), 0, alt - 1)
    acc = np.zeros((alt, larg), dtype=np.float32)
    np.add.at(acc, (alt - 1 - ys, xs), 1)
    acc = np.log1p(acc)
    acc = acc / (acc.max() or 1)
    img = np.zeros((alt, larg, 3), dtype=np.float32)
    for i in range(3):
        img[..., i] = acc * cor[i]
    return img


def _graticula_wave(d, x0, larg, alt, vmin, vmax, rotulos=True):
    f = fonte(10)
    def yy(v):
        return alt - 1 - (v - vmin) / (vmax - vmin) * (alt - 1)
    for v, c in [(16, (220, 60, 60)), (235, (220, 60, 60))]:
        d.line([(x0, yy(v)), (x0 + larg, yy(v))], fill=c, width=1)
    for p in (25, 50, 75):
        v = 16 + p / 100 * 219
        d.line([(x0, yy(v)), (x0 + larg, yy(v))], fill=(70, 70, 70), width=1)
    if rotulos:
        d.text((x0 + 2, yy(235) - 12), "100% / 235", font=f, fill=(220, 90, 90))
        d.text((x0 + 2, yy(16) + 1), "0% / 16", font=f, fill=(220, 90, 90))


def waveform_luma(Y, larg=360):
    img = _wave(Y, larg=larg, cor=(200, 255, 200))
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    _graticula_wave(d, 0, larg, H_SCOPE, 0, 255)
    d.text((larg - 70, 2), "Waveform Y", font=fonte(11), fill=(200, 200, 200))
    return im


def parade_rgb(Y, Cb, Cr, larg_canal=150):
    R, G, B = ycbcr_para_rgb_pct(Y, Cb, Cr)
    # escala vertical: -10%..110% para enxergar o que passa do legal
    vmin, vmax = -10, 110
    paineis = []
    for c, cor in ((R, (255, 80, 80)), (G, (80, 255, 80)), (B, (100, 140, 255))):
        img = _wave(c, larg=larg_canal, vmin=vmin, vmax=vmax, cor=cor)
        paineis.append(img)
    sep = np.zeros((H_SCOPE, 3, 3), dtype=np.float32) + 40
    full = np.concatenate([paineis[0], sep, paineis[1], sep, paineis[2]], axis=1)
    im = Image.fromarray(np.clip(full, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    W = im.width
    def yy(p):
        return H_SCOPE - 1 - (p - vmin) / (vmax - vmin) * (H_SCOPE - 1)
    for p, c in [(0, (220, 60, 60)), (100, (220, 60, 60)), (50, (70, 70, 70))]:
        d.line([(0, yy(p)), (W, yy(p))], fill=c, width=1)
    d.text((W - 80, 2), "Parade RGB %", font=fonte(11), fill=(200, 200, 200))
    return im


def _alvo_709(r, g, b):
    y = KR * r + KG * g + KB * b
    cb = (b - y) / (2 * (1 - KB))
    cr = (r - y) / (2 * (1 - KR))
    return cb * 224, cr * 224  # em código 8 bits a partir de 128


def vectorscope(Cb, Cr, tam=256, zoom=1.0):
    u = (Cb.ravel() - 128) * zoom
    v = (Cr.ravel() - 128) * zoom
    xs = (u + 128).astype(int)
    ys = (128 - v).astype(int)
    dentro = (xs >= 0) & (xs < tam) & (ys >= 0) & (ys < tam)  # com zoom, o que sai do quadro é descartado
    acc = np.zeros((tam, tam), dtype=np.float32)
    np.add.at(acc, (ys[dentro], xs[dentro]), 1)
    acc = np.log1p(acc)
    acc = acc / (acc.max() or 1)
    # cor de cada posição = matiz correspondente
    gy, gx = np.mgrid[0:tam, 0:tam]
    cbm = (gx - 128) / zoom
    crm = (128 - gy) / zoom
    Rr, Gg, Bb = ycbcr_para_rgb_pct(np.full_like(cbm, 140.0), cbm + 128, crm + 128)
    rgb = np.stack([Rr, Gg, Bb], axis=-1) / 100 * 255
    rgb = np.clip(rgb * 0.6 + 100, 0, 255)
    img = rgb * acc[..., None]
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    c = tam / 2
    rad = 112 * zoom
    d.ellipse([c - rad, c - rad, c + rad, c + rad], outline=(60, 60, 60))
    d.line([(0, c), (tam, c)], fill=(45, 45, 45))
    d.line([(c, 0), (c, tam)], fill=(45, 45, 45))
    f = fonte(10)
    for nome, rgbp in (("R", (1, 0, 0)), ("Yl", (1, 1, 0)), ("G", (0, 1, 0)),
                       ("Cy", (0, 1, 1)), ("B", (0, 0, 1)), ("Mg", (1, 0, 1))):
        for frac_, lado in ((0.75, 4), (1.0, 2)):
            cb, cr = _alvo_709(*(frac_ * x for x in rgbp))
            x, y = c + cb * zoom, c - cr * zoom
            d.rectangle([x - lado, y - lado, x + lado, y + lado], outline=(150, 150, 150))
        cb, cr = _alvo_709(*(0.75 * x for x in rgbp))
        d.text((c + cb * zoom * 1.18 - 5, c - cr * zoom * 1.18 - 6), nome, font=f, fill=(170, 170, 170))
    a = math.radians(LIMITES["pele_angulo"])
    d.line([(c, c), (c + math.cos(a) * rad * 1.1, c - math.sin(a) * rad * 1.1)], fill=(255, 190, 120), width=1)
    d.text((4, tam - 14), f"pele {LIMITES['pele_angulo']:.0f}°" + (f"  zoom {zoom:g}x" if zoom != 1 else ""),
           font=f, fill=(255, 190, 120))
    return im


def histograma(Y, Cb, Cr, larg=300):
    R, G, B = ycbcr_para_rgb_pct(Y, Cb, Cr)
    im = Image.new("RGB", (larg, H_SCOPE), (0, 0, 0))
    d = ImageDraw.Draw(im)
    def hist(c, vmin, vmax):
        h, _ = np.histogram(c.ravel(), bins=larg, range=(vmin, vmax))
        return h / (h.max() or 1)
    for c, cor in ((R, (255, 70, 70)), (G, (70, 255, 70)), (B, (90, 130, 255))):
        h = hist(c, -10, 110)
        pts = [(i, H_SCOPE - 1 - h[i] * (H_SCOPE - 20)) for i in range(larg)]
        d.line(pts, fill=cor, width=1)
    hy = hist((Y - 16) / 219 * 100, -10, 110)
    for i in range(larg):
        d.line([(i, H_SCOPE - 1), (i, H_SCOPE - 1 - hy[i] * (H_SCOPE - 20))], fill=(110, 110, 110))
    for p in (0, 100):
        x = (p + 10) / 120 * larg
        d.line([(x, 0), (x, H_SCOPE)], fill=(220, 60, 60))
    d.text((larg - 75, 2), "Histograma %", font=fonte(11), fill=(200, 200, 200))
    return im


def miniatura(Y, Cb, Cr, alt=H_SCOPE):
    R, G, B = ycbcr_para_rgb_pct(Y, Cb, Cr)
    rgb = np.stack([R, G, B], axis=-1) / 100.0
    rgb = np.clip(rgb, 0, 1) ** 1.0 * 255
    im = Image.fromarray(rgb.astype(np.uint8))
    w = int(im.width * alt / im.height)
    return im.resize((w, alt), Image.LANCZOS)


def linha_escopos(Y, Cb, Cr, titulo, linhas_txt, zoom_vs=1.0):
    blocos = [miniatura(Y, Cb, Cr), waveform_luma(Y), parade_rgb(Y, Cb, Cr), vectorscope(Cb, Cr, zoom=zoom_vs),
              histograma(Y, Cb, Cr)]
    gap = 6
    W = sum(b.width for b in blocos) + gap * (len(blocos) + 1)
    topo = 22 + 16 * len(linhas_txt)
    im = Image.new("RGB", (W, H_SCOPE + topo + gap), (18, 18, 18))
    d = ImageDraw.Draw(im)
    d.text((gap, 4), titulo, font=fonte(15), fill=(255, 255, 255))
    for i, t in enumerate(linhas_txt):
        d.text((gap, 24 + 16 * i), t, font=fonte(12), fill=(210, 210, 210))
    x = gap
    for b in blocos:
        im.paste(b, (x, topo))
        x += b.width + gap
    return im


def empilhar(imagens, fundo=(18, 18, 18)):
    W = max(i.width for i in imagens)
    H = sum(i.height for i in imagens) + 4 * len(imagens)
    out = Image.new("RGB", (W, H), fundo)
    y = 0
    for i in imagens:
        out.paste(i, (0, y))
        y += i.height + 4
    return out


# ---------------------------------------------------------------------------
# Alertas — cada um cita a regra
# ---------------------------------------------------------------------------
def alertas(cena):
    a = []
    n = cena["numeros"]
    q = cena["quadro"]
    if q["Y_p01"] < LIMITES["ebu_y_min"]:
        a.append(f"preto efetivo (p0,1) {q['Y_p01']:.0f} < {LIMITES['ebu_y_min']:.1f} abaixo da faixa preferida EBU R103 v3.0 (5)")
    if q["Y_p999"] > LIMITES["ebu_y_max"]:
        a.append(f"branco efetivo (p99,9) {q['Y_p999']:.0f} > {LIMITES['ebu_y_max']:.1f} acima da faixa preferida EBU R103 v3.0 (246)")
    if n.get("BRNG_pct") is not None and n["BRNG_pct"] > LIMITES["area_fora_pct"]:
        a.append(f"{n['BRNG_pct']:.2f}% da área fora de 16–235/16–240 (signalstats BRNG, limite nominal BT.709) > "
                 f"{LIMITES['area_fora_pct']}% — aviso: a norma EBU usa 5–246")
    if q["fora_gamut_rgb_pct"] > LIMITES["area_fora_pct"]:
        a.append(f"{q['fora_gamut_rgb_pct']}% da área com R, G ou B fora de 5–246 (-5%..105%) > 1% (EBU R103 v3.0, sem o filtro de medida da norma)")
    if q["Y_p01"] > 16 + 0.08 * 219:
        a.append(f"preto levantado: preto efetivo {pct(q['Y_p01']):.0f}% — sem preto real no quadro (conferir se é intenção)")
    if q["Y_p999"] < 16 + 0.80 * 219:
        a.append(f"branco baixo: branco efetivo {pct(q['Y_p999']):.0f}% — quadro sem altas (conferir se é intenção)")
    ar, ag, ab = q["altas_RGB"]
    if max(ar, ag, ab) - min(ar, ag, ab) > 6:
        a.append(f"altas desequilibradas R{ar} G{ag} B{ab} — dominante se as altas forem neutras (parede/papel branco)")
    br, bg, bb = q["baixas_RGB"]
    if max(br, bg, bb) - min(br, bg, bb) > 4:
        a.append(f"baixas desequilibradas R{br} G{bg} B{bb} — dominante nas sombras se forem neutras")
    p = q.get("pele")
    if p and abs(p["desvio_da_linha"]) > 10:
        lado = "para o vermelho/magenta" if p["desvio_da_linha"] < 0 else "para o amarelo/verde"
        a.append(f"pele {p['angulo_mediano']}° ({p['desvio_da_linha']:+}° da linha, {lado}) — {p['origem']}")
    return a


# ---------------------------------------------------------------------------
# Programa
# ---------------------------------------------------------------------------
def parse_cenas(txt):
    out = []
    for parte in txt.split(","):
        a, b = parte.split("-")
        out.append((float(a), float(b)))
    return out


def diagnosticar(video, pasta, limiar=10.0, amostra=5.0, cenas_txt=None, sdr=False, pele=None, zoom_vs=1.0,
                 cenas_fixas=None, rotulo=None):
    video = Path(video)
    info = probe(video)
    pre = TONEMAP_HLG if (sdr and eh_hdr(info)) else None
    escala = 4.0 if (info["bits"] == 10 and not pre) else (16.0 if info["bits"] == 12 and not pre else 1.0)
    cortes, quadros = analisar(video, pasta, limiar, amostra, pre)
    if cenas_fixas:
        cenas = cenas_fixas
    elif cenas_txt:
        cenas = parse_cenas(cenas_txt)
    else:
        cenas = montar_cenas(cortes, info["duracao"])
    resultado = {"video": str(video), "rotulo": rotulo or video.stem, "info": info, "tonemap_aplicado": bool(pre),
                 "limiar_corte": limiar, "amostra_fps": amostra, "cortes": agrupar_cortes(cortes), "cenas": []}
    linhas_img = []
    for i, (a, b) in enumerate(cenas, 1):
        meio = (a + b) / 2
        Yf, Cbf, Crf = extrair_quadro_ycbcr(video, meio, largura=None, pre=pre)
        nums = agregar(quadros, a, b, escala)
        med = medidas_quadro(Yf, Cbf, Crf, pele)
        passo = max(1, Yf.shape[1] // 480)
        Y, Cb, Cr = Yf[::passo, ::passo], Cbf[::passo, ::passo], Crf[::passo, ::passo]
        cena = {"n": i, "inicio": a, "fim": b, "quadro_t": round(meio, 3), "numeros": nums, "quadro": med}
        cena["alertas"] = alertas(cena)
        resultado["cenas"].append(cena)
        txt = [
            f"Y preto ef./p10/médio/p90/branco ef.: {med['Y_p01']:.0f} / {nums['YLOW']:.0f} / {nums['YAVG']:.0f} / "
            f"{nums['YHIGH']:.0f} / {med['Y_p999']:.0f}  (= {pct(med['Y_p01']):.0f}% / {pct(nums['YAVG']):.0f}% / "
            f"{pct(med['Y_p999']):.0f}%)   sat média {nums['SATAVG']:.1f}, p90 {nums['SATHIGH']:.1f}   fora 16–235: {med['Y_fora_16_235_pct']}%",
            f"altas RGB {med['altas_RGB']}  baixas RGB {med['baixas_RGB']}  fora gamut {med['fora_gamut_rgb_pct']}%"
            + (f"   pele {med['pele']['angulo_mediano']}° ({med['pele']['desvio_da_linha']:+}°) croma {med['pele']['croma_mediana']}"
               if med["pele"] else "   pele: não detectada"),
        ]
        titulo = f"{rotulo or video.stem} · cena {i} · {a:.2f}–{b:.2f}s (quadro {meio:.2f}s)"
        linhas_img.append(linha_escopos(Y, Cb, Cr, titulo, txt, zoom_vs))
    folha = empilhar(linhas_img)
    folha.save(pasta / "folha_escopos.png")
    (pasta / "diagnostico.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    (pasta / "diagnostico.md").write_text(relatorio_md(resultado), encoding="utf-8")
    return resultado


def relatorio_md(r):
    i = r["info"]
    L = [f"# Diagnóstico — {Path(r['video']).name}", "",
         f"{i['largura']}×{i['altura']} · {i['fps']} fps · {i['duracao']:.2f} s · {i['pix_fmt']} ({i['bits']} bits) · "
         f"range `{i['range']}` · matriz `{i['matriz']}` · transferência `{i['transferencia']}` · primárias `{i['primarias']}`",
         ""]
    if eh_hdr(i):
        L.append("⚠️ **Fonte HDR** (" + i["transferencia"] + "). " +
                 ("Números medidos depois do tonemap para SDR BT.709." if r["tonemap_aplicado"] else
                  "Números medidos no sinal HDR cru: os limites SDR abaixo não se aplicam. Rode com `--sdr`."))
        L.append("")
    if i["range"] == "pc":
        L.append("⚠️ Arquivo marcado como **faixa cheia (pc, 0–255)**; os limites 16–235 abaixo são da faixa limitada.")
        L.append("")
    L.append(f"Cortes detectados (scdet t={r['limiar_corte']}): " + (", ".join(f"{c:.2f}s" for c in r["cortes"]) or "nenhum"))
    L.append("")
    L.append("Preto/branco efetivos e pele: medidos no quadro do meio da cena, em resolução cheia. Y médio, saturação e "
             "'fora 16–235' (BRNG): média de todos os quadros amostrados da cena.")
    L.append("")
    L.append("Valores em código 8 bits (preto 16, branco 235 — ITU-R BT.709-6) e % (0% = 16, 100% = 235).")
    L.append("")
    L.append("| Cena | Tempo | Preto ef. (p0,1) | Y médio | Branco ef. (p99,9) | Fora 16–235 | Sat. média | Sat. p90 | Altas RGB % | Baixas RGB % | Fora gamut RGB | Pele |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for c in r["cenas"]:
        n, q = c["numeros"], c["quadro"]
        pele = f"{q['pele']['angulo_mediano']}° ({q['pele']['desvio_da_linha']:+}°)" if q["pele"] else "—"
        L.append(f"| {c['n']} | {c['inicio']:.2f}–{c['fim']:.2f} | {q['Y_p01']:.0f} ({pct(q['Y_p01']):.0f}%) | "
                 f"{n['YAVG']:.0f} ({pct(n['YAVG']):.0f}%) | {q['Y_p999']:.0f} ({pct(q['Y_p999']):.0f}%) | "
                 f"{n['BRNG_pct']:.2f}% | {n['SATAVG']:.1f} | "
                 f"{n['SATHIGH']:.1f} | {q['altas_RGB']} | {q['baixas_RGB']} | {q['fora_gamut_rgb_pct']}% | {pele} |")
    L.append("")
    L.append("## Alertas")
    algum = False
    for c in r["cenas"]:
        for a in c["alertas"]:
            L.append(f"- Cena {c['n']}: {a}")
            algum = True
    if not algum:
        L.append("- Nenhum.")
    L.append("")
    L.append("Alerta é medida, não veredito: preto levantado ou dominante podem ser o look pretendido. Quem decide é o usuário.")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("-o", "--pasta")
    ap.add_argument("--limiar", type=float, default=10.0, help="limiar do scdet (0–100). Menor = mais cortes.")
    ap.add_argument("--amostra", type=float, default=5.0, help="quadros por segundo medidos pelo signalstats")
    ap.add_argument("--cenas", help="cenas manuais: 0-3.2,3.2-8")
    ap.add_argument("--sdr", action="store_true", help="se a fonte for HLG/PQ, medir depois do tonemap para BT.709")
    ap.add_argument("--pele", help="região de pele x,y,w,h em fração do quadro (ex.: 0.4,0.2,0.2,0.2)")
    ap.add_argument("--zoom-vs", type=float, default=1.0, help="zoom do vectorscope (2 = croma baixa ampliada)")
    a = ap.parse_args()
    pasta = Path(a.pasta) if a.pasta else Path(a.video).with_name(Path(a.video).stem + "_diag")
    pele = tuple(float(x) for x in a.pele.split(",")) if a.pele else None
    r = diagnosticar(a.video, pasta, a.limiar, a.amostra, a.cenas, a.sdr, pele, a.zoom_vs)
    sys.stdout.reconfigure(encoding="utf-8")
    print(relatorio_md(r))
    print(f"Folha: {pasta / 'folha_escopos.png'}")


if __name__ == "__main__":
    main()
