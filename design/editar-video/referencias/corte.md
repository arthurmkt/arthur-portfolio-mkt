# Corte: regra de seis, piscar, corte na ação, J e L cut

Base: pesquisa feita em 05/11/2026 (entrevistas e livro de Walter Murch via fontes que o citam, ajuda oficial do Adobe Premiere, guias da Frame.io, ITU-R BT.1359) mais medição local com ffmpeg 8.1.2.
Legenda: **[norma]** · **[oficial]** documentação do fabricante · **[prática]** editor reconhecido · **[medido]** · **[sem fonte]**.

Limite de sempre: eu meço tempo de plano, cortes por minuto e sincronia. **Emoção, história e ritmo, que pesam mais, são julgamento humano.**

## 1. Regra de seis (Murch, *In the Blink of an Eye*) [prática]

O corte ideal atende seis critérios ao mesmo tempo, em ordem de peso:

| # | Critério | Peso |
|---|---|---|
| 1 | Fiel à emoção do momento | 51% |
| 2 | Faz a história andar | 23% |
| 3 | Cai num momento ritmicamente certo | 10% |
| 4 | Respeita o rastro do olho (onde está a atenção no quadro) | 7% |
| 5 | Respeita o plano da tela (linha de 180°, direção na tela) | 5% |
| 6 | Respeita a continuidade do espaço 3D | 4% |

- Emoção sozinha pesa mais que as outras cinco juntas.
- Quando não dá para atender tudo, **abre-se mão de baixo para cima**: nunca sacrificar emoção antes de história, história antes de ritmo, e assim por diante. Acertar um critério de cima esconde falha nos de baixo; o contrário não acontece.
- Na prática: entre a tomada "limpa" e a tomada com a melhor atuação, fica a melhor atuação, mesmo com erro pequeno de continuidade.

## 2. O piscar

- O corte é uma "piscada": encerra uma ideia e abre a próxima. Cortar onde o pensamento termina. **[prática]**
- Cortar **1 a 2 quadros antes** de a pessoa piscar, nunca no quadro do piscar. Depois do piscar só para efeito de susto ou "olhar duas vezes". **[prática]**
- Só vale para quem está "em personagem". Entrevistado nervoso, gente lendo teleprompter e rosto gerado por IA piscam sem relação com o pensamento.
- Teste de repetição: tocar o trecho em tempo real 3 vezes e marcar o corte no sentimento. Se as 3 marcações caem no mesmo quadro, o ritmo foi achado. Se não, o ponto de corte ainda não existe ali.

## 3. Corte na ação

- O corte "casado na ação" (a mão começa o gesto no plano A e termina no B) é o jeito padrão de esconder o corte dentro do movimento. **[oficial, Adobe]**
- Murch não usa como regra automática: diz que ele não esconde tanto quanto se acha e tira o impacto de um corte forte. Usar quando a continuidade importa, não por reflexo. **[prática]**
- Erro mecânico típico: o gesto repete (quadros demais) ou pula (quadros de menos). Conferir passando quadro a quadro pelo corte e ajustar 1–3 quadros.

## 4. Ritmo: o que dá para medir

- Cortes por minuto = cortes ÷ (duração em s ÷ 60). Duração média de plano = duração ÷ (cortes + 1). `escopos.py` e a receita R12 detectam os cortes.
- Referência do livro, para longa-metragem americano: diálogo ~6 cortes/min, ação ~25 cortes/min. **Não é meta para vídeo curto de rede social**; nenhuma plataforma publica número de cortes por minuto.
- Detecção automática (`scdet`) erra: acusa corte em flash e chicote de câmera e perde corte entre planos parecidos. Conferir na folha de quadros.

## 5. J cut e L cut [oficial, Adobe]

- **J cut:** o áudio do próximo plano começa antes da imagem dele (antecipação, apresentar lugar ou pessoa pelo som).
- **L cut:** o áudio do plano que sai continua por baixo da imagem seguinte (reação, continuidade, narração sobre b-roll).
- Em vídeo de rede social com pessoa falando: cortar para outra imagem no meio da fala e manter a voz por baixo mostra mais em menos tempo. **[prática, Frame.io]**
- Duração do avanço/atraso: nenhuma fonte dá número. Na prática, de alguns quadros a ~1 s em diálogo. **[sem fonte]**
- J cut cuja graça é o som no primeiro 1–2 s não funciona em vídeo que começa mudo no feed.

`scripts/montar.py` monta seco, J e L a partir de uma lista JSON.

## 6. Áudio nas emendas

| Situação | Curva | Por quê |
|---|---|---|
| Material diferente (tomadas distintas) | potência constante: `acrossfade c1=qsin:c2=qsin` | a curva linear padrão do ffmpeg (`tri`) afunda ~3 dB no meio (medido: −21,07 → −24,03 dBFS RMS; `qsin` segurou −21,07) **[medido]** |
| Material coerente (mesma tomada, mesmo ruído de sala) | ganho constante: `tri` | potência constante incha até ~+3 dB e pode clipar |

- Buraco entre falas se preenche com **som ambiente da sala**, nunca com silêncio digital. Pedaço de ambiente com mais de ~10 quadros; loop curto vira pulsação. **[prática]**
- Clique na emenda: fade de poucos ms ou crossfade; evitar fade feito com keyframe de volume.
- Cortar diálogo em consoante, não em vogal: em vogal o timbre pula mesmo com nível igual.
- Reduzir ruído **depois** de preencher os buracos, senão a fala limpa e o ambiente cru ficam com ruído de fundo diferente.
- O `acrossfade` encurta o áudio pela duração D da transição: estender os trechos D/2 de cada lado e conferir as durações com ffprobe.

## 7. Limites que reprovam

- **Sincronia labial** de quem fala na câmera: dentro de +90 ms (som adiantado) e −185 ms (som atrasado); a pessoa começa a perceber em +45/−125 ms. — ITU-R BT.1359-1 **[norma]**. J/L cut mexe só no áudio de quem está fora da câmera.
- Transição sem sobra de mídia (quadro congelado ou repetido dentro do fade) reprova no controle de qualidade. **[oficial, Adobe]**
- Áudio e vídeo começam juntos e terminam com diferença menor que 1 quadro (33 ms a 30 fps). **[sem fonte, valor de trabalho]**

## 8. Sintoma → causa → correção

| Sintoma | Causa provável | Correção |
|---|---|---|
| Corte parece um tique, "algo no olho" | caiu no piscar | mover 1–2 quadros antes do piscar |
| Corte atrasado, "grudento" | depois do fim natural da frase | antecipar para o fim do pensamento |
| Corte tecnicamente perfeito mas cena sem vida | continuidade priorizada sobre atuação | trocar pela tomada com melhor atuação |
| O olho procura o assunto depois do corte | foco salta de um terço para o outro | reenquadrar para o foco entrar perto de onde saiu, ou assumir o salto |
| Personagens trocam de lado | linha de 180° cruzada sem plano de transição | plano neutro no eixo, ou movimento de câmera mostrando a travessia |
| Ruído de fundo liga e desliga a cada fala | silêncio digital entre falas | preencher com ambiente, crossfade nas emendas |
| Nível afunda no meio da transição | curva `tri` em material diferente | `qsin` |
| Boca fora de sincronia depois do J/L | áudio deslizado em vez de rolado | ressincronizar; fazer J/L só com edição de rolagem |
