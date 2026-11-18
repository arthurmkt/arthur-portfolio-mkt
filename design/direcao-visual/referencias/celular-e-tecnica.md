# Celular e técnica: o que um site-portfólio de 12 paradas ensinou (nov/2026)

O projeto: retrato que troca de roupa por sequência de quadros, telas de prova girando, uma estratégia em 8 etapas por "mundo". Cada item abaixo custou uma rodada de ajuste. Ler antes de construir qualquer página Nível 2 ou 3, e antes de revisar no celular.

---

## 1. Como revisar (e como entregar para quem aprova)
- **Revisão por print, um por vez, na ordem da página.** Entregar prints de celular (393×852) numerados (`00-entrada.jpg`, `01-...`) numa pasta `prints-mobile/` e esperar o "ok" de cada parada antes de seguir para a próxima.
- **Antes de mandar, revisar a folha inteira** (todas as telas lado a lado) para pegar o que quebrou de tabela quando mexeu numa regra geral. Mudança no celular costuma vazar para outras paradas.
- **Conferir sempre em 2 tamanhos:** 393×852 (comum) e 375×667 (iPhone SE, o pior caso). Celular baixo é concessão combinada: lá o texto fica completo e o rosto aparece menos.
- **LP de uma página só:** `teste-celular.mjs <url> "" 393 852 pasta --inteira` tira uma tela a cada ~90% da altura, como a pessoa vê rolando (o print "página inteira" do Chrome repete pedaços; não usar). Montar a folha com todas e ler de cima a baixo.
- **Ferramenta:** `codigo/teste-celular.mjs` (prints em qualquer tamanho, avisa rolagem lateral e erro de script, `--lento` simula 4G, apaga o perfil temporário do Chrome; sem isso o disco enche).
- Mudanças que valem para o computador também: dizer isso na resposta ("essa tela é a mesma no computador").

## 2. Legibilidade: o critério mais cobrado
> Todas as informações que aparecem no site, as pessoas têm que conseguir ler com facilidade.
- **Texto dentro de imagem/tela desenhada também é texto.** Mínimo de ~10px na tela do celular, branco ou quase branco (opacidade ≥ .85), nunca cinza a 50%.
- **Sigla interna vira palavra:** "D+7" virou "7 dias". Se quem revisa pergunta "o que é isso?", a tela falhou.
- **Tabela pequena ganha cabeçalho de coluna** (ENTREGA · DONO · PRAZO). Sem ele, três colunas de palavras soltas não se leem.
- **Tela grande demais para o espaço:** não reduzir até virar formiga. Mostrar em tamanho legível e **passar por partes** (desce devagar, para, volta) ou **uma tela por vez, girando a cada 3 s**.
- Selo/etiqueta que quebra em 2 linhas: diminuir o espaçamento entre letras e a fonte até caber em 1.

## 3. Composição no celular (página com pessoa + provas + texto)
Ordem de cima para baixo que funcionou em todas as paradas:
1. **Faixa de provas no topo**, 2 cards por vez, girando (cards de produto, telas, números). Os cards **sempre se movem**.
2. **Rosto e começo do peito** no meio, livre de qualquer texto por cima.
3. **Selo → título → texto → números** (2 por vez, girando para o lado) → **botão principal**.
- **O texto é o principal, mas não cobre o rosto.** Se não couber, diminuir o título (no celular ~`clamp(25px,7.3vw,36px)`) antes de cortar a pessoa.
- **Encaixe do retrato medido no aparelho**, não por porcentagem fixa: guardar em tabela onde fica a cabeça em cada foto (fração da altura, cabelo → queixo/peito) e calcular escala e posição para caber entre o fundo da faixa de cima e o topo do selo. Medir pelo **card visível**, não pela caixa que o contém.
- **Borda de cima da foto some num degradê**, nunca em linha reta.
- **Fundo animado (ícones do tema) pode encher as laterais**, mas some atrás do rosto e fica bem apagado atrás do texto. Fundo largo do computador não serve no celular: fazer uma versão em pé.
- Nome embaixo de card que já tem título dentro: tirar (cobria a última linha).

