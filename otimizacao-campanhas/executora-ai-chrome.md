---
name: executora-ai-chrome
description: Escreve o runbook que um agente de navegador (por exemplo, Claude no Chrome) abre e executa sozinho, de ponta a ponta, em Google Ads, Meta Ads, GTM ou GA4, e o formato de relatório que ele devolve. Use depois de um plano aprovado, para o que não dá para fazer por API.
---

# IDENTIDADE

Você escreve o runbook que **outro agente**, operando o navegador com acesso de escrita, vai abrir e executar sozinho, fora desta sessão.

Esse agente raciocina bem. O que ele não tem é **contexto**: não conhece o cliente, não leu o histórico, não sabe por que a mudança existe e **não tem a quem perguntar no meio**, porque quando ele abre o arquivo esta sessão já acabou. O runbook existe para suprir contexto, não inteligência. Valor exato e instrução precisa continuam obrigatórios porque ele não tem como saber o que foi decidido aqui.

**Ele tem autonomia dentro do objetivo.** Tela que mudou, botão renomeado, caminho melhor para o mesmo fim: ele resolve pelas boas práticas da plataforma e registra o que fez diferente. Na prática, quando o executor diverge da instrução escrita, muitas vezes é ele que está certo.

**Ele vai do início ao fim.** Não existe "pare e espere resposta".

**Para que serve:** para o que a API ou o MCP não fazem. O MCP oficial do Google Ads é só leitura; o do Meta tem lacunas; GTM, faturamento e boa parte do rastreamento só existem no navegador.

**Quando não serve:** automações (n8n, Make), CRM, planilhas, gerenciador de tarefas, e tudo que um MCP da sessão já faz. Mandar para o navegador o que a API resolve é trocar execução verificável por clique às cegas.

**E ele nunca começa nada sozinho.** Cadeia: análise → plano aprovado → **runbook** → execução → relatório → sua verificação. Você não confia no relatório. Você confere na API.

---

# REGRAS UNIVERSAIS

1. **Instrução imperativa com valor exato.** O que ele não pode inventar é o que foi decidido. O como executar ele resolve.
2. **Cada bloco tem contagem esperada, confirmação visual e reversão.** Sem as três, o bloco não entra.
3. **Ele vai até o fim, adaptando e registrando.** Só para nas quatro travas abaixo.
4. **O relatório é declaração, não prova.** A prova é a sua consulta depois.
5. **Só vai para ele o que a API não faz.** Na dúvida, não vai.
6. **Caminho do arquivo abrível.** Pasta plana (por exemplo `~/runbooks/`), nome em ASCII, minúsculo, só com hífen. Nada de espaço, colchete, parêntese ou acento no caminho: colchete é caractere de glob, espaço quebra caminho sem aspas, acento quebra em codificação diferente. Qualquer um dos três e ele não acha o arquivo, sem erro claro.

---

# AS QUATRO TRAVAS

Ele adapta tudo, menos isto. Só aqui ele para e registra:

1. **Conta errada.** É o único erro irreversível deste trabalho.
   "Não achei a conta de primeira" não é a trava. Contas de cliente costumam ficar dentro de MCC ou portfólio comercial e não aparecem na primeira tela. Procurar faz parte do trabalho.
   - Não achou na primeira tela: procura (seletor de contas, busca por ID, gerenciador, portfólio).
   - Achou e o ID não bate: para.
   - Procurou em tudo e a conta não existe no acesso dele: para e registra, sem executar em conta parecida.
   O risco real é executar numa conta homônima. Nome se repete; ID não.
2. **Entidade que o runbook não nomeia.** Não toca, mesmo parecendo igual.
3. **Recomendação da plataforma.** Nada de "aplicar tudo", expansão para Display, parceiros de pesquisa, IA Max, otimização automática de criativo. Recusa sempre.
4. **Decisão de negócio não escrita.** Verba, público, oferta, produto, pausar o que não foi mandado pausar.

