# Regras fixas: o que não muda de projeto para projeto

Tiradas de sites que deram certo no ar (uma agência com fundo escuro e uma página de lista de espera de app com serifada) e de boas práticas de tipografia e acessibilidade. Os valores entre parênteses são os que foram usados de fato, para servir de régua.

---

## Tipografia: é ela que dá cara de "pensado"

1. **No máximo 2 famílias.** Uma de display (títulos) e uma de texto. Dá para fazer com uma só (ex.: Manrope com contraste de peso) ou com par serifada + sans (ex.: Bodoni Moda + Karla).
2. **O contraste vem de UM eixo, forte:**
   - por **peso**: título fino (300) com a palavra-chave em 800 (`h1 strong{font-weight:800}`), ou
   - por **família**: serifada de display + sans de texto.
   Contraste fraco (500 com 600, ou duas sans parecidas) é o que deixa com cara de template.
3. **Peso máximo definido.** Num app, "nada passa de 600" tirou a cara de cartaz. Definir o teto na folha de direção.
4. **Título com espaçamento negativo:** `letter-spacing:-.01em` a `-.03em`, `line-height:1.04–1.12`. Texto com `line-height:1.5–1.6`.
5. **`text-wrap:balance` em todo título.** Em parágrafo, `text-wrap:pretty`.
6. **Largura da linha medida em caracteres:** título principal ≤ 14ch, texto de apoio 48–62ch, texto corrido ≤ 70ch.
7. **Escala fluida com `clamp()`**: título `clamp(40px,6.2vw,76px)`, seção `clamp(32px,4.4vw,54px)`.
8. **Corpo ≥ 17px na web.** Campo de formulário com 16px no mínimo, senão o iPhone dá zoom.
9. **Etiqueta acima do título (eyebrow):** 11–13px, caixa alta, `letter-spacing:.14–.16em`, na cor de destaque. Uma por seção, no máximo.
10. **Números com `font-variant-numeric:tabular-nums`.** Número grande pode ser fino (300) e enorme. A unidade vai menor, na cor de destaque.
11. **Fonte hospedada no próprio site em woff2**, com `font-display:swap` e `unicode-range`. Google Fonts só em protótipo.

## Cor

12. **Uma cor de destaque. Uma.** Ela ocupa menos de 10% da tela: botão, eyebrow, um detalhe por bloco.
13. **Duas versões do destaque:** a normal para fundo escuro e uma mais escura para texto sobre fundo claro, para passar no contraste (`--accent-2`).
14. **Fundo com temperatura, nunca cinza neutro:** azul-tinta (`#0f1623`), ou preto quente (`#0C0A09`) com seções "brasa" (`#17120E`) e "vinho" (`#3A1620`). O preto puro `#000` só fica bem em app com foto ocupando a tela.
15. **Texto em 3 níveis de opacidade sobre o fundo**, não em 3 cinzas inventados: 100% / ~70% / ~45%.
16. **Linhas e bordas em rgba de 10–13%** da cor do texto. Borda sólida cinza denuncia template.
17. **Tokens com nome que conta a história:** `--tinta --brasa --marfim --ouro` ou `--ink --paper --accent`. Trocar a cor de um projeto = trocar os tokens, nada mais.

## Layout e ritmo

18. **Grade assimétrica no topo**, não tudo centralizado: `1.35fr / .65fr` no herói e `1.2fr / .8fr` nos números. Centralizar fica para a coluna estreita de celular e para o fechamento.
19. **Ritmo de fundos entre seções:** escuro → claro → cinza → faixa colorida. Seções todas iguais = página sem respiração.
20. **Espaçamento generoso e fluido:** seção `clamp(64px,9vw,120px)`, largura máxima ~1180px, margem lateral `clamp(16px,4vw,40px)`.
21. **Raio de canto consistente:** um valor para card (18–26px), pílula `999px` para botão e chip. Não misturar 4, 8, 12 e 22 na mesma página.
22. **Fechamento forte:** o rodapé pode ser um bloco inteiro na cor de destaque com a chamada final. O fim da página é a última chance de conversão, não um rodapé cinza.

## Imagem

23. **Produto real ou pessoa real no herói.** O card do app de verdade, o fundador, a loja. Ilustração genérica e foto de banco de imagem estão fora.
24. **Tratamento único para todas as fotos:** por exemplo P&B, contraste 1.12 e um véu da cor de destaque. Um tratamento só deixa fotos de origens diferentes parecendo um ensaio.
25. **`object-fit:cover` com `object-position` escolhido** (`50% 28%` para não cortar o rosto). WebP em 2 tamanhos (400 e 680).

