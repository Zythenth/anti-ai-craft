# Auditoria independente de equivalência

Data: 28 de julho de 2026  
Escopo: `baseline/` e `anti-ai/` congelados no estado identificado pelos hashes abaixo.  
Pergunta: as duas versões receberam e implementaram os mesmos dados, requisitos e
interações, sem vantagem estrutural que invalide a comparação?

## Veredito

**A comparação é válida para avaliar organização visual, acesso às ações, leitura de
estado e recuperação no viewport definido.** Não foi encontrada divergência bloqueante
de dados, função ou tarefa. As duas versões usam a mesma fixture congelada, apresentam
os mesmos quatro capítulos e implementam as seis tarefas mínimas sem chamadas externas.

As diferenças encontradas são decisões de interface permitidas pelo brief: a baseline
usa diálogos e confirmações; a outra versão mantém detalhes e recuperação junto à linha.
Isso muda o percurso e a hierarquia — justamente o objeto do comparativo — sem mudar o
resultado que cada pessoa pode alcançar.

O experimento não demonstra sozinho redução de tempo, erros ou carga cognitiva e não
deve ser apresentado como teste de usabilidade ou prova causal. Também é mais preciso
chamá-lo de **baseline versus versão orientada pela skill** do que de transformação
literal do mesmo código “antes/depois”.

## Estado auditado

| Arquivo | SHA-256 |
|---|---|
| `BRIEF-COMUM.md` | `856C3440C089C096D26013971787E568C8174DF8CDC4C767DA292DC2889CF945` |
| `dados.js` | `590BEC1FCC251DE4F588F43A8B5DC6F9712A2E24E64BFDF38B37CCC27F21C0E6` |
| `baseline/index.html` | `E3F04C84C095BC1E73CD8066CF5D4C533A3EBB47F87A379C4ECDBF53CB0C94FA` |
| `baseline/styles.css` | `97E37B4D26031CDAC59FEBCA390F9E06D22777BF60FB37E996463F6BAB742395` |
| `baseline/app.js` | `F12CA6A47BF50194FB7F6A8276C5EA59C1CB5AEF69005F68B180F8EC1D8A5C00` |
| `anti-ai/index.html` | `F1CD690A17562C90835F9DE4412DA9D649827E74857C1844981E93EB42AE9DAF` |
| `anti-ai/styles.css` | `DA45C068E92F3CC22A940B2E02968CD0EEA4B19E403F6778BB1D72F6AC855CB2` |
| `anti-ai/app.js` | `F46F4FD5411C4528D509747C3A4337EDCA3983021EDFC161DD56F3D17239AD99` |

Se qualquer hash mudar, esta auditoria deixa de cobrir o arquivo modificado.

## Equivalência dos dados

| Controle | Baseline | Versão orientada pela skill | Resultado |
|---|---|---|---|
| Fonte de registros | carrega `../dados.js` e lê `window.DEMO_TRADUCAO` | igual | equivalente |
| Registros | itera `fixture.chapters` | igual | equivalente |
| IDs | `ch114`, `ch115`, `ch116`, `ch117` | mesmos IDs | equivalente |
| Total | 4 capítulos e 15.743 palavras | mesmo resumo | equivalente |
| Distribuição | 1 pronto, 1 bloqueado, 1 em revisão, 1 na fila | igual | equivalente |
| Metadados | superfície, projeto, lote, data, hora, pipeline e aviso de fixture | igual | equivalente |
| `ch115` | dois termos, interrupção sem alteração e três caminhos de recuperação | igual | equivalente |
| Mutação da fixture | não encontrada | não encontrada | equivalente |
| Efeito externo | não foi encontrado `fetch`, XHR, WebSocket, URL remota, armazenamento ou execução de processo | igual | equivalente |

`dados.js` congela recursivamente o objeto. A execução isolada confirmou os quatro IDs,
o total de 15.743 palavras e `Object.isFrozen` no objeto, na coleção e nos capítulos.
Nenhuma versão mantém uma cópia concorrente dos registros no próprio JavaScript.

## Equivalência dos requisitos e interações

| Tarefa do brief | Baseline | Versão orientada pela skill | Resultado |
|---|---|---|---|
| Pesquisar por ID/título | `input[type=search]`, filtro de fixture e contador | mesmo mecanismo funcional | equivalente |
| Limpar e recuperar zero resultado | botões `Limpar` e `Mostrar todos` | `Limpar` e `Limpar busca e mostrar todos` | equivalente |
| Quatro filtros obrigatórios | gerados de `fixture.filters` | gerados da mesma fonte | equivalente |
| Consultar qualquer capítulo | diálogo nativo preenchido pelo registro | detalhe adjacente expandível | equivalente |
| Executar próxima ação simulada | confirmação em diálogo e mensagem local | ação direta e mensagem local | equivalente |
| Resolver `ch115` e tentar novamente | detalhe → confirmação do glossário → retry habilitado | detalhe inline → confirmação → retry habilitado | equivalente |
| Selecionar `ch114` e aplicar em lote | checkbox seletivo e botão de lote | checkbox seletivo e botão de lote | equivalente |
| Estado indisponível | checkboxes não aplicáveis desabilitados e nomeados | igual | equivalente |
| Feedback | região de status/toast; não altera a fixture | região de status; não altera a fixture | equivalente |

