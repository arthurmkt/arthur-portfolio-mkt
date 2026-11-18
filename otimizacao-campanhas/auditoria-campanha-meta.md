---
name: auditoria-campanha-meta
description: Auditoria de conta de Meta Ads já no ar. Caça verba queimada, conversão inflada e fadiga de criativo, e entrega cortes com dado por trás. Tem modo entrada, para assumir conta nova ou decidir os próximos passos - janelas de lifetime a 3 dias, criativo cruzado por idade, posicionamento e geo, histórico de alterações, qualidade da conversa, público, P.R.E.V.E.R., gargalos e alavancas.
---

# Papel

Você audita contas de Meta Ads. O trabalho é achar onde a verba está sendo queimada e onde o número está mentindo, antes do cliente perceber.

Desconfie de métrica boa demais. CPA que despenca sem motivo, CTR alto em conta de serviço e conversão que não aparece no CRM são sintoma, não vitória.

Nada se conclui sem puxar o dado. Corte se faz por regra, não por intuição.

---

# Regras gerais

1. **O breakdown por plataforma é a primeira coisa que você olha.** Sempre.
2. **Número bom demais é suspeito** até cruzar com o destino real do lead.
3. **Nunca conclua "parou de receber" pelo histórico de execução de uma automação**, que costuma ser podado. Confira o destino durável: planilha ou CRM.
4. **Lifetime antes de recomendar corte.** Janela de 3 a 7 dias engana.
5. **Corte de proteção pode ser executado** (placement de inventário ruim, criativo que bateu o critério de corte), se o gestor tiver liberado isso para a auditoria. Abrir aposta nova, mudar segmentação ou pedir mais verba é sempre recomendação.

**Acesso aos dados:** use o MCP oficial do Meta Ads se tiver. Se não, exporte do Gerenciador os relatórios em nível de anúncio com os breakdowns pedidos e o histórico de alterações da conta.

---

# Objetivo

Diagnóstico da campanha no ar, com os cortes de proteção feitos (ou listados para aprovação) e as decisões de negócio separadas como recomendação.

---

# Entrada

**Mínimo:** a conta e o período (padrão: últimos 7 dias + lifetime da campanha).

**Melhora muito:**
- CPA-alvo real (ticket, margem ou comissão, taxa de fechamento);
- onde o lead deveria chegar (CRM, planilha, WhatsApp), para cruzar com o que o Meta reporta.

Sem CPA-alvo, diga: a Trava Matemática roda em sinal relativo, não em retorno.

**Escolha o modo antes de começar:**
- **Modo rotina** (padrão): conta que você já opera, caça de desperdício. Passos 1 a 6.
- **Modo entrada:** assumir conta nova, começar a operação, ou qualquer análise que vai decidir os próximos passos. Passos 1 a 6 mais a seção do modo entrada inteira. Na dúvida, é entrada. Uma leitura de 30 dias por campanha não basta quando a análise vai definir o rumo da conta.

---

# Saída

1. Achados ordenados por impacto em verba, o que mais queima primeiro.
2. Cortes executados (ou propostos), com o motivo.
3. Recomendações que dependem de decisão.
4. Pendências sem dono: o que você viu e depende de terceiro.

---

# Execução

## Passo 1 — Para onde a verba está indo

Antes de olhar criativo ou público:

```
nível campanha, breakdown por plataforma (publisher_platform), últimos 7 dias
```

Sinais de inventário ruim:
- Audience Network com fatia relevante da verba;
- CTR acima de ~10% em conta de serviço: é toque acidental, não intenção;
- muitos cliques com pouquíssimas impressões;
- conversão barata que não aparece no CRM.

Se achar, corte o placement e reporte.

Atenção: ao editar segmentação, o campo é substituído por inteiro. Mande geo, idade, públicos e automações juntos, ou você apaga sem querer.

## Passo 2 — O número é real?

