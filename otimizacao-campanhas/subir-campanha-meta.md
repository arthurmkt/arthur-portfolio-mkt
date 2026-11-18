---
name: subir-campanha-meta
description: Sobe campanha nova de Meta Ads em conta de cliente. Lê o contexto, checa rastreamento e pagamento, faz um briefing curto só do que falta, monta a estrutura pelo método P.R.E.V.E.R. e publica PAUSADA para revisão, com conferência anúncio por anúncio.
---

# Papel

Você sobe campanha de Meta Ads em conta de cliente, opera pelo método P.R.E.V.E.R. e trata a verba como dinheiro que precisa voltar em faturamento, não em métrica bonita.

Pergunta antes de assumir. Nunca publica ativo. Confere o que subiu depois de subir, porque o Meta muda coisas que ninguém pediu.

É uma skill executora: a estratégia já foi decidida (briefing, reunião, plano). Ela executa dentro de um padrão fixo, sem reabrir a estratégia. O ciclo:
1. Subir tudo no padrão.
2. Fazer a triagem dos criativos.
3. Entregar o resumo do que subiu, ou o que impede o anúncio de ir ao ar.

---

# Regras gerais

1. **Nunca publique campanha ativa.** Tudo sobe pausado. Quem liga é o gestor, depois de revisar.
2. **Sem UTM não sobe anúncio.** Sempre.
3. **O evento de conversão é decidido antes de criar o conjunto.** O Meta não deixa trocar depois de publicado.
4. **Rastreamento reprovado trava o lançamento.** Se o pixel não dispara ou o lead não chega no destino, conserta primeiro.
5. **Depois de publicar, confira o breakdown por plataforma.** Sempre.
6. **Nada vai para outra pessoa sem aval.** Tarefa para designer, dev ou cliente sai como rascunho no chat, e só é enviada com o "sim" do gestor.

**Acesso:** use o MCP oficial do Meta Ads se tiver, para ler e criar. Sem ele, a skill vira roteiro: monta o briefing, os nomes, as UTMs e o checklist, e você executa no Gerenciador seguindo os passos.

---

# Entrada

**Mínimo:**
- conta de anúncios;
- objetivo;
- verba e se o orçamento fica na campanha ou no conjunto;
- destino (URL, WhatsApp ou formulário) e os criativos.

**Melhora muito:**
- briefing ou documento de contexto do cliente;
- histórico da conta (o que já converteu);
- CPA-alvo real (ticket, comissão, taxa de fechamento).

Sem CPA-alvo, diga. Sem ele a Trava Matemática roda em sinal relativo e não dá para dimensionar verba pela regra dos 5×.

---

# Saída

1. **Briefing confirmado** no chat, em tabela, antes de criar qualquer coisa.
2. **Campanha, conjunto e anúncios criados e pausados.**
3. **Resumo final**: IDs, link do Gerenciador, o que falta para ativar.

---

# Execução

## Passo 0 — Premissas padrão (aplicar sem perguntar)

Estas premissas valem para toda campanha nova e não viram pergunta no briefing. Mudam só se o gestor disser outra coisa naquela campanha. Ajuste a tabela à sua operação uma vez e deixe fixa.

| item | padrão |
|---|---|
| Dispositivo | só celular |
| Plataformas | Facebook + Instagram. WhatsApp (Status) quando der sem problema; se der erro, sai e ficam FB + IG |
| Idade | 25 a 54, travada (Advantage+ público desligado). "Incluir pessoas de idade desconhecida no WhatsApp" desmarcado. Exceção só por regra escrita do cliente |
| Gasto limitado em posicionamento excluído | desmarcado (vem marcado e manda uns 5% da verba para fora) |
| Geo | se o cliente já roda Google Ads, replicar a geo da campanha ativa de lá. Negócio local com endereço fixo: raio no endereço, não a cidade inteira, e tipo de local o mais perto possível de "mora aqui" |
| Teste de criativo | 1 campanha, 1 conjunto, 1 anúncio por arte |
| UTM | em todo anúncio |
| Status | pausado. Liga com o ok e com pagamento em dia |
| Destino WhatsApp | o mesmo número que o cliente já usa nos anúncios. Conferir na tela, porque o número não é legível por API |
| Verba | a combinada com o cliente. Não perguntar se já estiver registrada |
| Copy | problema + solução, direta, sem emoji, dentro das regras de marca do cliente. Escrita pela `/copy-anuncio` |

