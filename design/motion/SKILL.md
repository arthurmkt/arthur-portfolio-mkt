---
name: motion
description: Faz motion graphics em código e entrega o MP4 pronto — reel 9:16, vídeo 16:9, anúncio curto, vinheta, animação de LP. Escreve a animação em HTML/Canvas com relógio único, renderiza quadro a quadro no computador (Playwright + ffmpeg) e revisa por folha de quadros antes de entregar. Use quando pedirem "motion", "motion graphics", "vídeo animado", "animar", "reel animado", "vinheta", "animação de logo", "animação pra LP", "número animado", "reel de resultado" ou /motion. Não serve para filmar, para foto realista nem para gerar vídeo por IA a partir de imagem.
user-invocable: true
---

# Motion em código

**O vídeo nasce de código.** Eu escrevo um programa que desenha cada quadro a partir de um relógio `t`, renderizo quadro a quadro e monto o MP4. Por isso cor em hex, fonte da marca e números saem exatos: estão escritos, não interpretados por um gerador. E por isso pedir "30% mais lento" ou "passa para 9:16" muda uma linha, sem refazer a peça.

**O que não faz:** filmar pessoa, lugar ou produto; imagem fotorrealista do zero; adivinhar a marca. Foto, vídeo e tela reais da marca entram como arquivo, e o código anima o que for fornecido.

**Vídeo real de base entra como sequência de quadros**, nunca como `<video>`: `ffmpeg -i base.mp4 -q:v 3 frames/f%04d.jpg` e, no `draw`, a imagem do quadro `floor(t × fps) + 1`, carregada sob demanda. Com `<video>` o servidor do render não atende Range (o seek não anda) e a conexão de mídia nunca fecha (o `networkidle` estoura).

**Requisitos:** Python 3.10+, `pip install playwright` + `playwright install chromium` (o script usa o canal `chrome`; troque para o Chromium padrão em `abrir()` se não tiver o Chrome instalado), ffmpeg e ffprobe no PATH.

Arquivos desta skill:
- `assets/template.html`: motor com relógio único, semente fixa, easings, stagger, player com barra de tempo e nome da cena, área segura.
- `scripts/render.py`: renderiza o MP4 quadro a quadro, a versão curta por trechos e a folha de revisão.
- `tecnicas.md`: as 39 técnicas em 7 grupos, com os parâmetros de cada uma e as combinações por objetivo.
- `exemplos/reel-resultado-8s.html`: peça pronta de 8 s (número embaralhado → barras → CTA com confete), com dados de exemplo.

Pasta de trabalho: uma pasta por peça (ex.: `motion/<marca>/<peça>/`). O HTML, os assets (logo, fotos, fonte), o MP4 e as folhas de revisão ficam juntos.

---

## Passo 0 — Kit da marca

Monte o kit **uma vez por marca**, a partir do manual, do site ou do que a pessoa mandar:

| Item | Como entra |
|---|---|
| Paleta | **hex com papel**: fundo, texto, destaque, número. 3 a 4 cores; 7 cores é sobra de cor e falta de contraste |
| Fontes | nome exato. Google Fonts → `<link>`; fonte própria → **arquivo** na pasta + `@font-face` |
| Logo | **arquivo** (SVG ou PNG transparente). Nunca desenhar o logo do zero nem descrever em palavras: sem arquivo, pedir |
| Tom de movimento | 2 a 3 adjetivos (calmo, energético, premium, popular) → define easing e corte |
| Números | os reais, com período e fonte. Sem número conferido → ou peço, ou ele aparece na tela rotulado **"dados de exemplo"** |
| Oferta, CTA, @/site | do briefing. Urgência só com prazo real |
| Trilha | arquivo licenciado da marca ou de banco + **BPM** e segundo do drop |

Salve o kit em `motion.md` na pasta da marca. Da segunda peça em diante, ele é lido, não remontado.

## Passo 1 — Triagem: os 6 componentes

Checklist reimpresso, **uma pergunta por turno**, item preenchido nunca reaberto, e o que o briefing já responde entra preenchido. Faltou um componente, eu decido sozinho, e quase sempre diferente do que a pessoa queria.

```
1. Formato — proporção + resolução + duração + fps
2. Cena — o que aparece, em que ordem, quantos segundos cada
3. Textos — as frases exatas, entre aspas (lista fechada, literal)
4. Técnica — pelo nome (tecnicas.md)
5. Ritmo e som — easing, stagger, BPM / trilha
6. Entrega — MP4 · versão curta de 6 s · player para revisão · HTML em loop (LP) · fundo transparente
```

