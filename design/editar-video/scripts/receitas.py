#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Receitas ffmpeg do /editar-video — fonte única: listar, mostrar e TESTAR num clipe real.

Uso:
  python receitas.py listar
  python receitas.py mostrar R12
  python receitas.py testar CLIPE.mp4 [--so R12,R30] [-o pasta]   # roda todas, confere saída com ffprobe
  python receitas.py md > ../referencias/receitas-ffmpeg.md        # gera a página de referência

Placeholders: {ent} entrada · {ent2} 2ª entrada (outro trecho) · {sai} saída · {logo} PNG com alfa ·
{ass} legenda .ass · {lut} .cube · {fontes} pasta de fontes · {t} instante (s) · {d} duração (s)
Cada receita tem "fonte": documento oficial/norma que sustenta o parâmetro, ou "prática comum, sem fonte".
"""
import argparse
import json
import shlex
import subprocess
import sys
import time
from pathlib import Path

FF = "https://ffmpeg.org/ffmpeg-filters.html"
TAGS = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
H264 = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", *TAGS, "-movflags", "+faststart"]

R = [
    # ---------------------------------------------------------------- ENTRADA / CONFORMAR
    dict(id="R01", area="entrada", titulo="Ler formato, faixa e tags de cor",
         cmd=["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
              "stream=codec_name,width,height,pix_fmt,r_frame_rate,avg_frame_rate,color_range,color_space,"
              "color_transfer,color_primaries:format=duration", "-of", "json", "{ent}"],
         saida=False, fonte="https://ffmpeg.org/ffprobe.html",
         nota="r_frame_rate ≠ avg_frame_rate indica taxa variável (VFR). color_transfer arib-std-b67 = HLG; smpte2084 = PQ."),
    dict(id="R02", area="entrada", titulo="Taxa variável (VFR do celular) → constante",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-vf", "fps=30", "-fps_mode", "cfr", *H264, "-c:a", "aac", "-b:a", "192k", "{sai}"],
         fonte=FF + "#fps-1", nota="fps duplica/descarta quadros para a grade de 30. Fazer ANTES de cortar, senão o corte cai fora do quadro."),
    dict(id="R03", area="entrada", titulo="HLG do iPhone → SDR BT.709 (tonemap mobius)",
         cmd=["ffmpeg", "-y", "-i", "{ent_hlg}", "-vf",
              "zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:param=0.7:desat=0:peak=4.926,zscale=t=bt709:m=bt709:r=tv,format=yuv420p", *H264, "-c:a", "copy", "{sai}"],
         fonte=FF + "#tonemap-1 · ITU-R BT.2408 (branco ref. = 75% HLG, cinza 18% = 38% HLG) · BT.2446 (branco ref. ≈ 90% SDR)",
         nota="Só para fonte HLG/PQ (conferir R01). Medido 05/11 em patches HLG: cinza 18% → 43,4% SDR (OETF BT.709 dá ~41%), "
              "branco ref. → 88,6%, 100% HLG → 99,1%. A cadeia antiga npl=100 punha o cinza em 58% (médios e pele claros demais). "
              "Pele: conferir no vectorscope, conversores diferentes divergem em cor saturada."),
    dict(id="R04", area="entrada", titulo="Faixa cheia (pc, 0–255) → limitada (tv, 16–235)",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-vf", "scale=in_range=pc:out_range=tv,format=yuv420p", *H264, "-c:a", "copy", "{sai}"],
         fonte=FF + "#scale-1 · EBU R103 v3.0 (faixa cheia precisa estar sinalizada no contêiner)",
         nota="Só se R01 mostrar color_range=pc E o conteúdo for de fato 0–255 (signalstats YMIN≈0/YMAX≈255 em área grande). "
              "format=yuv420p sozinho NÃO converte faixa (testado na pesquisa)."),
    dict(id="R05", area="entrada", titulo="Corrigir só a etiqueta (sem mexer nos pixels)",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-vf", "setparams=range=tv:colorspace=bt709:color_primaries=bt709:color_trc=bt709",
              *H264, "-c:a", "copy", "{sai}"],
         fonte=FF + "#setparams", nota="Etiqueta ≠ conversão: setparams só declara. Usar quando o arquivo está certo mas sem tag."),
    dict(id="R06", area="entrada", titulo="Reenquadrar 16:9 → 9:16 (corte central)",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-vf", "crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920:flags=lanczos",
              *H264, "-c:a", "copy", "{sai}"],
         fonte=FF + "#crop", nota="Trocar o x do crop para seguir o rosto. Em fonte 9:16 a receita corta de novo: só para fonte horizontal."),
    # ---------------------------------------------------------------- DIAGNÓSTICO
    dict(id="R10", area="diagnóstico", titulo="Números por quadro (signalstats) em texto",
         cmd=["ffmpeg", "-v", "error", "-i", "{ent}", "-vf", "signalstats=stat=brng,metadata=mode=print:file=stats.txt",
              "-f", "null", "-"],
         saida=False, fonte=FF + "#signalstats-1 · " + FF + "#metadata_002c-ametadata",
         nota="Grava stats.txt na pasta atual (file= relativo evita escape de caminho). "
              "Valores na profundidade do arquivo (10 bits: 64–940). BRNG = fração de pixels fora de 16–235/16–240 "
              "(fixo, ignora color_range). HUEMED usa atan2(U,V)+180, outra convenção que a do vectorscope. "
              "Para a folha completa use escopos.py."),
    dict(id="R11", area="diagnóstico", titulo="Waveform + parade + vectorscope do ffmpeg num quadro",
         cmd=["ffmpeg", "-y", "-ss", "{t}", "-i", "{ent}", "-frames:v", "1", "-filter_complex",
              "[0:v]scale=540:-2,format=yuv444p,split=2[a][b];[a]waveform=g=green:fl=numbers:d=parade:c=7,scale=-2:540,format=rgb24[w];[b]vectorscope=m=color3:g=color:f=white+black+name,scale=540:540,format=rgb24[v];[w][v]hstack=inputs=2[s]", "-map", "[s]", "{sai_png}"],
         fonte=FF + "#waveform · " + FF + "#vectorscope",
         nota="O vectorscope do ffmpeg não desenha a linha de pele; para ela use escopos.py."),
    dict(id="R12", area="diagnóstico", titulo="Detectar cortes (cenas)",
         cmd=["ffmpeg", "-i", "{ent}", "-vf", "scale=320:-2,scdet=t=10,metadata=mode=print:key=lavfi.scd.time", "-f", "null", "-"],
         saida=False, fonte=FF + "#scdet-1", nota="t menor = mais cortes. Cortes a ≤0,3 s um do outro são o mesmo corte/transição."),
    # ---------------------------------------------------------------- COR PRIMÁRIA (sempre em RGB 16 bits)
    dict(id="R20", area="cor", titulo="Pontos de preto e branco por canal (normalizar + equilibrar)",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-vf",
              "format=gbrp16le,colorlevels=rimin=0.02:gimin=0.02:bimin=0.03:rimax=0.97:gimax=0.98:bimax=0.99,format=yuv420p",
              *H264, "-c:a", "copy", "{sai}"],
         fonte=FF + "#colorlevels · Colorist Guide Resolve 20, lição 5 (equilibrar antes do look)",
         nota="Valores do exemplo: tirar do diagnóstico (baixas_RGB / altas_RGB em %). format=gbrp16le antes: medido, sem ele o Y médio cai 1,1 código."),
    dict(id="R21", area="cor", titulo="Balanço por faixa (sombras / médios / altas)",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-vf",
              "format=gbrp16le,colorbalance=rs=0:bs=0.01:rh=-0.02:bh=0.02:pl=1,format=yuv420p", *H264, "-c:a", "copy", "{sai}"],
         fonte=FF + "#colorbalance", nota="pl=1 preserva a luminância. Valores -1..1; ajustes reais ficam em ±0,01–0,05 (prática comum, sem fonte)."),
    dict(id="R22", area="cor", titulo="Temperatura de cor",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-vf", "format=gbrp16le,colortemperature=temperature=6200:pl=1,format=yuv420p",
              *H264, "-c:a", "copy", "{sai}"],
         fonte=FF + "#colortemperature", nota="6500 = neutro. Abaixo esquenta, acima esfria. Kelly: balancear temperatura primeiro, depois verde/magenta."),
    dict(id="R23", area="cor", titulo="Contraste com pivô (linear)",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-vf",
              "format=gbrp16le,lutrgb=r='clip((val/maxval-0.435)*1.1+0.435,0,1)*maxval':g='clip((val/maxval-0.435)*1.1+0.435,0,1)*maxval':"
              "b='clip((val/maxval-0.435)*1.1+0.435,0,1)*maxval',format=yuv420p", *H264, "-c:a", "copy", "{sai}"],
         fonte=FF + "#lutrgb · Colorist Guide Resolve 20 (Contrast + Pivot)",
         nota="Pivô = ponto que não se move. 0,435 é o pivô padrão do Resolve (Colorist Guide); escolher pelo Y médio da cena."),
    dict(id="R24", area="cor", titulo="Curva em S suave",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-vf", "format=gbrp16le,curves=all='0/0 0.25/0.22 0.75/0.79 1/1',format=yuv420p",
              *H264, "-c:a", "copy", "{sai}"], fonte=FF + "#curves", nota="Pontos x/y em 0–1 (0 = preto legal)."),
    dict(id="R25", area="cor", titulo="Saturação exata (matriz BT.709, cinza parado)",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-vf",
              "format=gbrp16le,colorchannelmixer=rr=1.0787:rg=-0.0715:rb=-0.0072:gr=-0.0213:gg=1.0285:gb=-0.0072:br=-0.0213:"
              "bg=-0.0715:bb=1.0928,format=yuv420p", *H264, "-c:a", "copy", "{sai}"],
         fonte=FF + "#colorchannelmixer · ITU-R BT.709-6 (pesos de luma 0,2126/0,7152/0,0722)",
         nota="Exemplo = saturação 1,10. graduar.py calcula a matriz para qualquer valor."),
    dict(id="R26", area="cor", titulo="Vibrância (satura mais o que está pouco saturado)",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-vf", "format=gbrp16le,vibrance=intensity=0.15,format=yuv420p", *H264, "-c:a", "copy", "{sai}"],
         fonte=FF + "#vibrance", nota="Conferir a pele no vectorscope depois: vibrância também empurra tom de pele."),
    dict(id="R27", area="cor", titulo="Legalizar no fim (trava 16–235 / 16–240)",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-vf",
              "format=yuv444p16le,limiter=min=4096:max=60160:planes=1,limiter=min=4096:max=61440:planes=6,format=yuv420p",
              *H264, "-c:a", "copy", "{sai}"],
         fonte=FF + "#limiter · EBU R103 v3.0 (legalizar só depois de todo o resto)",
         nota="Corte seco: se muita área bate no limite, corrija a cor antes em vez de cortar aqui."),
    # ---------------------------------------------------------------- LOOK / LUT
    dict(id="R30", area="look", titulo="Aplicar LUT .cube",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-vf", "format=gbrp16le,lut3d=file='{lut_f}':interp=tetrahedral,format=yuv420p",
              *H264, "-c:a", "copy", "{sai}"],
         fonte=FF + "#lut3d · Adobe Cube LUT Specification 1.0 · Colorist Guide (interpolação tetraédrica)",
         nota="A LUT espera um espaço de entrada; aplicar LUT de Log em vídeo Rec.709 estraga a cor."),
    dict(id="R31", area="look", titulo="LUT com intensidade (mistura com o original)",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-filter_complex",
              "[0:v]format=gbrp16le,split[a][b];[b]lut3d=file='{lut_f}'[l];[a][l]blend=all_expr='A*0.4+B*0.6'[o];[o]format=yuv420p[v]",
              "-map", "[v]", "-map", "0:a?", *H264, "-c:a", "copy", "{sai}"],
         fonte=FF + "#blend-1", nota="0,6 = 60% da LUT. Alternativa: gerar_lut.py --misturar --forca 0.6 (uma LUT só)."),
    # ---------------------------------------------------------------- CORTE / MONTAGEM
    dict(id="R40", area="corte", titulo="Recortar trecho com precisão de quadro",
         cmd=["ffmpeg", "-y", "-ss", "1.5", "-i", "{ent}", "-t", "2", *H264, "-c:a", "aac", "-b:a", "192k", "{sai}"],
         fonte="https://ffmpeg.org/ffmpeg.html#Main-options",
         nota="-ss antes do -i + reencode = preciso. Com -c copy o corte cai no keyframe mais próximo (impreciso)."),
    dict(id="R41", area="corte", titulo="Juntar trechos (concat com reencode)",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-i", "{ent2}", "-filter_complex",
              "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]", "-map", "[v]", "-map", "[a]", *H264, "-c:a", "aac", "-b:a", "192k", "{sai}"],
         fonte=FF + "#concat", nota="Os trechos precisam ter mesma resolução, fps e formato de áudio. Para J/L cut use montar.py."),
    dict(id="R42", area="corte", titulo="Dissolve / transição (xfade + acrossfade)",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-i", "{ent2}", "-filter_complex",
              "[0:v][1:v]xfade=transition=fade:duration=0.5:offset={off}[v];[0:a][1:a]acrossfade=d=0.5[a]",
              "-map", "[v]", "-map", "[a]", *H264, "-c:a", "aac", "-b:a", "192k", "{sai}"],
         fonte=FF + "#xfade · " + FF + "#acrossfade", nota="offset = duração do 1º trecho − duração da transição."),
    # ---------------------------------------------------------------- CAMADAS / TEXTO
    dict(id="R50", area="camadas", titulo="Logo PNG com transparência no canto",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-i", "{logo}", "-filter_complex",
              "[1:v]scale=220:-1[l];[0:v][l]overlay=W-w-80:260:format=auto,format=yuv420p[v]", "-map", "[v]", "-map", "0:a?",
              *H264, "-c:a", "copy", "{sai}"],
         fonte=FF + "#overlay-1", nota="Posição dentro da área segura da plataforma (referencias/plataformas.md)."),
    dict(id="R51", area="camadas", titulo="Texto com caixa (drawtext)",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-vf",
              "drawtext=fontfile='/System/Library/Fonts/Supplemental/Arial.ttf':text='TEXTO EXATO':fontsize=64:fontcolor=white:"
              "box=1:boxcolor=black@0.6:boxborderw=24:x=(w-text_w)/2:y=h*0.62:enable='between(t,0.5,2.5)'",
              *H264, "-c:a", "copy", "{sai}"],
         fonte=FF + "#drawtext-1", nota="Texto verbatim da lista fechada. Fonte da marca: trocar fontfile pelo arquivo .ttf/.otf."),
    dict(id="R52", area="camadas", titulo="Queimar legenda ASS",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-vf", "subtitles='{ass_f}':fontsdir='{fontes_f}'", *H264, "-c:a", "copy", "{sai}"],
         fonte=FF + "#subtitles-1 (estilo ASS BorderStyle 4)",
         nota="Estilo testado: Montserrat SemiBold 58 em 1080×1920, BorderStyle 4, MarginV 440."),
    dict(id="R53", area="camadas", titulo="Vinheta",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-vf", "vignette=angle=PI/5", *H264, "-c:a", "copy", "{sai}"],
         fonte=FF + "#vignette", nota="Efeito espacial: fica fora da LUT. Acabamento, depois do look."),
    dict(id="R54", area="camadas", titulo="Modo de mesclagem (tela) entre duas camadas",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-i", "{ent2}", "-filter_complex",
              "[0:v]format=gbrp[a];[1:v]format=gbrp[b];[a][b]blend=all_mode=screen:all_opacity=0.35,format=yuv420p[v]",
              "-map", "[v]", "-map", "0:a?", "-shortest", *H264, "-c:a", "copy", "{sai}"],
         fonte=FF + "#blend-1", nota="Mesclar em RGB (format=gbrp) para o modo bater com o do After Effects/Photoshop."),
    # ---------------------------------------------------------------- MOVIMENTO
    dict(id="R60", area="movimento", titulo="Zoom-in suave sem tremer (easing inOut)",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-vf",
              "scale=iw*4:ih*4:flags=lanczos,zoompan=z='1+0.12*(3*pow(min(on/({d}*30),1),2)-2*pow(min(on/({d}*30),1),3))':"
              "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30",
              *H264, "-c:a", "copy", "{sai}"],
         fonte=FF + "#zoompan · smoothstep 3t²−2t³ (easing inOut)",
         nota="Ampliar 4× antes do zoompan evita o tremor do arredondamento de posição (prática comum, sem fonte oficial; testar na folha)."),
    dict(id="R61", area="movimento", titulo="Estabilizar (vidstab, 2 passadas)",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-vf", "vidstabdetect=shakiness=5:result={trf_f}", "-f", "null", "-",
              "&&", "ffmpeg", "-y", "-i", "{ent}", "-vf", "vidstabtransform=input={trf_f}:smoothing=30:zoom=5,unsharp=5:5:0.6",
              *H264, "-c:a", "copy", "{sai}"],
         fonte=FF + "#vidstabdetect-1 · " + FF + "#vidstabtransform-1", nota="zoom=5 corta 5% para esconder borda. Mais suavização = mais corte."),
    dict(id="R62", area="movimento", titulo="Câmera lenta 50% com áudio",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-filter_complex", "[0:v]setpts=2*PTS[v];[0:a]atempo=0.5[a]",
              "-map", "[v]", "-map", "[a]", *H264, "-c:a", "aac", "-b:a", "192k", "{sai}"],
         fonte=FF + "#setpts_002c-asetpts · " + FF + "#atempo", nota="Duplica quadros. Para fluidez real precisa de fonte 60 fps (60→30 = 50% limpo)."),
    # ---------------------------------------------------------------- ACABAMENTO
    dict(id="R70", area="acabamento", titulo="Redução de ruído (hqdn3d) antes da cor",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-vf", "hqdn3d=2:1.5:3:3", *H264, "-c:a", "copy", "{sai}"],
         fonte=FF + "#hqdn3d-1 · Colorist Guide Resolve 20, lição 8 (denoise logo após a entrada)", nota="Forte demais = pele de cera."),
    dict(id="R71", area="acabamento", titulo="Nitidez no fim (cas)",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-vf", "cas=strength=0.4", *H264, "-c:a", "copy", "{sai}"],
         fonte=FF + "#cas", nota="Último filtro antes do encode (Mixing Light: nitidez no fim da cadeia)."),
    dict(id="R72", area="acabamento", titulo="Tirar banding de degradê (deband)",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-vf", "deband=1thr=0.02:2thr=0.02:3thr=0.02:range=16:blur=1", *H264, "-c:a", "copy", "{sai}"],
         fonte=FF + "#deband", nota="Céu, parede lisa, fundo degradê. Granulação leve também mascara (noise=alls=4:allf=t)."),
    # ---------------------------------------------------------------- ÁUDIO
    dict(id="R80", area="áudio", titulo="Medir loudness (EBU R128)",
         cmd=["ffmpeg", "-nostats", "-i", "{ent}", "-af", "ebur128=peak=true", "-f", "null", "-"], saida=False,
         fonte=FF + "#ebur128-1 · EBU R128 / ITU-R BS.1770", nota="Ler o resumo no fim: I (integrado, LUFS), LRA, True peak."),
    dict(id="R81", area="áudio", titulo="Normalizar loudness (loudnorm)",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1:LRA=11", "-c:a", "aac", "-b:a", "192k",
              "-ar", "48000", "{sai}"],
         fonte=FF + "#loudnorm · EBU R128 (método)",
         nota="-14 LUFS para redes = prática comum, sem fonte oficial da Meta/TikTok. Broadcast EBU R128 = -23 LUFS."),
    dict(id="R82", area="áudio", titulo="Abaixar a trilha quando há voz (ducking)",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-i", "{ent2}", "-filter_complex",
              "[1:a]volume=0.5[m];[0:a]asplit[voz][sc];[m][sc]sidechaincompress=threshold=0.05:ratio=8:attack=20:release=300[md];"
              "[voz][md]amix=inputs=2:normalize=0[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
              "-shortest", "{sai}"],
         fonte=FF + "#sidechaincompress", nota="ent = vídeo com voz; ent2 = trilha. Trilha licenciada (biblioteca da plataforma ou do cliente)."),
    # ---------------------------------------------------------------- ENTREGA / QC
    dict(id="R90", area="entrega", titulo="Exportar para Reels/TikTok (H.264, BT.709, faststart)",
         cmd=["ffmpeg", "-y", "-i", "{ent}", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-profile:v", "high",
              "-pix_fmt", "yuv420p", *TAGS, "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "{sai}"],
         fonte="https://ffmpeg.org/ffmpeg-codecs.html#libx264_002c-libx264rgb · specs da plataforma em referencias/plataformas.md",
         nota="CRF 18 = alta qualidade para sobreviver à recompressão da plataforma (prática comum, sem fonte oficial)."),
    dict(id="R91", area="entrega", titulo="Conferir encode contra o master (VMAF)",
         cmd=["ffmpeg", "-i", "{ent}", "-i", "{ent}", "-lavfi", "[0:v][1:v]libvmaf=n_threads=4", "-f", "null", "-"], saida=False,
         fonte=FF + "#libvmaf · Netflix VMAF", nota="1ª entrada = distorcido, 2ª = referência. No teste usa o mesmo arquivo (VMAF ≈ 100)."),
]


def achar(rid):
    for r in R:
        if r["id"].lower() == rid.lower():
            return r
    raise SystemExit(f"receita {rid} não existe")


def fmt(cmd):
    return " ".join(shlex.quote(c) if (" " in c or "'" in c or ";" in c or "[" in c) else c for c in cmd)


def preparar_assets(pasta, clipe):
    from PIL import Image, ImageDraw
    pasta.mkdir(parents=True, exist_ok=True)
    logo = pasta / "logo_teste.png"
    im = Image.new("RGBA", (400, 160), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 399, 159], 30, fill=(255, 255, 255, 200))
    d.text((40, 50), "LOGO", fill=(20, 20, 20, 255))
    im.save(logo)
    ass = pasta / "teste.ass"
    ass.write_text("""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,58,&H00FFFFFF,&H00FFFFFF,&HFF000000,&H80000000,1,0,0,0,100,100,0,0,4,18,0,2,80,80,440,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.20,0:00:02.50,Default,,0,0,0,,Legenda de teste