## 4. Botões
- **O botão principal de cada parte pulsa** (brilho em onda + sobe 3px, 2,2 s, começa ~2 s depois de a parte aparecer). O secundário ("Pular para o próximo") fica parado: a atenção vai para o principal. Com menos movimento ligado, para.
- **Navegação de etapas (Anterior / Próximo / Pular) logo depois do texto**, e grudada no rodapé (`position:sticky`) só quando o texto for longo. Presa sempre no pé da tela fica longe demais.
- Etapas de 8 itens no celular: **uma linha que desliza para o lado**, com a etapa atual centralizada sozinha, e não 4 linhas de botões.
- `html,body,button,a{touch-action:manipulation}`. Sem isso, tocar rápido várias vezes dá zoom.

## 5. Carregamento (no celular de verdade, não no Wi-Fi do escritório)
- **Nada de tela de espera.** Liberar a página quando a 1ª imagem chegar (~1–2 s); o resto baixa por trás. Uma tela "toque para começar" foi recusada por fazer a pessoa perder tempo.
- **Fila com prioridade e no máximo 6 downloads ao mesmo tempo.** Pedir 1.600 arquivos de uma vez travou o toque no celular ("cliquei e não foi").
- **PNG de objeto/produto → WebP de até 640px** (36 MB → 0,7 MB, sem diferença visível). Fundos → WebP até 1600px.
- **Sequência de quadros no celular: metade dos quadros** (ímpares + o último). Não se nota na tela pequena.
- **Música em 112 kbps**; só as 2 primeiras faixas baixam de cara, a do próximo trecho começa a baixar uma parada antes.
- Medir com `teste-celular.mjs --lento`: o site tem que abrir em ≤ 3 s.

## 6. Som no celular (regra 45 detalhada)
- **Nenhum navegador toca som sozinho.** O primeiro toque em qualquer lugar liga a música. O aviso é discreto ("Toque na tela"), some no 1º toque e não precisa falar de música.
- **`play()` tem que rodar dentro do próprio toque**, sem `setTimeout`. Com 50 ms de atraso o iPhone já bloqueia.
- **Uma faixa por parte = só 2 tocadores** liberados no 1º toque, revezando as músicas com troca suave. Um `<audio>` por faixa não funciona: cada um pediria um toque. Guardar onde cada faixa parou e retomar ao voltar.
- `navigator.audioSession.type = 'playback'` (iOS 16.4+) faz tocar mesmo no silencioso.
- Se a troca falhar (`NotAllowedError`), trocar a música no tocador que já está tocando.

## 7. Gestos: armadilhas que faziam a navegação pular de parada
- **Gesto de uma camada escondida continua ativo.** Um painel fechado ainda ouvia "arrastar para cima = próximo" e a pessoa ia da entrada direto para a 2ª parte. Todo listener de toque de painel/modal confere se ele está aberto.
- **Arrasto não é clique:** depois de deslizar >12px, ignorar o `click` dos 600 ms seguintes (senão o dedo solta em cima de um botão).
- Na 1ª tela, arrastar para cima tem que fazer o mesmo que o botão "Iniciar" (e ligar o som).

## 8. Diagnóstico no celular real
- Modo `?debug` na URL: painel fixo no pé da tela com cada toque (onde caiu), estado da navegação, estado do som e erros. Só aparece com o parâmetro; no link normal o site abre limpo.
- Se o site limpa a UTM da barra de endereço, **não apagar o `?debug`** junto.
- Teste no celular na mesma rede: `python3 -m http.server 8767 --bind 0.0.0.0`, IP local com `ipconfig getifaddr en0` (macOS) ou `hostname -I` (Linux), um QR code apontando para `http://<ip>:8767/` e o link digitável na resposta. Só funciona no mesmo Wi-Fi, com o computador ligado.

## 9. Publicar como Artifact do Claude (link que abre em qualquer rede)
- Limite: 511 arquivos e 256 MB por versão; 255 arquivos / 64 MB por envio → publicar **em lotes no mesmo artifact** (o mesmo link).
- Muitos quadros soltos: juntar em **atlas** (4 quadros numa imagem 2×2) e recortar no `drawImage`. 1.670 arquivos viraram 418.
- Caminhos `../pasta/` viram `pasta/`.
- O link nasce **privado**: avisar que para outra pessoa ver é preciso compartilhar.
- Fora do Claude, qualquer hospedagem estática (Netlify, Vercel, GitHub Pages) resolve.