**Formato pela plataforma:**

| Proporção | Resolução | Onde roda | Duração típica |
|---|---|---|---|
| 9:16 | 1080×1920 | Reels, Stories, TikTok, Shorts | 8–15 s, gancho no 1º quadro |
| 4:5 | 1080×1350 | feed IG/FB | 6–15 s |
| 1:1 | 1080×1080 | feed, alguns posicionamentos | 6–15 s |
| 16:9 | 1920×1080 | YouTube, apresentação, telão, site | 5 s (vinheta) a explicativos longos |
| LP | largura da página (ex.: 1440) | hero e seções | loop leve de 5–10 s, entregue como HTML |

30 fps cobre quase tudo. 60 fps só em zoom, partículas rápidas e movimento de câmera. Peça de anúncio: sempre uma **versão de 6 s** com a mesma assinatura, para teste.

## Passo 2 — Roteiro com minutagem (portão)

Antes de escrever código, mostre o roteiro e **espere aprovação**:

```
Formato: 9:16 · 1080×1920 · 15 s · 30 fps · trilha 120 BPM (cortes em 3 / 7 / 11 s)
Kit: fundo #050505 · destaque #E50914 · número #FFDD00 · Morganite / IBM Plex Sans · logo.svg

| Cena | Tempo | Técnica | O que acontece | Texto (literal) | Entra / sai |
```

Regras do roteiro:
- **Uma ideia por cena.** Se a cena precisa de duas frases, são duas cenas.
- **2 a 4 s por cena.** Abaixo de 2 s, o texto não dá tempo de ler.
- **Tempo de leitura:** 1 s para cada 3 palavras + 1 s de margem. Número sozinho: 1,5 s · 3 palavras: 2 s · 6 palavras: 3 s · 9 palavras: 4 s. Frase que pede mais de 4 s é longa demais para uma cena: divide ou corta palavra (cortar palavra de copy aprovada é decisão de quem aprovou).
- **Diga como entra e como sai.** A saída liga uma cena à próxima.
- **Gancho nos 3 primeiros segundos** em 9:16 e 4:5. A mensagem principal nunca fica para o fim.
- **Corte na batida:** batida = 60 ÷ BPM segundos; compasso = 4 batidas. Cena com duração em múltiplos do compasso fecha redonda (120 BPM: batida 0,5 s, compasso 2 s · 128: 0,47 / 1,88 · 100: 0,6 / 2,4 · 90: 0,67 / 2,67).

## Passo 3 — Construção

Copie `assets/template.html` para a pasta de trabalho e preencha `CFG`, `BRAND` e `SCENES`. Leis do código, porque é delas que depende o MP4 sair igual ao que foi aprovado no player:

1. **Tudo é função de `t`.** Nada de `setTimeout`, `Date.now()`, CSS transition/animation ou estado acumulado entre quadros. A letra 3 no instante 1,4 s está sempre no mesmo lugar.
2. **Semente fixa** (`rng(CFG.SEED + i)`) em todo valor aleatório. Sem ela, o exportado sai diferente do aprovado.
3. **Simulação** (física, boids, tecido): fórmula analítica em `t`, ou pré-cálculo no carregamento a passo fixo (1/240 s), guardado por quadro e lido pelo índice. Nunca integrar dentro do `draw`.
4. **Fontes em `CFG.FONTS`** e assets em `CFG.ASSETS`: o motor espera carregar antes do primeiro quadro. Fonte que não carregou cai em genérica sem avisar, e é o erro mais comum.
5. **Área segura no 9:16:** texto, número e logo dentro de 250 px do topo, 350 px da base, 120 px da direita e 60 px da esquerda (valores aproximados; mudam com os apps).
6. **Easing com intenção:** `inOut` é o padrão; `back` (overshoot) nas entradas de texto, pinos e números; `linear` só em rotação contínua e rolagem; `bounce` só em objeto que cai. Stagger de **0,07 s entre letras** e **0,15 s entre cards**.
7. **Hierarquia:** o número principal é o maior elemento da cena.
8. Comentário no topo de cada cena com o tempo e a técnica.

Peça longa ou com técnica pesada (shader, simulação): **uma cena por vez**. Construa, revise e aprove a cena antes de juntar. Peça curta (até ~15 s, 4 cenas leves) pode nascer inteira, mas a revisão continua cena a cena.

## Passo 4 — Revisão antes de mostrar