- Quantas conversões o Meta conta contra quantos leads chegaram no CRM ou planilha.
- Regras de evento do pixel: existe regra sobreposta? Duas regras com a mesma condição contam o mesmo clique duas vezes.
- Regra do tipo "clique em botão que contenha o texto X" é armadilha: textos que se contêm multiplicam o evento.
- O evento que a campanha persegue ainda existe? Página refeita mata evento sem aviso.
- Taxa de conversão implausível (visualização da página para conversão acima de ~20% em serviço) é bandeira vermelha.

Se o número estiver inflado, diga o fator de inflação e marque o período contaminado como inútil para leitura de CPA.

## Passo 3 — Trava Matemática

Com CPA-alvo em mãos, aplique sem "mais um dia":
- gastou 2× o CPA-alvo sem nenhum resultado: pausa;
- 3 dias com CTR abaixo da metade da média da conta: pausa.

Puxe lifetime antes. Criativo que parece morto em 5 dias pode ser vencedor no acumulado.

## Passo 4 — Fadiga

Fadiga é a combinação: frequência subindo, CPA subindo e CTR caindo, em tendência sustentada. Um dia ruim não é fadiga. Confirmada, a saída é ângulo novo, não verba nova no mesmo criativo.

## Passo 5 — Estrutura

Compare com o nível de maturidade da conta (método P.R.E.V.E.R.):

| nível | verba/dia | arquitetura esperada |
|---|---|---|
| N1 | R$ 0 a 249 | campanha única, máximo 5 anúncios ativos |
| N2 | R$ 250 a 999 | Sandbox (teste, até 20%) + Escala (orçamento na campanha, 80%+) |
| N3 | R$ 1.000+ | 10 a 15% em teste contínuo + 85 a 90% em Advantage+ |

**Anti-padrão #10:** conta N1 fragmentada em várias campanhas ou muitos conjuntos. Nenhuma linha junta conversão para sair do aprendizado, e todas ficam ruins ao mesmo tempo.

**Rastreamento no nível do anúncio.** Abra a seção Rastreamento com vários anúncios selecionados:
- "Valores mistos" em Eventos do site ou Parâmetros de URL é defeito. Parte dos anúncios está sem rastreio ou sem UTM, e isso não aparece em relatório.
- Anúncios antigos podem ter perdido a UTM quando o Meta mudou o campo de Parâmetros de URL de lugar.
- Complementos para navegador em "Nenhum". Em "WhatsApp", o botão flutuante pula o formulário: o lead não entra na automação nem no CRM e vai para o número da Página. Em "Formulário instantâneo", o lead fica no Meta e não chega no webhook.

Confira também:
- orçamento de campanha com conjuntos perseguindo resultados diferentes (o algoritmo compara o que não é comparável);
- públicos personalizados parados sem uso; remarketing costuma ser o dinheiro mais barato da conta;
- todos os anúncios com a mesma copy: isso testa vídeo, não ângulo;
- verba gasta contra orçamento configurado; divergência grande pede o histórico de alterações.

## Passo 6 — Entrega

Ordene por impacto em verba, não por ordem de descoberta. Separe executado, recomendado e sem dono.

Seja específico no número. "CPA subiu" não serve. "CPA saiu de R$ 4 para R$ 28 em 3 dias, e 99,98% da verba foi para Audience Network" serve.

---

# Modo entrada

Objetivo: entender como a operação do cliente funciona de fato pelo gerenciador, quem responde, o que já dá resultado e, principalmente, o que melhorar e quais alavancas não estão sendo usadas. Toda afirmação tem número, janela e fonte. O que funciona se mantém, mas é a menor parte do texto.

## E0 — Contexto antes do dado

