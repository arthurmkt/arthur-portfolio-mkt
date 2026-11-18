#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Folha de revisão antes/depois, por cena, com os números lado a lado.

Uso:
  python comparar.py ANTES DEPOIS [-o PASTA] [--limiar 10] [--cenas 0-3,3-8] [--pele x,y,w,h] [--zoom-vs 2]

As cenas são detectadas no ANTES e reaplicadas ao DEPOIS (mesma minutagem). Se o corte mudou a duração,
passe --cenas manualmente ou compare trecho a trecho.

Saídas em PASTA (padrão: <depois>_comparacao/):
  folha_antes_depois.png — por cena: split (esq. antes | dir. depois) | waveform antes/depois | vectorscope antes/depois
  comparacao.md          — tabela de números antes → depois por cena + alertas que sumiram/surgiram
  antes/ e depois/       — diagnóstico completo de cada um (diagnostico.json/.md, folha_escopos.png)
"""
import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
import escopos as E  # noqa: E402


def split(Ya, Cba, Cra, Yd, Cbd, Crd, alt=E.H_SCOPE):
    a = E.miniatura(Ya, Cba, Cra, alt)
    d = E.miniatura(Yd, Cbd, Crd, alt)
    w = a.width
    out = a.copy()
    out.paste(d.crop((w // 2, 0, w, alt)), (w // 2, 0))
    dr = ImageDraw.Draw(out)
    dr.line([(w // 2, 0), (w // 2, alt)], fill=(255, 255, 0), width=1)
    tf = E.fonte(max(10, alt // 40))
    dr.text((4, 4), "antes", font=tf, fill=(255, 255, 0))
    dr.text((w // 2 + 4, 4), "depois", font=tf, fill=(255, 255, 0))
    return out


def lado_a_lado(a, d, rotulo_a="antes", rotulo_d="depois"):
    out = Image.new("RGB", (a.width + d.width + 4, a.height), (40, 40, 40))
    out.paste(a, (0, 0))
    out.paste(d, (a.width + 4, 0))
    dr = ImageDraw.Draw(out)
    dr.text((4, 16), rotulo_a, font=E.fonte(11), fill=(255, 255, 0))
    dr.text((a.width + 8, 16), rotulo_d, font=E.fonte(11), fill=(255, 255, 0))
    return out


def fmt_delta(a, d, casas=0, sufixo=""):
    if a is None or d is None:
        return "—"
    return f"{a:.{casas}f}{sufixo} → {d:.{casas}f}{sufixo}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("antes")
    ap.add_argument("depois")
    ap.add_argument("-o", "--pasta")
    ap.add_argument("--limiar", type=float, default=10.0)
    ap.add_argument("--amostra", type=float, default=5.0)
    ap.add_argument("--cenas")
    ap.add_argument("--sdr", action="store_true", help="aplicar tonemap no ANTES se ele for HLG/PQ")
    ap.add_argument("--pele")
    ap.add_argument("--zoom-vs", type=float, default=1.0)
    a = ap.parse_args()
    pasta = Path(a.pasta) if a.pasta else Path(a.depois).with_name(Path(a.depois).stem + "_comparacao")
    pele = tuple(float(x) for x in a.pele.split(",")) if a.pele else None

    ra = E.diagnosticar(a.antes, pasta / "antes", a.limiar, a.amostra, a.cenas, a.sdr, pele, a.zoom_vs, rotulo="antes")
    cenas = [(c["inicio"], c["fim"]) for c in ra["cenas"]]
    dur_d = E.probe(a.depois)["duracao"]
    if abs(dur_d - ra["info"]["duracao"]) > 0.2 and not a.cenas:
        print(f"⚠️ Durações diferentes (antes {ra['info']['duracao']:.2f}s, depois {dur_d:.2f}s): "
              "as cenas do antes podem não bater no depois. Use --cenas.")
        cenas = [(x, min(y, dur_d)) for x, y in cenas if x < dur_d]
    rd = E.diagnosticar(a.depois, pasta / "depois", a.limiar, a.amostra, None, False, pele, a.zoom_vs,
                        cenas_fixas=cenas, rotulo="depois")

    linhas = []
    pre_a = E.TONEMAP_HLG if (a.sdr and E.eh_hdr(ra["info"])) else None
    for ca, cd in zip(ra["cenas"], rd["cenas"]):
        t = ca["quadro_t"]
        Ya, Cba, Cra = E.extrair_quadro_ycbcr(a.antes, t, pre=pre_a)
        Yd, Cbd, Crd = E.extrair_quadro_ycbcr(a.depois, t)
        # split em tamanho de revisão (1080 de largura): é nele que o olho julga, a folha é o mapa
        Yg, Cbg, Crg = E.extrair_quadro_ycbcr(a.antes, t, largura=1080, pre=pre_a)
        Yh, Cbh, Crh = E.extrair_quadro_ycbcr(a.depois, t, largura=1080)
        split(Yg, Cbg, Crg, Yh, Cbh, Crh, alt=Yg.shape[0]).save(pasta / f"split_cena{ca['n']}.png")
        blocos = [
            split(Ya, Cba, Cra, Yd, Cbd, Crd),
            lado_a_lado(E.waveform_luma(Ya, 300), E.waveform_luma(Yd, 300)),
            lado_a_lado(E.vectorscope(Cba, Cra, zoom=a.zoom_vs), E.vectorscope(Cbd, Crd, zoom=a.zoom_vs)),
        ]
        na, nd, qa, qd = ca["numeros"], cd["numeros"], ca["quadro"], cd["quadro"]
        txt = [
            f"preto ef. {E.pct(qa['Y_p01']):.0f}% → {E.pct(qd['Y_p01']):.0f}%   Y médio {E.pct(na['YAVG']):.0f}% → "
            f"{E.pct(nd['YAVG']):.0f}%   branco ef. {E.pct(qa['Y_p999']):.0f}% → {E.pct(qd['Y_p999']):.0f}%   "
            f"sat média {na['SATAVG']:.1f} → {nd['SATAVG']:.1f}   fora 16–235 {na['BRNG_pct']:.2f}% → {nd['BRNG_pct']:.2f}%",
            f"altas RGB {qa['altas_RGB']} → {qd['altas_RGB']}   pele "
            + (f"{qa['pele']['angulo_mediano']}° → " if qa["pele"] else "— → ")
            + (f"{qd['pele']['angulo_mediano']}° (croma {qd['pele']['croma_mediana']})" if qd["pele"] else "—"),
        ]
        gap = 6
        W = sum(b.width for b in blocos) + gap * (len(blocos) + 1)
        topo = 22 + 16 * len(txt)
        im = Image.new("RGB", (W, E.H_SCOPE + topo + gap), (18, 18, 18))
        dr = ImageDraw.Draw(im)
        dr.text((gap, 4), f"cena {ca['n']} · {ca['inicio']:.2f}–{ca['fim']:.2f}s · quadro {t:.2f}s",
                font=E.fonte(15), fill=(255, 255, 255))
        for i, s in enumerate(txt):
            dr.text((gap, 24 + 16 * i), s, font=E.fonte(12), fill=(210, 210, 210))
        x = gap
        for b in blocos:
            im.paste(b, (x, topo))
            x += b.width + gap
        linhas.append(im)
    E.empilhar(linhas).save(pasta / "folha_antes_depois.png")

    L = [f"# Antes × depois — {Path(a.depois).name}", "",
         f"Antes: `{a.antes}`  ", f"Depois: `{a.depois}`", "",
         "| Cena | Tempo | Preto ef. | Y médio | Branco ef. | Fora 16–235 | Sat. média | Sat. p90 | Altas RGB % | Pele |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for ca, cd in zip(ra["cenas"], rd["cenas"]):
        na, nd, qa, qd = ca["numeros"], cd["numeros"], ca["quadro"], cd["quadro"]
        pele = (f"{qa['pele']['angulo_mediano'] if qa['pele'] else '—'}° → "
                f"{qd['pele']['angulo_mediano'] if qd['pele'] else '—'}°")
        L.append(f"| {ca['n']} | {ca['inicio']:.2f}–{ca['fim']:.2f} | "
                 f"{fmt_delta(E.pct(qa['Y_p01']), E.pct(qd['Y_p01']), 0, '%')} | "
                 f"{fmt_delta(E.pct(na['YAVG']), E.pct(nd['YAVG']), 0, '%')} | "
                 f"{fmt_delta(E.pct(qa['Y_p999']), E.pct(qd['Y_p999']), 0, '%')} | "
                 f"{fmt_delta(na['BRNG_pct'], nd['BRNG_pct'], 2, '%')} | "
                 f"{fmt_delta(na['SATAVG'], nd['SATAVG'], 1)} | {fmt_delta(na['SATHIGH'], nd['SATHIGH'], 1)} | "
                 f"{qa['altas_RGB']} → {qd['altas_RGB']} | {pele} |")
    L += ["", "## Alertas", ""]
    for ca, cd in zip(ra["cenas"], rd["cenas"]):
        sumiram = [x for x in ca["alertas"] if x not in cd["alertas"]]
        if sumiram or cd["alertas"]:
            L.append(f"**Cena {ca['n']}**")
            L += [f"- ✅ resolvido (antes): {x}" for x in sumiram]
            L += [f"- ⚠️ depois: {x}" for x in cd["alertas"]]
    # consistência entre cenas (igualar): desvio do Y médio e da saturação
    ys = [E.pct(c["numeros"]["YAVG"]) for c in rd["cenas"]]
    ss = [c["numeros"]["SATAVG"] for c in rd["cenas"]]
    ys_a = [E.pct(c["numeros"]["YAVG"]) for c in ra["cenas"]]
    ss_a = [c["numeros"]["SATAVG"] for c in ra["cenas"]]
    if len(ys) > 1:
        L += ["", "## Consistência entre cenas (amplitude máx − mín)", "",
              f"- Y médio: {max(ys_a) - min(ys_a):.1f} pts → {max(ys) - min(ys):.1f} pts",
              f"- Saturação média: {max(ss_a) - min(ss_a):.1f} → {max(ss) - min(ss):.1f}",
              "", "Cenas do mesmo ambiente devem ficar próximas; cenas de ambientes diferentes podem divergir de propósito."]
    (pasta / "comparacao.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(L))
    print(f"\nFolha: {pasta / 'folha_antes_depois.png'}")


if __name__ == "__main__":
    main()
