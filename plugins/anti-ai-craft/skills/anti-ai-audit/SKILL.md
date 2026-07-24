---
name: anti-ai-audit
description: "Auditar interface, acessibilidade, responsividade, código, arquitetura, testes, documentação, estados e comportamento real em modo estritamente somente leitura. Usar somente quando invocada explicitamente com repositório, caminho, diff, screenshots ou interface em execução; encaminhar achados aprovados à anti-ai-remediate em vez de corrigir. Ler evidências do projeto e produzir achados por severidade com falsos positivos rejeitados."
---

# Auditoria Anti-IA

Executar auditoria sem detectar nem atribuir autoria. Avaliar defeitos, vulnerabilidades, acessibilidade, manutenção, padrões genéricos e inconsistências somente por evidência observável.

## Manter estritamente read-only

Não editar, formatar, instalar, remover, criar arquivo permanente, fazer stage, commit ou push. Não executar comandos que gerem caches, snapshots, lockfiles, bancos, artefatos ou migrações no projeto. Diagnóstico que precise escrever deve usar diretório temporário fora do alvo e não pode alterar estado externo. Se o usuário pedir correções, concluir o relatório e encaminhar os IDs aprovados para `$anti-ai-remediate`; esta skill nunca aplica mudanças.

## Preparar

1. Resolver o tipo de alvo — repositório, caminho, diff, commit, branch, worktree, screenshot ou app — e fixar baseline.
2. Ler instruções, README, especificação, design system, código, testes, configs e histórico relevante.
3. Quando o alvo estiver em Git, registrar raiz, branch, HEAD, status e alterações preexistentes sem modificá-las. Para branch ou PR, identificar o upstream ou alvo documentado e calcular o `merge-base` com HEAD; não presumir `main`, `HEAD^` ou o commit anterior. Registrar o comando e o SHA usados como baseline. Fora de Git, marcar esses campos como não aplicáveis.
4. Em revisão de diff, comparar `merge-base..HEAD` ou o intervalo explicitamente solicitado e separar o que foi introduzido ou agravado da dívida preexistente.
5. Identificar usuários, tarefas, dados, estados, invariantes e superfícies.
6. Quando houver brief, arquitetura da informação, tokens, plano ou checkpoint no escopo, verificar estado, autoridade e atualidade antes de tratá-los como fonte. Arquivo presente não significa concluído, e artefato não vence código ou decisão posterior automaticamente.
7. Para UI, carregar diretamente [princípios de design](../anti-ai-design/references/design-principles.md), [arquitetura da informação](../anti-ai-design/references/information-architecture.md), [design tokens](../anti-ai-design/references/design-tokens.md), [antipadrões visuais](../anti-ai-design/references/design-antipatterns.md) e [acessibilidade](../anti-ai-design/references/accessibility-baseline.md).
8. Para código, carregar diretamente [antipadrões de código](../anti-ai-code/references/code-antipatterns.md), [testes](../anti-ai-code/references/testing-antipatterns.md) e [arquitetura](../anti-ai-code/references/architecture-antipatterns.md).
9. Para segurança, carregar diretamente [checklist de segurança](../anti-ai-security/references/security-checklist.md) e [validação e severidade](../anti-ai-security/references/validation-and-severity.md), mantendo esta auditoria sem edições.

## Auditar

- Usar [audit-checklist.md](references/audit-checklist.md) para cobertura.
- Usar [severity-model.md](references/severity-model.md) para impacto e confiança.
- Usar [report-template.md](references/report-template.md) para o relatório.
- Executar aplicação e capturar evidência real somente quando estiver disponível e for read-only.
- Citar arquivo/linha, componente, screenshot, viewport, comando ou trace.
- Manter ledger de candidatos; fechar cada item como confirmado, suprimido, não aplicável, dependente de infraestrutura, não verificado ou duplicado.
- Validar candidatos, buscar a evidência que os derrotaria e rejeitar falsos positivos.
- Separar problema do produto de preferência estética/código.
- Continuar auditando todo o escopo planejado depois do primeiro achado. Um problema confirmado não encerra famílias, arquivos, fluxos ou superfícies ainda não examinados; registrar explicitamente qualquer corte de cobertura.
- Quando uma pergunta de produto, infraestrutura ou baseline permanecer material, registrar origem pesquisada, recomendação, efeito sobre severidade/confiança e trabalho independente concluído. Bloquear somente a família ou superfície dependente.
- Para UI, declarar perfil de evidência e cobertura por superfície/rota, estado, viewport e tema/input. Não apresentar screenshot fornecido ou código isolado como validação completa de runtime.

## Regras de achado

Cada achado precisa de:

- ID e título;
- área;
- severidade e confiança;
- arquivo, linha ou componente;
- controle ou causa raiz afetada;
- ator e pré-condições;
- evidência;
- contraprova mais forte examinada;
- lacuna de prova;
- impacto;
- justificativa da severidade;
- regra violada;
- classificação do achado;
- correção recomendada;
- risco da correção;
- validação necessária;
- critérios de aceitação.

Separar severidade, confiança e prioridade de remediação. Deduplicar somente quando controle/causa, comportamento, impacto e correção forem os mesmos; preservar todas as localizações.

Não detectar, atribuir nem especular sobre autoria ou proveniência. Usar somente classificações observáveis como “padrão genérico”, “decisão sem justificativa funcional”, “code smell”, “inconsistência”, “defeito confirmado” ou “evidência insuficiente”.

## Encerrar

Ordenar por severidade e dependência. Separar achados confirmados, decisões pendentes, preferências, falsos positivos rejeitados e dívida preexistente. Informar cobertura, matriz de fechamento, comandos com exit codes, limitações, áreas não auditadas e risco residual. Se nada qualificar, declarar explicitamente: **Nenhum achado qualificável**.