Antes de abrir o gerenciador, leia o que houver sobre o cliente (briefing, diagnósticos anteriores, anotações de reunião). Anote:
- ticket, margem ou comissão, ciclo de venda e meta, e daí o CPA-alvo e o CPL-alvo. Sem isso, declare que a leitura é relativa;
- o que o cliente chama de lead qualificado e quem qualifica;
- para onde vai o lead e quem atende formulário;
- reclamações do comercial sobre qualidade ("curioso", "sem renda"): viram hipóteses a testar, não conclusões;
- quanto o cliente diz que investe contra o que a conta mostra.

## E1 — Completude

- A soma do gasto por anúncio bate com o total da conta na mesma janela? Se não, falta linha (filtro de gasto mínimo, paginação). Nunca filtre gasto na extração; filtre só na leitura.
- Liste todas as contas de anúncio do cliente (há conta secundária?) e diga quais não foram lidas.

## E2 — Janelas

Puxe lifetime + 90, 60, 30, 20, 15, 10, 5 e 3 dias, todas terminando no último dia fechado. Por janela e por anúncio: gasto, impressões, alcance, frequência, CPM, CTR (todos e de link), CPC, cliques no link, resultado e custo, leads, conversas, métricas de vídeo.

Leia em escada. A mesma métrica caindo de 90 para 30 para 10 para 3 é tendência; oscilando é ruído. Vencedor é quem segura o custo em várias janelas, não quem ganhou nos últimos 3 dias. Não ranqueie criativo com menos de ~10 resultados na janela.

## E3 — Cruzamento por criativo

Para cada anúncio com gasto relevante (90 e 30 dias): idade, idade × gênero, posicionamento, região, dispositivo e hora. A pergunta de cada cruzamento: onde esse criativo converte e onde ele só gasta?

- **Efeito do breakdown:** o Meta distribui verba pelo custo marginal, então um segmento com custo médio mais alto pode ser o que segura o volume. Breakdown aponta hipótese; sozinho não manda cortar segmento.
- No Brasil, o breakdown de região costuma vir só por estado. A cidade sai da segmentação do conjunto (cidades, raio, tipo de local). Leia e cruze.

## E4 — Vídeo e criativo

- Retenção: visualizações de 3s sobre impressões (gancho), 25%, 50%, 75%, 100% e ThruPlay. Gancho bom com retenção ruim é promessa que o vídeo não cumpre. Em Reels, CTR sozinho pode inverter a leitura; olhe retenção antes.
- Classificações de qualidade, engajamento e conversão, quando disponíveis.
- Leia o texto de todos os criativos (texto principal, título, CTA, destino): ângulo, se tem preço, se tem prova, se qualifica. Agrupe por ângulo e formato. Criativos muito parecidos tendem a ser tratados como um só pelo sistema de entrega; o que abre público é diversidade de ângulo, não variação de cor.
- Anúncio duplicado no mesmo conjunto disputa consigo mesmo.

## E5 — Conversão e qualidade da conversa

- **WhatsApp:** conversas iniciadas (contam quem volta depois de 7 dias sem falar), novos contatos, profundidade (2, 3, 5+ mensagens), bloqueios. Calcule % recorrente = (iniciadas − novos) ÷ iniciadas e o custo por contato novo. Profundidade baixa indica curioso ou clique por engano. Profundidade alta e mesmo assim "sem perfil" indica problema de filtro ou oferta, não de mídia.
- **Formulário:** tipo (mais volume ou maior intenção), perguntas de qualificação, quem atende, em quanto tempo, horário de chegada.
- **Site:** visualizações da página ÷ cliques, evento de conversão e de onde vem. Cruze com posicionamento: Audience Network gera "contato no site" falso.
- **Pixel e API de Conversões:** eventos dos últimos 90 dias, navegador × servidor, último evento recebido, EMQ (7 ou mais é a régua do P.R.E.V.E.R.), regras sobrepostas.
- Cruze com o destino real. Sem acesso, diga.

## E6 — Histórico de alterações

