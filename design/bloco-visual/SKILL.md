---
name: bloco-visual
description: Monta ou atualiza o bloco visual de uma marca no Figma — a página "00 · Bloco visual" do arquivo "[Marca] — Criativos", com estilos de cor e degradê, estilos de texto, logo como componente, safe area, repertório, regras fixas e peças aprovadas, tudo derivado do sistema_visual.md da marca. É a régua da marca para compor peças no Figma; não é template de layout. Use quando pedirem "bloco visual", "régua da marca no Figma", "preparar o Figma do cliente", "kit da marca no Figma" ou /bloco-visual <marca>.
user-invocable: true
argument-hint: marca
---

# Bloco visual no Figma

**O bloco é a marca transformada em coisa utilizável no Figma**: estilos de cor e de texto, logo como componente, guia de safe area e as regras que valem acima da referência. Na hora de compor uma peça (à mão ou com outra skill de produção de criativos, se você tiver uma), aplique estilos e componentes daqui em vez de redigitar hex, fonte e logo.

**O bloco não é layout.** A composição de cada peça continua vindo da referência dela. Nada neste arquivo decide alinhamento, posição ou arco de carrossel. Um "template por cliente" engessa as peças e foi descartado de propósito.

**Requisitos:** o MCP oficial do Figma conectado (com permissão de escrita via `use_figma`) e, na pasta da marca, os arquivos descritos em "Antes de começar".

---

## Antes de começar

1. **Material da marca.** Pedir (ou ler da pasta do projeto) o arquivo de identidade `sistema_visual.md`, que é a fonte da verdade do bloco: paleta com hex e função, degradês, famílias tipográficas com pesos, regras de logo, formatos. Se existirem, ler também: um arquivo de vetos da marca, um de frases fixas/linha legal/CTA, exemplos de peças e o `figma.md` (se existir → **modo atualização**, no fim deste arquivo). Não existe `sistema_visual.md`? Montar um junto com a pessoa antes de abrir o Figma.
2. **Arquivos:** logos numa pasta `assets/logos/` (o que estiver em `evitar/` não entra), peças aprovadas em `assets/aprovados/`. Faltou → vira pendência no bloco, nunca suposição.
3. **Skills do Figma, nesta ordem:** `figma-create-new-file` antes de `create_new_file`; `figma-use` e `figma-generate-design` antes do primeiro `use_figma` (via `get_figma_skill` se o plugin não estiver instalado). Em todo `use_figma`, declarar essas skills como o MCP pedir.
4. **Orçamento de chamadas.** O MCP do Figma tem limite por dia e por minuto que depende do assento e do plano (o assento Dev do plano Professional, em out/2026, dava 200 por dia e 10 por minuto; assento Collab dá muito menos). `whoami` e `create_new_file` costumam ficar fora da conta. Montar em poucas chamadas grandes e dizer quantas chamadas a rodada gastou. Se uma chamada bater em limite, rodar `whoami` antes de concluir qualquer coisa: o assento pode ter mudado.
5. **Autochecagem embutida.** Toda chamada que monta ou corrige termina com a função de `scripts/figma_autochecagem.js`, colada no fim do script, devolvendo o resultado junto com os IDs. Ela verifica fonte ausente ou substituída, texto que pode cortar, nó que passa da moldura do pai, largura acima de 2160, imagem sem arquivo, moldura branca sobre cor, ênfase fora do trecho e copy diferente. O erro mecânico é pego dentro da própria chamada, sem rodada extra.

---

## Passo 1 — Arquivo e sessão

- `figma.md` existe → usar o `fileKey` dele.
- Não existe → perguntar se a marca já tem arquivo no Figma (pedir o link). Se não tiver: `create_new_file` com nome `[Marca] — Criativos`, `planKey` via `whoami`.
- `create_session` com o `fileKey` e repetir o `sessionId` em toda chamada.
- A primeira página vira `00 · Bloco visual`. Peças ficam em outras páginas (`AAAA-MM · <campanha>`).

## Passo 2 — Fontes (portão antes de qualquer estilo de texto)

1. `figma.listAvailableFontsAsync()` e procurar cada família do `sistema_visual.md`, com os estilos exatos (o nome do estilo varia: `"Semi Bold"` no Inter, `"SemiBold"` na Libre Franklin; nunca chutar).
2. **Família ausente → nunca trocar sozinho.** Montar uma página `Tipografia · candidatas` com **três provas 1080×1350 lado a lado** (headline de uma copy real da marca + palavra de ênfase no degradê da marca + apoio + corpo), recomendar uma com o porquê e esperar a escolha. Escolhida, apagar a página de provas.
3. **Conferir se a substituta tem itálico** (e os pesos que o sistema visual usa). Se a marca usa itálico como ênfase e a substituta não tem, dizer na hora: a ênfase vai ter que ficar só na cor.

