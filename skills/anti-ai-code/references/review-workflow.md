# Workflow de revisão e implementação

## Gates permanentes

1. **Compreender antes de agir:** ler o sistema, traçar o caminho e resolver ambiguidades materiais.
2. **Preservar o escopo:** não transformar a tarefa em limpeza geral ou expansão arquitetural.
3. **Exigir evidência antes de afirmar:** executar a verificação, ler a saída e separar fato, inferência e desconhecido.

## 1. Resolver escopo

- Confirmar análise versus edição.
- Identificar arquivos, comportamento, requisitos e risco.
- Ler instruções e fontes de verdade.
- Registrar branch, HEAD, status e alterações preexistentes quando houver Git.
- Definir critérios de sucesso e, para mudanças arriscadas, estratégia de reversão antes de editar.

## 2. Construir modelo do sistema

- Mapear entradas, outputs, side effects, persistência e boundaries.
- Identificar invariantes, estados e API pública.
- Localizar implementação, callers, testes, config, dependências e histórico relevante.
- Não revisar snippet como sistema completo quando o contexto existe.

## 3. Descobrir candidatos

Procurar nesta ordem:

1. falha funcional reproduzível;
2. perda/corrupção e falso sucesso;
3. autorização e vulnerabilidade;
4. transação, concorrência e async;
5. contrato/API/dependência inventados;
6. teste que não detecta regressão;
7. smell com impacto de manutenção;
8. preferência subjetiva.

## 4. Validar candidato

Para cada candidato:

- localizar arquivo/linha;
- descrever caminho de execução;
- reproduzir ou construir teste mínimo;
- confirmar requisito/invariante;
- verificar se já existe proteção;
- procurar false positives e condições de alcance;
- calibrar impacto e confiança.

Não reportar grep sem caminho executável como bug confirmado.

## 5. Corrigir

Quando autorizado:

1. preservar trabalho preexistente;
2. escrever/reproduzir regressão e, quando viável, observar a falha esperada antes da correção;
3. identificar causa, não somente sintoma;
4. aplicar menor mudança coerente;
5. preservar API pública e padrões locais;
6. não esconder falha;
7. não expandir arquitetura;
8. atualizar documentação somente se o contrato realmente mudou.
9. manter evidência diagnóstica temporária até a correção ser confirmada; depois removê-la ou normalizá-la de forma deliberada.

## 6. Validar

- Executar teste focado antes/depois.
- Rodar suíte proporcional ao risco.
- Rodar lint/typecheck/build/análise estática pertinentes.
- Verificar dependências/config/APIs reais.
- Para persistência: testar falha parcial, rollback e retry.
- Para concorrência: testar ordem, cancelamento, timeout e duplicação.
- Revisar diff e arquivos não intencionais.

## 7. Relatar

Cada achado inclui:

- título e classificação;
- arquivo/linha;
- evidência/reprodução;
- impacto;
- regra/contrato violado;
- correção sugerida;
- risco da correção;
- validação necessária.

Cada correção inclui:

- causa;
- arquivos alterados;
- mudança mínima;
- regressão;
- comandos/resultados;
- validação não executada;
- risco restante.
