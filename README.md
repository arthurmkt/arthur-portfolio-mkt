# Skills de marketing para o Claude Code

Arthur Candido. Gestor de tráfego, trabalho com Meta Ads, Google Ads, rastreamento, automação e CRM.
Estas são as skills que eu uso no dia a dia para otimizar conta, subir campanha, pesquisar mercado, cuidar da parte visual e atender lead com IA, em versão limpa para outros profissionais usarem.

## O que tem aqui

### Otimização de campanhas (`otimizacao-campanhas/`)

| Skill | O que faz |
|---|---|
| `/rotina-meta` | Rodada de otimização de uma conta de Meta Ads: lê contexto e histórico antes do número, varre a conta bloco a bloco e entrega decisões com o dado por trás, sem aplicar nada. |
| `/auditoria-campanha-meta` | Auditoria de conta Meta já no ar: verba queimada, conversão inflada, fadiga de criativo. Tem modo entrada para assumir conta nova. |
| `/subir-campanha-meta` | Sobe campanha nova no Meta: confere rastreamento e pagamento, faz briefing curto e publica pausada para revisão. |
| `/pesquisa-meta-ads` | Pesquisa para Meta Ads: persona, públicos por etapa do funil, interesses, criativos da concorrência e ângulos. |
| `/copy-anuncio` | Texto do anúncio (principal, título, descrição no Meta; títulos e descrições de RSA no Google). |
| `/rotina-google-ads` | Auditoria completa de uma conta Google Ads, superfície por superfície, com decisões e sem aplicar nada. |
| `/analise-termos-google-ads` | Lê o CSV de termos de pesquisa, classifica por intenção e devolve o que manter e o que negativar. |
| `/pesquisa-google-ads` | Pesquisa para Google Ads: persona com faixa de renda, keywords por intenção, negativas, concorrentes e anúncios. |
| `/plano-google-ads` | Transforma decisões aprovadas em runbook por blocos e confere cada bloco na conta antes de seguir. |
| `/trilha-lead-google-ads` | Segue o lead do clique até o CRM quando a conversão do painel não bate com a realidade. |
| `/executora-ai-chrome` | Escreve o runbook que um agente de navegador executa sozinho no Google Ads, Meta Ads, GTM ou GA4, e o relatório que ele devolve. |

### Design (`design/`)

| Skill | O que faz |
|---|---|
| `direcao-visual` | Define conceito, cor, tipografia, ritmo e movimento antes de construir site, LP ou peça. Mostra três direções e revisa página pronta contra uma lista anti-IA. |
| `bloco-visual` | Monta no Figma a página de régua da marca (cores, textos, logo, safe area, regras) a partir de um arquivo de identidade. |
| `motion` | Motion graphics em HTML/Canvas renderizado quadro a quadro para MP4 (Playwright + ffmpeg). |
| `editar-video` | Edição e correção de cor com ffmpeg, julgando por medição (escopos e números por cena), com LUT, cortes, legenda e entrega para Reels/TikTok. |

### SDR de IA (`sdr-ia/`)

Prompt base de um agente de WhatsApp que qualifica, trata objeção, agenda e confirma presença, com um modelo de base de conhecimento. Veja `sdr-ia/README.md`.

## Como instalar

Skills de otimização (são comandos de um arquivo só):

```bash
cp otimizacao-campanhas/*.md ~/.claude/commands/
```

Skills de design (são pastas com scripts e referências):

```bash
cp -R design/* ~/.claude/skills/
```

Depois, abra o Claude Code e chame pelo nome (`/rotina-meta`, `/motion` etc.). As skills de design também são chamadas sozinhas quando o pedido combina com a descrição delas.

O que cada uma precisa para rodar está no próprio arquivo. Em geral:
- Otimização: acesso à conta. Se você tiver o MCP oficial do Meta Ads ou do Google Ads configurado, a skill lê direto; senão, exporte o relatório do gerenciador e passe o arquivo.
- `motion` e `editar-video`: Python 3, ffmpeg e, no caso da `motion`, Playwright com Chromium.
- `bloco-visual`: Figma com o MCP oficial conectado.

## Antes de usar

São pontos de partida. Os critérios de corte, os limites de verba e as janelas de análise refletem como eu trabalho em contas de lead e de e-commerce no Brasil. Leia, ajuste os números à sua conta e ao seu cliente, e nunca aplique uma decisão que você não entendeu. As skills de otimização foram feitas para recomendar; quem aplica é você.

## Licença

MIT. Veja `LICENSE`.