""", encoding="utf-8")
    lut = pasta / "teste.cube"
    subprocess.run([sys.executable, str(Path(__file__).parent / "gerar_lut.py"), "--cadeia",
                    "colortemperature=temperature=6000", "-o", str(lut)], check=True, capture_output=True)
    # 2ª entrada: outro trecho do mesmo clipe, mesmo formato
    ent2 = pasta / "trecho2.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "4", "-i", str(clipe), "-t", "3", *H264, "-c:a", "aac", "-b:a", "192k",
                    "-ar", "48000", str(ent2)], check=True)
    ent = pasta / "trecho1.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(clipe), "-t", "3", *H264, "-c:a", "aac", "-b:a", "192k",
                    "-ar", "48000", str(ent)], check=True)
    # trecho HLG 10 bits (HEVC, BT.2020, ARIB STD-B67), como o iPhone grava — para testar a R03 de verdade
    ent_hlg = pasta / "trecho_hlg.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(ent), "-vf",
                    "zscale=tin=bt709:t=arib-std-b67:pin=bt709:p=bt2020:min=bt709:m=2020_ncl:r=tv,format=yuv420p10le",
                    "-c:v", "libx265", "-x265-params",
                    "colorprim=bt2020:transfer=arib-std-b67:colormatrix=bt2020nc:range=limited:log-level=error",
                    "-tag:v", "hvc1", "-c:a", "copy", str(ent_hlg)], check=True)
    return ent, ent2, logo, ass, lut, ent_hlg


def esc_f(p):
    return Path(p).resolve().as_posix().replace(":", "\\:")


def montar(cmd, subs):
    out = []
    for c in cmd:
        for k, v in subs.items():
            c = c.replace("{" + k + "}", str(v))
        out.append(c)
    return out


def testar(clipe, pasta, so=None):
    ent, ent2, logo, ass, lut, ent_hlg = preparar_assets(pasta, clipe)
    fontes = Path("/System/Library/Fonts/Supplemental")  # Mac
    resultados = []
    for r in R:
        if so and r["id"] not in so:
            continue
        sai = pasta / f"{r['id']}.mp4"
        subs = {"ent": ent, "ent2": ent2, "ent_hlg": ent_hlg, "sai": sai, "sai_png": pasta / f"{r['id']}.png", "logo": logo, "ass": ass,
                "lut": lut, "fontes": fontes, "t": "1.0", "d": "3", "off": "2.5", "ent_f": esc_f(ent).replace("'", ""),
                "lut_f": esc_f(lut), "ass_f": esc_f(ass), "fontes_f": esc_f(fontes), "trf_f": "transforms.trf"}
        cmd = montar(r["cmd"], subs)
        partes = [[]]
        for c in cmd:
            if c == "&&":
                partes.append([])
            else:
                partes[-1].append(c)
        t0 = time.time()
        ok, erro = True, ""
        for p in partes:
            pr = subprocess.run(p, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=pasta)
            if pr.returncode != 0:
                ok, erro = False, (pr.stderr or pr.stdout)[-400:]
                break
        dur = time.time() - t0
        info = ""
        if ok and r.get("saida", True):
            alvo = subs["sai_png"] if "{sai_png}" in r["cmd"] else sai
            pr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                 "stream=width,height,nb_frames,color_space,color_range", "-of", "csv=p=0", str(alvo)],
                                capture_output=True, text=True)
            info = pr.stdout.strip()
            if not info:
                ok, erro = False, "saída sem vídeo"
        resultados.append({"id": r["id"], "titulo": r["titulo"], "ok": ok, "segundos": round(dur, 1), "saida": info, "erro": erro})
        print(f"{'OK ' if ok else 'ERRO'} {r['id']} {r['titulo']} ({dur:.1f}s) {info}" + ("" if ok else f"\n     {erro}"), flush=True)
    (pasta / "resultado_testes.json").write_text(json.dumps(resultados, ensure_ascii=False, indent=2), encoding="utf-8")
    falhas = [x for x in resultados if not x["ok"]]
    print(f"\n{len(resultados) - len(falhas)}/{len(resultados)} receitas OK")
    return not falhas


def md():
    L = ["# Receitas ffmpeg — testadas", "",
         "Gerado por `scripts/receitas.py md`. Testar de novo: `python scripts/receitas.py testar clipe.mp4`.", "",
         "Regras que valem para todas (medidas aqui, 05/11/2026, ffmpeg 8.1.2):",
         "- Filtro de cor em RGB (`colorlevels`, `colorbalance`, `colortemperature`, `curves`, `lutrgb`, `lut3d`, `colorchannelmixer`, "
         "`vibrance`) vem depois de `format=gbrp16le`. Sem isso o ffmpeg negocia RGB de 8 bits e a ida e volta perde 1,1 código de Y "
         "médio (139,73 → 138,61) e corta super-brancos; com 16 bits a ida e volta sai exata (139,74).",
         "- Caminho em filtro no Mac: `file='/pasta/arquivo.cube'` (aspas simples; caminho com `:` ou espaço precisa de escape com `\\`).",
         "- Tags de saída: `-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv` — conferidas com ffprobe nas saídas.",
         ""]
    area = None
    for r in R:
        if r["area"] != area:
            area = r["area"]
            L += [f"## {area.capitalize()}", ""]
        L += [f"### {r['id']} — {r['titulo']}", "", "```bash", fmt(r["cmd"]), "```", "",
              f"- **Fonte:** {r['fonte']}", f"- **Nota:** {r['nota']}", ""]
    return "\n".join(L)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="acao", required=True)
    sp.add_parser("listar")
    m = sp.add_parser("mostrar")
    m.add_argument("id")
    t = sp.add_parser("testar")
    t.add_argument("clipe")
    t.add_argument("-o", "--pasta", default="teste_receitas")
    t.add_argument("--so")
    sp.add_parser("md")
    a = ap.parse_args()
    if a.acao == "listar":
        for r in R:
            print(f"{r['id']}  [{r['area']}]  {r['titulo']}")
    elif a.acao == "mostrar":
        r = achar(a.id)
        print(fmt(r["cmd"]))
        print("Fonte:", r["fonte"])
        print("Nota:", r["nota"])
    elif a.acao == "testar":
        so = set(a.so.split(",")) if a.so else None
        sys.exit(0 if testar(Path(a.clipe).resolve(), Path(a.pasta).resolve(), so) else 1)
    elif a.acao == "md":
        print(md())


if __name__ == "__main__":
    main()
