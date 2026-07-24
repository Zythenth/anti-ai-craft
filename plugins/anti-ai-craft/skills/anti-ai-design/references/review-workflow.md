# Workflow de revisão visual

## Sumário

- [Preflight](#1-preflight)
- [Estrutura sem decoração](#2-estrutura-sem-decoração)
- [Conteúdo e estados](#3-conteúdo-e-estados)
- [Direção e alternativas](#4-direção-e-alternativas)
- [Implementação autorizada](#5-implementação-autorizada)
- [Captura real](#6-captura-real)
- [Passes separados](#7-passes-separados)
- [Comparação antes/depois](#8-comparação-antesdepois)
- [Gate humano](#9-gate-humano)
- [Relatório](#10-relatório)

## 1. Preflight

- Registrar escopo e se edição está autorizada.
- Ler fontes de verdade e estado do código.
- Listar usuários, tarefas, telas, rotas, dados e estados.
- Classificar a superfície e o mandato de preservação/refino/redesign.
- Listar defaults prováveis relevantes; não impor quantidade ritual.
- Separar identidade existente de decoração.
- Definir critérios de aceitação e viewports.
- Fixar contrato de direção e referência dominante quando houver criação ou redesign.
- Registrar os arquivos, versões, seções, telas e artefatos realmente lidos, vinculando cada decisão à evidência correspondente.

## 2. Estrutura sem decoração

Revisar em escala de cinza e, quando possível, sem efeitos:

- ordem de leitura;
- ação primária;
- hierarquia;
- agrupamentos;
- densidade;
- sequência de foco;
- prioridade por viewport.

## 3. Conteúdo e estados

Usar dados reais ou fixtures explicitamente marcadas. Exercitar:

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

## 6. Captura real

- Executar a aplicação.
- Capturar screenshot real, não mock desatualizado.
- Usar os mesmos dados/estado para antes/depois.
- Registrar viewport, escala, tema e fluxo.
- Capturar ao menos estreito, intermediário e amplo quando o escopo for responsivo.
- Incluir estados críticos, não apenas happy path.

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

## 8. Comparação antes/depois

Para cada mudança, registrar:

- problema anterior;
- evidência;
- decisão;
- resultado observável;
- regressão potencial;
- validação executada.

Não declarar “melhor” apenas por preferência. Comparar tarefa, tempo, erro, legibilidade, acesso, densidade e coerência.

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

Separar achados por severidade e classificação. Incluir fonte de verdade, screenshot/viewport/estado/tema, componente/arquivo/linha, desvio, impacto, evidência, correção sugerida, risco e decisão passar/bloquear. Declarar explicitamente o que não foi testado.
