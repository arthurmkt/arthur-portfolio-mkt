# Correção de cor: ordem, contraste, saturação

Base: pesquisa feita em 05/11/2026 em fontes primárias (normas ITU/EBU, manuais Adobe/Blackmagic, documentação das plataformas), citadas linha a linha, mais medições locais com ffmpeg 8.1.2.
Legenda: **[norma]** norma ITU/EBU · **[oficial]** manual Blackmagic/Adobe/ffmpeg · **[profissional]** colorista publicado · **[medido]** teste nosso aqui, ffmpeg 8.1.2 · **[sem fonte]** prática comum, não é regra.

## 1. Ordem de sinal (o que vem antes de quê)

| # | Etapa | No `graduar.py` | Fonte |
|---|---|---|---|
| 0 | Conformar: VFR→CFR, HLG→SDR, faixa, escala | `conformar` | Colorist Guide Resolve 20, lição 7: transformação de cor no início (Pre-Clip) **[oficial]** |
| 1 | Redução de ruído | `filtro` antes da cor | Colorist Guide 20, lição 8: denoise logo após a transformação de entrada deu o melhor resultado **[oficial]** |
| 2 | Faixa tonal: preto, branco, contraste | `niveis`, `contraste`, `curva` | Colorist Guide 20, lição 1 (faixa tonal primeiro); Van Hurkman, *Color Correction Handbook* 2ª ed., cap. 4: contraste antes da cor; Adobe Color mode: contraste/exposição global antes dos controles por zona **[oficial]** |
| 3 | Equilíbrio de cor: temperatura, depois verde/magenta | `temperatura`, `balanco` | Cullen Kelly, Mixing Light "10-Minute Grade: Shot Balancing": temperatura primeiro, depois tint, lendo o vectorscope **[profissional]** |
| 4 | Igualar cenas | `cenas[]` | Colorist Guide 20, lição 1–2: equilibrar e igualar antes do look **[oficial]** |
| 5 | Secundárias (pele, céu) | `filtro` com máscara | Colorist Guide 20, lição 5: equilíbrio, igualar e secundárias antes de contraste forte/criativo **[oficial]** |
| 6 | Look (LUT criativa, saturação de estilo) | `look[]` | Colorist Guide 20, lição 7: look no Post-Clip, depois de igualar; LUT 33 ou 65 pontos, interpolação tetraédrica **[oficial]** |
| 7 | Acabamento: vinheta, granulação, nitidez | `acabamento[]` | Mixing Light (Dan Moran): nitidez no fim da cadeia **[profissional]**; Colorist Guide 20: Timeline só para grão/vinheta/saída **[oficial]** |
| 8 | Legalizar | `legalizar: true` | EBU R103 v3.0: legalizador só depois de todo o resto, com cautela **[norma]** |
| 9 | Texto, legenda, logo | receitas R50–R52 | ITU-R BT.2408-9 §9: gráficos e legendas na saída SDR, depois da conversão **[norma]** |
| 10 | Encode com tags BT.709 | R90 | ver `entrega.md` |

**Por que a ordem importa:** cada etapa recebe o que a anterior entregou. Um preto esmagado cedo não volta depois: no exemplo da lição 5 do Colorist Guide, Lift −0,20 num nó e "restaurar" com curva no nó seguinte deu sombra chapada, manchada e supersaturada **[oficial]**.

**Conflito registrado:** Kelly monta o look global primeiro e corrige plano a plano por baixo; o Colorist Guide equilibra primeiro. Os dois concordam na **ordem de sinal** (equilíbrio antes, look depois); só muda a ordem em que o colorista trabalha. Para um pipeline em código, vale a ordem de sinal.

## 2. Contraste e curvas

