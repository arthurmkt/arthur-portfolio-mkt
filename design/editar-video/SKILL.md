---
name: editar-video
description: Edita vídeo real em nível profissional com ffmpeg local — correção de cor (normalizar → equilibrar → igualar cenas → look), saturação, contraste, níveis legais BT.709, tom de pele, HLG do iPhone para SDR, cortes, J/L cut, camadas, texto, legenda, LUT .cube, zoom/estabilização, loudness e entrega para Reels/TikTok. Julga cor por medição (escopos e números por cena), não por "parece", e entrega folha antes/depois com os números. Use quando pedirem "editar vídeo", "corrigir cor", "color", "colorir", "igualar as cenas", "tá lavado", "tá escuro", "pele estranha", "aplicar LUT", "gerar LUT", "cortar", "J cut", "L cut", "legendar e tratar", "deixar o vídeo profissional" ou /editar-video. Motion graphics feito do zero é a /motion.
user-invocable: true
---

# Edição de vídeo medida

**Princípio:** cor se julga por medição. Toda mudança de cor que eu proponho vem com o número que a motivou (escopo, percentil, ângulo de pele) e com o número depois. Toda regra desta skill tem fonte ao lado; o que não tem fonte aparece como **[sem fonte]** e nunca como regra.

**Limite declarado:** eu vejo quadros e números, não assisto o vídeo rodando. **Ritmo, sensação do corte e gosto do look são julgamento de quem pediu.** Na entrega, peço explicitamente que a pessoa assista no celular.

**Requisitos:** ffmpeg e ffprobe (testado no 8.1.2, com libvidstab para a R61), Python 3.10+ com `numpy` e `Pillow` (`pip install numpy pillow`).

## Arquivos

| Arquivo | Para quê |
|---|---|
| `scripts/escopos.py` | diagnóstico por cena: folha de escopos (waveform, parade RGB, vectorscope com linha de pele, histograma) + `diagnostico.md/json` com alertas e fonte |
| `scripts/comparar.py` | antes × depois por cena: folha, `split_cenaN.png` em 1080, tabela de números e alertas resolvidos/novos |
| `scripts/graduar.py` | aplica o plano de correção (JSON) na ordem de sinal, em RGB 16 bits; `--previa` gera quadros parados antes/depois |
| `scripts/gerar_lut.py` | transforma a correção aprovada num `.cube` (33/65) para Premiere/Resolve/CapCut e prova por PSNR |
| `scripts/montar.py` | monta trechos com corte seco, J cut e L cut a partir de uma lista (JSON) |
| `scripts/receitas.py` | 38 receitas ffmpeg com fonte; `testar clipe.mp4` roda todas; `md` gera `referencias/receitas-ffmpeg.md` |
| `referencias/cor-fluxo.md` | ordem de sinal, contraste, curvas, saturação, precisão 16 bits |
| `referencias/niveis-e-escopos.md` | BT.709, EBU R103 v3.0, como ler cada escopo, como o script mede |
| `referencias/pele.md` | linha de pele, faixa de croma, sintoma → causa → correção |
| `referencias/hdr-hlg.md` | HLG do iPhone → SDR, níveis BT.2408, cadeia medida |
| `referencias/corte.md` | Murch (regra de seis, piscar), corte na ação, J/L cut, emendas de áudio, sincronia |
| `referencias/plataformas.md` | Meta e TikTok: formato, área segura, duração, o que é oficial e o que não é |
| `referencias/receitas-ffmpeg.md` | as 38 receitas por grupo (entrada, diagnóstico, cor, look, corte, camadas, movimento, acabamento, áudio, entrega) |

Pasta de trabalho: uma pasta por peça (ex.: `editar-video/<projeto>/<peça>/`): bruto, plano, prévias, folhas e final juntos.

Nos comandos abaixo, `~/.claude/skills/editar-video` é o lugar onde a skill foi instalada. Ajuste se instalou em outro lugar.

---

## Passo 0 — Entrada (sem portão)

```bash
python ~/.claude/skills/editar-video/scripts/receitas.py mostrar R01   # e rodar com o arquivo
```

Decidir antes de tudo, pelos números do ffprobe:
- `color_transfer=arib-std-b67` (HLG) ou `smpte2084` (PQ) → converter para SDR primeiro (`referencias/hdr-hlg.md`, R03). Nunca só trocar a etiqueta.
- `r_frame_rate ≠ avg_frame_rate` → taxa variável: R02 antes de cortar (a Meta exige taxa fixa, Ads Guide).
- `color_range=pc` → conferir se o conteúdo é mesmo 0–255 antes de converter (R04). O `signalstats` ignora a etiqueta de faixa.
- Arquivo de IA, gravação de tela: costumam vir sem tag ou em faixa cheia. Medir antes de supor.

## Passo 1 — Diagnóstico medido (portão 1)

```bash
python ~/.claude/skills/editar-video/scripts/escopos.py bruto.mp4 -o diag            # SDR
python ~/.claude/skills/editar-video/scripts/escopos.py bruto.mp4 -o diag --sdr      # HLG: mede depois do tonemap
python ~/.claude/skills/editar-video/scripts/escopos.py bruto.mp4 --pele 0.35,0.15,0.3,0.25   # região do rosto
```