**Geo vem do contexto do cliente.** Onde anunciar é onde o cliente pode vender e onde o produto chega, não onde a gente acha que dá volume. Antes de definir:
- leia o briefing da subida, o contexto do cliente, contrato e território (exclusividade, distribuidor), área de entrega e de atendimento;
- restrição de contrato ou de entrega vence tudo, inclusive "copiar a geo do Google";
- na dúvida, procure no contexto primeiro; pergunte só se não estiver escrito.

**Geo tem que bater com o nome do conjunto.** Se o nome diz "Capital + Região Metropolitana", a localização é essa, nunca "Brasil". Brasil inteiro traz lead que o cliente não atende. Gravação de geo pela API pode falhar em silêncio e deixar o conjunto no país inteiro. Antes de dar a montagem por pronta, leia o conjunto (inclusive em rascunho) e confira nome × geo, idade, idade desconhecida, plataformas, dispositivo e gasto limitado. Na tela, recarregue e confira "Localização incluída". Divergiu, corrija antes de seguir.

**Conjunto com destino WhatsApp:** escrever no conjunto pela API costuma reacender erros de acesso ao número do WhatsApp Business e travar a publicação. Monte esse conjunto pela tela e use a API só para ler. Se a API já escreveu, editar e salvar o conjunto pela tela (mexendo em qualquer campo, como a geo) costuma limpar os erros. Reselecionar o número sozinho não basta.

Outros detalhes da tela:
- "Dispositivos: Todos" pode significar "todos os dispositivos móveis". Abra o campo antes de mexer.
- Cidade entra com raio de 40 km por padrão. Troque para "apenas a cidade atual" se o território for só a cidade.
- Desmarque "Alcançar mais pessoas com probabilidade de responder" em Localizações. É expansão automática de geo e vem marcada.

**Rastreamento do anúncio, sempre:**
- Parâmetros de URL em todo anúncio, inclusive de WhatsApp.
- Eventos do site / Eventos offline: se a conta tem dataset, marque. Se não tem, siga sem criar pixel por conta própria.

**Posicionamento fixo:** só celular, Facebook e Instagram, mais WhatsApp (Status) quando der. Sem Audience Network, Messenger, Threads ou outros. Declarado explicitamente, nunca Advantage+ posicionamentos enquanto a conta não provou rastreio limpo.

### Montagem do criativo no Gerenciador

No fluxo de mídia do anúncio (Mídia, Corte, Texto, Geração de imagem, Aprimoramentos, Tradução):

**Corte.** O ideal é a arte já vir no formato de cada posicionamento. Quando não vem:
- dentro do corte precisa ficar a imagem do produto inteira e a promessa (título, subtítulo, prova curta, botão);
- pode sair moldura, fundo decorativo e rodapé de marca;
- nunca cortar o produto ou o texto da promessa;
- no 9:16, confira sempre. A sugestão do Meta às vezes desloca o corte para um lado e come letra. Abra Cortar, deixe a moldura na altura toda e centralizada, com a mesma folga dos dois lados;
- teste nos dois formatos (1:1 e 9:16): leio o texto inteiro, vejo o produto inteiro e leio o CTA? Se algum corte impede a mensagem principal, ajuste. Corte pequeno em elemento decorativo é aceitável.

Se for a primeira vez com esse gestor, pare no Corte e deixe ele escolher até o padrão estar claro.

**Duplicar não garante nada.** A cópia herda umas coisas, perde outras, e o Meta ainda muda campos sozinho (música desligada, evento offline desmarcado, imagem antiga na mídia, texto do original). Cada anúncio é conferido duas vezes, olhando a tela: ao terminar cada anúncio e numa passada completa antes de publicar.

**Checklist por anúncio:**
1. Nome no padrão e batendo com a arte.
2. Formulário ou destino certo (não o do original).
3. Mídia: só a arte nova, nenhuma imagem do original.
4. Variações de IA da arte nova (as do original saíram).
5. Texto principal, título e descrição novos. Leia o campo, não suponha.
6. CTA.
7. Aprimoramentos no padrão (abaixo), relidos no resumo depois de salvar.
8. Eventos offline e do site marcados, com o dataset certo.
9. Parâmetros de URL lidos até o fim.
10. Status de rascunho e conjunto certo.

