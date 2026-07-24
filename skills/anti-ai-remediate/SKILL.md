---
name: anti-ai-remediate
description: "Aplicar somente achados de auditoria confirmados, aprovados pelo usuário, reproduzíveis e dentro do escopo atual. Usar somente quando invocada explicitamente com IDs ou relatório aprovado e autorização para editar; não usar para revisão aberta, limpeza especulativa ou correções não aprovadas. Ler o estado do alvo e, quando Git existir, branch/HEAD/status; implementar correções mínimas, executar regressões e relatar resultado por achado."
---

# Remediação Anti-IA

Corrigir somente achados confirmados, aprovados, reproduzíveis e dentro do escopo. Não transformar remediação em refatoração geral.

## Exigir entrada suficiente

Obter:

- relatório ou achados com IDs;
- subconjunto aprovado pelo usuário;
- escopo de arquivos/comportamento;
- autorização para editar;
- critérios de aceitação e validações esperadas.

Se não houver achado reproduzível ou escopo de correção, não ativar mudanças. Encaminhar investigação para auditoria/análise.

## Preparar

1. Detectar se o alvo pertence a um repositório Git. Somente nesse caso registrar branch, HEAD, status, staged e untracked; fora de Git, registrar inventário e hashes dos arquivos relevantes sem executar comandos Git.
2. Preservar alterações preexistentes.
3. Ler relatório aprovado e evidência.
4. Carregar [remediation-protocol.md](references/remediation-protocol.md).
5. Carregar [validation-checklist.md](references/validation-checklist.md) e usá-lo antes do handoff.
6. Carregar [approval-gates.md](references/approval-gates.md) para limites.
7. Para código, carregar [workflow de revisão](../anti-ai-code/references/review-workflow.md) e [testes](../anti-ai-code/references/testing-antipatterns.md).
8. Para UI, carregar [workflow visual](../anti-ai-design/references/review-workflow.md), [acessibilidade](../anti-ai-design/references/accessibility-baseline.md) e [contrato de direção](../anti-ai-design/references/direction-contract.md).
9. Para segurança, carregar [workflow de remediação](../anti-ai-security/references/remediation-workflow.md) e [validação e severidade](../anti-ai-security/references/validation-and-severity.md).

## Corrigir

1. **Gate de elegibilidade, ainda read-only:** revalidar estado atual, reprodução, reachability, invariante e escopo. Classificar como pronto, já corrigido/sem mudança, bloqueado por prova, bloqueado por produto ou fora de escopo.
2. **Gate do plano, ainda sem editar:** mapear IDs, causa, boundary, arquivos, comportamento que muda e permanece, regressão/validação positiva, risco e rollback.
3. **Gate de aplicação:** quando Git existir, revalidar HEAD e status; sempre revalidar os arquivos. Corrigir uma causa lógica por vez e mapear qualquer agrupamento de IDs.
4. **Gate de verificação congelada:** comprovar que o caso original não reproduz, o uso legítimo funciona, a regressão é sensível ao controle, siblings/bypasses foram verificados e diff/comandos cobrem só o pretendido.
5. Para UI, executar e capturar antes/depois com mesmos dados, estados e viewports.
6. Se a validação falhar, marcar falha e voltar ao plano; não empilhar remendos.
7. Solicitar nova aprovação quando o plano, risco, comportamento ou escopo mudar materialmente.

## Limites

Não:

- refatorar toda a arquitetura;
- modificar áreas independentes;
- inventar requisito;
- ocultar falha;
- reduzir cobertura;
- atualizar todas as dependências;
- introduzir framework;
- criar camada genérica sem necessidade;
- substituir funcionalidade por mock;
- afirmar correção sem reprodução;
- aprovar visual automaticamente;
- apagar trabalho existente;
- fazer commit ou push sem autorização explícita.

## Saída

Por achado, informar status: corrigido e validado, corrigido com validação parcial, não reproduzido, já corrigido/sem mudança, bloqueado por prova, bloqueado por produto, bloqueado por escopo, falhou na validação ou rejeitado. Incluir causa, mudança, arquivos, regressão, comandos/resultados, diff relevante, risco restante e aprovação necessária.
