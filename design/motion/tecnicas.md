# Biblioteca de técnicas — motion em código

Organizado a partir de um material de estudo sobre motion graphics com o Claude (39 técnicas, 7 grupos). Cada linha tem o **nome da técnica** (é ele que diz qual algoritmo usar), os parâmetros que precisam ser decididos e o uso em cliente.

**Camada e peso:** HTML/CSS e Canvas 2D = leve · Canvas com simulação ou pixel a pixel = médio · WebGL (shader) = pesado. No template tudo é desenhado em Canvas 2D. Shader entra como um segundo canvas WebGL desenhado por cima, e só quando a peça pede.

---

## 1. Ritmo e forma

| # | Técnica | Parâmetros a decidir | Uso em projeto |
|---|---|---|---|
| 1 | **Curvas de easing** | linear · inOut · back (overshoot) · bounce; duração do trajeto (ex.: 1,8 s) | comparar "processo lento × rápido"; treinar o time |
| 2 | **Morphing de formas** | nº de pontos interpolados (ex.: 180), sequência de formas, overshoot na troca, contornos em eco | passar pelos ícones dos serviços e terminar no contorno do logo; loader |
| 3 | **Cascata em grade** | grade (ex.: 20×9), atraso proporcional à distância do centro, flip, 2ª onda | revelar foto do cliente; transição entre cenas |
| 4 | **Transições e glitch** | máscara circular · cortina em N faixas · separação RGB com fatias e ruído; 1 s cada | ligar cenas; wipe na cor da marca; glitch suave para tecnologia |
| 5 | **Zoom infinito** | formas aninhadas, escala por nível (1,3×), giro por nível (9°), níveis/s (1,7) | abertura de evento; túnel com o logo; loop de telão |

## 2. Texto e mensagem

| # | Técnica | Parâmetros a decidir | Uso em projeto |
|---|---|---|---|
| 6 | **Tipografia cinética** | letra por letra, queda com giro, overshoot, **0,07 s entre letras**, 1 letra em destaque, saída | abrir com a oferta ou o nome da marca |
| 7 | **Hero com tipografia cinética** (LP) | linhas subindo por máscara uma a uma, sublinhado desenhado, botão pulsando na batida, loop de 8 s | hero de landing page |
| 8 | **Gancho com legenda dinâmica** (9:16) | palavras uma a uma estilo karaokê, a atual em destaque, dentro da área segura, seta pulando no fim | gancho de Reels nos 3 primeiros segundos |
| 9 | **Texto embaralhado** | placas estilo painel de aeroporto, embaralha 22×/s, trava em sequência (0,16 s entre letras), muda de cor ao travar | **revelar preço, desconto ou número de resultado**; contagem de lançamento |
| 10 | **Desenho de traço** | curva (Lissajous, logo, rota), duração do traço, gradiente ao longo do caminho, ponta luminosa | assinatura ou logo se desenhando; rota no mapa; sublinhado de headline |
| 11 | **Títulos e lower thirds** (16:9) | título de capítulo, logo fixo no canto, lower third (barra + nome/cargo), cartão de citação, fundo transparente | entrevista, podcast, webinar |

## 3. Dados e prova

| # | Técnica | Parâmetros a decidir | Uso em projeto |
|---|---|---|---|
| 12 | **Dados animados** | barras com overshoot + valor contando, contador (0 → valor), linha que se desenha com área | prova com números reais do case |
| 13 | **Corrida de barras** (16:9) | N categorias × período, barras trocando de posição, mês grande no canto, dados da planilha | comparar canais ou períodos |
| 14 | **Antes e depois** (9:16) | cortina com alça arrastando, número contando do antes ao depois, selos de benefício | mostrar o resultado do cliente |
| 15 | **Top 3 com contagem** (9:16) | barras de progresso no topo, número gigante que vira (3, 2, 1), card por item, 2,4 s por item | lista em Story; cada item exportável como imagem de carrossel |
| 16 | **Prova social em movimento** (LP) | disparo ao entrar na tela, contadores, faixa de logos rolando, depoimentos trocando a cada 2,6 s | seção de prova social da LP |
| 17 | **Medidores e líquido** | anéis de progresso com contagem no centro, tanque enchendo com onda dupla e bolhas | meta do mês; reunião de resultado |
| 18 | **Mapas e conexões** | mapa de pontos, hub pulsando, pinos caindo com overshoot, rotas em arco com ponto viajando, "+N" na chegada | cidades atendidas; origem dos leads |

## 4. Interface e conversão