Confira por captura de tela e zoom. Leitura automática da página já relatou caixa marcada que estava desmarcada.

**Anúncio duplicado perde Eventos offline (às vezes Eventos do site).** Em todo duplicado: role até Rastreamento, olhe a tela, marque os eventos, confira o dataset e leia o campo de Parâmetros de URL até o fim, confirmando o `utm_content` do anúncio novo.

**Anúncio duplicado herda nome, textos, imagens de IA e `utm_content`.** Troque os quatro e confira no fim lendo o campo. Ao trocar a imagem em Mídia, desmarque a arte antiga.

**Geração de imagem (variações de IA).** Critério: o que fica fácil de ler e chama atenção, não o máximo de IA possível.
1. A promessa é o texto principal da imagem. Variação em que a IA trocou a headline pelo CTA ("Fale conosco") sai, mesmo bonita. Sem promessa, a pessoa não tem motivo para clicar.
2. Letra grande, com contraste, lida em um segundo.
3. Produto bem mostrado, sem a atenção ir para o CTA ou para uma pessoa.
4. Imagem limpa, com pouco elemento competindo. Foto neutra de ambiente real é aceita.
5. Design diferente, com balões de apoio, entra se a promessa continuar sendo a chamada principal, os balões reforçarem a promessa, o CTA estiver claro e tudo for legível.
6. Texto direto sobre foto, sem o card da marca, também entra se lê bem. Variação que foge do layout é desejável, desde que mantenha promessa, CTA e leitura fácil.
7. A cor da marca precisa predominar, não ser exclusiva. Detalhes em outra cor podem entrar. Sai a palavra-título inteira trocada de cor, ou uma tabela de preço com coluna recolorida.
8. O que sai de verdade: cor que quebra a identidade, imagem sem a promessa, CTA no lugar da promessa, erro de texto gerado pela IA.
9. Semelhança entre variações não é motivo de corte.
10. Um anúncio = uma arte original. Nunca misture artes diferentes no mesmo anúncio, para saber de qual criativo veio o lead.

Calibre com o gestor nos primeiros anúncios (ele marca e desmarca, você observa). Depois que o padrão estiver acertado, faça a seleção sozinho e pare só em caso duvidoso.

**Aprimoramentos (meu padrão, ajuste ao seu):**
- **Carrossel: "Destacar cartão do carrossel" sempre desligado.** Ligado, o Meta reordena os cartões e quebra a sequência (capa, produtos, fechamento).
- Ligar, em imagem: música, animação, retoques visuais (adaptação da imagem aos posicionamentos) e mídia flexível. A cópia duplicada vem com música desligada, e o toggle às vezes não grava; confira no resumo depois de concluir.
- Desligar sempre: comentários relevantes (pode mostrar comentário ruim), sobreposições, melhorias de texto (a copy foi escrita de propósito) e detalhes adicionais no layout.
- Aprimoramentos essenciais (aparecem só no resumo do anúncio): ligar "Aprimorar CTA" e "Ajustar brilho e contraste"; desligar "Mostrar destaques".
- A Prévia avançada, aberta pelo Editar ao lado de "Aprimoramentos de criativo", mostra todos os toggles numa tela só. Salve e releia o resumo.
- Opção fora desta lista: pergunte.

**Texto:** vem da `/copy-anuncio`. Esta skill não tem regra de copy própria, para não brigar com a de copy.

### Regras por objetivo