## Movimento

26. **Uma assinatura de movimento por página e no máximo 2 apoios.** Exemplo: assinatura = fundo em fluxo; apoios = revelação por palavra e cascata.
27. **Easing de saída longa:** `cubic-bezier(.16,1,.3,1)`, de .45s a .95s. Nada de `ease-in-out` sem graça.
28. **Revela ao entrar na tela, uma vez,** com atraso em cascata de 60–90ms entre irmãos.
29. **Hover discreto:** `translateY(-1px)` no botão, `-3px` no card. Nada que pule.
30. **`prefers-reduced-motion` desliga tudo:** o shader, o letreiro, o brilho, as revelações. Obrigatório.
31. **Nunca animar largura, altura ou top.** Só `transform` e `opacity`.

## Interação e formulário

32. **`:focus-visible` com contorno na cor de destaque** em todo botão, link e campo.
33. **Botão principal grande no celular:** 56px de altura, largura total abaixo de 900px.
34. **Erro do formulário na própria label**, em texto, não só borda vermelha.
35. **Micro-texto de confiança abaixo do botão:** "Leva 20 segundos." / "Sem spam. Avisamos uma vez."

## Texto (anda junto com o visual)

36. **Título de 2 a 5 palavras** sempre que der.
37. **Cada bloco diz por que existe.** Uma regra ou limite sempre vem com uma linha de motivo.
38. **"Para quem é / Não é para você se"** filtra e gera confiança.
39. **Número concreto em vez de adjetivo.**

## Performance e rastreamento

40. **Scripts pesados depois da interação:** carregar o GTM no primeiro scroll ou toque, com uma rede de segurança (timer) para quem sai sem interagir. Atenção: algumas ferramentas de depuração (Tag Assistant) e times de mídia preferem o GTM imediato. Decida com quem cuida da medição antes de adiar.
41. **Shader com `powerPreference:"low-power"`**, só se houver WebGL, só sem menos movimento, e com fallback em CSS (uma classe `.gl` liga o canvas, senão fica o degradê).
42. **Medir só no domínio de produção** (travar por hostname), para teste não virar visita.

## Carregamento e som

43. **Carregamento nunca bloqueia.** Nada de tela de porcentagem que segura a pessoa. A primeira cena aparece **em menos de 2 segundos**, com uma imagem fixa do primeiro quadro, e o resto (vídeo, 3D, sequência de imagens) carrega **enquanto ela já lê e rola**. Se houver carregador, ele dura no máximo ~1,5 s e já mostra a marca. Se demorar mais, a página abre assim mesmo.
44. **A rolagem funciona desde o primeiro segundo.** Nunca exigir clique para poder rolar.
45. **Som só depois de um gesto da pessoa.** Navegador nenhum toca áudio sozinho. O **primeiro toque em qualquer lugar** liga a música, sem tela de espera e sem botão "entrar com som": um aviso discreto ("Toque na tela") que some no 1º toque basta. O `play()` roda **dentro do próprio toque**, sem atraso. Uma música por parte = **2 tocadores que revezam** (no celular cada `<audio>` precisa do seu toque). Controle de som sempre visível; a escolha fica lembrada (localStorage). Detalhe técnico em `celular-e-tecnica.md` §6.
46. **A interação tem que ser óbvia para quem não é da bolha tech.** Quem lê pode ser RH, dono de empresa ou cliente leigo. Por isso:
   - a instrução fica **em português simples** ("Role para continuar", "Toque para ver a estratégia"), nunca só um ícone ou um termo em inglês;
   - a pista **se mexe** (seta ou mouse animado) e some sozinha depois da primeira rolagem;
   - se a pessoa ficar ~4 s parada na primeira cena, a pista **reaparece** ou a cena **avança um pouco sozinha** para mostrar que há mais;
   - existe sempre um caminho de **botão** ("Próximo", "Ver tudo") além da rolagem, para quem não entendeu o gesto;
   - **modo guiado**: quando a experiência depende de rolagem, a página pode **avançar sozinha de seção em seção**, parando em cada ponto importante, como um filme com capítulos. A pessoa pode **pausar, voltar e assumir a rolagem a qualquer momento**: o automático para assim que ela rola ou toca. Barra de progresso por seção sempre visível;
   - antes de publicar, **testar com 1 pessoa de fora da bolha**: ela entende o que fazer sem ajuda em 5 s?

