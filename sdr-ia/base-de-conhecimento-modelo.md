# Base de conhecimento (modelo)

Preencha com os dados do seu negócio e cole no bloco `<knowledge_base>` do `prompt-sdr.md`. Se a sua plataforma aceita arquivo de conhecimento separado, suba este arquivo direto.

A SDR só pode afirmar o que está aqui. O que faltar, ela responde que vai confirmar com a equipe. Por isso vale escrever as respostas para as perguntas que mais chegam no WhatsApp, com as palavras que o cliente usa.

Os exemplos abaixo são de uma clínica fictícia de fisioterapia. Apague e troque pelos seus.

---

## 1. Serviços

Liste o que você vende, com o nome que o cliente usa (não só o nome técnico).

| Serviço | Para quem é | Duração / sessões | Observação |
|---|---|---|---|
| {{servico_1}} | {{publico}} | {{duracao}} | {{observacao}} |
| Exemplo: Fisioterapia para dor lombar | Quem sente dor nas costas há mais de 2 semanas | 10 sessões de 50 min | Começa sempre pela avaliação |
| Exemplo: Pilates clínico | Pós-tratamento ou prevenção | 2x por semana | Turmas de até 3 pessoas |

## 2. Primeiro passo (o que a SDR agenda)

- Nome: {{tipo_de_compromisso}} (ex.: avaliação)
- Duração: {{duracao}} (ex.: 60 min)
- Valor: {{valor}} (ex.: R$ 80, abatido se fechar o tratamento)
- O que acontece nela: {{descricao}} (ex.: conversa sobre o histórico, testes de movimento, plano por escrito)
- O que levar: {{o_que_levar}} (ex.: exames recentes, roupa confortável)

## 3. Preço

Diga o que a SDR pode e o que não pode informar.

- Pode informar: {{precos_liberados}} (ex.: valor da avaliação, valor da sessão avulsa)
- Não informa antes da avaliação: {{precos_bloqueados}} (ex.: pacote de tratamento, porque depende do caso)

## 4. Formas de pagamento

- {{forma_1}} (ex.: Pix)
- {{forma_2}} (ex.: cartão de crédito em até 6x)
- Convênio / reembolso: {{regra}} (ex.: não atende convênio, emite recibo para reembolso)

## 5. Diferenciais

Escreva o que é verdade e o cliente consegue conferir. Evite adjetivo solto.

- {{diferencial_1}} (ex.: o mesmo fisioterapeuta acompanha do começo ao fim)
- {{diferencial_2}} (ex.: horário às 7h e às 19h para quem trabalha)
- {{diferencial_3}} (ex.: estacionamento conveniado na rua da clínica)

## 6. Para quem é (e para quem não é)

- Atende: {{perfil_atendido}} (ex.: adultos e idosos com dor muscular ou articular)
- Não atende: {{perfil_fora}} (ex.: crianças, pós-operatório de coluna nas primeiras 6 semanas)
- O que fazer com quem está fora: {{encaminhamento}} (ex.: agradecer e indicar procurar um ortopedista)

## 7. O que o cliente quer resolver

Em uma ou duas frases por perfil, na voz do cliente. Isso ajuda a SDR a fazer a pergunta certa.

- {{perfil_1}}: "{{frase_do_cliente}}"
  Exemplo: quem tem dor lombar: "Quero conseguir trabalhar sentado o dia todo sem travar no fim da tarde."
- {{perfil_2}}: "{{frase_do_cliente}}"

## 8. Perguntas frequentes

| Pergunta do lead | Resposta da SDR (2 a 4 linhas) |
|---|---|
| {{pergunta}} | {{resposta}} |
| Exemplo: Precisa de pedido médico? | Não precisa. Se você tiver exames ou laudo, traga na avaliação que ajuda bastante. |
| Exemplo: Tem estacionamento? | Tem estacionamento conveniado na mesma rua, é só pedir o selo na recepção. |

## 9. Regras do negócio

- Antecedência mínima para agendar: {{regra}} (ex.: 2 horas)
- Política de falta e remarcação: {{regra}} (ex.: remarcar até 12h antes sem custo)
- Quem atende fora do horário: {{regra}} (ex.: ninguém; a SDR agenda e a equipe confirma no dia seguinte)
- Quando passar para um humano: {{regra}} (ex.: reclamação, pedido de reembolso, dúvida clínica específica)