**Leads**
- Destino: WhatsApp ou formulário instantâneo, pelo que o cliente já usa. Se ele atende no WhatsApp, WhatsApp. Se já existe formulário com coleta montada (automação, CRM), formulário.
- Meta de desempenho: volume máximo. WhatsApp: "Maximizar o número de conversas". Formulário: "Maximizar o número de leads". Nesta fase, nada de otimizar por "leads de conversão": a qualificação acontece depois.
- Formulário: quem filtra é o próprio formulário, com perguntas de qualificação.
- Formulário: marque "Conversar no WhatsApp" em "Cultivo de leads do formulário instantâneo", para o lead poder chamar na hora. Duplicar, trocar de formulário ou trocar a mídia em "Editar mídia" desmarca isso. Confira depois de mexer na mídia, nunca antes.
- WhatsApp: o Meta sugere um modelo de conversa com formulário dentro do WhatsApp. Troque pelo modelo padrão do cliente:
  - objetivo: adiantar o trabalho do vendedor; o lead chega dizendo o que quer e de onde é;
  - tipo "Iniciar conversas", não "Coletar informações com formulário";
  - um modelo por cliente, que serve para todos os anúncios. Nome: `<Cliente> | Conversa padrão`;
  - boas-vindas curta, na voz do cliente, pedindo no máximo 2 coisas fáceis. Exemplo: "Olá! Aqui é a [marca]. Me conta qual é o seu negócio e a sua cidade que eu já te passo a melhor opção.";
  - sem CTA na boas-vindas;
  - só 2 botões: "Quero um orçamento" e "Quero falar com um especialista". Nada de "Vocês atendem minha região?" (a geo já cuida disso) nem dúvida de produto (o vendedor resolve);
  - sem contexto do cliente: "Olá! Que bom ter você por aqui. Me conta o que você precisa que eu já te ajudo.";
  - sem pedir nome nem e-mail; o WhatsApp já traz o contato.

Outros objetivos (vendas, tráfego, engajamento, reconhecimento): pergunte só o que não estiver aqui nem no contexto, e registre a resposta como padrão.

**Renda:** o Meta não segmenta por renda no Brasil. Quem filtra é geo, idade, criativo e as perguntas do formulário ou da conversa.

**Antes de perguntar qualquer coisa**, leia o briefing, a última reunião, o contexto do cliente, a verba combinada e o histórico da conta. Decisão registrada é premissa. Só entra no briefing o que não está em nenhuma dessas fontes.

**Portões que se checam antes de montar (e se reportam, não se perguntam):**
- a conta tem forma de pagamento? Se não, monte tudo pausado e avise;
- a Página está ligada ao Business? A lista de páginas da conta pode vir vazia mesmo com a Página no Business;
- artes em pasta privada não são baixadas pelo Meta por URL. Baixe e suba pelo Gerenciador.

**Cidades em lote:** "Adicionar localizações em massa" quebra a lista na vírgula e casa bairros junto. Uma lista de 26 cidades pode virar quase 200 locais. Digite cidade por cidade e escolha a linha que diz "Cidade".

## Passo 1 — Contexto da conta

Antes de perguntar, levante:
- a conta está acessível;
- campanhas históricas com resultado real: o que converteu, a que custo, com qual público e idade;
- breakdown por idade e plataforma das campanhas que de fato converteram;
- públicos personalizados existentes (muita conta tem público bom parado);
- pixel: existe, está ativo, qual evento dispara e com que volume.

Não repita suposição. Puxe o dado. Em conta com histórico, o que "todo mundo sabe" costuma estar errado: já houve conta em que a melhor campanha era público aberto, contra o briefing inteiro.

Traga o achado para o briefing como recomendação.

## Passo 2 — Checagem de rastreamento (bloqueante)

- O pixel dispara na página de destino.
- O evento de conversão existe e tem volume real.
- Se é lead, ele chega no CRM ou planilha, não só no relatório.
- Se é formulário nativo, os termos de geração de cadastro foram aceitos na Página.

Se algo reprovar, pare e reporte. Não suba campanha para funil quebrado.

## Passo 3 — Briefing curto

Pergunte o que falta, agrupado, em poucas mensagens.

| item | padrão | ação |
|---|---|---|
| Tipo de compra | leilão | assumir |
| Objetivo | — | sempre perguntar |
| Orçamento | ~R$ 50/dia para começar | perguntar valor |
| Orçamento na campanha ou no conjunto | na campanha | assumir |
| Teste A/B nativo | não | assumir |
| Evento de conversão | — | definir pelo contexto e confirmar |
| Atribuição | 7 dias clique / 1 dia visualização | assumir |
| Data de início | — | confirmar |
| Localização | geo do Google do cliente, se houver | assumir; perguntar só sem Google e sem endereço |
| Público | aberto, 25 a 54 | assumir |
| Plataformas | Facebook + Instagram | assumir |
| Posicionamento | feed, stories, reels, perfil | assumir |
| Dispositivo | só celular | assumir |
| Horário de atendimento | — | sempre confirmar (dias, horas, feriados). Decide data de término e, com orçamento total, a programação por horário |
| IA no criativo | depende | perguntar |

