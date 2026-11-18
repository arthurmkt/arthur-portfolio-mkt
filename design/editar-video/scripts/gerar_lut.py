#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera LUT 3D .cube (Adobe Cube LUT Specification 1.0) a partir de uma correção feita em ffmpeg,
para levar o look aprovado para Premiere / Resolve / CapCut / Final Cut.

Uso:
  python gerar_lut.py --identidade -o neutra.cube                       # LUT neutra (teste de encanamento)
  python gerar_lut.py --plano plano.json -o look.cube                    # "global" + "look" do plano do graduar.py
  python gerar_lut.py --cadeia "colortemperature=temperature=6000" -o x.cube
  python gerar_lut.py --misturar look.cube --forca 0.6 -o look_60.cube   # intensidade: mistura com a neutra
  python gerar_lut.py --conferir look.cube --plano plano.json --video clip.mp4   # PSNR LUT × cadeia

Só entra o que é operação por pixel em RGB (níveis, balanço, temperatura, contraste, curva, saturação, LUT).
Operações por cena ("cenas" do plano) e filtros espaciais (nitidez, ruído, vinheta) NÃO viram LUT.
A LUT recebe e devolve R'G'B' BT.709 com gama (o mesmo sinal do vídeo); a entrada precisa estar nesse espaço.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))


def grade_identidade(n):
    v = np.linspace(0.0, 1.0, n)
    b, g, r = np.meshgrid(v, v, v, indexing="ij")  # r varia mais rápido (ordem do .cube)
    return np.stack([r.ravel(), g.ravel(), b.ravel()], axis=-1)


def aplicar_cadeia(rgb, cadeia):
    n_pix = rgb.shape[0]
    larg = 1089 if n_pix % 1089 == 0 else n_pix
    alt = n_pix // larg
    raw = (np.clip(rgb, 0, 1) * 65535 + 0.5).astype("<u2").tobytes()
    cmd = ["ffmpeg", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-s", f"{larg}x{alt}", "-i", "-",
           "-vf", f"format=gbrp16le,{cadeia},format=rgb48le", "-f", "rawvideo", "-"]
    out = subprocess.run(cmd, input=raw, capture_output=True, check=True).stdout
    return np.frombuffer(out, dtype="<u2").astype(np.float64).reshape(-1, 3) / 65535.0


def escrever_cube(caminho, dados, n, titulo):
    linhas = [f'TITLE "{titulo}"', f"LUT_3D_SIZE {n}", "DOMAIN_MIN 0.0 0.0 0.0", "DOMAIN_MAX 1.0 1.0 1.0"]
    linhas += [f"{r:.6f} {g:.6f} {b:.6f}" for r, g, b in dados]
    # LF puro: a Adobe Cube LUT Specification 1.0 considera CRLF inválido (o ffmpeg aceita, outros programas não)
    Path(caminho).write_text("\n".join(linhas) + "\n", encoding="ascii", newline="\n")


def ler_cube(caminho):
    n = None
    dados = []
    for linha in Path(caminho).read_text(encoding="ascii", errors="ignore").splitlines():
        s = linha.strip()
        if not s or s.startswith("#"):
            continue
        if s.startswith("LUT_3D_SIZE"):
            n = int(s.split()[1])
            continue
        if s[0].isalpha():
            continue
        dados.append([float(x) for x in s.split()[:3]])
    return n, np.array(dados)


def cadeia_do_plano(plano):
    import graduar as G
    f = []
    for op in plano.get("global", []) + plano.get("look", []):
        f += G.op_para_filtro(op)
    if plano.get("cenas"):
        print("⚠️ As operações de 'cenas' (igualar) ficam fora da LUT: a LUT é uma só para o vídeo todo.")
    return ",".join(f) or "null"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-o", "--saida")
    ap.add_argument("--tamanho", type=int, default=33, help="pontos por eixo (33 ou 65, padrão de mercado)")
    ap.add_argument("--identidade", action="store_true")
    ap.add_argument("--plano")
    ap.add_argument("--cadeia")
    ap.add_argument("--misturar")
    ap.add_argument("--forca", type=float, default=1.0)
    ap.add_argument("--conferir")
    ap.add_argument("--video")
    ap.add_argument("--titulo", default="editar-video")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    n = a.tamanho
    ident = grade_identidade(n)

    if a.conferir:
        cad = cadeia_do_plano(json.loads(Path(a.plano).read_text(encoding="utf-8"))) if a.plano else a.cadeia
        lut = Path(a.conferir).resolve().as_posix().replace(":", "\\:")  # filtergraph: file='C\:/...' (testado)
        r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", a.video, "-i", a.video, "-filter_complex",
                            f"[0:v]format=gbrp16le,{cad},format=yuv444p[x];"
                            f"[1:v]format=gbrp16le,lut3d=file='{lut}':interp=tetrahedral,format=yuv444p[y];"
                            "[x][y]psnr", "-frames:v", "60", "-f", "null", "-"], capture_output=True, text=True)
        linha = [l for l in r.stderr.splitlines() if "PSNR" in l]
        print(linha[-1] if linha else r.stderr[-800:])
        print("Referência: PSNR ≥ 45 dB = diferença invisível na prática (prática comum de codificação, sem fonte normativa).")
        return

    if a.identidade:
        dados = ident
    elif a.misturar:
        n2, lut = ler_cube(a.misturar)
        n = n2
        dados = grade_identidade(n) * (1 - a.forca) + lut * a.forca
    else:
        cad = cadeia_do_plano(json.loads(Path(a.plano).read_text(encoding="utf-8"))) if a.plano else a.cadeia
        dados = aplicar_cadeia(ident, cad)
        if a.forca != 1.0:
            dados = ident * (1 - a.forca) + dados * a.forca
    escrever_cube(a.saida, np.clip(dados, 0, 1), n, a.titulo)
    print(f"{a.saida} · {n}³ = {n ** 3} pontos")


if __name__ == "__main__":
    main()
