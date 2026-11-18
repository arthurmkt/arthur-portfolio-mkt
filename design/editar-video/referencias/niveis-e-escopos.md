# Níveis legais e leitura de escopos

Base: pesquisa feita em 05/11/2026 em fontes primárias (normas ITU/EBU, manuais Adobe/Blackmagic, documentação das plataformas), citadas linha a linha, mais medições locais com ffmpeg 8.1.2.
Legenda: **[norma]** · **[oficial]** · **[profissional]** · **[medido]** · **[sem fonte]** (prática comum, não é regra).

## 1. Números do BT.709 (ITU-R BT.709-6, 06/2015) [norma]

| | 8 bits | 10 bits |
|---|---|---|
| Preto (Y e R'G'B') | 16 | 64 |
| Branco nominal | 235 | 940 |
| Croma (Cb, Cr) | 16–240, neutro 128 | 64–960, neutro 512 |
| Reservado (sincronismo) | 0 e 255 | 0–3 e 1020–1023 |
| Pesos de luma | Y' = 0,2126 R' + 0,7152 G' + 0,0722 B' | |

Fórmula: D = INT[(219·E' + 16)·2^(n−8)] para luma/RGB; D = INT[(224·E' + 128)·2^(n−8)] para croma. — BT.709-6, itens 3.2–3.4, 4.6, 4.7.

O monitor de referência é BT.1886 (gama 2,4, branco de referência 100 cd/m²); ele não muda nenhum parâmetro do sinal BT.709. — ITU-R BT.1886-0 **[norma]**

## 2. Tolerância (EBU R103 v3.0, maio/2020) [norma]

| Faixa | 8 bits | 10 bits |
|---|---|---|
| Nominal (alvo de material graduado) | 16–235 | 64–940 |
| Preferida (tolerância) | 5–246 | 20–984 |
| Total (teto absoluto) | 1–254 | 4–1019 |

- Vale igual para **Y e para R, G, B**.
- Só é "fora do gamut" se **mais de 1% da área** sair da faixa preferida, medido depois de um filtro passa-baixa (horizontal 1,2,3,4,3,2,1 /16; vertical 1,2,1 /4).
- Material graduado deve ficar perto da faixa **nominal**; a preferida é folga para ao vivo e conversão HDR→SDR.
- Legalizador só no fim, com cautela: pode criar artefato pior que o erro.
- Faixa cheia em arquivo é permitida, desde que sinalizada no contêiner.
- ⚠️ **Conflito:** a versão de 2000 (Y −1% a 103%, RGB −5% a 105%) foi substituída em 2016/2020, mas ainda aparece em specs de emissora. Se houver spec de entrega própria, vale a spec.

**Plataformas sociais:** Meta, TikTok e YouTube não publicam limite de nível ou de gamut. O YouTube trata SDR como BT.709 e converte faixa cheia em limitada. — YouTube Help 1722171 **[oficial]**. Que plataformas tratem arquivo sem tag como limitado/BT.709 é **[sem fonte]**.

## 3. Como o `escopos.py` mede (e por quê)

| Número | O que é | Por quê |
|---|---|---|
| Preto/branco efetivos | percentis 0,1% e 99,9% do Y no quadro do meio, resolução cheia | YMIN/YMAX do signalstats pegam um pixel isolado (no Roteiro 1 deram 0 e 255 com 99,9% dos pixels entre 16 e 235) **[medido]** |
| Fora 16–235 | BRNG do signalstats, média da cena | BRNG usa 16–235/16–240 fixos e ignora `color_range`: arquivo em faixa cheia dá alarme falso. Conferir R01 antes **[oficial: vf_signalstats.c]** |
| Fora gamut RGB | % da área com R, G ou B fora de 5–246 | R103 v3.0. Sem o filtro da norma, então é um pouco mais rígido **[norma, adaptado]** |
| Altas/baixas RGB | média de R, G, B nos 5% mais claros/escuros | Neutro = R=G=B; diferença no topo = dominante nas altas, embaixo = nas sombras. — Adobe "Working with Video Scopes" (08/2026) **[oficial]** |
| Pele | ângulo mediano no vectorscope vs linha de 123° | ver `pele.md` |

- O `signalstats` dá valores na profundidade do arquivo (10 bits: 64–940); o `escopos.py` converte para escala de 8 bits. **[medido]**
- O HUEMED do `signalstats` usa atan2(U,V)+180 (vermelho ≈167, amarelo ≈95, cinza 180). É outra convenção que a do vectorscope; para a pele, vale o ângulo do `escopos.py`. **[medido pela pesquisa]**

## 4. Lendo cada escopo

- **Waveform Y:** altura = brilho, posição horizontal = posição no quadro. Escala 0–100% (Adobe: parecida com IRE, mas não igual). — Adobe "Working with Video Scopes" **[oficial]**
- **Parade RGB:** três waveforms lado a lado. Em área neutra (parede branca, papel, cinza) os três ficam da mesma altura; diferença no alto = dominante nas altas, embaixo = nas sombras. Corrige com níveis por canal. — Adobe; documentação ffmpeg `waveform` **[oficial]**
- **Vectorscope:** ângulo = matiz, distância do centro = saturação. Caixas internas = 75%, externas = 100%. Mancha centrada = balanço neutro; deslocada = dominante para aquele lado. — Adobe **[oficial]**
- **Histograma:** distribuição sem posição; serve para ver acúmulo encostado nas pontas (corte), não para localizar problema. — Frame.io Workflow Guide **[profissional]**
- O passa-baixa do escopo esconde pico; no Resolve, "Extents" mostra o excesso real. — resumo do manual Resolve 21.1 **[secundário]**

## 5. Alvos aproximados (não são regra)

- Preto em 0–2% e branco difuso em 90–95% com especular a 100% em SDR web: conselho comum de tutorial **[sem fonte]**.
- Rosto claro a 60–70% IRE em SDR: regra de bolso **[sem fonte]**; a tabela atribuída a Van Hurkman (via Larry Jordan, 2021) dá luma de pele clara 45–70%, média 30–60%, escura 15–35% **[secundário]**.
- Diferença máxima de 2–3% entre canais em área neutra como critério de aprovação **[sem fonte]**. O `escopos.py` alerta acima de 6 pontos nas altas e 4 nas baixas: são limiares nossos, de triagem.