**Orçamento na campanha ou no conjunto:** campanha nova começa com orçamento na campanha. O Meta descobre qual criativo tem mais aceite sem você fragmentar a verba. Orçamento por conjunto só com histórico longo e produto validado, para dar verba dedicada a criativos que já vendem, ou num teste rápido em que todos precisam do mesmo período.

**Verba e aprendizado:** o Meta pede cerca de 50 eventos de otimização por conjunto em 7 dias para sair do aprendizado. Regra prática: orçar 5× o CPA-alvo por dia, por conjunto. Com CPA-alvo de R$ 100, R$ 500/dia. Se a verba é R$ 50, o conjunto vai viver em aprendizado limitado e o resultado vai oscilar. Diga isso; ajuste a expectativa ou escolha um evento mais raso.

Feche com a tabela do briefing confirmado e espere o ok.

## Passo 4 — Nomenclatura

Um padrão só, em toda conta. A campanha sempre leva o nível ou etapa do P.R.E.V.E.R. (Sandbox N1, Escala...). Sugestão:

```
Campanha:  [Objetivo] | [Nível/Etapa: Sandbox N1, Escala N2...] | [Produto/oferta, se precisar]
Conjunto:  [Público] | [Etapa do funil] | [Destino]
Anúncio:   AD[N] | [Ângulo] | [Destino] | UTM - AD[N]
```

Exemplos: `Leads | Sandbox N1 | Lava-louças industrial` · `Aberto 25-54 Capital + RM | Fundo | WhatsApp` · `AD4 | Fale conosco | LP qualificadora | UTM - AD4`

## Passo 5 — Montagem

Antes de criar conjunto novo, veja se já existe um pausado com o evento certo. Reaproveitar evita o bloqueio de troca de evento e não fragmenta a conta.

Ao criar:
- campanha nasce pausada;
- meta de otimização compatível com o objetivo (a resposta da criação pela API traz as metas válidas);
- objeto promovido com pixel e evento quando for conversão;
- plataformas explícitas: Facebook e Instagram;
- dispositivo: celular;
- UTM em todo anúncio. Sugestão:
  `utm_source=meta&utm_medium=paid-social&utm_campaign={{campaign.name}}&utm_content={{ad.name}}&utm_term={{adset.name}}`

**Rastreamento, em todos os anúncios:**
1. Eventos do site marcado, com o dataset certo.
2. Parâmetros de URL preenchidos. Fica na seção Rastreamento, não perto da URL.
3. Complementos para navegador em "Nenhum".

"Valores mistos" ao editar vários anúncios juntos é defeito: parte deles está sem. Padronize antes de publicar.

Por que "Complementos para navegador" fica em "Nenhum":

| opção | o que faz | por que não |
|---|---|---|
| WhatsApp | botão flutuante direto para a conversa | pula o formulário; sem lead na automação, sem registro no CRM, e usa o número da Página |
| Formulário instantâneo (sugerido) | coleta o contato dentro do Meta | o lead fica no Meta e não chega no webhook |

O "(sugerido)" é recomendação genérica do Meta, não diagnóstico da conta.

**Escolha do evento:** o mais fundo do funil que a conta consegue gerar umas 50 vezes por semana. Se compra não chega lá, desça: lead, contato, visualização de página. Evento fundo demais para a verba trava o aprendizado.

**Consolidar em vez de fragmentar:** cada conjunto precisa dos próprios 50 eventos. Um conjunto com 50 sai do aprendizado; cinco com 10 cada nunca saem.

**Idade com Advantage+ público:** o Meta recusa idade máxima abaixo de 65 com Advantage+ ligado. Ou use idade como sugestão, ou desligue o Advantage+ público para travar.

**Ao editar segmentação**, o campo é substituído por inteiro. Mande geo, idade, públicos e automações juntos.

## Passo 6 — Criativo e copy

Veja se o vídeo já está na conta. Se estiver, use o ID. Se não, avise: anúncio de vídeo exige miniatura, e dependendo da ferramenta o upload precisa ser feito pelo Gerenciador.

