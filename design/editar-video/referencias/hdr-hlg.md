# HLG / HDR do celular → SDR BT.709

Base: pesquisa feita em 05/11/2026 em fontes primárias (normas ITU/EBU, manuais Adobe/Blackmagic, documentação das plataformas), citadas linha a linha, mais medições locais com ffmpeg 8.1.2.
Legenda: **[norma]** · **[oficial]** · **[medido]** · **[sem fonte]**.

## 1. Como reconhecer

`receitas.py mostrar R01`: `color_transfer=arib-std-b67` = HLG; `smpte2084` = PQ. O iPhone grava Dolby Vision perfil 8.4 sobre base HLG: HEVC Main10, 10 bits, primárias/matriz BT.2020 (códigos 9/18/9), com átomo `amve`. — Apple TN3145 **[oficial]**

Mostrar HLG numa tela BT.709 sem converter dá imagem dessaturada com desvio de matiz. — ITU-R BT.2408-9 §3.2.1; BT.2390-12 §6.4 **[norma]**. Só trocar a etiqueta para BT.709 deixa o cinza mais ou menos no lugar, mas lava a cor (vermelho saturado → RGB 199,46,27). **[medido pela pesquisa]**

## 2. Níveis de referência HLG (ITU-R BT.2408-9, 03/2026) [norma]

| Referência | Sinal HLG | cd/m² (tela de 1000) |
|---|---|---|
| Branco de referência (cartão branco 100%, gráficos) | 75% | 203 |
| Cartão cinza 18% | 38% | 26 |
| Pele clara (Fitzpatrick 1–2) | 55–65% | 65–110 |
| Pele média (3–4) | 45–60% | 40–85 |
| Pele escura (5–6) | 25–45% | 10–40 |

## 3. Onde o branco de referência deve cair no SDR

- BT.2446-1 Método B: ≈90% SDR (branco difuso em SDR graduado costuma ficar em ~90%). **[norma]**
- BT.2408-9: ~95% em produção ao vivo; mínimo de 86% citado; estudo da Philips 91–100%. **[norma]**
- Converter imagem acabada por luz de tela (display-light), comprimindo as altas acima do branco de referência; corte seco só se o sinal for muito controlado. — BT.2408-9 §5.2, §7.6.4 **[norma]**
- Converter cor antes ou junto da passagem de 10 para 8 bits; quantizar antes dá banding. — Apple, *Incorporating HDR video with Dolby Vision* **[oficial]**

## 4. A cadeia (medida aqui, 05/11/2026, em patches HLG 10 bits gerados no ffmpeg)

```
zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:param=0.7:desat=0:peak=4.926,zscale=t=bt709:m=bt709:r=tv,format=yuv420p
```

| Cadeia | Cinza 18% (38% HLG) | Branco ref. (75%) | ~60% HLG (pele clara) | 100% HLG |
|---|---|---|---|---|
| **Atual: npl=203 + mobius 0,7** | **43,4%** | **88,6%** | 65,8% | 99,1% |
| Antiga (versão anterior): npl=100 + mobius | 58,4% | 89,5% | — | 98,6% |
| npl=203 + mobius 0,5 | 43,4% | 84,9% | 65,8% | 98,2% |
| npl=203 + hable | 32,0% | 61,6% | 47,5% | 90,4% |
| npl=203 + clip | 43,4% | 89,0% | 65,8% | 100% (corta) |

Referência para o cinza: a OETF do BT.709 leva 18% de reflectância a ≈41% de sinal **[norma, cálculo]**. A cadeia antiga deixava médios e pele ~15 pontos claros demais.

**Por que npl=203 e peak=4,926:** o `zscale` (zimg) lineariza HLG supondo tela de 1000 cd/m² com gama 1,2; `npl` define qual luminância vira 1,0 linear. Com npl=203, o branco de referência (203 cd/m²) vira 1,0. Sem metadado, o `tonemap` supõe pico 10; com npl≠100 o pico tem que ir à mão: 1000/203 = 4,926. — código do zimg e `libavfilter/colorspace.c` **[oficial: código-fonte]**

**Limites desta cadeia:**
- Testada em patches sintéticos e num trecho HLG gerado no teste (`receitas.py testar`), **ainda não num arquivo HLG de iPhone real**. No primeiro vídeo HLG real, rodar `escopos.py --sdr` e conferir pele e cinza.
- Conversores divergem em cor saturada: um patch de pele saiu RGB 218,124,102 no zscale e 241,147,124 no libplacebo. Conferir a pele no vectorscope. **[medido pela pesquisa]**
- O libplacebo no padrão sai bem mais escuro (cinza 30%, branco 69%), e a detecção de pico faz o resultado depender do conteúdo de cada quadro. Não usar sem configurar. **[medido pela pesquisa]**
- O efeito do metadado Dolby Vision do iPhone (`apply_dolbyvision` no libplacebo) não foi testado.

## 5. Entregar HDR ou converter?

A Meta aceita HDR (HLG/PQ) no Reels e gera a versão SDR no servidor com o próprio tonemap (Meta Engineering, 07/2023). Não há spec oficial da Meta ou do TikTok sobre como tratam HDR enviado **[sem fonte oficial de spec]**. Padrão desta skill: **entregar SDR BT.709**, para o resultado não depender do tonemap de cada plataforma e aparelho. Se o usuário quiser testar HDR, é decisão dele.