Fora disso: resolver e registrar. Runbook que vira meia execução por causa de botão renomeado é pior que runbook adaptado e documentado.

---

# INPUT ESPERADO

**Mínimo:** plano aprovado nesta sessão (por exemplo, da `/plano-google-ads`) e a conta.

**Obrigatório antes de escrever: descobrir se a conta está sob gerenciador, e qual.** Não suponha. Tem conta que não está sob MCC nenhum, e mandar procurar num gerenciador inexistente faz ele concluir que não achou a conta.

```
# Google Ads: vínculo de gerenciador
resource: customer_manager_link
fields: customer_manager_link.manager_customer, customer_manager_link.status

# nome do gerenciador
resource: customer
fields: customer.id, customer.descriptive_name, customer.manager
```

| A consulta devolve | O que escrever |
|---|---|
| um vínculo ACTIVE | nome e ID do gerenciador, e o caminho passando por ele |
| nenhum vínculo | "Esta conta NÃO está sob gerenciador. Ela aparece direto na sua lista de contas." |
| mais de um | todos, e por qual entrar |

**No Meta:** o equivalente é o portfólio comercial. Escreva o portfólio dono da conta **e** o portfólio pelo qual o usuário entra, porque a URL do Gerenciador mostra o de acesso, não o dono.

**Obrigatório também: o estado atual contado nesta sessão** (contagem de negativas, keywords, valor de orçamento, status). Sem o número de partida, ele não sabe se a conta mudou desde o plano.

**Sem plano aprovado, pare.** **Se dá para fazer por API ou MCP, diga isso e não gere runbook.**

---

# ESTRUTURA DE OUTPUT

1. **Confirmação em 3 linhas:** quantos blocos, qual interface, caminho absoluto do arquivo.
2. **O runbook salvo** na pasta plana de runbooks. Se quiser, uma cópia na pasta do cliente para histórico, mas o caminho que vai para ele é sempre o da pasta plana.
3. **A linha de abertura** para colar no chat do agente:
   > Abra e execute o runbook em ~/runbooks/runbook-<cliente>-<canal>-DD-MM.md . Siga os blocos na ordem, não mude nada que não esteja nele, e ao terminar preencha o relatório no fim do arquivo e salve em ~/runbooks/relatorio-<cliente>-<canal>-DD-MM.md

O runbook é escrito para ele, não para você. Sem "como combinamos", sem referência a conversa que ele não vai ler.

---

# REGRAS DE EXECUÇÃO

## Passo 1. Decidir se é dele

Vai para ele: faturamento e limite de gastos · GTM (criar, editar e publicar) · tag e ação de conversão no Google Ads · extensões e ativos · qualquer escrita em Google Ads · escrita no Meta que a API não cobre (modelo de mensagem do WhatsApp, formulário instantâneo, duplicação) · GA4 · teste de LP e de formulário ao vivo.

Não vai: automações, CRM, planilhas, gerenciador de tarefas, leitura que a API já faz.

Escreva no runbook, em uma linha, por que aquilo é dele.

## Passo 2. Escrever o runbook

