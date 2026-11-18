# SDR de IA base

Prompt de sistema para um agente que atende leads no WhatsApp, qualifica, trata objeção e agenda o primeiro atendimento (avaliação, consulta, diagnóstico, reunião). O objetivo dele é o lead aparecer no horário marcado.

## Arquivos

- `prompt-sdr.md`: o prompt, em blocos (papel, empresa, modelos de mensagem, filosofia consultiva, base de conhecimento, integração com CRM, regras de formato e fluxo, objeções, confirmação, protocolo de ferramentas, processo mental, formato de saída).
- `base-de-conhecimento-modelo.md`: o que a SDR pode afirmar sobre o negócio. Vem com exemplo de uma clínica fictícia.

## Como usar

1. Preencha a base de conhecimento com os dados reais do negócio.
2. No prompt, troque tudo que está entre `{{ }}`. Os campos `{{data_hora}}`, `{{dia_semana}}`, `{{saudacao}}` e `{{nome}}` são preenchidos pela sua automação a cada mensagem.
3. Cole a base no bloco `<knowledge_base>` (ou suba como arquivo, se a plataforma permitir).
4. Ligue as ferramentas de agenda que a sua automação oferece (consultar horário, criar, reagendar, cancelar) e descreva cada uma no `<tool_usage_protocol>`.
5. Teste com conversas de verdade antes de ligar para o tráfego: lead com pressa, lead que só quer preço, lead que some e volta pela automação do CRM.

Funciona em qualquer stack que aceite prompt de sistema e chamada de ferramenta (n8n, Make, plataformas de agente no WhatsApp, API direta do modelo). O bloco de CRM está escrito de forma genérica: ajuste os nomes das etapas aos do seu funil.

## O que esta versão não faz

É a base. Não tem memória de aprendizado entre conversas nem revisão automática antes de enviar. Vale olhar as conversas toda semana e ajustar a base de conhecimento e as objeções com o que aparecer.