Substituições que já funcionaram (reaproveitar quando a mesma família aparecer):

| Oficial | Substituta | Por quê |
|---|---|---|
| Franklin Gothic | Libre Franklin | releitura aberta da própria Franklin Gothic |
| Georgia | Gelasio | mesmas métricas da Georgia |
| Cheltenham | Frank Ruhl Libre | venceu 3 provas: proporção estreita e ar de manchete; **sem itálico** |

## Passo 3 — Estilos

- **Cor:** um estilo por cor da paleta, `<Marca>/Cor/<nome>`, sólido. Descrição curta da função.
- **Degradê:** `<Marca>/Degradê · <nome>`, forma fixa de 2 paradas. Transformações:
  - horizontal, esquerda → direita: `[[1,0,0],[0,1,0]]`
  - diagonal, sup. esq. → inf. dir.: `[[0.5,0.5,0],[-0.5,0.5,0.5]]`
  - vertical, cima → baixo: `[[0,1,0],[-1,0,1]]`
  - paradas de degradê levam `a` na cor; tinta sólida não.
- **Texto:** `<Marca>/T1 …`, `T2 …`, `T3 …` e, quando a marca tiver regra de botão, `<Marca>/CTA …`. O tamanho é **base** (o da peça sai da razão de escala medida na referência). Substituta → a descrição do estilo diz de qual fonte oficial ela é substituta e a data da decisão. Caixa alta de CTA é `textCase = "UPPER"`: a copy continua literal.
- Aplicar sempre pelos setters assíncronos: `setFillStyleIdAsync`, `setTextStyleIdAsync`, `setRangeFillStyleIdAsync`.

## Passo 4 — A página do bloco

Moldura de 2400 px de largura (depois do `resize`, devolver `primaryAxisSizingMode = 'AUTO'`, senão a altura trava), margem 120, fundo branco, anotações em **Inter** (é a "papelaria" do bloco, não a marca). Linhas horizontais nunca passam de 2160 px de largura útil: some as larguras antes de montar.

| Seção | Conteúdo |
|---|---|
| Cabeçalho | nome da marca, "régua da marca, não layout", fonte da verdade (`sistema_visual.md` + data) e "se divergirem, o .md vence e o bloco é refeito" |
| 01 · Cores | amostras com nome, hex e função; regras de uso de fundo (claro/escuro) |
| 02 · Degradês e ênfase | amostras dos degradês + a forma fixa + regras de ênfase da marca (ex.: vermelho × dourado, contraste medido) |
| 03 · Tipografia | substituição declarada (se houver) + regras + **uma amostra por estilo, com o estilo aplicado** |
| 04 · Logo | versões como componentes + regra de uso + situação dos arquivos (tamanho, o que falta) |
| 05 · Formato e safe areas | componente `<Marca>/Safe area <proporção>` (zonas de fora em vermelho 12%, área útil tracejada) + formatos de outras plataformas |
| 06 · Repertório | entra / sai |
| 07 · Regras fixas | o que vale acima da referência: pessoa real, vetos, frases fixas, linha legal, ajustes aprovados |
| 08 · Exemplares aprovados | as peças aprovadas + "o que estas peças mostram" (logo, ênfase, claro/escuro, medidas fora do padrão) |

**Pendência é cartão, nunca suposição:** fundo `#FFF8F0`, contorno vermelho tracejado, título `PENDENTE — …` dizendo exatamente o que falta e quem fornece.

**Contêineres de auto layout nascem com fundo branco.** Em qualquer contêiner que fique sobre cor ou foto, zerar `fills = []`.

## Passo 5 — Imagens e logo

- **Subida:** criar antes o retângulo do tamanho certo, `upload_assets` com `nodeIds` (ordem = ordem das URLs), e `curl -F "file=@<caminho>;type=image/jpeg"` **a partir de um caminho curto** (a pasta da marca; caminho longo de pasta temporária já falhou). Logo `FIT`; foto `FILL`.
- **Só PNG ou JPEG.** WebP entrou no arquivo mas saiu em branco no screenshot; converter com PIL antes.
- **Logo oficial → componente** com `figma.createComponentFromNode(retângulo)`. Nome `<Marca>/Logo · <versão> · <cor>`; descrição com tamanho do arquivo e limite de uso.
- **Símbolo sozinho** pode ser recortado do arquivo oficial (corte por linhas transparentes com PIL), sem redesenho. Declarar como recorte.
- **Versão de cor derivada (ex.: escura para papel claro) só com aprovação:** componente com dois retângulos. O primeiro é a máscara (`isMask = true`, `maskType = "ALPHA"`) preenchida com a **imagem do logo pelo `imageHash` do upload** (não copiar `fills` do componente oficial: depois do `createComponentFromNode` eles vêm vazios); o segundo é a cor, pelo estilo da paleta. Nome com `(derivada)`; descrição com "não é arquivo oficial da marca" e a data da aprovação.
- **Logo pequeno é pendência:** dizer até que largura ele serve sem borrar.
- **Conferir o componente de logo depois do `createComponentFromNode`:** ele pode nascer como **moldura com fundo branco sólido** em volta do retângulo da imagem, e some o logo branco. Ler `fills` do componente e do filho; se o filho tem a `IMAGE`, zerar `fills = []` do componente.
- **Marca sem paleta registrada:** extrair das variáveis do tema do site (`:root`) + área ocupada por cor, separar o que é da plataforma (WhatsApp, padrão do tema), medir contraste e **só criar estilo depois da aprovação**.