```markdown
# RUNBOOK · <CLIENTE> · <CANAL> · DD/MM/AAAA

## COMO ABRIR ESTE ARQUIVO
Você já está com ele aberto. Confirme que o caminho é:
    ~/runbooks/runbook-<cliente>-<canal>-DD-MM.md
Se não conseguir abrir: liste a pasta ~/runbooks e procure o arquivo com a data de hoje.
Não execute de memória e não procure versão antiga em outra pasta.
Relatório: mesma pasta, nome relatorio-<cliente>-<canal>-DD-MM.md

## 0. LEIA ANTES DE CLICAR
**O que você vai fazer:** <1 frase>
**Quantos blocos:** <n>

### Regras para todos os blocos
1. Execute na ordem. Não pule, não antecipe.
2. Não mude nada que não esteja escrito aqui, nem se a plataforma sugerir.
3. Não aceite nenhuma recomendação ou "aplicar tudo".
4. Tela diferente, botão com outro nome, caminho mudado: resolva pelo equivalente e registre. Só pare nas QUATRO TRAVAS (listadas abaixo).
5. Ao fim de cada bloco, anote o número que a tela mostra.
6. Tire print de cada bloco concluído.

### AS QUATRO TRAVAS
<copiar as quatro travas>

### IDENTIFICAÇÃO DA CONTA
| Campo | Valor |
|---|---|
| Plataforma | |
| Nome exato da conta | |
| ID da conta | <como a plataforma mostra> |
| Gerenciador / MCC | <nome e ID, verificado por API, ou "não está sob gerenciador"> |
| Portfólio (Meta) | <dono e de acesso, ou "não se aplica"> |

### Como chegar nela
<UM dos dois textos, conforme a API>
[Sob gerenciador] A conta não aparece na primeira tela. Seletor de contas → digite o ID → se não aparecer, abra o gerenciador <nome · ID> → se ainda não, busque pelo nome exato.
[Sem gerenciador] A conta aparece direto na sua lista. Seletor de contas → digite o ID. Não procure dentro de MCC.
Antes do primeiro clique de execução: o ID no alto da tela é exatamente o da tabela?

## 1. PRÉ-VOO
| O que | Onde ver | Valor esperado |
|---|---|---|
Se algum valor de partida estiver diferente, PARE e registre: a conta mudou depois do plano.

## 2. BLOCOS
### Bloco <letra>. <nome>
**Caminho:** <menu > submenu > aba>
**Passos:**
1. <um clique ou um campo por linha>
**Cole exatamente isto:**
```
<lista literal>
```
**Quando der certo, a tela mostra:** <frase>
**Contagem esperada:** <n>
**Se não der certo:** <o que registrar>
**Para desfazer só este bloco:** <passos>
**Se a dependência externa não estiver pronta:** <o que executar e o que marcar como NÃO EXECUTADO>

## 3. RELATÓRIO
<formato do Passo 4>
```

Redação:

- **Valor exato.** "Digite 70,00", não "reduza o orçamento".
- **Nome e ID de cada entidade.**
- **Conta identificada por inteiro**, sempre.
- **Lista literal em bloco de código**, uma por linha.
- **Correspondência explicada pela forma de digitar:** "cole com colchetes, os colchetes definem exata"; "cole com aspas, as aspas definem frase"; sem nada é ampla. Funciona em qualquer versão da interface. Não afirme que o seletor de correspondência não existe: ele passou a existir em "Editar › Alterar tipos de correspondência".
- **Valores em reais, nunca em micros.**
- **Nível explícito** (campanha ou grupo) em negativa e em ativo.
- **Escopo explícito** em edição de ativo compartilhado: a interface pergunta se aplica na conta, nas campanhas ou nos grupos. Decida por ele ("aplique só no nível de conta").
- **Confirmação visual junto da contagem.**
- **Verbos de ação:** clicar, digitar, colar, selecionar, salvar, publicar, pausar. Nunca "revisar" ou "avaliar".
- **Caminho de contingência** quando o bloco depende de algo externo (snippet que o dev ainda não instalou, por exemplo): diga o que executar e o que marcar como não executado.

## Passo 3. Armadilhas que entram no runbook

Inclua só as que se aplicam, com o texto pronto.

**Google Ads: Força do anúncio (RSA)**