## Celular (detalhe e motivo em `celular-e-tecnica.md`)
47. **Toda informação na tela se lê com facilidade no celular**, inclusive texto dentro de imagem, card e tela desenhada: ≥ ~10px, quase branco. Sigla interna vira palavra ("D+7" → "7 dias"); tabela pequena tem cabeçalho.
48. **Texto não cobre o rosto.** Ordem no celular: provas em cima (2 por vez, girando) → pessoa → selo, título, texto, números (girando) → botão. Se não couber, o título encolhe primeiro.
49. **Muitos cards = um ou dois por vez, girando**, nunca vários pequenos ao mesmo tempo. Tela comprida passa por partes, em tamanho legível.
50. **O botão principal pulsa; o secundário fica parado.** Navegação de etapas logo depois do texto (grudada no rodapé só se o texto for longo).
51. **Fila de download com prioridade** (máx. 6 ao mesmo tempo), PNG de objeto → WebP ≤ 640px, metade dos quadros no celular. Toque que "não responde" quase sempre é a rede entupida.
52. **Gesto de camada fechada não pode agir**, arrasto não vira clique, `touch-action:manipulation` contra o zoom do toque duplo.
53. **Revisão por print, parada por parada**, em 393×852 e 375×667 (`codigo/teste-celular.mjs`).
54. **Aviso de cookies nunca cobre o botão principal da 1ª tela.** No celular, uma barra alta cobre o botão do topo e ~20% de cada tela até a pessoa responder. Barra fina e baixa (1 linha + 2 botões pequenos), ou o CTA do topo posicionado acima dela. Conferir no print 393×852.

## Aprendido numa LP de loja de entretenimento
55. **O enfeite sai da marca ou do lugar real, nunca do banco de ícones.** Os personagens de fliperama foram redesenhados quadradinho por quadradinho a partir da grade do próprio logo e viraram mascote (corredor animado entre a abertura e as fotos, card de cada loja, rodapé). O fundo era a estampa do carpete da loja, a ~10–13% de opacidade, com posição deslocada por seção (`--carpete-pos`) para parecer um tapete contínuo, e o divisor entre seções era em degraus de pixel. Pergunta da direção: *o que existe no logo ou no espaço do cliente que pode virar textura, mascote ou divisor?*
56. **Cada seção tem a sua cor da paleta** (no título, na borda dos cards e no acento), sempre tirada do logo. Dá ritmo sem inventar cor.
57. **Modo revisão no link de aprovação.** O que o cliente ainda não confirmou (preço, número, endereço, foto provisória) aparece com etiqueta amarela na própria página, e uma classe no `<html>` (`class="revisao"`) desliga tudo para produção. O cliente aprova olhando o que falta, e nada inventado vai ao ar.
58. **Animação decorativa contínua só roda enquanto aparece na tela.** Com menos movimento ligado, a cena fica **parada numa pose que ainda conta a história**, sem sumir.

---

## Antes de entregar (checagem técnica)
- [ ] A primeira cena aparece em **< 2 s no 4G** e a rolagem funciona sem precisar esperar nem clicar
- [ ] Abre e lê bem em **360px** de largura, sem rolagem lateral
- [ ] Contraste **AA**: texto ≥ 4.5:1; o destaque sobre fundo claro usa a versão escura
- [ ] Com **menos movimento** ligado, nada anima e nada fica invisível
- [ ] Sem JS, o conteúdo aparece (classe `.js` só arma as animações)
- [ ] Fontes woff2 locais, imagens WebP com tamanho certo, herói sem imagem gigante
- [ ] `:focus-visible` em tudo que é clicável; o Tab percorre a página na ordem
- [ ] Título, descrição e OG image preenchidos
- [ ] Olhei rodando, rolei até o fim no celular
- [ ] Prints em **393×852 e 375×667** de todas as partes, folha lado a lado conferida antes de mandar (`codigo/teste-celular.mjs`)
- [ ] Teste com `--lento` (4G): abre em ≤ 3 s e o 1º toque responde
- [ ] Nenhum texto (nem dentro de card/imagem) abaixo de ~10px ou em cinza fraco no celular
- [ ] Se tem som: o 1º toque liga e a música troca em cada parte; nada de tela de espera
- [ ] Gestos de painel fechado desligados; tocar rápido não dá zoom
- [ ] Botão fixo do celular some quando a seção de destino (formulário/lojas) está na tela
- [ ] Animação decorativa pausada fora da tela; vídeo da abertura com botão de pausar e sem carregar na economia de dados
- [ ] `class="revisao"` tirada do `<html>` antes de publicar para tráfego