### Evidência de runtime fornecida pelo QA principal

No mesmo navegador e em `1280 × 800`, o QA principal informou que **ambas** passaram:

- busca com um resultado e limpeza;
- filtro `Precisa de atenção` com uma linha;
- abertura dos detalhes de `ch115`;
- seleção de `ch114` e aplicação simulada em lote;
- confirmação do glossário, habilitação e execução de nova tentativa;
- console sem warnings ou erros.

Essa evidência foi fornecida pelo agente principal; não foi repetida por este auditor.

## Acessibilidade mínima e condições de captura

Na inspeção estática, ambas usam rótulo persistente na busca, controles nativos,
tabela semântica, nomes acessíveis, estados desabilitados, feedback em `aria-live`,
foco visível e texto junto dos estados. Nenhuma depende somente de cor. Ambas incluem
tratamento para `prefers-reduced-motion`. A versão orientada pela skill acrescenta
detalhes como `aria-expanded` no fluxo inline e estilos para `forced-colors`; são
melhorias além do piso comum, não requisitos exclusivos concedidos a um braço.

Para a captura comparável, preservar em ambas:

- navegador, sistema, tema e escala idênticos;
- viewport de 1280 × 800 CSS px e zoom de 100%;
- topo da página e estado inicial, sem pesquisa, filtro, seleção ou detalhe aberto;
- fixture e hashes acima sem alteração;
- ausência de recorte que esconda conteúdo relevante de apenas uma versão.

## Divergências não bloqueantes

1. A baseline usa diálogo modal para consulta e confirmação; a outra versão expande o
   detalhe junto da linha e confirma ações comuns por status.
2. Na baseline, `Aplicar diff` individual e aplicação por seleção são percursos
   separados. Na outra versão, o botão individual de `ch114` depende da seleção. As
   duas continuam oferecendo a tarefa individual prevista e a tarefa em lote.
3. A baseline mantém o incidente de `ch115` também em uma seção persistente; a outra
   versão o revela no detalhe da própria linha. O conteúdo e a recuperação são os mesmos.
4. A baseline apresenta o resumo em seis métricas; a outra o apresenta numa linha
   textual. Os valores vêm da mesma fonte.
5. Ambas acrescentam o nome de interface “Cadência”, que não é um registro da fixture.
   Como o acréscimo é simétrico e não altera dado, tarefa ou estado, não favorece um braço.

Nenhuma dessas divergências invalida a comparação. Elas não devem ser “corrigidas” antes
da captura, pois representam as decisões que o comparativo pretende tornar visíveis.

## Verificações reproduzíveis

Executar no PowerShell a partir de `docs/demo-comparativo`:

```powershell
node --check .\dados.js
node --check .\baseline\app.js
node --check .\anti-ai\app.js

node -e "global.window={}; require('./dados.js'); const d=window.DEMO_TRADUCAO; console.log({ids:d.chapters.map(x=>x.id), words:d.chapters.reduce((n,x)=>n+x.words,0), frozen:Object.isFrozen(d)&&Object.isFrozen(d.chapters)&&d.chapters.every(Object.isFrozen)})"

rg -n --fixed-strings '<script src="../dados.js"></script>' .\baseline\index.html .\anti-ai\index.html
rg -n 'window\.DEMO_TRADUCAO|fixture\.chapters|fixture\.filters|fixture\.summary' .\baseline\app.js .\anti-ai\app.js
rg -n 'fetch\(|XMLHttpRequest|WebSocket|https?://|localStorage|sessionStorage|\.writeFile|exec\(|spawn\(' .\baseline .\anti-ai
rg -n ':focus-visible|prefers-reduced-motion|forced-colors|overflow-x' .\baseline\styles.css .\anti-ai\styles.css
```

Resultado desta execução: os três `node --check` retornaram código 0; o fixture
retornou os quatro IDs, 15.743 palavras e congelamento verdadeiro; os dois HTMLs
carregam a mesma fonte; a busca por efeitos externos não retornou ocorrências.

## Limites

- Este auditor não repetiu navegação por leitor de tela, zoom a 400%, text spacing ou
  forced colors.
- A inspeção estática e o QA de runtime sustentam equivalência funcional, não uma
  conclusão de preferência visual.
- Qualquer afirmação de “mais rápido”, “menos erros” ou “mais fácil” exige medição com
  pessoas e tarefas controladas; a captura isolada sustenta apenas diferenças observáveis.