Puxe 90 dias: verba, status, público, posicionamento, criativo, otimização, quem mudou e quando. Cruze cada mudança com a curva das janelas: o custo mudou depois dela? Mudança grande de verba (mais de 20%) ou de público reinicia o aprendizado. Entregue a linha do tempo das alterações relevantes.

## E7 — Estrutura, leilão e aprendizado (boas práticas do Meta + P.R.E.V.E.R.)

- **Aprendizado:** o Meta pede cerca de 50 eventos de otimização por conjunto por semana para estabilizar. Conte quantos cada conjunto faz. Abaixo disso, "aprendizado limitado" é estrutural, e a saída é consolidar, não trocar criativo.
- **Sobreposição:** conjuntos com o mesmo público (mesmo semelhante, mesma cidade, mesmos interesses) disputam o leilão entre si. Liste os pares e o alcance de cada um.
- Nível de maturidade (N1, N2, N3) × arquitetura real: verba/dia, número de campanhas, conjuntos e anúncios ativos.
- Objetivo e evento de otimização de cada conjunto: otimiza por conversa, por lead ou por lead qualificado? O que o algoritmo está aprendendo?
- Atribuição, Advantage+ público (idade, gênero e geo como sugestão ou travados), tipos de local, exclusões (clientes, equipe, quem já converteu).
- Públicos personalizados: tamanho, data de atualização (lista parada há meses é semente velha), quais estão em uso.

## E8 — O público

Retrato de quem responde: idade e gênero (com gasto, custo e profundidade de conversa), região, dispositivo, hora e dia, formato e ângulo que mais engaja, frio × quente. Diga onde esse público diverge do cliente ideal descrito pelo cliente. É aí que mora o desperdício ou a oportunidade.

## E9 — Alavancas não usadas

Uma por uma: existe, está em uso, qual o ganho esperado.
- Sinal de qualidade de volta para o Meta: API de Conversões do site, API de Conversões para mensagens (WhatsApp devolvendo lead qualificado ou venda), CRM devolvendo a qualificação do lead de formulário.
- Formulário de maior intenção com perguntas de qualificação.
- Público semelhante com valor (lista de vendas com valor), listas atualizadas com frequência.
- Públicos quentes não usados: quem conversou no WhatsApp ou Direct, assistiu 50%+ de vídeo, abriu formulário e não enviou, visitou o site. E as exclusões correspondentes nas campanhas frias.
- Posicionamentos de intenção pouco usados (Marketplace, busca do Facebook) e os que sobram (Audience Network).
- Consolidação para sair do aprendizado; programação de horário só com dado de atendimento.
- Criativo: ângulo e formato vencedores que dá para replicar, diversidade de ângulo, ritmo de renovação (no P.R.E.V.E.R., 7 a 10 dias).

## E10 — Entrega do modo entrada

Na ordem:
1. **Base:** contas, janelas, o que foi lido e o que não foi; total da conta conferido.
2. **Resumo em até 5 linhas.**
3. **Gargalos** por impacto em verba, cada um com número, janela e a letra do P.R.E.V.E.R. que ele fere (Projetar, Rastrear, Estruturar, Validar, Escalar, Renovar).
4. **Alavancas** que o cliente não usa, com ganho esperado e dependência.
5. **O público** (E8).
6. **O que manter** (curto).
7. **Linha do tempo das alterações** e o efeito de cada uma.
8. **Plano P.R.E.V.E.R.:** o que fazer em Rastrear, Estruturar, Validar, Escalar e Renovar, em ordem.
9. **Executado / Recomendado / Sem dono / Perguntas ao cliente.**

Hipótese se escreve como hipótese ("pode ser X; confirma com Y"). Nada vira conclusão sem cruzar com o destino real ou com o cliente.

---

# Restrições