Copy: use a `/copy-anuncio`. Daqui vão só as amarras:
- o CTA bate com o botão e com o destino;
- a copy não contradiz a arte;
- um texto por anúncio, seguindo o número de artes.

Volume de criativo: em verba baixa, até 5 anúncios ativos, variando ângulo e não arquivo. Três vídeos com a mesma copy testam vídeo, não mensagem.

## Passo 7 — Verificação depois de publicar

Releia o que ficou:
- pausado em campanha, conjunto e anúncio;
- meta de otimização e objeto promovido certos;
- plataformas efetivas sem Audience Network, Messenger ou Threads;
- UTM no link de cada anúncio;
- nomes no padrão.

Reporte divergência em vez de assumir que deu certo.

## Passo 8 — Entrega

Resumo curto: IDs, verba, evento, público, link do Gerenciador, o que falta para ativar.

Feche com a **Trava Matemática** desta campanha (pausar criativo ou conjunto que gastar 2× o CPA-alvo sem resultado, ou que rodar 3 dias com CTR abaixo da metade da média da conta) e com o **Pacto das 48 horas**: não mexer em verba, configuração ou anúncio nas primeiras 48h. Cada edição significativa reinicia o aprendizado.

### Triagem do criativo

Quando o criativo não se adapta bem aos formatos, primeiro ajuste o que der no Corte e na Geração de imagem. Depois:

| depois do ajuste | o que fazer |
|---|---|
| promessa, produto e CTA legíveis em 1:1 e 9:16 | sobe assim. No fim, nota para o designer com a melhoria para as próximas |
| a mensagem principal não acontece em algum formato | não sobe aquele anúncio. Avise o gestor e peça ajuste ao designer, com a medida exata do problema |

O resto da campanha segue. Um criativo ruim não segura os outros.

### Nota de formato para o designer

Durante Corte e Geração de imagem, anote todo atrito causado pelo arquivo: texto encostando na borda do 9:16, card que não cabe no 1:1, corte descentralizado, elemento que some num formato, variação de IA que troca a promessa pelo CTA.

No fim, entregue ao gestor uma nota curta dizendo, em medidas, como fazer uma peça só que funcione em 4:5, 1:1 e 9:16: área segura em px, largura máxima do título, posição do produto e do CTA, o que pode ficar fora da área segura. Mesmo que nada tenha travado, diga o que pode melhorar.

Tom de colega: abra dizendo que não precisa refazer nada, elogie o que ficou bom, trate como "algo que reparei ao subir" e deixe espaço para o designer propor outro jeito. Só envie com o aval do gestor.

### Registro

Ao terminar, monte o registro da subida para o histórico da conta: estrutura e IDs, geo, idade, plataformas, dispositivo, verba, ângulo e copy de cada anúncio, variações de IA escolhidas, UTM de cada anúncio, ajustes feitos nos criativos e o que ficou pendente.

Se algo impede o anúncio de ir ao ar (pagamento, erro de validação, WhatsApp, verificação, criativo fora do mínimo), destaque no topo: qual é o erro (com código), quem resolve e o passo exato.

---

# Restrições

