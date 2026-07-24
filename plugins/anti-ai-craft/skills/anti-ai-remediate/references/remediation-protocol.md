# Protocolo de remediação

## 1. Estado inicial

- Resolver raiz e instruções do projeto.
- Detectar primeiro se o alvo pertence a um repositório Git.
- Quando Git existir, registrar branch, HEAD, status, staged e untracked com comandos somente leitura.
- Fora de Git, registrar inventário, metadados e hashes dos arquivos relevantes; não executar comandos Git nem tratar sua ausência como falha.
- Usar status, diff e hashes somente leitura para comprovar preservação. Não duplicar arquivos do usuário como mecanismo de prova.
- Não limpar, resetar, stashar ou sobrescrever mudanças preexistentes.

## 2. Gate de elegibilidade — somente leitura

- Listar IDs aprovados.
- Confirmar severidade, evidência, arquivos e dependências.
- Revalidar estado atual, reachability e invariante antes de planejar mudança.
- Classificar cada ID como pronto, já corrigido/sem mudança, bloqueado por prova, bloqueado por produto ou fora de escopo.
- Ordenar por causa e dependência para evitar correções duplicadas.

## 3. Gate do plano — ainda sem editar

- Executar caso original.
- Registrar resultado antes da mudança.
- Construir teste mínimo quando não existir.
- Confirmar que falha pela causa descrita, não por ambiente.
- Para UI, capturar estado/viewport anterior.
- Mapear causa, boundary, arquivos, comportamento que muda e permanece, regressão, validação positiva, risco e rollback.
- Agrupar IDs somente quando a relação com a mesma causa e mudança estiver explícita.
- Para fluxo persistido, representar o lote por resultado, origem, dependências, critério de pronto e prova; o plano não amplia a lista de IDs autorizados.

## 4. Gate de aplicação

- Traçar entrada, estado, side effects e saída.
- Identificar primeira violação de invariante.
- Quando Git existir, revalidar HEAD e status; sempre revalidar o conteúdo dos arquivos imediatamente antes de editar.
- Preferir correção no boundary certo.
- Preservar API pública e arquitetura.
- Evitar abstração/flag/config genérica.
- Documentar tradeoff se mais de uma correção for válida.

## 5. Implementação

- Editar somente arquivos necessários.
- Preservar style e convenções.
- Não engolir exceção, retornar sucesso falso ou relaxar validação.
- Garantir transação, rollback, idempotência e concorrência conforme o caso.
- Para UI, preservar identidade e implementar comportamento/acessibilidade completos.
- Corrigir uma causa lógica por vez e executar uma prova antes da próxima.
- Para navegação ou URL pública, preservar deep links, refresh, back/forward, retorno e compatibilidade, ou implementar migração/redirect aprovado.
- Para tokens, editar a fonte autoritativa, regenerar outputs pelo comando oficial e validar consumidores, modos e estados afetados; não substituir valores em massa sem mapa de uso.

## 6. Gate de verificação congelada

- Demonstrar falha antes quando viável.
- Demonstrar sucesso depois.
- Cobrir limite/falha relacionada.
- Evitar mock que confirma o próprio mock.
- Não regravar snapshot sem revisão.
- Confirmar que o teste falha se o controle corrigido for retirado.
- Verificar siblings, aliases e bypasses relacionados.
- Se falhar, marcar o ID como falhou na validação e voltar ao plano; não empilhar remendos.

## 7. Validação

- Rodar teste focado.
- Rodar suíte proporcional ao risco.
- Rodar lint/typecheck/build/análise pertinente.
- Revisar diff.
- Reexecutar reprodução.
- Para UI, capturar depois e comparar.
- Confirmar que a estratégia de rollback está documentada e, quando o risco justificar, ensaiada em ambiente seguro ou por dry-run antes da entrega.
- Quando houver fluxo de design, reconciliar código, evidência, status da tarefa e artefatos diretamente afetados. Atualizar documento apenas com autorização.

## 8. Handoff

- Relacionar arquivos e achados.
- Fornecer comandos e resultados exatos.
- Informar validação não executada.
- Listar risco restante.
- Confirmar estado Git quando aplicável e ausência de commit/push.
- Relatar status por ID, inclusive sem mudança e bloqueios.

## Rollback

- Reverter somente hunks criados nesta remediação; nunca usar reset, checkout ou stash para apagar trabalho alheio.
- Para dados/migrações, definir backup, compatibilidade e estratégia de reversão antes da mudança.
- Ensaiar restauração, down migration, feature rollback ou procedimento equivalente em ambiente seguro quando falha de reversão puder causar perda, indisponibilidade ou inconsistência material. Se o ensaio não for possível, declarar a lacuna antes de aplicar.
- Declarar irreversibilidade antes de agir e exigir autorização específica.