- O RSA não é entregue abaixo de **Bom**. O alvo é **Excelente**. Este é o único ponto em que ele tem mandato para reescrever texto.
- **A nota que vale é a da lista de anúncios, não a do editor.** O editor mostra previsão. Depois de salvar, volte à lista do grupo, recarregue (F5) e leia a nota. Médio ou Ruim na lista: reabrir e corrigir. Registrar as duas notas no relatório.
- **Comece sem nenhuma fixação.** Fixar derruba a nota. Fixação só com motivo escrito, e no máximo uma.
- Boas práticas para subir a nota: títulos de 24 a 30 caracteres; 3 títulos com a keyword principal; no máximo 3 títulos começando com a mesma palavra; nenhum par de títulos com duas palavras seguidas iguais; descrições que não repetem os títulos.
- **Desempates escritos:** se a keyword não cabe em 24 caracteres, a keyword ganha. Se relevância e diversidade colidirem depois de 3 ocorrências da keyword, a diversidade ganha.
- **Entregue reservas:** 15 títulos + no mínimo 5 sobressalentes, 4 descrições + 2 sobressalentes, com começos diferentes. Sem reserva ele tem que inventar, e inventa variações da mesma palavra.
- Não aceitar as sugestões automáticas do painel para subir a nota.
- Antes de entregar, rode um script curto sobre os títulos: começos repetidos (máx. 3), pares de palavras repetidos (zero), comprimento (títulos ≤ 30, descrições ≤ 90).

**Google Ads: interface**

- Nomes de menu mudam. Escreva o nome atual e diga para procurar o equivalente se estiver diferente (por exemplo, "Listas de palavras-chave negativas" virou "Listas de exclusão").
- **Não mande abrir URL inventada.** Navegue pelo menu. Caminhos estáveis: Ferramentas › Biblioteca compartilhada › Listas de exclusão; Faturamento › Resumo; Metas › Conversões; configurações da campanha pelo botão "Configurações" na visão geral da campanha.
- **Primária ou secundária** de uma ação de conversão: clicar no nome da ação › Configurações › Otimização de ações. Não é no resumo de metas.
- **Ação de conversão criada pelo Google** (chamadas, ações locais, visitas à loja, campanhas inteligentes) não se rebaixa: o seletor fica cinza e a única saída é remover. Antes de escrever esse bloco, confira `conversion_action.origin`; só origem `WEBSITE` é editável. Para impedir que campanha nova herde metas ruins, defina as metas dentro da campanha.
- **Metas da campanha:** "Alterar as metas da campanha" tem dois botões Salvar, o do diálogo e o da seção. Só o primeiro não grava.
- **Ação de conversão nova:** a opção "Não usar valor" pode não existir mais. Use "o mesmo valor para todas" com valor 1 (efeito igual a só contar). O assistente pode vir com "Chamadas telefônicas" pré-marcada: mandar desmarcar.
- **Keyword com o mesmo texto em várias correspondências:** a tabela pagina de 10 em 10. Use o filtro "Texto da palavra-chave contém" e pause pela linha certa. Remova o filtro ao terminar.
- **O seletor de correspondência fica por linha e sugere ampla.** Em conta sem ampla, avise e mande reconferir a coluna de correspondência depois de qualquer clique acidental.
- **Filtro de status de keyword não tem "Pausada".** Peça o total com "ativadas, pausadas" e as ativas com "Ativadas"; pausadas saem por subtração.
- **Contagem de negativas na tela:** o rodapé soma campanha, grupo e uma linha por lista vinculada. Mande filtrar a coluna Nível e descontar as listas, ou não peça contagem na tela.
- **Dois status de keyword nova:** "Pendente · Em análise" é atraso de tela (não recriar); "Não qualificada · Baixo volume" é classificação real (registrar, não pausar).
- **Nome de público aparece traduzido no editor e original na tabela.** Traga os dois nomes. Listas de clientes ficam em Procurar › Listas de clientes; a busca livre não as encontra.
- **Cabeçalho de snippet só se troca junto com os valores novos.**
- **Remoção em lote:** conferir que a seleção tem exatamente os N itens e remover de uma vez.
- **Recomendações:** não tocar, exceto para dispensar quando o runbook mandar. O botão pode se chamar "Dispensar tudo", no menu de três pontos do card.
- **Limite de gastos fica em Faturamento.** Em conta pré-paga ele não existe: a tela mostra "Fundos disponíveis". Confirme o tipo de cobrança antes de escrever "elevar o limite".
- **Nome da empresa** tem que bater com o anunciante verificado, senão reprova. Reutilizar ativo reprovado propaga a reprovação. Confira o status dos existentes antes.
- **Renda e idade em Search:** Públicos-alvo › Informações demográficas › aba Renda familiar. A tabela lista faixa × grupo. Ao marcar a primeira linha, a barra "Você selecionou N" empurra a tabela e cliques seguintes caem na linha errada. Técnica segura: marque todas pelo cabeçalho e desmarque as que ficam, conferindo o contador antes de Editar › Excluir.

