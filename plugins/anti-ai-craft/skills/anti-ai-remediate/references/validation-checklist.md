# Checklist de validação

## Geral

- [ ] Elegibilidade foi revalidada no estado atual.
- [ ] Git foi detectado antes de consultar branch, HEAD ou status; fora de Git, foram usados inventário e hashes dos arquivos relevantes.
- [ ] Quando Git existe, HEAD e status foram rechecados; em todos os casos, os arquivos foram rechecados antes de editar.
- [ ] O problema foi reproduzido antes.
- [ ] A causa corresponde ao achado aprovado.
- [ ] A mudança está dentro do escopo.
- [ ] Alterações preexistentes foram preservadas.
- [ ] API pública e comportamento válido foram preservados.
- [ ] Teste de regressão falha antes e passa depois, quando viável.
- [ ] A regressão falharia novamente sem o controle corrigido.
- [ ] Um uso legítimo positivo continua funcionando.
- [ ] Siblings, aliases e bypasses pertinentes foram verificados.
- [ ] Teste focado passou.
- [ ] Suíte proporcional passou.
- [ ] Lint/typecheck/build pertinentes passaram.
- [ ] Diff contém apenas mudanças intencionais.
- [ ] Estratégia de rollback está documentada e é compatível com alterações preexistentes.
- [ ] Rollback foi ensaiado em ambiente seguro quando o risco justificava; impossibilidade e risco residual foram declarados.
- [ ] A evidência foi reexecutada após a última mudança relevante.
- [ ] O estado da tarefa deriva da prova e dos IDs; código escrito não foi marcado automaticamente como validado.
- [ ] Nenhum erro foi ocultado.
- [ ] Nenhum mock substitui funcionalidade.
- [ ] Nenhuma dependência/framework/config desnecessária foi adicionada.

## Dados e operações

- [ ] Validação de entrada e invariantes.
- [ ] Autorização no boundary correto.
- [ ] Transação e rollback em falha parcial.
- [ ] Retry e idempotência.
- [ ] Concorrência, await, cancelamento e timeout.
- [ ] Estado terminal e erro observáveis.
- [ ] Segredos/PII ausentes de código e logs.

## UI

Selecionar somente checks aplicáveis ao widget, risco, plataforma, mudança e
evidência disponível; marcar o restante como `não aplicável` ou `não exercitado`
com motivo, sem declarar cobertura.

- [ ] Screenshot antes/depois com mesmos dados e viewport quando houver runtime visual comparável.
- [ ] Viewports pertinentes às superfícies responsivas alteradas.
- [ ] Conteúdo e estados reais afetados.
- [ ] Teclado, foco, Escape e retorno de foco para widgets correspondentes.
- [ ] Semântica, labels e mensagens afetadas.
- [ ] Contraste, cor não exclusiva e targets quando estilos ou interação mudarem.
- [ ] Reflow, zoom, text spacing e strings longas quando layout/conteúdo puderem ser afetados.
- [ ] Reduced motion quando movimento existir ou mudar.
- [ ] Alteração ampla recebeu aprovação humana.
- [ ] Mudanças de navegação/URL preservam link direto, refresh, back/forward, retorno e compatibilidade aplicáveis.
- [ ] Mudanças de tokens partiram da fonte autoritativa, regeneraram outputs oficialmente e cobriram consumidores, modos e estados afetados.
- [ ] Código, evidência, status da tarefa e artefatos autorizados diretamente afetados não se contradizem; pendências fora do escopo foram registradas sem edição.

## Handoff

- [ ] Cada ID tem status final independente.
- [ ] Comandos e códigos de saída registrados.
- [ ] Limitações declaradas.
- [ ] Risco restante declarado.
- [ ] Git rechecado quando aplicável.
- [ ] Nenhum stage, commit ou push não autorizado.
