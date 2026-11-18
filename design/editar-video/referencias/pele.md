# Pele: linha de pele, faixa de saturação, sintomas

Base: pesquisa feita em 05/11/2026 (manual do DaVinci Resolve, artigos de Cullen Kelly na Frame.io, ColorChecker) mais medição local com ffmpeg 8.1.2.
Legenda: **[oficial]** manual do fabricante · **[prática]** colorista reconhecido · **[medido]** teste local · **[sem fonte]** prática comum sem número publicado.

## 1. A linha de pele

- Quase todo vectorscope (Resolve, Lumetri, ScopeBox) desenha uma linha entre o alvo vermelho e o amarelo, a ~123° no sentido anti-horário a partir do eixo +Cb, por volta de 11 horas. O manual do Resolve chama de "referência geral para o matiz médio da pele", não de alvo exato. **[oficial]**
- Pele saudável sob luz neutra, de qualquer tom, cai numa cunha estreita perto dessa linha. O tom de pele muda principalmente o brilho e a saturação, quase nada o matiz. **[prática]**
- A pessoa julga pele como "cor de memória": pele puxando para verde ou magenta parece errada muito antes do resto do quadro. Por isso é a checagem de matiz mais útil que existe. **[prática]**
- Medido aqui: o patch "light skin" do ColorChecker cai em 123,0° e o "dark skin" em 122,2°, com 21% e 16% do raio máximo de croma. **[medido]**

## 2. Como medir (o que o `escopos.py` faz)

- Recortar **só pele**: testa, bochecha ou pescoço, com luz uniforme, sem brilho especular, maquiagem, lábios, cabelo ou fundo. `--pele x,y,w,h` (frações do quadro) quando a máscara automática pegar madeira, bege ou laranja.
- Medir **no espaço de exibição** (BT.709 SDR), depois da conversão de HLG/log. Ângulo medido em log ou HLG não significa nada.
- Ângulo θ = atan2(Cr−128, Cb−128) em graus (8 bits, faixa limitada, BT.709). Croma % = hypot(Cb−128, Cr−128) / 112 × 100.
- Equivalência com o `signalstats` do ffmpeg: θ = (270 − HUEAVG) mod 360. A linha de 123° corresponde a HUEAVG ≈ 146–147. **[medido]**
- Medir de novo no arquivo final codificado: tag de cor errada (BT.601 no lugar de BT.709) gira a pele ~3°.

## 3. Faixas de trabalho

| O quê | Alvo | Tolerância |
|---|---|---|
| Ângulo médio da pele (luz neutra) | ~123° | ±5° = "na linha"; até ±10° com luz quente/fria motivada **[sem fonte para o número]** |
| Croma da pele | 15–30% do raio máximo | acima de ~40% fica laranja/queimada de sol **[sem fonte para o número]** |
| Diferença entre planos da mesma pessoa na mesma cena | o menor possível | até ~3–5° **[sem fonte]** |

Nenhuma norma de transmissão nem plataforma (Meta, TikTok, YouTube) reprova vídeo por matiz de pele. Pele nunca é parâmetro legal; só conta para gamut quando a saturação é empurrada demais.

## 4. Ordem de correção

1. Balanço de branco e exposição nas primárias. A pele tem que estar certa quando as primárias terminam. **[prática]**
2. Curvas, depois Hue-vs-Hue para **comprimir** os matizes vizinhos na direção da linha (ex.: ponto laranja-amarelo +7 a +8°, laranja do meio −5 a −6°). **[prática]**
3. Qualificador (máscara de pele) só em último caso, largo e suave. Em vídeo 4:2:0 comprimido, máscara estreita dá halo e mancha.
4. Look criativo só depois. Se a pele fora da linha é intenção (cena quente de pôr do sol), ela fica: a linha é guia, não lei.

## 5. Sintoma → causa → correção

| Sintoma | Causa provável | Correção |
|---|---|---|
| Pele amarelada/esverdeada; traço para o amarelo (> ~130°) | luz fluorescente/LED verde, balanço de branco da câmera, Hue-vs-Hue empurrando laranja para amarelo | corrigir tint (mais magenta) nas primárias sobre algo neutro; não girar o matiz da imagem toda |
| Pele rosada/magenta ou vermelha; traço para o vermelho (< ~115°) | tint magenta, correção de verde exagerada, blush na amostra, saturação nos vermelhos | tirar magenta; amostrar pele sem maquiagem; baixar saturação de vermelho (`huesaturation colors=r`) |
| Pele laranja ou de plástico depois do tratamento | saturação global ou aquecimento que sobe o croma (medido: +6 pontos de croma) | recuar a saturação global, usar vibrância; manter croma da pele em ~30% ou menos |
| Traço da pele dividido em dois braços | duas temperaturas de luz no rosto (janela + lâmpada) | equilibrar pelo lado da luz principal; aceitar diferença parcial no outro |
| Pele muda entre planos da mesma pessoa | balanço automático do iPhone, câmeras diferentes, look aplicado desigual | medir θ por plano e igualar nas primárias até poucos graus |
| Pele certa no editor e errada na plataforma | tag de cor ausente/errada ou HLG não convertido | converter para BT.709 SDR, gravar as tags e medir no arquivo final |

## 6. Erros comuns

- Medir o quadro inteiro: o fundo domina o escopo. Sempre recortar pele.
- Girar a imagem toda com `hue=h` para pôr a pele na linha: todas as outras cores giram junto.
- Achar que pele negra e pele clara pedem ângulos diferentes. Mudam brilho e croma, não o matiz.
- Neutralizar uma cena quente ou fria que era intencional.
- Comparar escopos de programas diferentes sem saber se o gráfico é Cb/Cr ou U/V e qual matriz (601/709) ele usa.