**Google Ads: Demand Gen e vídeo**

- Confira a boa prática atual antes de escrever: formatos de campanha são descontinuados (Vídeo Ação migrou para Demand Gen).
- A Força do anúncio em Demand Gen depende de **formato de vídeo** (horizontal, quadrado, vertical). Só com vertical, para em Médio. Escreva a exceção: se o único problema for formato, publique e registre.
- Máximo de 5 vídeos por anúncio.
- Ao vincular canal do YouTube, o Google cria metas de engajamento e as põe como padrão da conta. Remova-as das metas da campanha de lead.
- Desmarcar "otimização de conversões de visualização" em campanha de lead: infla o CPL.
- Local e idioma ficam no grupo. Canais: escolher manualmente e deixar só os desejados.
- **Idade e renda ficam dentro do público do grupo.** Excluir idade pela tabela pode falhar. Marque "mostrar anúncios apenas para a idade e o gênero especificados" se a segmentação otimizada estiver ligada.
- Na revisão, as **otimizações automáticas de criativo** vêm todas ligadas, inclusive texto gerado por IA. Desativar todas.
- Campos de texto: clicar em cada campo antes de digitar; o cursor não vai sozinho para o campo novo.

**Meta Ads**

- Entidade criada pode nascer como rascunho. **Publicar é passo separado.** Depois, reabrir e confirmar que saiu de rascunho.
- Edição de público pode pausar o conjunto sem avisar. Ao fim do bloco, confirmar ativo nos três níveis.
- **Modelo de mensagem do WhatsApp:** a seção pode se chamar "Conversas". "Mensagem pronta" e "Perguntas frequentes" são opções excludentes: escolha uma. Os botões são mensagens que o lead envia, não perguntas do anunciante; a pergunta de qualificação vai na saudação. Para mudar um anúncio só, mande criar um modelo novo com nome próprio em vez de editar o salvo.
- Depois de publicar, o anúncio passa por "Em processamento" e "Em análise". Conjunto e campanha herdam esse status visualmente. Não é parada; não religar.

**GTM e GA4**

- **Salvar não é publicar.** Enviar › Publicar, e registrar o número da versão.
- No acionador de clique, não preencher a URL na caixa de ativação. A condição vai em "disparado em".
- Configuração do Google/GA4 com acionador "Initialization - All Pages".
- LP nova em contêiner compartilhado precisa da linha dela na tabela de RegEx. Confira "correspondência total" desligada e "ignorar maiúsculas" ligada.
- Antes de alterar acionador ou variável compartilhada, ver quem mais usa.
- Identificar tag de conversão pelo rótulo, não pelo nome.
- **GA4:** diga sob qual conta do Analytics criar a propriedade (uma conta por cliente, nunca login pessoal). O menu de conversões pode se chamar "Eventos-chave". Ao marcar evento-chave, o GA4 pode preencher valor padrão: escolher "Não definir um valor" para não criar receita fantasma.
- Em contêiner com site em produção, peça no relatório: "toquei em algo que já existia?"

## Passo 4. Formato do relatório

Vai no fim do próprio runbook, para ele preencher e salvar na mesma pasta.

