# Futurista — o que existe de mais avançado e quando usar

**Regra:** futurista é tempero, não prato. Um efeito-assinatura por página. O conteúdo tem que funcionar sem ele (sem JS, sem WebGL, com menos movimento). Se o efeito pesa no celular do anúncio, ele perde para a conversão.

Pesquisado em nov/2026. Antes de usar algo novo, conferir o suporte no MDN ou no caniuse. Blog costuma errar versão de navegador.

---

## 1. O que já está pronto em `codigo/`
- **Fundo em fluxo com WebGL**: shader de ruído da mesma família do degradê animado da Stripe, fixo atrás da página. Desliga sozinho sem WebGL ou com menos movimento.
- **Revelação por palavra**: cada palavra do título sobe de dentro de uma máscara (o efeito do SplitText, feito à mão).
- **Cascata ao entrar na tela**, números contando, parallax leve, letreiro contínuo, linha do tempo que se desenha, brilho atravessando os cards escuros.

Isso já é nível de site premiado. O próximo passo não é mais efeito, é **escolher um** e executar melhor.

## 2. CSS nativo (sem biblioteca, leve)
| Recurso | O que faz | Suporte (nov/26) | Como usar |
|---|---|---|---|
| **Animação ligada à rolagem** (`animation-timeline: view()` / `scroll()`) | Elemento anima conforme rola, sem JS | Chrome/Edge sim; Safari e Firefox chegando, com fontes conflitantes | Sempre dentro de `@supports (animation-timeline: view())`, com a versão IntersectionObserver de reserva |
| **View Transitions entre páginas** (`@view-transition { navigation: auto }`) | Transição suave de uma página para outra, como em app | Chromium e Safari 18.2+; Firefox em andamento (foco do Interop 2026) | Site com várias páginas. Sem suporte, a navegação fica normal |
| **`@property`** | Anima degradê e cor de verdade | Amplo | Borda girando, degradê que respira no botão |
| **`color-mix()` / `oklch()`** | Gera as variações da cor de destaque a partir de um token só | Amplo | `--acento-escuro: color-mix(in oklch, var(--acento), black 20%)` |
| **Container queries** | O componente se adapta ao espaço dele, não à tela | Amplo | Cards que vivem em lugares diferentes |
| **Fonte variável** | Anima o peso ou a largura da letra | Amplo | Título que ganha peso ao rolar (combina com o contraste 300→800) |

## 3. Bibliotecas (quando o CSS não chega)
- **GSAP + ScrollTrigger + SplitText**: o padrão dos sites premiados. **Ficou 100% gratuito, plugins inclusive, até para uso comercial** (Webflow comprou a GreenSock). Usar quando houver sequência de rolagem com várias etapas ("pin" de seção, linha do tempo amarrada ao scroll). Há skills oficiais: `github.com/greensock/gsap-skills`.
- **Lenis**: rolagem suave. Cuidado: mexe na rolagem nativa e pode irritar no celular. Só em site-vitrine, nunca em LP de anúncio.
- **Three.js / React Three Fiber**: 3D de verdade (objeto girando, cena). Pesado, só quando o produto é físico e o 3D mostra algo que a foto não mostra.
- **OGL**: WebGL mínimo, bem mais leve que o Three. Bom para shader de fundo e distorção de imagem.
- **VFX-JS** (Codrops, 2025): aplica efeito WebGL a qualquer elemento do HTML, texto inclusive, sem montar cena.

## 4. Ferramentas sem código (para montar ou ajustar sem programar)
- **Unicorn Studio**: monta shader e efeito WebGL num editor visual e exporta um embed. Bom para o fundo-assinatura.
- **Spline**: cena 3D no navegador, com embed. Pesado: usar só no herói, com imagem de reserva.
- **Rive**: animação vetorial interativa (ícone que reage, mascote, botão vivo). Leve. Ótimo em app.

## 4b. Site cinematográfico (o objeto se mexe com a rolagem): receita completa
Referência que originou a receita: um anúncio de curso sobre "sites cinematográficos com IA". Mostrava espaguete em espiral, espetinho e pão folha flutuando e se montando conforme a rolagem, sobre um fundo liso da mesma cor da página. É a técnica das páginas de produto da Apple, com o vídeo feito por IA.