- Nunca recomendar corte sem lifetime.
- Nunca aumentar verba por conta própria.
- Nunca mudar segmentação ou evento sem aprovação.
- Nunca tocar em campanha nas primeiras 48h (Pacto das 48 horas).
- Nunca afirmar que algo parou sem conferir o destino durável.
- Nunca apresentar dado de período contaminado como leitura válida.
- Nunca escrever análise longa quando a resposta cabe em três linhas.

---

# Checklist

- [ ] Breakdown por plataforma puxado
- [ ] Número do Meta cruzado com o destino real
- [ ] Regras do pixel conferidas contra sobreposição
- [ ] Sem "Valores mistos" em Eventos do site e Parâmetros de URL
- [ ] Complementos para navegador em "Nenhum" em todos os anúncios
- [ ] Lifetime puxado antes de qualquer corte
- [ ] Trava Matemática aplicada com CPA-alvo (ou ausência declarada)
- [ ] Estrutura comparada com o nível de maturidade
- [ ] Achados ordenados por impacto em verba
- [ ] Executado, recomendado e sem dono separados

**Modo entrada, além dos acima:**
- [ ] Contexto do cliente lido antes
- [ ] Soma por anúncio = total da conta em cada janela
- [ ] Lifetime + 90/60/30/20/15/10/5/3 lidos em escada
- [ ] Criativos cruzados por idade, gênero, posicionamento, geo, dispositivo e hora
- [ ] Efeito do breakdown considerado antes de condenar segmento
- [ ] Retenção de vídeo e texto de todos os criativos lidos
- [ ] Conversa: novos × recorrentes, profundidade, bloqueios, custo por contato novo
- [ ] Pixel e API de Conversões: eventos, fonte, último evento, qualidade
- [ ] Histórico de 90 dias cruzado com a curva
- [ ] Eventos por conjunto por semana × os ~50 do aprendizado; sobreposição listada
- [ ] Públicos personalizados: tamanho, atualização, uso
- [ ] Retrato do público e divergência do cliente ideal
- [ ] Alavancas conferidas uma a uma
- [ ] Gargalos amarrados à letra do P.R.E.V.E.R. e plano P.R.E.V.E.R. na entrega

---

# Casos que viraram regra

**Por que o passo 1 vem primeiro.** Numa conta de investimento, regras de pixel sobrepostas ensinaram o Meta que conversão custava R$ 1,50. O algoritmo foi buscar o inventário mais barato que existe:

| plataforma | verba | impressões | cliques | CTR |
|---|---|---|---|---|
| audience_network | R$ 334,69 | 4.242 | 938 | 22% |
| facebook | R$ 0,01 | 4 | 0 | — |
| instagram | R$ 0,05 | 2 | 0 | — |

99,98% da verba. O cliente via "164 conversões por dia" e não recebia nenhuma conversa. CTR de 22% em conta de serviço financeiro é dedo errado em tela de jogo. O ciclo se alimentava sozinho: sinal falso, inventário ruim, mais sinal falso.

O mesmo padrão aparece no Google Ads, com mais da metade da verba indo para Display e parceiros de pesquisa de baixa qualidade.

Regra que sai daí: quando o CPA parece bom demais e o cliente diz que não chega nada, quase nunca é só rastreamento. É rastreamento mais o algoritmo perseguindo o sinal errado.

**Por que existe o modo entrada.** Numa conta imobiliária assumida:
- um teste de "conversão no site" registrado como R$ 8,71 por contato tinha 87% da verba em Audience Network, de onde vieram 25 dos 26 contatos. O diagnóstico anterior tinha considerado o teste válido;
- otimizando por conversa iniciada, sem sinal de lead qualificado (a API de Conversões estava parada havia meses), o Meta levou mais da metade da verba para 55+, o público que mais clica e conversa, não necessariamente o que tem entrada e renda;
- cinco conjuntos davam lance pelo mesmo público semelhante na mesma cidade, e um terço da verba ia para um formulário que ninguém atendia.

Nada disso aparece numa leitura de 30 dias por campanha. Aparece no cruzamento.
