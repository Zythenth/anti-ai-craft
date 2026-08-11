# Contrato de direção — Cadência

## Escopo e fontes de verdade

- Superfície: operação local de uma fila de tradução.
- Mandato: criar uma implementação estática isolada, sem identidade anterior a preservar.
- Fontes lidas: `README.md`; `docs/demo-comparativo/BRIEF-COMUM.md`; `docs/demo-comparativo/dados.js`; skill instalada `anti-ai-design` 0.4.0 e suas referências `design-principles.md`, `design-antipatterns.md`, `accessibility-baseline.md`, `direction-contract.md` e `review-workflow.md`.
- Fonte autoritativa dos registros: somente `window.DEMO_TRADUCAO`, carregada de `../dados.js`.

## Contrato

1. **Tese:** apresentar o lote como uma pauta operacional compacta, em que estado, impedimento e ação estão alinhados na mesma linha de leitura.
2. **Modo e tarefa dominante:** operar; localizar um capítulo, reconhecer sua situação e executar a próxima ação segura.
3. **Primeiro viewport:** em 1280 × 800, o cabeçalho identifica ambiente e lote; o resumo comprova a composição da fila; busca, filtros e as quatro linhas ficam imediatamente alcançáveis.
4. **Caminho principal:** ler resumo → localizar ou filtrar → reconhecer estado → consultar contexto → executar uma ação simulada e receber confirmação sem perda de foco.
5. **Estrutura:** cabeçalho mínimo, contexto do lote, faixa única de resumo/execução, ferramentas e tabela. Detalhes aparecem junto da linha de origem.
6. **Cor e tipo:** verde profundo estrutura o ambiente; papel claro sustenta leitura; vermelho é reservado ao bloqueio/ação; âmbar, verde e cinza identificam outros estados sempre acompanhados de texto e símbolo. Sans-serif conduz operação, serif aparece somente no título e mono somente em IDs, horários e pipeline.
7. **Assinatura:** códigos de capítulo funcionam como uma margem de pauta, enquanto a marca de cadência usa três batidas contidas no cabeçalho.
8. **Default rejeitado:** não usar painel de cartões/KPIs, hero promocional, menus de reticências ou ações importantes escondidas; os dados pedem comparação por linha e ações diretas.
9. **Risco principal:** a densidade da tabela perder legibilidade ou gerar overflow. Validar 1280 × 800 e reflow estreito; abaixo de 720 px, cada linha preserva a ordem de prioridade sem rolagem horizontal global.
10. **Invariantes:** quatro registros e seus valores exatos; dados marcados como demonstração; nenhuma mutação externa; busca, filtros, consulta, seleção, recuperação do bloqueio, foco visível e anúncio das ações.

## Decisões de componentes

- `dados.js`: reutilizar diretamente, sem cópia ou mutação.
- Tabela da fila: criar com HTML nativo, por ser comparação bidimensional de registros homogêneos.
- Busca e filtros: compor com `input[type=search]` e botões com `aria-pressed`.
- Ações por capítulo: criar como botões visíveis, sem overflow, porque são frequentes e há no máximo duas por linha.
- Detalhes e recuperação: estender a linha com uma região adjacente; evita modal e mantém o contexto do capítulo bloqueado.
- Seleção em lote: criar somente para registros marcados `selectable`; os demais controles permanecem desabilitados e nomeados.
- Dependências, chamadas de rede, fontes e assets externos: fora do escopo.

## Estados e recuperação

- Busca/filtro: resultado atualizado em região `aria-live`; zero resultado oferece restauração explícita.
- Consulta: botão expõe `aria-expanded` e mantém o detalhe no fluxo da linha.
- Seleção: checkbox nativo, estado `checked`, mudança visual e ação de lote desabilitada até seleção válida.
- Glossário bloqueado: abertura mantém a região junto de `ch115`; confirmação local habilita a tentativa, sem alterar o fixture.
- Ações: todas encerram em mensagem visível e anunciada; nenhuma executa scripts ou escreve arquivos.

## Critérios verificáveis

- Abrir por `file://` sem dependência externa e sem erro de JavaScript.
- Exibir os quatro IDs e o resumo `4 / 15.743 / 1 / 1 / 1 / 1` do fixture.
- Busca por ID/título, limpeza e quatro filtros funcionais.
- Consulta disponível para todos os capítulos.
- Seleção/aplicação em lote disponível apenas para o registro pronto.
- Fluxo de `ch115`: resolver → confirmar → tentar novamente, sempre com feedback simulado.
- Foco visível; controles nativos; landmarks, headings, labels e mensagens programáticas.
- Sem rolagem horizontal global no viewport-alvo e no reflow estreito implementado.

## Arquivos entregues

- `index.html`: estrutura semântica e carregamento da fonte compartilhada.
- `styles.css`: direção visual, estados, foco, reflow e modos de alto contraste/redução de movimento.
- `app.js`: renderização do fixture, busca, filtros, detalhes, seleção, recuperação e feedback simulado.
- `DIRECAO.md`: contrato, decisões, critérios, validações e limites deste braço.

## Validações e limitações

- Exercitado: sintaxe de `app.js` e `dados.js`; carga e congelamento de `window.DEMO_TRADUCAO`; quatro IDs; total de 15.743 palavras; referência única a `../dados.js`; ausência de URL externa no HTML; ausência de cópia dos títulos no JavaScript; `git diff --check` no diretório do braço.
- Revisão visual em navegador, percurso real de Tab/Shift+Tab, leitor de tela, zoom, text spacing e forced colors: não exercitados nesta sessão porque nenhum navegador estava disponível no runtime integrado.
- O CSS inclui composições para 1280 × 800 e reflow abaixo de 720 px, mas a ausência de captura real limita afirmações sobre acabamento e clipping ao que foi verificado estaticamente.
