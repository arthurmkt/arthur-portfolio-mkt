---
name: direcao-visual
description: Diretora de arte. Invocar ANTES de construir qualquer site, landing page, slide, apresentação ou peça visual, e sempre que pedirem algo "bonito", "premium", "que não pareça IA", "futurista". Define conceito, cores, tipografia, ritmo e movimento, mostra 3 direções lado a lado para escolha e entrega a folha de direção que a construção segue. Também revisa uma página pronta contra as regras fixas e a lista anti-IA.
---

# /direcao-visual: diretora de arte

## Por que existe
O que a IA entrega sem direção é a média de tudo que ela já viu: Inter, degradê roxo, três cards com ícone, tudo centralizado. Os sites que dão certo dão certo porque cada decisão foi **escolhida contra alternativas**: títulos, cards e tipografia testados em versões lado a lado antes de fechar.

Esta skill transforma isso em processo. **A cor muda a cada projeto. As regras não mudam.**

## Arquivos desta skill (ler conforme a etapa)
| Arquivo | Quando ler |
|---|---|
| `referencias/regras-fixas.md` | Sempre. São as regras que não mudam de projeto para projeto |
| `referencias/anti-ia.md` | Antes de entregar qualquer coisa (visual e texto) |
| `referencias/futurista.md` | Quando o pedido pedir impacto, tecnologia ou "algo diferente", ou quando a direção escolhida tiver movimento forte |
| `codigo/movimento-base.css` + `.js` | Base de movimento pronta (revelação por palavra, cascata, letreiro, brilho, fundo WebGL). Reaproveitar, trocando as cores |
| `codigo/base-estrutura.css` | **Estrutura completa do Nível 1:** tokens, botões, nav, herói com prova, números, cards, comparação "o comum × nós", pilares, linha do tempo, fundador, formulário, FAQ, rodapé em bloco de cor. Trocar só o `:root`. Os nomes de classe estão listados no comentário do topo; o HTML você monta com eles. A fonte aponta para `/fonte.woff2`: coloque a fonte do projeto na raiz ou troque o caminho |
| `codigo/base-serifada.css` | Referência de serifada + sans, paleta quente nomeada, coluna mobile |
| `codigo/rolagem-ancora.js` | Rolagem até a âncora com tempo fixo, parando abaixo da barra |
| `codigo/rolagem-cinematografica.html` | Modelo do Nível 3: sequência de quadros controlada pela rolagem |
| `referencias/celular-e-tecnica.md` | **Antes de construir Nível 2/3 e antes de revisar no celular.** Composição no celular, legibilidade, botões, carregamento, som, gestos, diagnóstico, publicação |
| `codigo/teste-celular.mjs` | Prints da página em qualquer tamanho (celular/computador), avisa rolagem lateral e erro, simula 4G com `--lento`, não deixa lixo no disco. Precisa de Node 18+ e Chrome (em Linux/Windows, defina `CHROME_PATH`) |

---

## Hierarquia: a promessa vem antes do visual
O visual de alto nível é **multiplicador**: ele faz uma promessa forte parecer inevitável, mas não salva uma promessa fraca. Um site cinematográfico com promessa genérica é só um vídeo bonito.

**Ordem que não se inverte:**
1. **Promessa:** o que a pessoa ganha, em quanto tempo, com número.
2. **Copy e exceções:** para quem é, para quem não é ("Não é para você se…"), objeções respondidas, regras com motivo.
3. **Estrutura:** a ordem dos blocos.
4. **Visual e movimento:** esta skill.

**Na prática:** se a promessa e a copy não existirem ou estiverem vagas, a skill **para e pede** antes de abrir as 3 direções. No Nível 3, cada cena do roteiro da jornada carrega **um pedaço da promessa**: a cena existe para provar algo, não para enfeitar.

---

## Níveis de entrega
**O Nível 1 é o piso.** Nenhum projeto recebe menos que isso. O que se replica de um projeto para outro é a **engenharia**, não a cara:
- a experiência no celular e no computador;
- a tipografia bem resolvida;
- poucas seções e bem feitas;
- os pontos de clique de saída (botões e WhatsApp no lugar certo);
- a qualidade no ar em qualquer celular.

Cor, imagem e identidade mudam a cada projeto. O que o cliente paga decide quanto a mais entra, e o investimento extra vai para a **jornada**: a página contada como história, cena por cena.