## Passo 6 — Conferir e registrar

1. **Autochecagem e print.** A chamada de montagem já devolve a autochecagem (ver "Antes de começar", item 5). Com `ok: false`, corrigir tudo numa chamada só, de novo com a autochecagem no fim. Com `ok: true`, tirar **um** print do frame dentro do próprio `use_figma` (`await frame.screenshot({ scale: 0.3 })`; o bloco tem cerca de 10.000 px de altura e o corte automático em 1024 px deixa tudo ilegível). O print serve para o que a autochecagem não vê: espaço, hierarquia, encostado e solto. Para ampliar uma região, tirar print do nó dela em escala maior.
2. **`figma.md`** na pasta da marca (modelo abaixo).
3. **`sistema_visual.md`:** registrar com data as decisões novas (substitutas de fonte, versões do logo, ajustes aprovados). O bloco nunca é a única cópia de uma decisão.
4. **Entrega:** link do arquivo, o que existe em cada seção, as pendências e quantas chamadas a rodada gastou.

### Modelo de `figma.md`

```markdown
# <Marca> — Figma

- **Arquivo:** [<Marca> — Criativos](<url>) · fileKey `<key>`
- **Bloco visual:** página `00 · Bloco visual`, frame `<Marca> — Bloco visual` (node `<id>`). Montado em <data> a partir de `sistema_visual.md` (<data do .md>).
- **Estilos de cor:** `<Marca>/Cor/*` · `<Marca>/Degradê · *`
- **Estilos de texto:** `<Marca>/T1 …` (substituta de … se houver) …
- **Componentes:** `<Marca>/Safe area <proporção>` · `<Marca>/Logo · …`
- **Peças:** uma página por mês ou campanha (`AAAA-MM · <campanha>`), um frame por peça

## Pendências do bloco
- …
```

### Esqueleto mínimo de `sistema_visual.md` (se a marca não tiver)

```markdown
# <Marca> — sistema visual (atualizado em <data>)
## Paleta
- <nome> #RRGGBB — função (fundo escuro, acento, texto...)
## Degradês
- <nome>: #RRGGBB → #RRGGBB, direção
## Tipografia
- Títulos: <família> <pesos> · Texto: <família> <pesos> · Ênfase: <itálico/cor/peso>
## Logo
- versões, cor sobre claro/escuro, tamanho mínimo, o que nunca fazer
## Formatos
- 1080×1350, 1080×1920 (safe area), 1080×1080...
## Regras fixas e vetos
- ...
```

---

## Modo atualização

Quando `figma.md` já existe:

- Comparar a data do `sistema_visual.md` com a data do bloco. Mudou → refazer **só as seções afetadas** (achar pelo nome `0N · …`), sem recriar o bloco.
- **Nunca duplicar estilo:** antes de criar, procurar pelo nome em `getLocalPaintStylesAsync()` / `getLocalTextStylesAsync()` e atualizar o existente.
- **Ajuste aprovado numa peça** (ex.: apoio colado na headline, CTA em caixa alta, logo no rodapé) → ler a peça ajustada no Figma, medir o que mudou e registrar em dois lugares: cartão "Ajustes aprovados" na seção 07 e `sistema_visual.md`.
- Material novo (logo melhor, peça aprovada) → trocar o preenchimento do mesmo componente/retângulo, para as peças que já usam o componente se atualizarem sozinhas.

## Nunca

- Decidir composição ou criar "template de peça" no bloco.
- Trocar família tipográfica sem a escolha de quem aprova.
- Redesenhar, distorcer ou recolorir o logo sem aprovação; desenhar logo que não foi fornecido.
- Preencher pendência com suposição (peça aprovada inventada, fonte "parecida", logo redesenhado).
- Entregar o bloco sem a autochecagem na última chamada de escrita, ou com `ok: false` sem dizer o que ficou.
