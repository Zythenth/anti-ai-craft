---
name: anti-ai-code
description: "Revisar ou implementar mudanças de código delimitadas, evitando comportamento não verificável, frágil, inventado, prolixo ou superengenheirado. Usar quando o pedido envolver módulos, diffs, testes, correções, refatorações ou requisitos de implementação; não usar para design puramente visual, auditoria ampla somente leitura, aplicação de achados numerados ou tradução. Ler o repositório, citar evidência por arquivo e linha e editar apenas quando solicitado, priorizando solução direta, coesa e mínima."
---

# Código Anti-IA

Tratar “anti-AI” como engenharia verificável, não como detecção de autoria. Evitar código que parece sofisticado, mas acrescenta volume, camadas, opções ou comentários sem resolver uma necessidade concreta. Padrões abordados aqui também podem ser escritos por humanos. Procurar primeiro defeitos reais e separar bug, vulnerabilidade, smell tradicional, heurística e preferência.

Usar `$anti-ai-audit` para uma varredura ampla somente leitura, `$anti-ai-security` para caminhos de abuso e `$anti-ai-remediate` quando já existem IDs aprovados. Esta skill serve a implementação ou revisão delimitada.

## Preparar

1. Confirmar escopo, autorização para editar e resultado esperado.
2. Ler AGENTS.md, README, documentação, configs, manifestos, lockfiles, scripts, código vizinho, testes e histórico Git quando ajudarem.
3. Registrar arquitetura, convenções, API pública, invariantes, alterações preexistentes e comandos oficiais.
4. Declarar somente pressupostos, interpretações concorrentes e trade-offs materiais. Investigar fatos no repositório; ordenar decisões por contrato/invariante, boundary/API e implementação. Ambiguidade de baixo risco pode ser assumida e explicitada; decisão de contrato ou segurança deve ser perguntada com recomendação, fundamento e consequência. Continuar ramos independentes.
5. Reproduzir o comportamento antes de chamar algo de bug.
6. Verificar API nesta ordem: repositório/lockfile/imports/tipos; pacote ou CLI instalado; documentação oficial da versão exata; release notes ou repositório oficial. Não inferir entre versões, linguagens ou SDKs.
7. Separar fato verificado, inferência e desconhecido. Se uma API, versão, comando, citação ou requisito não puder ser confirmado, declarar a limitação em vez de completar a lacuna por plausibilidade.

## Carregar referências

- Ler [code-antipatterns.md](references/code-antipatterns.md) para correção, erros, estado, segurança, integração e UI implementada.
- Ler [testing-antipatterns.md](references/testing-antipatterns.md) ao criar, revisar ou usar testes como evidência.
- Ler [architecture-antipatterns.md](references/architecture-antipatterns.md) ao avaliar abstração, fragmentação, compatibilidade, performance ou logging.
- Ler [debugging-and-evidence.md](references/debugging-and-evidence.md) ao depurar, refatorar, lidar com falhas repetidas ou montar a prova de uma alegação.
- Ler [review-workflow.md](references/review-workflow.md) para investigação, correção localizada, validação e relatório.
- Ler [sources.md](references/sources.md) ao justificar uma regra ou calibrar alegações de qualidade e correção.
- Quando a mudança vier de fluxo de design, ler o brief, a [arquitetura da informação](../anti-ai-design/references/information-architecture.md), os [tokens](../anti-ai-design/references/design-tokens.md) e o plano somente se forem relevantes e atuais; um rascunho ou arquivo presente não autoriza implementação.

## Revisar

1. Mapear requisitos e invariantes para caminhos concretos de execução.
2. Priorizar falhas observáveis: resultado errado, exceção, perda/corrupção, autorização, segurança, corrida, estado impossível ou contrato quebrado.
3. Traçar entrada, transformação, side effects, persistência e saída até a origem do valor defeituoso.
4. Procurar false success, erro engolido, fallback oculto, mutação parcial e rollback incompleto.
5. Verificar concorrência, async, ordem, idempotência e transações quando aplicáveis.
6. Procurar implementações ajustadas somente aos exemplos ou testes conhecidos, incluindo tabelas de casos especiais sem regra de domínio.
7. Formular uma hipótese falsificável por vez e escolher o menor experimento que a distingue de alternativas.
8. Confirmar cada achado por arquivo e linha, reprodução, teste, trace ou contrato.
9. Procurar a evidência que derrubaria o achado; quando contestado, revalidar do zero.
10. Rejeitar falsos positivos e rotular preferências.
11. Aplicar o teste de remoção: se helper, wrapper, classe, camada, configuração ou comentário puder desaparecer sem perder contrato, invariante, reuso real ou clareza, preferir a forma direta.
12. Quando houver plano, validar cada tarefa como resultado observável com origem, estratégia, dependências, critério de pronto e prova; rejeitar tarefas que apenas nomeiam atividade.

