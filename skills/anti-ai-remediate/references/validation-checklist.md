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

- [ ] Screenshot antes/depois com mesmos dados e viewport.
- [ ] Desktop, tablet e mobile pertinentes.
- [ ] Conteúdo e estados reais.
- [ ] Teclado, foco, Escape e retorno de foco.
- [ ] Semântica, labels e mensagens.
- [ ] Contraste, cor não exclusiva e targets.
- [ ] Reflow, zoom, text spacing e strings longas.
- [ ] Reduced motion.
- [ ] Alteração ampla recebeu aprovação humana.

## Handoff

- [ ] Cada ID tem status final independente.
- [ ] Comandos e códigos de saída registrados.
- [ ] Limitações declaradas.
- [ ] Risco restante declarado.
- [ ] Git rechecado quando aplicável.
- [ ] Nenhum stage, commit ou push não autorizado.