**Produção (fora do código):**
1. **Imagem do objeto** gerada por IA (Nano Banana / GPT Image / Midjourney) ou foto real recortada. Ela fica **centralizada, sobre fundo liso na cor exata da página**, com luz de estúdio e sombra suave.
2. **Vídeo de 4 a 8 segundos** a partir dessa imagem (Veo, Kling, Runway, Higgsfield). A câmera fica parada e só o objeto se move: gira, se monta, explode em camadas, ingredientes se juntam. O fundo continua liso, sem cortes. Pedir no prompt: "static camera, seamless solid background #xxxxxx, no cuts".
3. **Vídeo → imagens:** 120 a 180 quadros em WebP. Desktop com 1600px de largura e celular com 900px, cada quadro com 30 a 60 KB. Dá para fazer com ffmpeg (`ffmpeg -i video.mp4 -vf scale=1600:-1 quadros/%04d.webp`) ou com Python e a biblioteca `av`.

**Código:** `codigo/rolagem-cinematografica.html`. É um canvas preso na tela que desenha o quadro equivalente ao quanto a pessoa rolou, com os textos entrando em faixas da rolagem. Ele:
- carrega 1 a cada 6 quadros primeiro, para funcionar no 4G;
- tem uma versão de celular;
- mostra uma imagem fixa para quem pediu menos movimento ou está sem JS.

**Onde funciona:** produto físico bonito, que ganha com movimento: comida, joia, máquina, equipamento, cosmético, imóvel (planta se montando). **Onde não funciona:** serviço sem objeto (consultoria, advocacia). Nesses casos a assinatura é tipografia ou fundo.

**Cuidados (as dúvidas dos próprios comentários do post: "não pesa?", "e no celular?", "PageSpeed?"):**
- 150 quadros ≈ 5 a 8 MB. Em **LP de anúncio** usar no máximo 1 cena no topo, ou trocar por vídeo curto em loop. O lugar natural é o **site-vitrine**.
- O primeiro quadro é uma `<img>` normal: o herói aparece na hora e o resto carrega depois.
- O fundo do vídeo e o `--fundo` da página têm que ser a mesma cor, senão aparece a "caixa" do vídeo.
- `<video>` com `currentTime` controlado pela rolagem é mais leve, mas engasga no Safari. Sequência de imagens é o caminho seguro.

## 5. Efeitos que ainda parecem novos (com moderação)
- **Tipografia cinética**: título que se monta, troca de palavra no lugar, peso variando ao rolar.
- **Distorção de imagem no hover** com shader (OGL ou VFX-JS).
- **Seção presa** (pin) em que o conteúdo troca enquanto a pessoa rola (GSAP).
- **Vídeo controlado pela rolagem**: produto girando conforme rola. Usar sequência de imagens ou vídeo bem comprimido.
- **Grão/ruído sutil por cima do fundo** (SVG `feTurbulence` ou PNG pequeno): tira a cara de "digital liso".
- **Cursor que reage** perto de botões (efeito magnético). Só no desktop.

**Já virou clichê, evitar:** vidro fosco em tudo, grade bento, orbe de degradê roxo borrado, partículas, "aurora" de fundo, cards inclinando em 3D no hover. Os componentes prontos de Aceternity UI e Magic UI ficaram tão usados em sites feitos por IA que denunciam.

## 6. Onde procurar referência e código
| Fonte | Para quê |
|---|---|
| **Codrops** (`tympanus.net/codrops`) | O melhor lugar: tutoriais de efeito avançado **com o código no GitHub**. Pegar um exemplo e adaptar é o caminho mais rápido para um efeito bom |
| **Awwwards**, **Godly** (`godly.website`), **SiteInspire**, **Land-book** | Galerias de site premiado: ver composição, ritmo e tipografia |
| **Shadertoy** | Shaders prontos para adaptar em fundo |
| **GSAP Showcase** e CodePen do GSAP | Exemplos de rolagem com código |
| **Fontshare**, **Google Fonts**, **Pangram Pangram**, **Velvetyne** | Fontes fora do óbvio (Fontshare e Velvetyne gratuitas) |
| `github.com/anthropics/skills`: skill `frontend-design` | Skill oficial da Anthropic contra a estética genérica de IA. Complementa esta |

## 7. Orçamento de peso (LP de anúncio)
- Página toda abaixo de ~1,5 MB no primeiro carregamento; herói visível em menos de 2,5s no 4G.
- WebGL só depois do primeiro desenho da página e com fallback em CSS.
- Script de terceiro (GTM, pixel) depois da interação .
- Em site-vitrine (institucional, a própria marca) pode gastar mais; em LP de anúncio, conversão manda.
