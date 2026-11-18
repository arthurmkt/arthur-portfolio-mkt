#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplica um plano de correção de cor (JSON) a um vídeo, na ordem de sinal profissional,
com precisão de 16 bits no RGB. Gera prévia em quadros parados ou o vídeo final.

Uso:
  python graduar.py plano.json --previa            # PNG antes|depois do quadro do meio de cada cena
  python graduar.py plano.json                     # renderiza o vídeo
  python graduar.py plano.json --mostrar           # só imprime a cadeia de filtros

Plano (JSON):
{
  "entrada": "bruto.mp4",
  "saida": "corrigido.mp4",
  "conformar": {"fps": 30, "escala": "1080:1920", "hdr_para_sdr": "auto"},
  "global": [ {"op": "temperatura", "kelvin": 6200}, ... ],          # vale para o vídeo todo
  "cenas":  [ {"inicio": 0, "fim": 2.0, "ops": [ {"op": "niveis", ...} ]}, ... ],  # igualar cena a cena
  "look":   [ {"op": "lut", "arquivo": "look.cube"} ],               # por último, depois de igualar
  "acabamento": [ {"op": "filtro", "cadeia": "unsharp=5:5:0.4"} ],
  "legalizar": true,
  "entrega": {"crf": 18, "preset": "slow", "audio": "copiar"}
}

Operações (todas em RGB 16 bits, 0–1 onde 0 = preto legal e 1 = branco legal):
  niveis       {"preto": [r,g,b] ou n, "branco": [r,g,b] ou n, "gama": n}      → colorlevels
  balanco      {"sombras": [r,g,b], "medios": [r,g,b], "altas": [r,g,b], "preservar_luz": true} → colorbalance
  temperatura  {"kelvin": 6500, "mistura": 1}                                  → colortemperature
  contraste    {"valor": 1.1, "pivo": 0.45}                                    → lutrgb (linear em torno do pivô)
  curva        {"todas": "0/0 0.25/0.22 0.75/0.8 1/1", "r": ..., "g": ..., "b": ...} → curves
  saturacao    {"valor": 1.1}                                                  → colorchannelmixer, pesos BT.709
  vibrancia    {"valor": 0.15}                                                 → vibrance
  lut          {"arquivo": "x.cube"}                                           → lut3d tetraédrica
  filtro       {"cadeia": "<filtros ffmpeg>"}                                  → cru (o filtro precisa aceitar gbrp16le)
Cada operação dentro de "cenas" recebe enable='between(t,inicio,fim)'.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import escopos as E  # noqa: E402

KR, KG, KB = 0.2126, 0.7152, 0.0722  # ITU-R BT.709-6, Parte 1, item 3.2


def _tripla(v):
    if isinstance(v, (int, float)):
        return [float(v)] * 3
    return [float(x) for x in v]


def _num(x):
    return f"{x:.5f}".rstrip("0").rstrip(".") if isinstance(x, float) else str(x)


def op_para_filtro(op):
    t = op["op"]
    if t == "niveis":
        p = _tripla(op.get("preto", 0.0))
        b = _tripla(op.get("branco", 1.0))
        s = (f"colorlevels=rimin={_num(p[0])}:gimin={_num(p[1])}:bimin={_num(p[2])}:"
             f"rimax={_num(b[0])}:gimax={_num(b[1])}:bimax={_num(b[2])}")
        if "gama" in op:  # gama via lutrgb depois dos níveis (colorlevels não tem gama)
            g = float(op["gama"])
            e = f"pow(clip(val/maxval,0,1),{_num(1 / g)})*maxval"
            s += f",lutrgb=r='{e}':g='{e}':b='{e}'"
        return [s]
    if t == "balanco":
        sh = _tripla(op.get("sombras", 0))
        md = _tripla(op.get("medios", 0))
        hi = _tripla(op.get("altas", 0))
        pl = ":pl=1" if op.get("preservar_luz", True) else ""
        return [f"colorbalance=rs={_num(sh[0])}:gs={_num(sh[1])}:bs={_num(sh[2])}:"
                f"rm={_num(md[0])}:gm={_num(md[1])}:bm={_num(md[2])}:"
                f"rh={_num(hi[0])}:gh={_num(hi[1])}:bh={_num(hi[2])}{pl}"]
    if t == "temperatura":
        return [f"colortemperature=temperature={_num(float(op['kelvin']))}:mix={_num(float(op.get('mistura', 1)))}"
                + (":pl=1" if op.get("preservar_luz", True) else "")]
    if t == "contraste":
        c = float(op["valor"])
        p = float(op.get("pivo", 0.435))
        e = f"clip((val/maxval-{_num(p)})*{_num(c)}+{_num(p)},0,1)*maxval"
        return [f"lutrgb=r='{e}':g='{e}':b='{e}'"]
    if t == "curva":
        partes = []
        for k, nome in (("todas", "all"), ("r", "red"), ("g", "green"), ("b", "blue")):
            if k in op:
                partes.append(f"{nome}='{op[k]}'")
        return ["curves=" + ":".join(partes)]
    if t == "saturacao":
        s = float(op["valor"])
        # Matriz de saturação em torno da luma BT.709: cinza (R=G=B) fica parado, croma escala por s.
        m = [[KR + (1 - KR) * s, KG * (1 - s), KB * (1 - s)],
             [KR * (1 - s), KG + (1 - KG) * s, KB * (1 - s)],
             [KR * (1 - s), KG * (1 - s), KB + (1 - KB) * s]]
        n = ["rr", "rg", "rb", "gr", "gg", "gb", "br", "bg", "bb"]
        v = [m[0][0], m[0][1], m[0][2], m[1][0], m[1][1], m[1][2], m[2][0], m[2][1], m[2][2]]
        return ["colorchannelmixer=" + ":".join(f"{a}={_num(b)}" for a, b in zip(n, v))]
    if t == "vibrancia":
        return [f"vibrance=intensity={_num(float(op['valor']))}"]
    if t == "lut":
        caminho = Path(op["arquivo"]).resolve().as_posix().replace(":", "\\:")  # filtergraph: file='C\:/...' (testado)
        return [f"lut3d=file='{caminho}':interp=tetrahedral"]
    if t == "filtro":
        return [op["cadeia"]]
    raise ValueError(f"operação desconhecida: {t}")


