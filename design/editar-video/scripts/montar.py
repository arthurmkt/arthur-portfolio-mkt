#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monta trechos em sequência com corte seco, J cut ou L cut, a partir de uma lista (JSON).

Uso:
  python montar.py lista.json            # renderiza
  python montar.py lista.json --mostrar  # imprime o filtergraph e a tabela de tempos

Lista:
{
  "saida": "montado.mp4",
  "fps": 30, "escala": "1080:1920",
  "cruzamento_audio": 0.04,          # s de crossfade qsin em cada emenda de áudio (0 = emenda seca)
  "trechos": [
    {"fonte": "a.mp4", "entrada": 1.20, "saida": 4.00},
    {"fonte": "b.mp4", "entrada": 0.50, "saida": 3.00, "emenda": {"tipo": "J", "seg": 0.5}},
    {"fonte": "a.mp4", "entrada": 9.00, "saida": 12.0, "emenda": {"tipo": "L", "seg": 0.4}}
  ]
}
"emenda" descreve a passagem do trecho anterior para este:
  J = o áudio deste trecho entra "seg" antes da imagem (precisa de sobra antes da entrada na fonte);
  L = o áudio do trecho anterior continua "seg" depois do corte de imagem (precisa de sobra depois da saída).
A imagem corta sempre no mesmo ponto; a duração total de áudio = duração total de vídeo.

Fontes: Adobe Premiere Help "Perform J cuts and L cuts" (08/2025); Adobe "Audio crossfade transitions"
(Constant Power ≈ dissolve; Constant Gain pode afundar no meio). No ffmpeg, acrossfade/afade usam curva
'tri' (linear) por padrão: medido pela pesquisa, afunda 3 dB no meio; 'qsin' segura o nível → c1=qsin:c2=qsin.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import escopos as E  # noqa: E402


def calcular(lista, base):
    tr = lista["trechos"]
    n = len(tr)
    lead = [0.0] * (n + 1)  # lead[k] = quanto o áudio do trecho k começa antes da imagem (negativo = L do anterior)
    for k in range(1, n):
        em = tr[k].get("emenda")
        if em:
            s = float(em["seg"])
            lead[k] = s if em["tipo"].upper() == "J" else -s
    c = float(lista.get("cruzamento_audio", 0.0))
    linhas = []
    for k, t in enumerate(tr):
        dur_fonte = E.probe(base / t["fonte"])["duracao"]
        vi, vo = float(t["entrada"]), float(t["saida"])
        ai = vi - lead[k] - (c / 2 if k > 0 else 0)
        ao = vo - lead[k + 1] + (c / 2 if k < n - 1 else 0)
        if ai < -1e-6 or ao > dur_fonte + 1e-6:
            raise SystemExit(f"Trecho {k + 1} ({t['fonte']}): áudio pede {ai:.3f}–{ao:.3f}s, fonte tem 0–{dur_fonte:.3f}s. "
                             "Sem sobra para essa emenda: diminuir 'seg' ou mudar entrada/saída.")
        linhas.append({"k": k, "fonte": t["fonte"], "video": (vi, vo), "audio": (ai, ao)})
    return linhas, c


def grafo(lista, linhas, c, entradas):
    fps = lista.get("fps", 30)
    esc = lista.get("escala")
    partes = []
    for L in linhas:
        i = entradas[L["fonte"]]
        vi, vo = L["video"]
        ai, ao = L["audio"]
        v = f"[{i}:v]trim=start={vi:.4f}:end={vo:.4f},setpts=PTS-STARTPTS,fps={fps}"
        if esc:
            v += f",scale={esc}:flags=lanczos,setsar=1"
        partes.append(v + f",format=yuv420p[v{L['k']}]")
        partes.append(f"[{i}:a]atrim=start={ai:.4f}:end={ao:.4f},asetpts=PTS-STARTPTS,"
                      f"aresample=48000,aformat=channel_layouts=stereo[a{L['k']}]")
    n = len(linhas)
    partes.append("".join(f"[v{k}]" for k in range(n)) + f"concat=n={n}:v=1:a=0[vout]")
    if n == 1:
        partes.append("[a0]anull[aout]")
    elif c > 0:
        atual = "a0"
        for k in range(1, n):
            out = "aout" if k == n - 1 else f"x{k}"
            partes.append(f"[{atual}][a{k}]acrossfade=d={c:.4f}:c1=qsin:c2=qsin[{out}]")
            atual = out
    else:
        partes.append("".join(f"[a{k}]" for k in range(n)) + f"concat=n={n}:v=0:a=1[aout]")
    return ";".join(partes)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lista")
    ap.add_argument("--mostrar", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    caminho = Path(a.lista).resolve()
    base = caminho.parent
    lista = json.loads(caminho.read_text(encoding="utf-8"))
    linhas, c = calcular(lista, base)
    fontes = []
    for L in linhas:
        if L["fonte"] not in fontes:
            fontes.append(L["fonte"])
    entradas = {f: i for i, f in enumerate(fontes)}
    fc = grafo(lista, linhas, c, entradas)
    total_v = sum(L["video"][1] - L["video"][0] for L in linhas)
    print("| Trecho | Fonte | Imagem | Áudio |")
    print("|---|---|---|---|")
    for L in linhas:
        print(f"| {L['k'] + 1} | {L['fonte']} | {L['video'][0]:.2f}–{L['video'][1]:.2f} | {L['audio'][0]:.2f}–{L['audio'][1]:.2f} |")
    print(f"Duração da imagem: {total_v:.3f}s")
    if a.mostrar:
        print(fc)
        return
    sai = base / lista.get("saida", "montado.mp4")
    cmd = ["ffmpeg", "-v", "error", "-y"]
    for f in fontes:
        cmd += ["-i", str(base / f)]
    cmd += ["-filter_complex", fc, "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "medium",
            "-crf", "18", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
            "-color_trc", "bt709", "-color_range", "tv", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-movflags", "+faststart", str(sai)]
    subprocess.run(cmd, check=True)
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,duration", "-of", "csv=p=0", str(sai)],
                       capture_output=True, text=True).stdout.split()
    print(f"{sai}\nDurações (tipo,duração): {' '.join(r)} — vídeo e áudio devem bater dentro de 1 quadro.")


if __name__ == "__main__":
    main()
