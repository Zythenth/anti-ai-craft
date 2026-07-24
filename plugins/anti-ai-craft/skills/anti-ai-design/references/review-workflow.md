# Workflow de revisão visual

## Sumário

- [Preflight](#1-preflight)
- [Estrutura sem decoração](#2-estrutura-sem-decoração)
- [Conteúdo e estados](#3-conteúdo-e-estados)
- [Direção e alternativas](#4-direção-e-alternativas)
- [Implementação autorizada](#5-implementação-autorizada)
- [Captura e perfil de evidência](#6-captura-e-perfil-de-evidência)
- [Passes separados](#7-passes-separados)
- [Comparação antes/depois](#8-comparação-antesdepois)
- [Gate humano](#9-gate-humano)
- [Relatório](#10-relatório)

## 1. Preflight

- Registrar escopo e se edição está autorizada.
- Ler fontes de verdade e estado do código.
- Listar usuários, tarefas, telas, rotas, dados e estados.
- Classificar elementos relevantes como reutilização direta, composição, extensão, criação, fora do escopo ou desconhecido, com evidência.
- Classificar a superfície e o mandato de preservação/refino/redesign.
- Listar defaults prováveis relevantes; não impor quantidade ritual.
- Separar identidade existente de decoração.
- Definir critérios de aceitação e viewports.
- Confirmar se o alvo é local, preview, staging ou produção e quais operações são
  somente leitura. Não presumir que executar a UI autoriza efeitos externos.
- Fixar contrato de direção e referência dominante quando houver criação ou redesign.
- Registrar os arquivos, versões, seções, telas e artefatos realmente lidos, vinculando cada decisão à evidência correspondente.
- Registrar decisões materiais por ID, dependência, origem e estado quando forem necessárias; encerrar quando nenhum ramo aberto alterar direção ou critérios.

## 2. Estrutura sem decoração

Revisar em escala de cinza e, quando possível, sem efeitos:

- ordem de leitura;
- ação primária;
- hierarquia;
- agrupamentos;
- densidade;
- sequência de foco;
- prioridade por viewport.

Para produto navegável, executar também um passe estrutural no runtime alcançável:

- conferir pontos de entrada, destinos, navegação global/local/contextual e rótulos;
- exercer URL direta, refresh, back/forward, retorno ao contexto e persistência;
- verificar estados sem acesso, destino ausente, interrupção, erro e recuperação;
- comparar a hierarquia percebida com a tarefa e a arquitetura da informação vigente.

Quando não houver runtime, limitar o passe ao perfil disponível e registrar quais
desses comportamentos permanecem `não exercitados`.

## 3. Conteúdo e estados

Preferir fixtures ou dados representativos explicitamente marcados. Usar dados
reais somente quando a evidência exigir, houver autorização e eles puderem ser
minimizados e redigidos. Exercitar:

- mínimo e máximo;
- títulos e valores longos;
- vazio;
- loading/processamento;
- sucesso;
- erro/retry;
- offline/indisponível;
- permissão;
- estado crítico.

## 4. Direção e alternativas

Quando houver decisão material:

1. formular duas ou três teses de composição;
2. explicar vínculo de cada uma com produto e tarefa;
3. comparar legibilidade, densidade, responsividade, acessibilidade, custo e risco;
4. escolher uma direção ou pedir decisão humana.

Não gerar variantes cosméticas equivalentes.

## 5. Implementação autorizada

- Preservar arquitetura, tokens, componentes e alterações preexistentes.
- Implementar comportamento e estados reais.
- Evitar dependência, asset, framework ou refatoração não solicitada.
- Manter mudança pequena e rastreável.
- Rodar lint, testes e build pertinentes.

## 6. Captura e perfil de evidência

Selecionar primeiro o perfil de evidência. Para `runtime completo` ou `runtime
parcial`, executar a aplicação e capturar evidência real, usando os mesmos
dados/estado no antes/depois e registrando viewport, escala, tema e fluxo. Incluir
estados críticos alcançáveis, não apenas happy path.

Antes de interagir, confirmar o ambiente e separar navegação somente leitura de
operações mutáveis. Submeter formulário, enviar mensagem, fazer upload, pagamento,
exclusão, escrita em banco ou chamada externa com efeito exige autorização
específica. Não usar produção quando local, preview ou staging provarem o mesmo
comportamento. Redigir segredos, credenciais, PII e conteúdo de cliente de
screenshots, arquivos e respostas; se a redação destruir a prova, registrar a
limitação em vez de expor o dado.

Para `artefato visual`, analisar apenas o screenshot ou vídeo fornecido. Para
`código apenas`, inspecionar estrutura e risco potencial sem exigir execução ou
captura e sem afirmar resultado renderizado.

Quando o escopo for responsivo e o projeto não definir breakpoints ou viewports de
teste, usar `375×812`, `768×1024` e `1280×800` como sondas reproduzíveis de
estreito, intermediário e amplo. Elas são fallbacks de investigação, não novos
breakpoints nem matriz obrigatória; reduzir ou ampliar a amostra conforme risco,
plataforma e superfícies afetadas.

Revisão não edita por padrão. Sem autorização, manter capturas em local temporário fora do alvo ou apresentá-las na conversa. Persistir screenshots ou relatório no projeto somente em caminho autorizado e coerente com suas convenções.

Perfis disponíveis:

1. **Runtime completo:** app executável, superfícies e estados alcançáveis.
2. **Runtime parcial:** alegações limitadas ao que foi alcançado.
3. **Artefato visual:** apenas o que está visível no screenshot ou vídeo fornecido.
4. **Código apenas:** estrutura e risco potencial, sem afirmar qualidade visual renderizada.

Antes de declarar validação final, exigir alvo executável, entrada conhecida, estado/dados reproduzíveis, viewport/tema definidos e critérios anteriores. Caso contrário, rotular revisão de plano, estática ou de protótipo e declarar o que ela não prova.

Criar matriz proporcional por superfície, criticidade, estados, viewports, tema/input, evidência e disposição. Usar `coberto`, `parcial`, `bloqueado`, `não exercitado` ou `não aplicável`; não exigir produto cartesiano de combinações.

## 7. Passes separados

Fazer dois passes independentes antes da síntese:

1. **Visual/UX, sem consultar detector ou checklist de estilo:** função, conteúdo, tarefa, hierarquia, linguagem, densidade e recuperação.
2. **Técnico/determinístico:** teclado/foco, semântica/leitor de tela, contraste/forced colors, zoom/reflow/text spacing, motion/reduced motion, performance e regressões.

Para cada candidato, aplicar o gate:

1. qual contrato, tarefa ou requisito é relevante;
2. se o caminho/componente está alcançável no runtime;
3. qual correção a evidência realmente determina;
4. qual observação derrotaria o achado.

Exercitar cenários representativos: iniciante e experiente, teclado e leitor de tela, mobile com interrupção, erro/undo/recuperação e conteúdo extremo. Não substituir isso por limites numéricos universais.

No passe de conteúdo, confirmar reconhecimento em vez de memorização, termos do usuário, voz ativa, nome consistente da ação em todo o fluxo e numeração reservada a sequências reais. No passe visual/técnico, confirmar a cadeia `primitivo → semântico → componente` em consumidores e estados reais.

Quando tokens forem alterados, verificar aliases, fonte versus output gerado, consumidores representativos, modos e estados. Quando múltiplos temas estiverem no escopo, cruzar estados críticos com ao menos um viewport estreito e um amplo, incluindo foco, erro, disabled, loading, overlays, mídia, forced colors e reduced motion quando aplicáveis.

Ligar sintoma renderizado à causa técnica e procurar contraprova. Screenshot não prova sozinho a causa; código não prova sozinho o resultado visual.

## 8. Comparação antes/depois

Para cada mudança, registrar:

- problema anterior;
- evidência;
- decisão;
- resultado observável;
- regressão potencial;
- validação executada.

Não declarar “melhor” apenas por preferência. Comparar tarefa, tempo, erro, legibilidade, acesso, densidade e coerência.

Quando houver artefatos do fluxo, comparar tarefa, brief, arquitetura da informação, tokens, plano, implementação e runtime. Classificar divergência como defeito, decisão posterior válida, artefato superado, ambiguidade ou lacuna de prova.

## 9. Gate humano

Solicitar aprovação antes de:

- mudar identidade, navegação principal ou tese de composição;
- substituir design system;
- alterar muitas telas;
- remover padrão reconhecível;
- escolher entre alternativas com tradeoffs de produto;
- aceitar mudança visual ampla mesmo quando tecnicamente válida.

Bloquear entrega diante de falha funcional, perda de dados/foco, ação primária oculta, conteúdo inventado, overflow global, estado só por cor ou regressão WCAG aplicável.

## 10. Relatório

Usar [design-review-template.md](design-review-template.md) para revisão formal. Separar severidade, confiança, prioridade e gate. Incluir perfil de evidência, cobertura, manifesto de capturas, fonte de verdade, screenshot/viewport/estado/tema, componente/arquivo/linha, desvio, impacto, contraprova, correção sugerida, risco e critérios de aceitação. Registrar decisões eficazes que devem ser preservadas e declarar o que não foi testado.

Emitir IDs `ADR-*` para achados sustentados. Revisão termina no relatório; oferecer aplicação somente após seleção explícita dos IDs, preferencialmente por `$anti-ai-remediate`.
