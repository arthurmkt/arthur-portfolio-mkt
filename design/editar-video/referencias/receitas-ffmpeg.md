# Receitas ffmpeg — testadas

Gerado por `scripts/receitas.py md`. Testar de novo: `python scripts/receitas.py testar clipe.mp4`.

Regras que valem para todas (medidas aqui, 05/11/2026, ffmpeg 8.1.2):
- Filtro de cor em RGB (`colorlevels`, `colorbalance`, `colortemperature`, `curves`, `lutrgb`, `lut3d`, `colorchannelmixer`, `vibrance`) vem depois de `format=gbrp16le`. Sem isso o ffmpeg negocia RGB de 8 bits e a ida e volta perde 1,1 código de Y médio (139,73 → 138,61) e corta super-brancos; com 16 bits a ida e volta sai exata (139,74).
- Caminho em filtro no Mac: `file='/pasta/arquivo.cube'` (aspas simples; caminho com `:` ou espaço precisa de escape com `\`).
- Tags de saída: `-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv` — conferidas com ffprobe nas saídas.

## Entrada

### R01 — Ler formato, faixa e tags de cor

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height,pix_fmt,r_frame_rate,avg_frame_rate,color_range,color_space,color_transfer,color_primaries:format=duration -of json {ent}
```

- **Fonte:** https://ffmpeg.org/ffprobe.html
- **Nota:** r_frame_rate ≠ avg_frame_rate indica taxa variável (VFR). color_transfer arib-std-b67 = HLG; smpte2084 = PQ.

### R02 — Taxa variável (VFR do celular) → constante

```bash
ffmpeg -y -i {ent} -vf fps=30 -fps_mode cfr -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a aac -b:a 192k {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#fps-1
- **Nota:** fps duplica/descarta quadros para a grade de 30. Fazer ANTES de cortar, senão o corte cai fora do quadro.

### R03 — HLG do iPhone → SDR BT.709 (tonemap mobius)

```bash
ffmpeg -y -i {ent_hlg} -vf zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:param=0.7:desat=0:peak=4.926,zscale=t=bt709:m=bt709:r=tv,format=yuv420p -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a copy {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#tonemap-1 · ITU-R BT.2408 (branco ref. = 75% HLG, cinza 18% = 38% HLG) · BT.2446 (branco ref. ≈ 90% SDR)
- **Nota:** Só para fonte HLG/PQ (conferir R01). Medido 05/11 em patches HLG: cinza 18% → 43,4% SDR (OETF BT.709 dá ~41%), branco ref. → 88,6%, 100% HLG → 99,1%. A cadeia antiga npl=100 punha o cinza em 58% (médios e pele claros demais). Pele: conferir no vectorscope, conversores diferentes divergem em cor saturada.

### R04 — Faixa cheia (pc, 0–255) → limitada (tv, 16–235)

```bash
ffmpeg -y -i {ent} -vf scale=in_range=pc:out_range=tv,format=yuv420p -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a copy {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#scale-1 · EBU R103 v3.0 (faixa cheia precisa estar sinalizada no contêiner)
- **Nota:** Só se R01 mostrar color_range=pc E o conteúdo for de fato 0–255 (signalstats YMIN≈0/YMAX≈255 em área grande). format=yuv420p sozinho NÃO converte faixa (testado na pesquisa).

### R05 — Corrigir só a etiqueta (sem mexer nos pixels)

```bash
ffmpeg -y -i {ent} -vf setparams=range=tv:colorspace=bt709:color_primaries=bt709:color_trc=bt709 -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a copy {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#setparams
- **Nota:** Etiqueta ≠ conversão: setparams só declara. Usar quando o arquivo está certo mas sem tag.

### R06 — Reenquadrar 16:9 → 9:16 (corte central)

```bash
ffmpeg -y -i {ent} -vf crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920:flags=lanczos -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a copy {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#crop
- **Nota:** Trocar o x do crop para seguir o rosto. Em fonte 9:16 a receita corta de novo: só para fonte horizontal.

## Diagnóstico

### R10 — Números por quadro (signalstats) em texto

```bash
ffmpeg -v error -i {ent} -vf signalstats=stat=brng,metadata=mode=print:file=stats.txt -f null -
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#signalstats-1 · https://ffmpeg.org/ffmpeg-filters.html#metadata_002c-ametadata
- **Nota:** Grava stats.txt na pasta atual (file= relativo evita escape de caminho). Valores na profundidade do arquivo (10 bits: 64–940). BRNG = fração de pixels fora de 16–235/16–240 (fixo, ignora color_range). HUEMED usa atan2(U,V)+180, outra convenção que a do vectorscope. Para a folha completa use escopos.py.

### R11 — Waveform + parade + vectorscope do ffmpeg num quadro

```bash
ffmpeg -y -ss {t} -i {ent} -frames:v 1 -filter_complex '[0:v]scale=540:-2,format=yuv444p,split=2[a][b];[a]waveform=g=green:fl=numbers:d=parade:c=7,scale=-2:540,format=rgb24[w];[b]vectorscope=m=color3:g=color:f=white+black+name,scale=540:540,format=rgb24[v];[w][v]hstack=inputs=2[s]' -map '[s]' {sai_png}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#waveform · https://ffmpeg.org/ffmpeg-filters.html#vectorscope
- **Nota:** O vectorscope do ffmpeg não desenha a linha de pele; para ela use escopos.py.

### R12 — Detectar cortes (cenas)

```bash
ffmpeg -i {ent} -vf scale=320:-2,scdet=t=10,metadata=mode=print:key=lavfi.scd.time -f null -
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#scdet-1
- **Nota:** t menor = mais cortes. Cortes a ≤0,3 s um do outro são o mesmo corte/transição.

## Cor

### R20 — Pontos de preto e branco por canal (normalizar + equilibrar)

```bash
ffmpeg -y -i {ent} -vf format=gbrp16le,colorlevels=rimin=0.02:gimin=0.02:bimin=0.03:rimax=0.97:gimax=0.98:bimax=0.99,format=yuv420p -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a copy {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#colorlevels · Colorist Guide Resolve 20, lição 5 (equilibrar antes do look)
- **Nota:** Valores do exemplo: tirar do diagnóstico (baixas_RGB / altas_RGB em %). format=gbrp16le antes: medido, sem ele o Y médio cai 1,1 código.

### R21 — Balanço por faixa (sombras / médios / altas)

```bash
ffmpeg -y -i {ent} -vf format=gbrp16le,colorbalance=rs=0:bs=0.01:rh=-0.02:bh=0.02:pl=1,format=yuv420p -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a copy {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#colorbalance
- **Nota:** pl=1 preserva a luminância. Valores -1..1; ajustes reais ficam em ±0,01–0,05 (prática comum, sem fonte).

### R22 — Temperatura de cor

```bash
ffmpeg -y -i {ent} -vf format=gbrp16le,colortemperature=temperature=6200:pl=1,format=yuv420p -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a copy {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#colortemperature
- **Nota:** 6500 = neutro. Abaixo esquenta, acima esfria. Kelly: balancear temperatura primeiro, depois verde/magenta.

### R23 — Contraste com pivô (linear)

```bash
ffmpeg -y -i {ent} -vf 'format=gbrp16le,lutrgb=r='"'"'clip((val/maxval-0.435)*1.1+0.435,0,1)*maxval'"'"':g='"'"'clip((val/maxval-0.435)*1.1+0.435,0,1)*maxval'"'"':b='"'"'clip((val/maxval-0.435)*1.1+0.435,0,1)*maxval'"'"',format=yuv420p' -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a copy {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#lutrgb · Colorist Guide Resolve 20 (Contrast + Pivot)
- **Nota:** Pivô = ponto que não se move. 0,435 é o pivô padrão do Resolve (Colorist Guide); escolher pelo Y médio da cena.

### R24 — Curva em S suave

```bash
ffmpeg -y -i {ent} -vf 'format=gbrp16le,curves=all='"'"'0/0 0.25/0.22 0.75/0.79 1/1'"'"',format=yuv420p' -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a copy {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#curves
- **Nota:** Pontos x/y em 0–1 (0 = preto legal).

### R25 — Saturação exata (matriz BT.709, cinza parado)

```bash
ffmpeg -y -i {ent} -vf format=gbrp16le,colorchannelmixer=rr=1.0787:rg=-0.0715:rb=-0.0072:gr=-0.0213:gg=1.0285:gb=-0.0072:br=-0.0213:bg=-0.0715:bb=1.0928,format=yuv420p -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a copy {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#colorchannelmixer · ITU-R BT.709-6 (pesos de luma 0,2126/0,7152/0,0722)
- **Nota:** Exemplo = saturação 1,10. graduar.py calcula a matriz para qualquer valor.

### R26 — Vibrância (satura mais o que está pouco saturado)

```bash
ffmpeg -y -i {ent} -vf format=gbrp16le,vibrance=intensity=0.15,format=yuv420p -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a copy {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#vibrance
- **Nota:** Conferir a pele no vectorscope depois: vibrância também empurra tom de pele.

### R27 — Legalizar no fim (trava 16–235 / 16–240)

```bash
ffmpeg -y -i {ent} -vf format=yuv444p16le,limiter=min=4096:max=60160:planes=1,limiter=min=4096:max=61440:planes=6,format=yuv420p -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a copy {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#limiter · EBU R103 v3.0 (legalizar só depois de todo o resto)
- **Nota:** Corte seco: se muita área bate no limite, corrija a cor antes em vez de cortar aqui.

## Look

### R30 — Aplicar LUT .cube

```bash
ffmpeg -y -i {ent} -vf 'format=gbrp16le,lut3d=file='"'"'{lut_f}'"'"':interp=tetrahedral,format=yuv420p' -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a copy {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#lut3d · Adobe Cube LUT Specification 1.0 · Colorist Guide (interpolação tetraédrica)
- **Nota:** A LUT espera um espaço de entrada; aplicar LUT de Log em vídeo Rec.709 estraga a cor.

### R31 — LUT com intensidade (mistura com o original)

```bash
ffmpeg -y -i {ent} -filter_complex '[0:v]format=gbrp16le,split[a][b];[b]lut3d=file='"'"'{lut_f}'"'"'[l];[a][l]blend=all_expr='"'"'A*0.4+B*0.6'"'"'[o];[o]format=yuv420p[v]' -map '[v]' -map 0:a? -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a copy {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#blend-1
- **Nota:** 0,6 = 60% da LUT. Alternativa: gerar_lut.py --misturar --forca 0.6 (uma LUT só).

## Corte

### R40 — Recortar trecho com precisão de quadro

```bash
ffmpeg -y -ss 1.5 -i {ent} -t 2 -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a aac -b:a 192k {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg.html#Main-options
- **Nota:** -ss antes do -i + reencode = preciso. Com -c copy o corte cai no keyframe mais próximo (impreciso).

### R41 — Juntar trechos (concat com reencode)

```bash
ffmpeg -y -i {ent} -i {ent2} -filter_complex '[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]' -map '[v]' -map '[a]' -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a aac -b:a 192k {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#concat
- **Nota:** Os trechos precisam ter mesma resolução, fps e formato de áudio. Para J/L cut use montar.py.

### R42 — Dissolve / transição (xfade + acrossfade)

```bash
ffmpeg -y -i {ent} -i {ent2} -filter_complex '[0:v][1:v]xfade=transition=fade:duration=0.5:offset={off}[v];[0:a][1:a]acrossfade=d=0.5[a]' -map '[v]' -map '[a]' -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a aac -b:a 192k {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#xfade · https://ffmpeg.org/ffmpeg-filters.html#acrossfade
- **Nota:** offset = duração do 1º trecho − duração da transição.

## Camadas

### R50 — Logo PNG com transparência no canto

```bash
ffmpeg -y -i {ent} -i {logo} -filter_complex '[1:v]scale=220:-1[l];[0:v][l]overlay=W-w-80:260:format=auto,format=yuv420p[v]' -map '[v]' -map 0:a? -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a copy {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#overlay-1
- **Nota:** Posição dentro da área segura da plataforma (referencias/plataformas.md).

### R51 — Texto com caixa (drawtext)

```bash
ffmpeg -y -i {ent} -vf 'drawtext=fontfile='"'"'/System/Library/Fonts/Supplemental/Arial.ttf'"'"':text='"'"'TEXTO EXATO'"'"':fontsize=64:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=24:x=(w-text_w)/2:y=h*0.62:enable='"'"'between(t,0.5,2.5)'"'"'' -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a copy {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#drawtext-1
- **Nota:** Texto verbatim da lista fechada. Fonte da marca: trocar fontfile pelo arquivo .ttf/.otf.

### R52 — Queimar legenda ASS

```bash
ffmpeg -y -i {ent} -vf 'subtitles='"'"'{ass_f}'"'"':fontsdir='"'"'{fontes_f}'"'"'' -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a copy {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#subtitles-1 (estilo ASS BorderStyle 4)
- **Nota:** Estilo testado: Montserrat SemiBold 58 em 1080×1920, BorderStyle 4, MarginV 440.

### R53 — Vinheta

```bash
ffmpeg -y -i {ent} -vf vignette=angle=PI/5 -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a copy {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#vignette
- **Nota:** Efeito espacial: fica fora da LUT. Acabamento, depois do look.

### R54 — Modo de mesclagem (tela) entre duas camadas

```bash
ffmpeg -y -i {ent} -i {ent2} -filter_complex '[0:v]format=gbrp[a];[1:v]format=gbrp[b];[a][b]blend=all_mode=screen:all_opacity=0.35,format=yuv420p[v]' -map '[v]' -map 0:a? -shortest -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a copy {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#blend-1
- **Nota:** Mesclar em RGB (format=gbrp) para o modo bater com o do After Effects/Photoshop.

## Movimento

### R60 — Zoom-in suave sem tremer (easing inOut)

```bash
ffmpeg -y -i {ent} -vf 'scale=iw*4:ih*4:flags=lanczos,zoompan=z='"'"'1+0.12*(3*pow(min(on/({d}*30),1),2)-2*pow(min(on/({d}*30),1),3))'"'"':x='"'"'iw/2-(iw/zoom/2)'"'"':y='"'"'ih/2-(ih/zoom/2)'"'"':d=1:s=1080x1920:fps=30' -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a copy {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#zoompan · smoothstep 3t²−2t³ (easing inOut)
- **Nota:** Ampliar 4× antes do zoompan evita o tremor do arredondamento de posição (prática comum, sem fonte oficial; testar na folha).

### R61 — Estabilizar (vidstab, 2 passadas)

```bash
ffmpeg -y -i {ent} -vf vidstabdetect=shakiness=5:result={trf_f} -f null - && ffmpeg -y -i {ent} -vf vidstabtransform=input={trf_f}:smoothing=30:zoom=5,unsharp=5:5:0.6 -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a copy {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#vidstabdetect-1 · https://ffmpeg.org/ffmpeg-filters.html#vidstabtransform-1
- **Nota:** zoom=5 corta 5% para esconder borda. Mais suavização = mais corte.

### R62 — Câmera lenta 50% com áudio

```bash
ffmpeg -y -i {ent} -filter_complex '[0:v]setpts=2*PTS[v];[0:a]atempo=0.5[a]' -map '[v]' -map '[a]' -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a aac -b:a 192k {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#setpts_002c-asetpts · https://ffmpeg.org/ffmpeg-filters.html#atempo
- **Nota:** Duplica quadros. Para fluidez real precisa de fonte 60 fps (60→30 = 50% limpo).

## Acabamento

### R70 — Redução de ruído (hqdn3d) antes da cor

```bash
ffmpeg -y -i {ent} -vf hqdn3d=2:1.5:3:3 -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a copy {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#hqdn3d-1 · Colorist Guide Resolve 20, lição 8 (denoise logo após a entrada)
- **Nota:** Forte demais = pele de cera.

### R71 — Nitidez no fim (cas)

```bash
ffmpeg -y -i {ent} -vf cas=strength=0.4 -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a copy {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#cas
- **Nota:** Último filtro antes do encode (Mixing Light: nitidez no fim da cadeia).

### R72 — Tirar banding de degradê (deband)

```bash
ffmpeg -y -i {ent} -vf deband=1thr=0.02:2thr=0.02:3thr=0.02:range=16:blur=1 -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a copy {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#deband
- **Nota:** Céu, parede lisa, fundo degradê. Granulação leve também mascara (noise=alls=4:allf=t).

## Áudio

### R80 — Medir loudness (EBU R128)

```bash
ffmpeg -nostats -i {ent} -af ebur128=peak=true -f null -
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#ebur128-1 · EBU R128 / ITU-R BS.1770
- **Nota:** Ler o resumo no fim: I (integrado, LUFS), LRA, True peak.

### R81 — Normalizar loudness (loudnorm)

```bash
ffmpeg -y -i {ent} -c:v copy -af loudnorm=I=-14:TP=-1:LRA=11 -c:a aac -b:a 192k -ar 48000 {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#loudnorm · EBU R128 (método)
- **Nota:** -14 LUFS para redes = prática comum, sem fonte oficial da Meta/TikTok. Broadcast EBU R128 = -23 LUFS.

### R82 — Abaixar a trilha quando há voz (ducking)

```bash
ffmpeg -y -i {ent} -i {ent2} -filter_complex '[1:a]volume=0.5[m];[0:a]asplit[voz][sc];[m][sc]sidechaincompress=threshold=0.05:ratio=8:attack=20:release=300[md];[voz][md]amix=inputs=2:normalize=0[a]' -map 0:v -map '[a]' -c:v copy -c:a aac -b:a 192k -shortest {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#sidechaincompress
- **Nota:** ent = vídeo com voz; ent2 = trilha. Trilha licenciada (biblioteca da plataforma ou do cliente).

## Entrega

### R90 — Exportar para Reels/TikTok (H.264, BT.709, faststart)

```bash
ffmpeg -y -i {ent} -c:v libx264 -preset slow -crf 18 -profile:v high -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart -c:a aac -b:a 192k -ar 48000 {sai}
```

- **Fonte:** https://ffmpeg.org/ffmpeg-codecs.html#libx264_002c-libx264rgb · specs da plataforma em referencias/plataformas.md
- **Nota:** CRF 18 = alta qualidade para sobreviver à recompressão da plataforma (prática comum, sem fonte oficial).

### R91 — Conferir encode contra o master (VMAF)

```bash
ffmpeg -i {ent} -i {ent} -lavfi '[0:v][1:v]libvmaf=n_threads=4' -f null -
```

- **Fonte:** https://ffmpeg.org/ffmpeg-filters.html#libvmaf · Netflix VMAF
- **Nota:** 1ª entrada = distorcido, 2ª = referência. No teste usa o mesmo arquivo (VMAF ≈ 100).