```bash
python ~/.claude/skills/motion/scripts/render.py peca.html --sheet auto --safe
```

Gera a folha com o meio e o fim de cada cena, com a área segura pintada. **Leia a folha** pelo método VER → AMPLIAR → CONFIRMAR (recorte ampliado em texto pequeno, número e logo) e passe as 6 camadas:

| Camada | Confere |
|---|---|
| 1. Técnica | duração, resolução e fps iguais ao pedido; sem quadro preto no começo ou no fim |
| 2. Marca | hex certos; fonte da marca carregada, não genérica; logo sem distorção, giro ou cor trocada; tom do movimento combina |
| 3. Leitura | uma ideia por cena; cada texto fica o tempo da regra; contraste do texto contra o fundo; número principal é o maior |
| 4. Plataforma | proporção certa; nada fora da área segura; gancho nos 3 primeiros segundos; funciona sem som |
| 5. Dados | números iguais aos fornecidos, sem arredondar; período e fonte; exemplo rotulado na tela; nenhum número inventado |
| 6. Direitos | trilha licenciada, da marca ou gerada; fotos e telas autorizadas; marca de terceiro só com permissão; promessa da oferta validada |

Para conferir um instante específico: `--sheet 1.5,2.9,3.1`. Problema achado eu corrijo antes de mostrar, sem perguntar.

**A 3ª passada do material, assistir no celular e sem som, é de quem aprova.** Eu confiro quadros, não a sensação do vídeo rodando. Na entrega, peça explicitamente essa passada.

## Passo 5 — Render e entrega

```bash
python ~/.claude/skills/motion/scripts/render.py peca.html                                   # MP4 inteiro
python ~/.claude/skills/motion/scripts/render.py peca.html --segments 0-3,11-15 -o peca_6s.mp4   # versão curta
python ~/.claude/skills/motion/scripts/render.py peca.html --audio trilha.mp3                # com trilha
```

Depois do render: `ffprobe` para confirmar resolução, fps, nº de quadros e duração. Entregue:
- o **MP4** (H.264, yuv420p, +faststart), pronto para subir;
- a **versão de 6 s**, se for anúncio;
- o **HTML com player** (abre no navegador: play, pausa, barra de tempo, nome da cena, área segura). É nele que quem aprova aponta o segundo exato do ajuste.

LP: a entrega é o próprio HTML em loop, sem MP4. Leveza primeiro: não pode pesar a página.

**Trilha:** a skill mixa um arquivo (`--audio`) e alinha os cortes ao BPM informado. Trilha **gerada** em código não está implementada; se pedirem, diga isso em vez de improvisar. Música de terceiros sem licença derruba o anúncio: nunca usar.

## Passo 6 — Ajuste

A primeira versão é rascunho. Ajuste bom aponta a **cena ou o segundo**, diz **o quanto** e diz **o que manter**: "Na cena 1 (0–3 s), segure o +248% travado 1,5 s antes de trocar. Não mexa no resto." Eu mudo só o trecho afetado e re-renderizo.

| Sintoma | Causa provável | Correção |
|---|---|---|
| Movimento robótico | easing linear | `inOut`, e `back` nas entradas |
| Tudo entra junto | sem stagger | 0,07 s entre letras, 0,15 s entre cards |
| Fonte diferente da marca | fonte não carregou | conferir `CFG.FONTS` / `@font-face` e o arquivo na pasta |
| Texto cortado no 9:16 | layout pensado em 16:9 | refazer na grade 1080×1920 respeitando a área segura |
| Player travando | partículas ou shader demais | menos elementos no player, contagem cheia só no render |
| Exportado diferente do player | aleatório sem semente ou estado acumulado | leis 1 a 3 do Passo 3 |
| Corte fora da batida | cenas sem relação com o BPM | durações em múltiplos da batida |
| Número errado | dado não veio | usar exatamente a lista fornecida, sem arredondar |

**Depois de publicado:** se a queda de retenção é nos 3 primeiros segundos, troque só a cena 1; se é numa cena do meio, encurte ou troque só aquela; se o clique não vem, teste encerramentos diferentes (confete, selo girando, QR) mantendo o resto igual. Uma variável por vez.

## Biblioteca da conta

Peça aprovada → no `motion.md` da marca, registre: o roteiro aprovado, as técnicas usadas, o caminho do HTML e, quando houver, a métrica dos primeiros 7 dias. A próxima peça começa do que já performou, e o encerramento padrão da marca (assinatura final com logo + CTA) é reaproveitado, não refeito.