- Lift = ponto de preto, Gain = ponto de branco, Gamma = médios; mexer muito no Gamma empurra os extremos, então iterar entre os três. — Resolve 18 Reference Manual, cap. 129 **[oficial]**
- Contraste afasta claros e escuros em torno do **pivô**. Imagem escura → pivô mais baixo (não esmagar sombra); imagem clara → pivô mais alto. — Resolve 18, cap. 129 **[oficial]**. Ao aumentar contraste, mover o pivô para que as altas subam mais do que as baixas descem. — Adobe Color mode, Default Adjust **[oficial]**
- Pivô padrão do Resolve 0,435: citado em fórum e no DCTL de Cullen Kelly, **não está no manual** **[sem fonte oficial]**. O 18% cinza no BT.709 codifica em ≈0,409 (OETF BT.709).
- Contraste "S" com ombro suave em vez de cortar nos extremos (padrão "Use S-curve for contrast" ligado). — Resolve 18, cap. 129/130 **[oficial]**
- Curva com dobra brusca ou pontos muito próximos dá contorno e solarização. — Resolve 18, cap. 132 **[oficial]**
- Contraste em RGB junto aumenta a saturação; contraste só no Y reduz a saturação percebida. — Resolve 18, cap. 129 **[oficial]**. ⚠️ Num teste da pesquisa a saturação medida não subiu com curva S em RGB: conferir no olho **[medido, divergente]**.
- Branco certo depende da imagem: especular e fonte de luz podem ir a 100%; rosto num interior baixo a 100% fica errado. — Apple Color 1.5 User Manual **[oficial]**
- **No ffmpeg:**
  - `eq` só aceita YUV 8 bits e pivota em 0,5 da faixa 0–255; em 10 bits converte para 8 sem avisar (banding). Não usar no fluxo HLG/10 bits. — `vf_eq.c` + teste local **[oficial + medido]**
  - `curves` só trabalha em RGB; pontos crescentes em x; `interp=pchip` garante curva monotônica. — documentação ffmpeg + `vf_curves.c` **[oficial]**
  - `lutyuv` trava sempre em 16–235/16–240 (64–940 em 10 bits), mesmo em faixa cheia; `clip()` precisa de 3 argumentos no 8.1.2. — `vf_lut.c` + teste local **[oficial + medido]**
  - Contraste com pivô exato: `lutrgb` linear (receita R23, op `contraste` do `graduar.py`).

## 3. Saturação e vibrância

- Saturação escala todas as cores por igual; vibrância mexe mais no que está pouco saturado e protege a pele (magenta→laranja mexe menos). — manual do After Effects, efeito Vibrance **[oficial]**
- No Resolve, Color Boost é o controle tipo vibrância; Saturation é o uniforme (−100 a +100). — Resolve 15 manual **[oficial]**. Mixing Light (Inhofer, 2019) questiona o rótulo "vibrância" **[profissional, conflito]**.
- Saturação estourando em altas/baixas: corrigir com curva Lum vs Sat, com queda suave, não com corte global. Para cortar só os pixels mais saturados: Sat vs Sat. — Resolve 15 manual **[oficial]**
- **Saturação exata no ffmpeg:** matriz `colorchannelmixer` com os pesos de luma BT.709 (0,2126 / 0,7152 / 0,0722, ITU-R BT.709-6 item 3.2): cinza fica parado e só a croma escala. É a op `saturacao` do `graduar.py` **[norma + medido]**.
- `vibrance` e `huesaturation` convertem para RGB por conta própria; dentro do `graduar.py` já entram em `gbrp16le`. **[medido]**
- "Manter o vectorscope dentro das caixas de 75%" como regra de rede social: **[sem fonte]** para web.
- Limite numérico tipo "nunca mais de +20–30% de saturação": opinião de praticante (Larry Jordan ~20%) **[sem fonte]**.

## 4. Precisão (medido aqui, 05/11/2026)

| Teste | Y médio | Y p90 | Conclusão |
|---|---|---|---|
| Original | 139,73 | 221,81 | — |
| `curves` neutro, RGB negociado sozinho (8 bits) | 138,61 | 220,45 | perde 1,1 código e corta super-branco |
| `format=gbrp16le,curves` neutro | 139,74 | 221,81 | ida e volta exata |

**Regra:** todo filtro de cor em RGB vem depois de `format=gbrp16le`. O `graduar.py` já faz isso.

- A etapa RGB16 já recorta R, G, B em 0–100%; por isso a saída do `graduar.py` fica dentro do gamut RGB. O `limiter` em YUV **não** corrige gamut RGB: num teste da pesquisa, 41,7% dos pixels continuavam fora depois dele. **[medido pela pesquisa]**
- O BRNG do `signalstats` subconta erro de gamut: 5,7% de BRNG para 35,7% de erro RGB real. Para gamut, vale o "fora gamut RGB" do `escopos.py`. **[medido pela pesquisa]**