## Implementar somente quando autorizado

- Preservar comportamento válido, arquitetura local e API pública.
- Preferir correção localizada e mudança mínima.
- Trabalhar em ciclos `mudança → prova`; não empilhar patches quando um experimento falhar.
- Implementar fatias verticais por comportamento, incluindo somente as camadas necessárias ao mesmo resultado. Não separar automaticamente estrutura, estilo, interação, testes ou segurança em tarefas sem consumidor.
- Preferir fluxo de controle direto, nomes do domínio e uma implementação coesa à fragmentação em helpers triviais.
- Criar teste de regressão quando viável.
- Não esconder erro, relaxar asserção, substituir função por mock ou devolver sucesso falso para fazer teste passar.
- Não adicionar fallback silencioso ou catch-all apenas para manter o fluxo aparentemente bem-sucedido; recuperar somente quando houver semântica explícita e observável.
- Não acrescentar framework, camada, dependência, feature flag, README, CI ou configuração fora do escopo.
- Não refatorar toda a área para corrigir um defeito localizado.
- Não preencher lacunas de produto com comportamento inventado.
- Não criar interface, factory, repository, adapter, service, strategy, wrapper ou configuração extensível para um único caso sem fronteira real.
- Não adicionar comentários ou docstrings que apenas narrem a sintaxe, prometam qualidade ou repitam o nome da função.
- Manter evidência diagnóstica temporária fora do diff sempre que possível. Se logs forem indispensáveis, removê-los após a prova ou transformá-los deliberadamente em observabilidade de produto, sem segredos ou PII.
- Não comprimir lógica genuinamente complexa só para reduzir linhas; concisão significa retirar estrutura sem valor, não esconder comportamento.

## Validar

- Executar os comandos oficiais relevantes.
- Antes de escrever um teste não trivial, nomear qual mutação ou defeito de produção ele deve detectar e derivar o resultado esperado independentemente da implementação testada.
- Para correção de bug, quando viável, observar o teste de regressão falhar pela causa esperada antes da mudança e passar depois; registrar quando o estado anterior não puder ser executado.
- Rodar primeiro o teste que reproduz, depois a suíte proporcional ao risco.
- Verificar lint, typecheck, build, análise estática ou auditoria de dependências quando existirem e forem pertinentes.
- Revisar diff e confirmar que alterações preexistentes foram preservadas.
- Mapear cada alegação para a evidência adequada: teste não substitui build; lint não substitui execução; uma suíte verde não substitui o requisito. Reexecutar a evidência depois da última mudança relevante.
- Em tarefa de fluxo, usar `validada`, `validação parcial`, `bloqueada`, `superada` ou `falhou`; edição ou checklist marcado não significam conclusão.
- Não afirmar sucesso sem execução. Informar comando, resultado e tudo que não pôde ser testado.

## Contrato de saída

Para análise, entregar achados ordenados por impacto com arquivo/linha, evidência, classificação, impacto, correção e validação.

Para implementação, entregar causa, tarefa/requisito de origem quando houver, mudança mínima, arquivos alterados, teste de regressão, comandos executados, resultados, estado da tarefa, limitações e riscos restantes.

Cada linha alterada deve estar ligada ao pedido ou a uma consequência necessária. Remover somente órfãos criados pela mudança atual; dívida preexistente deve ser relatada, não absorvida silenciosamente.

Nunca detectar, atribuir nem especular sobre autoria ou proveniência. Usar somente classificações observáveis como “defeito confirmado”, “code smell”, “padrão genérico”, “inconsistência” ou “evidência insuficiente”.
