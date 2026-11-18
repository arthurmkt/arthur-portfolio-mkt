# Plataformas: formato, área segura, ritmo

Base: pesquisa feita em 05/11/2026 em fontes primárias (normas ITU/EBU, manuais Adobe/Blackmagic, documentação das plataformas), citadas linha a linha, mais medições locais com ffmpeg 8.1.2.
Legenda: **[oficial]** documento da plataforma · **[sem fonte]** repetido por terceiros, sem página oficial aberta.

## 1. Meta: Ads Guide (conferido em 05/11/2026) [oficial]

| Posicionamento | Proporção / resolução | Duração | Área segura |
|---|---|---|---|
| Instagram Reels | 9:16 · 1440×2560 recomendado (1080×1920 = mesma proporção) | 0 s – 15 min | livre: **14% topo, 35% base, 6% cada lado** |
| Instagram Stories | 9:16 | 1 s – 60 min; ≥16 s pode virar 1–3 cards | "aproximadamente" os mesmos 14/35/6 |
| Facebook Feed | 4:5 · 1440×1800 | 1 s – 241 min | — |

Em 1080×1920: **269 px no topo, 672 px na base, 65 px nas laterais** (cálculo sobre os percentuais da Meta).

- Arquivo: MP4 ou MOV, H.264, pixel quadrado, **taxa de quadros fixa**, progressivo; áudio AAC estéreo ≥128 kbps; até 4 GB; sem edit lists. — Ads Guide, Reels/Stories/Feed
- Legenda: "opcional, mas recomendada" em todos; o guia não dá corpo, posição nem tempo.
- Som: Reels = "fortemente recomendado"; Stories e Feeds = "opcional, mas recomendado". **O Ads Guide não manda desenhar para som desligado.**
- Música em anúncio de Reels: áudio original ou biblioteca livre (Meta Sound Collection); evitar música licenciada.
- Texto que acompanha o anúncio: Reels 44 caracteres; Stories e IG Feed 125; FB Feed 50–150 (quanto mais texto, mais a interface cobre a base).

⚠️ **Conflitos:**
- Área segura: circula "220 px topo / 420 px base" (11,5% / 21,9%) em guias de terceiros, sem página da Meta. Vale o 14/35/6 do Ads Guide.
- A skill `/motion` usa 250 px topo / 350 px base / 120 px direita / 60 px esquerda. É **menos** que o Ads Guide pede na base (672 px). Para anúncio em Reels, usar 14/35/6.
- "Gancho nos 3 primeiros segundos" e estatísticas como "85% dos vídeos vistos sem som" só aparecem em terceiros (Coinis, QuickFrame, vidpros etc.), nenhuma página da Meta aberta. **[sem fonte]**

## 2. Ritmo de vídeo curto

O ritmo e a sensação do corte são **decisão do usuário**: eu vejo quadros e números, não assisto em tempo real. O que posso medir e apresentar:
- duração de cada plano (`escopos.py`: cortes detectados);
- onde está a primeira frase/imagem forte (minutagem);
- tempo de leitura de cada texto (1 s para cada 3 palavras + 1 s de margem; o TikTok limita em 5–10 palavras por segundo).

## 3. TikTok: Ads Help Center e Creative Codes (conferido em 05/11/2026) [oficial]

Ao contrário da Meta, o TikTok publica números de tempo.

| Regra | Número | Fonte |
|---|---|---|
| Proposta do conteúdo aparece logo | 0–3 s | Creative best practices **[oficial]** |
| Gancho resolvido | até 6 s (90% do impacto de lembrança acontece nos 6 primeiros segundos, dado TikTok 2020) | Creative Codes PDF, 2023 **[oficial]** |
| Estrutura | gancho → corpo (produto e diferenciais na tela) → fechamento com CTA forte | Creative Codes **[oficial]** |
| Texto na tela | no máximo 5–10 palavras por segundo | Creative best practices **[oficial]** |
| Formato | 9:16, ≥ 720p (1080×1920 é o comum) | Creative best practices **[oficial]** |
| In-Feed (não Spark) | 9:16 ≥ 540×960 · arquivo ≤ 500 MB · até 10 min · bitrate ≥ 516 kbps | In-Feed Ads **[oficial]** |
| TopView | 9:16 ≥ 540×960 · 5–60 s (9–15 s recomendado) · bitrate ≥ 2.500 kbps · nada de branco liso nem flash nos 3 primeiros segundos | TopView specs **[oficial]** |
| Som | áudio é obrigatório em anúncio de vídeo; TopView não pode ser mudo | Ad policy checklist **[oficial]** |

- **Área segura:** o TikTok não publica um número fixo em pixels. Ela muda com a dimensão, o tamanho da legenda e os complementos; use os arquivos de sobreposição que a própria plataforma disponibiliza para baixar. Na falta deles, o 14/35/6 da Meta é uma régua conservadora.
- **Duração:** conflito dentro da própria plataforma. O PDF "7 Top Tips" (dados de 2021) recomenda 21–34 s para In-Feed; o checklist do mesmo PDF e a especificação de TopView de 2026 falam em 9–15 s. Na dúvida, entregar a versão curta e testar.
- **Revisão de anúncio reprova:** pedido de ação que a interface não tem (deslizar para cima, cursor de mouse), grafia "esperta" para driblar política e criativo incoerente com a página de destino.
- **Estética:** a plataforma recomenda produção nativa, com cara de celular, troca de cena rápida, movimento, texto aparecendo e música. Vídeo brilhante demais de estúdio tende a parecer anúncio.