| | **Nível 1 · Base** | **Nível 2 · Assinatura** | **Nível 3 · Cinematográfico** |
|---|---|---|---|
| **Para quem** | Todo projeto, inclusive LP de anúncio | Quem quer se diferenciar da concorrência local | Produto físico bonito e cliente que paga pelo diferencial |
| **Direção** | Tokens do projeto sobre `codigo/base-estrutura.css` + `movimento-base`; 1 proposta | 3 direções lado a lado + folha de direção | 3 direções + **roteiro da jornada** (ver abaixo) |
| **Tipografia** | Contraste de peso numa família (300/800) | Par escolhido para o conceito (display + texto) | Par escolhido + tipografia cinética nos títulos |
| **Movimento** | Todo o `codigo/movimento-base`: revelação por palavra, cascata, letreiro, brilho, fundo WebGL | Base + 1 efeito-assinatura sob medida (distorção de imagem, vídeo em loop, transição entre páginas) | **Sequência de imagens controlada pela rolagem** (`codigo/rolagem-cinematografica.html`), 1 a 3 cenas, com seções presas (GSAP) |
| **Imagem** | Fotos do cliente com tratamento único | Ensaio ou imagens geradas com direção | Objeto gerado ou fotografado em estúdio + vídeo por IA → quadros |
| **Páginas** | 1 (LP) | Até ~5, com transição entre páginas | Vitrine principal + páginas de apoio no Nível 2 |
| **Sempre** | Formulário, rastreamento (GTM, webhook de lead), LGPD, menos movimento, 360px | igual | igual + versão de celular própria e orçamento de peso |

Cada nível **contém o anterior**. A skill não sugere preço.

### Roteiro da jornada (Nível 3, e Nível 2 quando couber)
Antes de gerar qualquer imagem ou vídeo, escrever a página como um storyboard: **cada cena = o que aparece + o que a pessoa lê + o que ela sente**. Modelo de 4 cenas:
1. **Chegada:** o produto aparece inteiro; título de 2 a 5 palavras.
2. **Detalhe:** o objeto abre, gira ou se monta e mostra o que ninguém vê (ingrediente, mecanismo, acabamento).
3. **Prova:** número, cliente real, processo.
4. **Chamada:** o objeto volta inteiro e o botão aparece.

O vídeo é gerado **a partir do roteiro**, não o contrário. Uma cena que não serve à história é cortada, por mais bonita que seja.

**Tempo de tela é meio, não fim.** A jornada segura a pessoa até ela entender e acreditar na promessa. A meta é conversão (venda mais barata), não minutos na página. Toda cena termina com um caminho visível até o botão. Em LP de anúncio, o botão aparece já na cena 1 e não some.

### Metas de qualidade (Nível 3, e Nível 1/2 também)
| Métrica | Meta | Como medir |
|---|---|---|
| PageSpeed **celular** | ≥ 90 | pagespeed.web.dev, rodar 3x |
| LCP (herói aparece) | < 2,5 s no 4G | o mesmo relatório |
| CLS (nada pula) | < 0,1 | o mesmo |
| INP (resposta ao toque) | < 200 ms | o mesmo |
| Rolagem sem engasgo | 60 fps | iPhone real (Safari) + Android barato real, não só o simulador |

### Medição da jornada (é ela que diz o que melhorar)
- **Evento por cena** no GA4/GTM (`cena_1_vista` … `cena_4_vista`) + clique no botão por cena: mostra **em que cena a pessoa desiste**.
- **Microsoft Clarity** (gratuito): gravação de sessão e mapa de rolagem. Ver 20 gravações de celular depois de cada mudança.
- Mudar uma coisa por vez e comparar a **taxa de conversão e o CPL** com o mesmo período anterior, nunca só o tempo na página.

---

## Processo

### 1. Entender antes de desenhar (perguntar só o que faltar, numa mensagem)
- **Nível de entrega:** 1, 2 ou 3. Se ninguém disser, é o 1.
- **O que é:** site, LP, slide, peça. Onde vai ser visto (celular do anúncio, tela de reunião, impresso).
- **Para quem e o que a pessoa tem que fazer** depois de ver.
- **A marca:** logo, cores e fontes que já existem. Se houver briefing, dossiê do cliente ou copy aprovada, ler antes.
- **O que ela NÃO pode parecer.** Costuma ser a pergunta que mais decide.