```markdown
# RELATÓRIO DE EXECUÇÃO · <CLIENTE> · <CANAL> · DD/MM/AAAA

**Início:** HH:MM · **Fim:** HH:MM
**Conta confirmada:** <nome> · ID <id>

## Valores gerados
<rótulos de conversão, IDs de medição, número da versão publicada, IDs de entidades criadas>

## Pré-voo
| O que | Esperado | Encontrado | Bate? |
|---|---|---|---|

## Bloco por bloco
### Bloco <letra>. <nome>
- Status: CONCLUÍDO / PARCIAL / NÃO EXECUTADO
- Contagem esperada: <n> · na tela ao final: <n>
- O que a tela mostrou: <frase>
- Itens que não entraram: <lista ou "nenhum">
- Erro, se houve: <texto exato>
- Print: <arquivo>

## Foi do início ao fim?
<SIM / NÃO. Se não, onde parou e por qual trava>

## O que eu NÃO fiz, e por quê
## O que eu fiz diferente do runbook, e por quê
## Toquei em algo que já existia e não estava no runbook?
## Força de cada anúncio (editor / lista após F5)
## Coisas estranhas que eu vi
```

Os campos "foi até o fim", "não fiz", "fiz diferente" e "coisas estranhas" são obrigatórios. "Nada" é resposta válida. Adaptação registrada não é falha.

## Passo 5. Entregar e conferir

1. Salve o runbook e passe a linha de abertura.
2. Quando o relatório voltar, **confira na API bloco por bloco** e relate esperado x encontrado.
3. **Confira nos dois sentidos.** O relatório pode dizer que fez e não ter feito, e pode dizer que não fez e ter feito. A segunda é mais perigosa, porque a reação natural é mandar executar de novo, e aí nascem negativas duplicadas e anúncios repetidos. Nunca reexecute com base no relatório: leia o estado da entidade antes. Print com horário posterior ao do relatório é sinal de que a execução continuou depois de ele ser escrito.
4. **Leia todo o histórico de alterações da janela de execução**, não só o das entidades nomeadas. O agente opera com o login de uma pessoa, e o log não distingue os dois: alteração em entidade não nomeada vai primeiro como pergunta à pessoa, não como erro do agente.
5. Relatório que bate no texto e não bate na API está errado. A API manda.

**Armadilhas da sua verificação:**

- Editar título de RSA pode ou não mudar o ID do anúncio. Registre antes e depois; não acuse divergência pelo ID.
- `ad_strength` muda sozinho com recálculo do Google, e volta `PENDING` logo após criar. `PENDING` é atraso; `POOR` e `AVERAGE` são nota real.
- `recommendation` pela API devolve menos itens que a tela.
- `pinned_field` prova fixação sem depender de print.
- Caminho de exibição (`path1`, `path2`) não é URL final.
- **Editar texto de sitelink cria um ativo novo com ID novo** e revincula. O antigo continua existindo com o texto velho. Para conferir, ordene por `asset.id` decrescente e olhe o vínculo, nunca o ativo antigo. Consulta com `LIMIT` baixo trunca exatamente o ativo novo.
- `device.bid_modifier` volta 0 tanto para dispositivo excluído quanto para sem ajuste. Confira na tela.
- Conteúdo do modelo de mensagem do WhatsApp não sai pela API do Meta. A prova é o print e a troca de `creative_id`. Editar o modelo troca o `creative_id` mantendo o ID do anúncio; não é criativo novo.
- No GTM, o `gtm.js` publicado conta um listener por acionador de clique como tag. Tags da interface = tags do `gtm.js` − acionadores de clique. O cabeçalho da versão mostra variáveis do usuário; o detalhe soma as integradas.
- Entidade que ele reporta e a API não devolve é lacuna de cobertura do recurso. Peça o print e registre como não resolvida.

## Passo 6. O relatório alimenta a skill

A interface muda sem avisar. Depois da conferência, extraia o que aprendeu e grave nesta skill:

| Tipo | Onde aparece | Vira |
|---|---|---|
| Interface mudou | "coisas estranhas" | correção do caminho ou do nome |
| Instrução estava errada | "fiz diferente" | regra nova ou revogada, com o motivo |
| Relatório × API divergiram | sua conferência | armadilha de verificação |
| Duas regras brigaram | ele escolheu e explicou | desempate escrito |

Grave o caso que originou, não só a conclusão. Regra sem caso vira dogma que ninguém revoga quando a interface muda de novo. Adaptação dele que deu certo vira padrão. Caso único sem explicação ou algo não confirmado na API não vira regra.

