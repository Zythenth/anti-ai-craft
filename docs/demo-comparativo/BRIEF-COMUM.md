# Brief comum — fila de tradução

## Objetivo

Criar uma tela operacional estática para acompanhar um lote de capítulos processados
por um pipeline de tradução. A pessoa responsável precisa reconhecer rapidamente o
que terminou, o que está em andamento, o que exige decisão humana e qual é a próxima
ação segura para cada capítulo.

As duas implementações do comparativo devem partir deste mesmo brief e carregar
`dados.js` sem copiar, substituir ou complementar os registros. Os dados são fixtures
de demonstração e não representam obra, cliente ou execução real.

## Ambiente e enquadramento

- Superfície: aplicação operacional usada em desktop.
- Usuário principal: pessoa revisora que acompanha V1, V3, diffs e glossário.
- Viewport de captura: **1280 × 800 CSS px**, zoom de 100%.
- Idioma: português do Brasil.
- Execução: arquivos estáticos locais, sem servidor, build, biblioteca, fonte ou
  chamada de rede obrigatória.
- Estado inicial: exatamente o definido em `window.DEMO_TRADUCAO`.
- Toda mutação é simulada na interface; nenhuma ação deve editar capítulos ou chamar
  scripts reais.

## Conteúdo obrigatório

Exibir, sem alterar valores ou inventar métricas:

1. Nome da superfície, projeto, lote, horário de referência e rótulo “Dados de demonstração”.
2. Resumo do lote: quatro capítulos, 15.743 palavras, um capítulo pronto, um bloqueado,
   um em revisão e um na fila.
3. Identificação da execução do pipeline e informação de que chamadas são isoladas.
4. Os quatro capítulos de `dados.js`, cada um com:
   - ID, título e quantidade de palavras;
   - etapa/estado atual;
   - situação do glossário;
   - resumo operacional;
   - horário previsto;
   - próxima ação e ação de consulta.
5. Para `ch115`, comunicar os dois termos pendentes, que a execução foi interrompida
   antes de alterar arquivos e quais caminhos de recuperação estão disponíveis.
6. Uma explicação curta de que ações executadas nesta demonstração são apenas simuladas.

Nenhum registro pode ser omitido, duplicado ou receber estado diferente. O mesmo
conteúdo deve estar presente no DOM inicial das duas implementações, ainda que a
organização e a forma de acesso sejam diferentes.

## Tarefas e interações mínimas

As seguintes tarefas devem ser possíveis com mouse e teclado:

1. Pesquisar por ID ou título do capítulo e limpar a pesquisa.
2. Filtrar a fila por `Todos`, `Precisa de atenção`, `Em andamento` e `Prontos`.
3. Consultar os detalhes de qualquer capítulo.
4. Acionar a próxima ação de cada capítulo. O resultado deve ser somente uma mensagem
   simulada e não deve modificar os dados compartilhados.
5. No capítulo bloqueado, abrir as decisões de glossário e tentar novamente depois da
   confirmação simulada. A interface deve manter o contexto do capítulo.
6. Selecionar o capítulo pronto e simular a aplicação do diff em lote.

É aceitável que controles estejam sempre visíveis, agrupados, em menus ou em outra
estrutura, desde que todas as tarefas sejam completas e que a implementação registre
o resultado simulado.

## Estados mínimos

- Estado padrão com os quatro capítulos.
- Filtro com resultado e filtro sem resultado.
- Pesquisa sem correspondência, com forma explícita de limpar/recuperar.
- Item selecionado e indisponível quando a ação não se aplica.
- Confirmação simulada de ação.
- Falha de `ch115` com efeito atual e caminhos de recuperação.
- Mensagem de sucesso ou status após cada ação simulada.

## Acessibilidade básica

- Usar HTML semântico e uma ordem de leitura e foco coerente.
- Oferecer nome acessível a todos os controles; o nome deve incluir o texto visível
  quando houver texto visível.
- Tornar toda funcionalidade operável por teclado, sem `tabindex` positivo.
- Manter indicador de foco visível.
- Não comunicar etapa, falha, seleção ou disponibilidade somente por cor ou posição.
- Associar pesquisa a um rótulo persistente.
- Expor expansão, seleção, estado desabilitado e mensagens dinâmicas de forma
  programática quando aplicável.
- Anunciar resultados simulados em uma região de status sem mover o foco.
- Manter alvos interativos com pelo menos 24 × 24 CSS px.
- Respeitar `prefers-reduced-motion` se houver movimento.

## Limites da comparação

Este brief não prescreve layout, navegação, densidade, componentes, paleta,
tipografia, bordas, raio, ícones ou movimento. Cada implementação pode tomar suas
próprias decisões visuais e estruturais, mas deve preservar integralmente função,
dados, tarefas, estados, viewport e restrições acima.

Para a captura final, usar o mesmo navegador, tema, zoom, viewport e estado inicial.
Não usar textos, registros ou interações diferentes para favorecer uma versão.

## Critérios de aceite

- Abre diretamente por arquivo local e não produz erro de JavaScript.
- Carrega `dados.js` como única fonte dos registros.
- Renderiza os quatro IDs e os valores exatos do fixture.
- Implementa as seis tarefas mínimas sem efeito externo.
- Mantém os requisitos básicos de teclado, foco, nomes e comunicação de estado.
- Cabe no viewport de captura sem rolagem horizontal global.
- Declara qualquer requisito não exercitado, em vez de assumir que foi validado.