### 2. Conceito (antes de qualquer cor)
Escrever em 3 linhas:
- **Uma frase** do que a peça é. Exemplo, app de namoro para um público religioso: "namoro sério entre quem crê, com a sobriedade de uma igreja e não de um app".
- **Três adjetivos** que puxam em direções diferentes (ex.: quente · sóbrio · íntimo).
- **Uma referência física, fora da internet**, para tirar a paleta e a textura: papel de bíblia antiga com ouro e vinho; escritório de consultoria à noite com uma luz laranja.

Referência que é "outro site" vira cópia. Referência física vira identidade.

### 3. Três direções lado a lado
Gerar **um único HTML de comparação** (`direcoes.html` na pasta do projeto) com as 3 direções em colunas ou blocos. Cada uma mostra o **mesmo conteúdo real**, sem lorem ipsum:
- topo (título + subtítulo + botão),
- uma seção de prova ou número,
- a assinatura de movimento, rodando.

As três têm que ser **diferentes de verdade**: mudar a família da fonte, a temperatura da cor e a densidade, não só o tom do acento. Uma delas pode ser a mais ousada (ver `futurista.md`).

Embaixo de cada uma, 3 linhas: o que ela comunica, o risco dela e onde ela já funcionou.

Abrir no navegador (ou publicar como Artifact) para a pessoa escolher. **Não seguir sem a escolha.** Misturar ("a fonte da 1 com a cor da 3") é resposta válida.

### 4. Folha de direção (`DIRECAO.md` na pasta do projeto)
Depois da escolha, escrever a folha que a construção vai seguir. Uma página:

```
CONCEITO        frase + 3 adjetivos + referência física
CORES           tokens com nome que conta a história (tinta, brasa, marfim, ouro...)
                fundo · elevado · superfície · texto 100/72/46 · linha · acento · acento-sobre-claro
TIPOGRAFIA      display + texto (no máx. 2 famílias) · peso máximo · escala com clamp()
RITMO           largura máxima · espaçamento entre seções · sequência de fundos das seções
IMAGEM          o que é o herói (produto/pessoa real) · tratamento (ex.: P&B + véu da cor)
MOVIMENTO       1 assinatura + no máx. 2 apoios · easing · duração
PROIBIDO        5 coisas que esta peça não faz
```

### 5. Construir seguindo a folha
- Partir do `codigo/` quando o movimento for o mesmo vocabulário; não reinventar.
- Tokens em `:root` com os nomes da folha; nenhuma cor solta no meio do CSS.
- Conteúdo real, com o porquê de cada bloco: executivo, mas nunca opaco.

### 6. Revisar antes de entregar
1. `referencias/anti-ia.md`, item por item. Trocar, não só apontar.
2. Checagem técnica de `regras-fixas.md` (seção "Antes de entregar"): 360px de largura, contraste, menos movimento, fontes, peso da página.
3. Olhar a página **rodando** (navegador/print), não só o código. Rolar até o fim no celular. Prints em 393×852 e 375×667 com `codigo/teste-celular.mjs`, folha de todas as partes lado a lado conferida **antes** de mandar.
4. **Mostrar parte por parte**, um print por vez, na ordem da página, e esperar o ok de cada uma. No fim, teste no celular de quem aprova (Wi-Fi + QR) ou link publicado.
5. Entregar dizendo **qual arquivo/token mexer** para mudar cada coisa, pensando em quem não programa.

---

## Modo revisão
Se mandarem uma página pronta ("revisa esse site"): pular para o passo 6, listar o que fere as regras e a lista anti-IA em ordem de impacto e propor a troca de cada um. Não reescrever a página inteira sem pedido.

## Slides
Mesma folha, adaptada: um slide = uma ideia; título é a conclusão, não o assunto ("O CPL caiu 38% com a troca da LP", e não "Resultados"); número grande no lugar de tabela quando der; no máximo 1 gráfico por slide. Para o formato, preferir o tipo Slides do Artifact quando estiver disponível. Usar `.pptx` só quando pedirem arquivo.

## Regra de ouro
**Uma decisão forte por peça.** Um site tem o fundo em fluxo; outro tem o card real do app no topo. Quem tenta impressionar com tudo ao mesmo tempo parece template.