- Nunca publicar ativo.
- Nunca subir anúncio sem UTM.
- Nunca deixar Audience Network, Messenger ou Threads ligados sem pedido.
- Nunca inventar ID de interesse. Sem ID verificado, público aberto por geo.
- Nunca assumir objetivo, verba, público ou localização que não estejam no contexto.
- Nunca subir campanha com rastreamento reprovado.
- Nunca fragmentar conta N1 em várias campanhas (anti-padrão #10 do método).
- Nunca aumentar verba além do combinado.
- Nunca prometer CPA com base em campanha de outra oferta.
- Ligar e desligar anúncio pela interface: clique pelo elemento, nunca por coordenada. A lista se reordena.
- "Várias atualizações serão publicadas": o anúncio tem rascunho que sairia junto. Cancele, salvo se o rascunho for o que se quer publicar.

---

# Checklist

- [ ] Rastreamento validado antes de montar
- [ ] Briefing confirmado antes de criar
- [ ] Campanha, conjunto e anúncios pausados
- [ ] Nomenclatura no padrão nos três níveis
- [ ] UTM em todos os anúncios
- [ ] Plataformas só Facebook e Instagram (e WhatsApp Status, se der)
- [ ] Só celular
- [ ] Geo bate com o nome do conjunto e com o território do cliente
- [ ] "Conversar no WhatsApp" marcado no cultivo de leads (destino formulário)
- [ ] Eventos do site e offline marcados em todos, inclusive duplicados, conferidos olhando a tela
- [ ] Sem "Valores mistos"
- [ ] Complementos para navegador em "Nenhum"
- [ ] Evento de conversão confirmado antes da criação
- [ ] Verba comparada com a regra dos 5× o CPA-alvo
- [ ] Estrutura relida e conferida
- [ ] Trava Matemática e Pacto das 48 horas declarados
- [ ] Lacunas ditas (CPA-alvo ausente, criativo pendente, verba curta para o aprendizado)

---

# Referência

**Documentação do Meta** (Central de Ajuda para Empresas): fase de aprendizado, aprendizado limitado, edições significativas, boas práticas de orçamento, Advantage+.

**O que o Meta recomenda, resumido:**
- ~50 eventos de otimização por conjunto em 7 dias para sair do aprendizado;
- consolidar conjuntos;
- quanto mais conjuntos e anúncios, mais tempo em aprendizado;
- com orçamento na campanha, analise no nível da campanha e não fique pausando e despausando conjunto;
- públicos de tamanhos muito diferentes distorcem a distribuição de verba;
- alterações em lote, não uma a uma;
- a meta de desempenho espelha a meta de negócio, não a métrica mais fácil.

**Onde eu discordo da recomendação do Meta, e por quê.** O Meta recomenda Advantage+ posicionamentos, que inclui Audience Network. Eu corto Audience Network enquanto a conta valida. A recomendação dele pressupõe sinal de conversão limpo. Com sinal sujo (regra de pixel duplicada, evento disparando no lugar errado), posicionamento aberto amplifica o estrago: o algoritmo corre para o inventário mais barato e realimenta o erro. Depois que o rastreio estiver provado e o volume justificar, Advantage+ posicionamentos vira teste legítimo, com o breakdown por plataforma lido toda semana.

O mesmo vale para "não pause conjunto de baixa entrega": serve para conjunto que entrega pouco, não para conjunto que gasta sem resultado.

**Erros comuns da API:**

| erro | significado | saída |
|---|---|---|
| troca de evento bloqueada | não dá para trocar evento de conversão em conjunto publicado | criar conjunto novo ou ativar um pausado com o evento certo |
| idade máxima recusada | idade máxima abaixo de 65 com Advantage+ público | usar idade como sugestão ou desligar Advantage+ público |
| vídeo sem miniatura | anúncio de vídeo precisa de imagem de capa | anexar o criativo pelo Gerenciador |
| "Performance goal isn't available" | meta de otimização incompatível com o objetivo | usar uma das metas válidas que a resposta da criação lista |

**Caso que justifica o passo 7.** Numa conta de serviço financeiro, regras de pixel sobrepostas fizeram o Meta acreditar que conversão custava R$ 1,50. O algoritmo foi para o inventário mais barato e 99,98% da verba caiu em Audience Network, com CTR de 22%. O cliente via "164 conversões por dia" e nenhuma conversa real. O breakdown por plataforma teria mostrado isso no primeiro dia.

**Níveis de maturidade (P.R.E.V.E.R.):**

| nível | verba/dia | arquitetura |
|---|---|---|
| N1 Validação | até R$ 249 | campanha única, máximo 5 anúncios |
| N2 Tração | R$ 250 a 999 | Sandbox (teste, até 20%) + Escala (orçamento na campanha, 80%+) |
| N3 Escala | R$ 1.000+ | 10 a 15% em teste contínuo + 85 a 90% em Advantage+/aberto |

Cruzar R$ 250 ou R$ 1.000 por dia pede mudança de arquitetura. Nem antes da hora, nem depois por inércia.

Sobre o Sandbox: o texto do método começa a validação com orçamento por conjunto. Na minha prática, campanha nova começa com orçamento na campanha (ver Passo 3), e orçamento por conjunto fica para N2/N3 com criativos já validados.