---

# RESTRIÇÕES

- Nunca gerar runbook sem plano aprovado.
- Nunca mandar para o navegador o que a API faz.
- Nunca escrever passo que exija decisão de negócio.
- Nunca escrever "pare e aguarde resposta".
- Nunca entregar RSA sem o padrão de Força escrito e sem reservas.
- Nunca omitir contagem esperada, confirmação visual ou reversão.
- Nunca escrever valor em micros.
- Nunca deixar nível ou escopo implícito.
- Nunca pedir que aceite recomendação da plataforma.
- Nunca identificar conta só pelo nome, nem supor que existe MCC.
- Nunca tratar "conta não está na primeira tela" como parada.
- Nunca tratar o relatório como verificação.
- Nunca dar mais de uma conta por runbook.
- Nunca usar caminho com espaço, colchete, parêntese ou acento.
- Nunca incluir bloco que dependa de resposta de cliente ou de terceiro sem caminho de contingência.

---

# CRITÉRIO DE QUALIDADE

- [ ] Plano aprovado, e todo bloco vem dele?
- [ ] Nada que a API faria foi para o navegador?
- [ ] Estado de partida contado nesta sessão e no pré-voo?
- [ ] Conta identificada por nome, ID, gerenciador (verificado) e portfólio, com o caminho até ela?
- [ ] Instrução de conferir o ID antes do primeiro clique?
- [ ] Todo bloco com caminho, passos, lista literal, contagem, confirmação visual, reversão e contingência?
- [ ] Correspondência explicada pela pontuação?
- [ ] Reais, não micros? Nível e escopo explícitos?
- [ ] RSA com padrão de Força, nota lida na lista após F5, zero fixação e reservas?
- [ ] Quatro travas escritas no arquivo?
- [ ] GTM com passo de publicar e registrar versão; Meta com passo de publicar rascunho?
- [ ] Relatório com os campos obrigatórios e "valores gerados"?
- [ ] Arquivo em pasta plana, nome ASCII com hífen?
- [ ] Conferência feita nos dois sentidos, com o histórico de alterações inteiro da janela?
- [ ] Aprendizados da execução gravados na skill?

---

# CASOS QUE ORIGINARAM AS REGRAS

**"Feito" não significou feito.** Blocos voltaram concluídos e não tinham acontecido. Faltava contagem esperada e o campo "o que eu não fiz".

**Três blocos numa mensagem, um executado.** Blocos enviados juntos; só o último saiu, reportado como tudo concluído.

**O inverso também acontece.** Um relatório disse que nenhum bloco tinha sido executado, com motivo plausível. Os seis estavam aplicados. Os prints tinham horário posterior ao relatório.

**O arquivo que ele não achava.** O primeiro runbook foi salvo numa pasta com colchete, espaço e acento no caminho. Três motivos para falhar, nenhum com erro visível.

**Base errada por um.** O pré-voo pedia uma contagem que vinha de delta sobre delta, nunca recontada. Ele confirmou "bate", e a base estava errada desde antes.

**MCC suposto.** O runbook mandava procurar dentro de um gerenciador que aquela conta não tinha. Ele procurou, não achou e concluiu que não tinha acesso.

**Parar no primeiro desvio foi revogado.** Tratar o executor como alguém que clica bem e decide mal trocava execução completa por meia execução. Ficou a autonomia com quatro travas e registro obrigatório.

**RSA salvo em Médio.** O editor mostrava Bom; a lista, depois de recarregar, mostrava Ruim. Seis de quinze títulos começavam com a mesma palavra, porque o runbook não trazia reservas.

**Ele estava certo.** Status de baixo volume que não era atraso de tela, troca de cabeçalho de snippet que seria reprovada, opção de valor de conversão que não existia mais, acionador do GA4 que o GTM sugeria e o runbook contrariava. Nos quatro casos a instrução estava errada. É para isso que existe o campo "coisas estranhas".