| # | Técnica | Parâmetros a decidir | Uso em projeto |
|---|---|---|---|
| 19 | **Interface animada** | celular com tela, notificação descendo, toque com ripple, badge pulando, swipe de card | telas reais do app/site; agendamento; checkout |
| 20 | **Produto flutuante com parallax** (LP) | painel inclinado flutuando, cards em profundidades diferentes, rolagem simulada | produto digital no hero |
| 21 | **Explicativo em etapas** (16:9) | N etapas numa linha, ponto percorrendo, círculo enchendo com ícone, 1,5 s por etapa, faixa final | explicar processo/produto |
| 22 | **Gradiente vivo e formulário** (LP) | 4 manchas de cor se misturando em loop, card de vidro fosco, e-mail digitado, clique, spinner, check desenhado | seção de captura |
| 23 | **Oferta com urgência** (9:16) | selo de prazo, preço riscado, novo preço entrando, contador de vagas caindo, cronômetro, botão com brilho | anúncio de oferta **com prazo real** |
| 24 | **CTA com confete** | botão, texto girando em círculo, cursor clica, ripple, N peças de confete com gravidade e giro | fechar com link da bio ou WhatsApp |

## 5. Partículas e simulação — descreva regras, não caminhos

Você não diz onde cada objeto para: descreve quantidade, forças, limites e passo da simulação. **Semente fixa obrigatória.** E a posição tem que ser recalculável em qualquer t: ou fórmula analítica, ou simulação pré-calculada no início (a 1/240 s) e lida pelo índice do quadro. **Nunca acumular estado entre quadros do player**, porque aí o player e o render divergem.

| # | Técnica | Parâmetros a decidir | Uso em projeto |
|---|---|---|---|
| 25 | **Sistema de partículas** | N (ex.: 1.400), explosão do centro, **amostrar os pixels** de texto/logo para formar a forma, atraso aleatório, dispersão com vento | formar o logo ou um número de resultado |
| 26 | **Física e colisão** | N corpos, gravidade, perda de energia no quique, colisão, empilhamento, passo de 1/240 s | produtos caindo na sacola; moedas no cofre |
| 27 | **Líquido (metaballs)** | nº de gotas, trajetórias, limiar suave pixel a pixel, degradê | bebida, cosmético; transição líquida |
| 28 | **Fluxo de ruído** | N partículas num campo de fluxo sem divergência, rastro de K passos, cor por faixa | fumaça/vapor (café, gastronomia); fundo de live |
| 29 | **Bando (boids)** | N agentes, separação/alinhamento/coesão, predador ou ímã | "leads atraídos pela marca"; funil |
| 30 | **Tecido simulado** | malha (ex.: 44×26), física de Verlet, preso no topo, vento com rajadas, luz pela normal | bandeira com logo; cortina revelando produto; moda, cama e banho |
| 31 | **Reação-difusão** | Gray-Scott (F, k), grade, semente com forma de texto/logo | cosmético, saúde, biotech, agro |

## 6. 3D e shaders

| # | Técnica | Parâmetros a decidir | Uso em projeto |
|---|---|---|---|
| 32 | **3D e parallax** | esfera de Fibonacci (N pontos) girando, wireframe, camadas de parallax | globo de pontos (atuação nacional); produto em wireframe |
| 33 | **Raymarching 3D** (WebGL) | formas por fórmula, smooth union, sombra suave, fresnel, câmera orbitando | produto premium; hero 3D |
| 34 | **Mergulho fractal** (WebGL) | Mandelbrot/Julia, zoom exponencial, coloração suave na paleta | telão de evento; abertura hipnótica |
| 35 | **Terreno procedural** (WebGL) | ruído fractal em camadas, voo de câmera, neblina, curvas de nível | agro, turismo, energia |

## 7. Marca, som e encerramento

| # | Técnica | Parâmetros a decidir | Uso em projeto |
|---|---|---|---|
| 36 | **Vinheta de marca** (16:9) | linhas convergindo, símbolo em traço e depois preenchido, nome subindo por máscara, brilho atravessando, 5 s | abrir ou fechar vídeos da marca; versão de 3 s para Reels |
| 37 | **Abertura audiorreativa** | BPM, reação ao bumbo (graves) e ao chimbal (agudos), espectro circular, flash na batida | podcast, evento, logo pulsando |
| 38 | **Final no tempo da música** | 1 palavra/diferencial por batida, zoom de impacto, onda de choque no golpe final | diferenciais do cliente; teaser de 6 s |
| 39 | **Assinatura final** | anel expandindo, palavras subindo por máscara, sublinhado da esquerda para a direita, tagline, fade no último 0,5 s | encerramento padrão da conta (logo + CTA + @/site) |

---

## Combinações por objetivo

| Objetivo | Formato | Sequência |
|---|---|---|
| Reel de resultado | 9:16 · 15 s | texto embaralhado (número) → dados animados → medidores → CTA com confete |
| Abertura premium | 16:9 · 10 s | raymarching na cor do produto → partículas formando o logo → assinatura final |
| Varejo e entrega | 9:16 · 20 s | interface do app → mapa das regiões → produtos caindo na sacola → corte na batida |
| Lançamento | 9:16 · 20 s | zoom infinito → tecido revelando o produto → tipografia cinética com a oferta → assinatura |
| Oferta por tempo limitado | 9:16 · 10 s | texto embaralhado com o desconto → medidor de estoque → selo girando → CTA com confete |
| Expansão de marca | 16:9 · 15 s | globo de pontos → mapa com cidades → dados animados → assinatura |
| Anúncio de teste | 9:16 · 6 s | tipografia cinética com a oferta → assinatura de 1 s |