Ler a folha pelo método VER → AMPLIAR → CONFIRMAR: o quadro, depois cada escopo, depois o número. Mostrar:
1. a folha (`folha_escopos.png`) e a tabela por cena;
2. **fatos medidos**, um por linha, com a regra e a fonte: "Cena 2: altas R 98,6 / G 90,0 / B 80,2 → dominante quente nas altas, se a parede for branca (Adobe, parade RGB)";
3. o que não sei pela medição (ex.: se o tom quente é intencional).

A máscara de pele automática (Chai & Ngan) pega madeira, bege e laranja. Se o rosto estiver pequeno ou houver objeto da mesma cor, passar `--pele` com a região do rosto.

**Portão 1:** quem pediu confirma o que é problema e o que é intenção. Não corrijo dominante que a pessoa quer.

## Passo 2 — Plano de correção e prévia (portão 2)

Escrever `plano.json` (formato no topo do `graduar.py`). Cada operação leva o motivo medido num campo `"porque"`. Ordem fixa: conformar → global → cenas (igualar) → look → acabamento → legalizar (`referencias/cor-fluxo.md`, seção 1).

- **Normalizar:** pontos de preto/branco por canal (`niveis`) a partir de `baixas_RGB` / `altas_RGB`.
- **Equilibrar:** temperatura primeiro, depois verde/magenta (`temperatura`, `balanco`).
- **Igualar cenas:** escolher a cena de referência (a mais aberta ou a mais próxima do look desejado, Colorist Guide 20, lição 2) e aproximar Y médio, altas RGB e pele das outras.
- **Look:** só depois de igualar. Saturação de estilo, LUT criativa. **Look é gosto: proponho, a pessoa decide.**

```bash
python ~/.claude/skills/editar-video/scripts/graduar.py plano.json --mostrar   # cadeia de filtros
python ~/.claude/skills/editar-video/scripts/graduar.py plano.json --previa    # antes|depois do meio de cada cena
```

**Portão 2:** aprovação da prévia. Ajuste vem com cena e quanto ("cena 3 menos quente, metade"). Mudo só o que foi pedido.

## Passo 3 — Render e comparação medida (portão 3)

```bash
python ~/.claude/skills/editar-video/scripts/graduar.py plano.json
python ~/.claude/skills/editar-video/scripts/comparar.py bruto.mp4 corrigido.mp4 -o comparacao --zoom-vs 2
```

Entregar `folha_antes_depois.png` + `comparacao.md` (números antes → depois, alertas resolvidos e novos, amplitude entre cenas). Se surgiu alerta novo, corrijo antes de mostrar.

**Portão 3:** aprovação do vídeo corrigido, assistido por quem pediu.

## Passo 4 — Corte, camadas, texto, movimento (quando pedido)

- **Corte:** lista de trechos em JSON → `montar.py` (seco, J, L). Regras e fontes em `referencias/corte.md`. Eu meço duração de plano e cortes por minuto; **o ritmo é a pessoa quem julga.**
- **Texto, legenda, logo:** R50–R52, sempre dentro da área segura da plataforma (`referencias/plataformas.md`). Texto literal de uma lista fechada. Legenda segue a fala, com tempo de leitura de 1 s para cada 3 palavras + 1 s.
- **Movimento sobre o vídeo:** zoom/pan com easing (R60), estabilização (R61), velocidade (R62).
- **Motion graphics do zero** (tipografia cinética, números animados): skill `/motion`, com o vídeo entrando como sequência de quadros.
- **Ordem:** gráficos e legenda entram **depois** da cor e da conversão HDR→SDR (ITU-R BT.2408-9 §9).

## Passo 5 — Revisão e entrega

Checklist antes de mostrar:
1. `comparar.py` sem alerta de nível/gamut no final; tags BT.709 conferidas com ffprobe.
2. Resolução, fps fixo, duração, nº de quadros, sem quadro preto no início/fim.
3. Texto dentro da área segura; legenda batendo com a fala.
4. Loudness medido (R80) e informado. O alvo de -14 LUFS é **[sem fonte oficial]**; uso se a pessoa concordar.
5. Encode R90 (H.264, yuv420p, BT.709, +faststart).
6. Sem flash forte nem branco liso nos 3 primeiros segundos se for TopView do TikTok (`plataformas.md`).
7. Pedir a passada de quem pediu, no celular: ritmo, sensação, pele.

Look aprovado que vai ser reaproveitado → `gerar_lut.py --plano plano.json -o <projeto>_look.cube` e `--conferir` para provar.

## Regras de código (medidas com ffmpeg 8.1.2, 05/11/2026)

1. Filtro de cor em RGB vem depois de `format=gbrp16le`. Em 8 bits a ida e volta perde 1,1 código de Y médio; em 16 bits sai exata.
2. Não usar `eq` em fluxo 10 bits/HLG: ele força 8 bits.
3. Caminho em filtro: `file='/pasta/arquivo.cube'` (aspas simples; caminho com `:` ou espaço precisa de escape com `\`).
4. Tags na saída: `-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv` (+ `setparams` no fim da cadeia do `graduar.py`).
5. Legalizar só no fim (EBU R103 v3.0). O `limiter` não corrige gamut RGB; a etapa RGB16 já recorta.
6. `-ss` antes do `-i` com reencode = corte preciso; com `-c copy` o corte cai no keyframe.