def com_enable(filtros, a, b):
    out = []
    for f in filtros:
        for parte in f.split(","):
            out.append(parte + f":enable='between(t,{_num(float(a))},{_num(float(b))})'")
    return out


def cadeia(plano, info):
    conf = plano.get("conformar", {})
    f = []
    hdr = conf.get("hdr_para_sdr", "auto")
    if (hdr == "auto" and E.eh_hdr(info)) or hdr is True:
        f.append(E.TONEMAP_HLG)
    if conf.get("fps"):
        f.append(f"fps={conf['fps']}")
    if conf.get("escala"):
        f.append(f"scale={conf['escala']}:flags=lanczos")
    f.append("format=gbrp16le")
    for op in plano.get("global", []):
        f += op_para_filtro(op)
    for cena in plano.get("cenas", []):
        for op in cena.get("ops", []):
            f += com_enable(op_para_filtro(op), cena["inicio"], cena["fim"])
    for op in plano.get("look", []):
        f += op_para_filtro(op)
    for op in plano.get("acabamento", []):
        f += op_para_filtro(op)
    f.append("format=yuv444p16le")
    if plano.get("legalizar", True):
        # trava Y 16–235 e Cb/Cr 16–240 (ITU-R BT.709-6) em 16 bits: 16<<8 = 4096, 235<<8 = 60160, 240<<8 = 61440
        f.append("limiter=min=4096:max=60160:planes=1")
        f.append("limiter=min=4096:max=61440:planes=6")
    f.append("format=yuv420p")
    f.append("setparams=range=tv:colorspace=bt709:color_primaries=bt709:color_trc=bt709")
    return ",".join(f)


TAGS = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]


def renderizar(plano, base, vf):
    ent = (base / plano["entrada"]).resolve()
    sai = (base / plano.get("saida", Path(plano["entrada"]).stem + "_cor.mp4")).resolve()
    ent_ = plano.get("entrega", {})
    cmd = ["ffmpeg", "-v", "error", "-stats", "-stats_period", "15", "-y", "-i", str(ent), "-vf", vf,
           "-c:v", "libx264", "-preset", ent_.get("preset", "slow"), "-crf", str(ent_.get("crf", 18)),
           "-profile:v", "high", "-pix_fmt", "yuv420p", *TAGS, "-movflags", "+faststart"]
    if ent_.get("audio", "copiar") == "copiar":
        cmd += ["-c:a", "copy"]
    else:
        cmd += ["-c:a", "aac", "-b:a", "192k", "-ar", "48000"]
    cmd.append(str(sai))
    subprocess.run(cmd, check=True)
    return sai


def previa(plano, base, vf, info):
    ent = (base / plano["entrada"]).resolve()
    pasta = base / (Path(plano.get("saida", "previa")).stem + "_previa")
    pasta.mkdir(exist_ok=True)
    cenas = plano.get("cenas") or [{"inicio": 0, "fim": info["duracao"]}]
    saidas = []
    for i, c in enumerate(cenas, 1):
        t = (float(c["inicio"]) + float(c["fim"])) / 2
        a = pasta / f"c{i}_antes.png"
        d = pasta / f"c{i}_depois.png"
        pre = E.TONEMAP_HLG + "," if E.eh_hdr(info) else ""
        # -ss depois do -i: o tempo t do filtro é o do vídeo, então o enable da cena vale
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(ent), "-ss", f"{t:.3f}", "-frames:v", "1",
                        "-vf", pre + "scale=1080:-2,format=rgb24", str(a)], check=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(ent), "-ss", f"{t:.3f}", "-frames:v", "1",
                        "-vf", vf + ",scale=1080:-2,format=rgb24", str(d)], check=True)
        saidas.append((a, d))
    from PIL import Image, ImageDraw
    ims = []
    for i, (a, d) in enumerate(saidas, 1):
        A, D = Image.open(a), Image.open(d)
        W = A.width + D.width + 8
        im = Image.new("RGB", (W, A.height + 30), (18, 18, 18))
        im.paste(A, (0, 30))
        im.paste(D, (A.width + 8, 30))
        dr = ImageDraw.Draw(im)
        dr.text((6, 6), f"cena {i} — antes | depois", font=E.fonte(18), fill=(255, 255, 255))
        ims.append(im)
    folha = E.empilhar(ims)
    folha.save(pasta / "previa.png")
    return pasta / "previa.png"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plano")
    ap.add_argument("--previa", action="store_true")
    ap.add_argument("--mostrar", action="store_true")
    a = ap.parse_args()
    caminho = Path(a.plano).resolve()
    plano = json.loads(caminho.read_text(encoding="utf-8"))
    base = caminho.parent
    info = E.probe(base / plano["entrada"])
    vf = cadeia(plano, info)
    sys.stdout.reconfigure(encoding="utf-8")
    if a.mostrar:
        print(vf)
        return
    if a.previa:
        print(previa(plano, base, vf, info))
        return
    print(renderizar(plano, base, vf))


if __name__ == "__main__":
    main()
