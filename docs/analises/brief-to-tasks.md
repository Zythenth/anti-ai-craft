# Análise da unidade de decomposição de brief em tarefas

## Resumo executivo

A unidade externa oferece uma ideia útil e ainda incompleta no plugin: transformar um brief em uma sequência executável de entregas verticais, cada uma com resultado observável. O plugin já é forte em leitura do contexto, preservação de escopo, critérios mensuráveis, validação por evidência, estados de interface, testes sensíveis e gates de remediação. A principal lacuna não está em “planejar mais”, mas em ligar essas capacidades a um formato explícito de tarefa com dependências, prova de conclusão e estado persistente.

A incorporação recomendada não cria uma sexta skill, não renomeia as cinco existentes e não impõe um caminho fixo de pastas. O comportamento deve entrar de forma distribuída:

- `$anti-ai-design` converte brief e inventário de interface em fatias de produto;
- `$anti-ai-code` converte requisitos e invariantes em mudanças pequenas com prova própria;
- `$anti-ai-audit` produz um mapa de cobertura e uma ordem sugerida de remediação sem editar;
- `$anti-ai-remediate` transforma IDs aprovados em lotes seguros, preservando gates;
- `$anti-ai-security` injeta dependências e critérios adversariais nas fatias afetadas.

O ganho esperado é um plano menor, executável e auditável. O risco principal é gerar listas longas que parecem precisas, mas não correspondem ao repositório nem demonstram conclusão. Por isso, toda tarefa proposta deve carregar evidência de origem, resultado verificável e critério de interrupção.

## Inventário lido

### Unidade externa

| Item | Quantidade | Conteúdo observado |
|---|---:|---|
| Arquivo principal de skill | 1 | Descoberta de brief, inspeção do frontend, classificação de componentes, decomposição, ordenação e gravação de checklist |
| Referências adicionais | 0 | Não há material separado para segurança, código, critérios de aceite ou persistência |
| Configuração de agente | 0 | Não há metadados próprios de interface |
| Scripts, templates ou assets | 0 | O modelo de saída está embutido no arquivo principal |

### Plugin atual

| Skill | Arquivo principal | Referências | Configuração de agente | Capacidades mais relevantes para esta análise |
|---|---:|---:|---:|---|
| `anti-ai-design` | 1 | 6 | 1 | brief, inventário, contrato de direção, estados, responsividade, acessibilidade, evidência visual |
| `anti-ai-code` | 1 | 6 | 1 | escopo, invariantes, mudança mínima, regressão, ciclo mudança–prova, arquitetura e testes |
| `anti-ai-audit` | 1 | 3 | 1 | cobertura, ledger de candidatos, severidade, critérios de aceitação e relatório somente leitura |
| `anti-ai-remediate` | 1 | 3 | 1 | elegibilidade, plano, aplicação, verificação congelada, rollback e status por achado |
| `anti-ai-security` | 1 | 4 | 1 | modelo de ameaça, superfícies, controles, abuso, testes negativos/positivos e risco residual |

Foram examinados integralmente 32 arquivos do plugin: cinco arquivos principais, 22 referências e cinco configurações de agente. A comparação considera o conjunto inteiro, não apenas os arquivos principais.

## O que a unidade externa realmente acrescenta

### 1. Decomposição orientada a resultado

A contribuição central é exigir que uma tarefa resulte em algo que possa ser construído e conferido como unidade. Isso evita separar artificialmente marcação, estilo e interação de um mesmo comportamento. O plugin já prescreve mudanças pequenas e verificáveis, mas ainda não define com clareza a anatomia de uma tarefa de implementação.

Uma fatia útil deve atravessar somente as camadas necessárias para entregar um comportamento observável. Ela pode incluir UI, domínio, persistência e teste quando todos são necessários ao mesmo resultado. “Vertical” não significa tocar todas as camadas nem criar uma arquitetura completa; significa não declarar concluído um fragmento que ainda não produz valor ou prova.

### 2. Dependências explícitas

A unidade externa reconhece dependências, porém mistura três critérios de ordenação sem resolver conflitos: fundação, destaque visual e risco. A versão melhorada deve registrar dependências duras, dependências preferenciais e oportunidades de paralelismo. A ordem final deve vir do caminho crítico e do custo de descobrir tarde uma hipótese errada.

### 3. Inventário antes da criação

Há uma boa exigência de inspecionar componentes, páginas, tokens, convenções, testes e dependências antes de criar tarefas. O plugin já lê quase todas essas fontes, mas não consolida a classificação operacional:

- reutilizar sem mudança;
- alterar;
- criar;
- fora do escopo;
- desconhecido até obter evidência.

Essa classificação reduz tarefas duplicadas e impede que o plano invente componentes ou infraestrutura.

### 4. Critério de pronto por tarefa

A unidade externa pede verificabilidade visual, mas não define um padrão robusto de prova. O plugin já contém a base necessária: reprodução, oráculo independente, teste sensível, execução real, screenshots equivalentes, validação acessível e registro de limitações. Falta condensar isso em um contrato curto por tarefa.

### 5. Persistência do plano

Salvar o plano é útil para continuidade, handoff e retomada, mas um caminho fixo e uma gravação automática conflitam com os modos somente leitura e com a arquitetura de cada repositório. A persistência deve ser opcional, autorizada e adaptada às convenções locais. Na ausência de autorização, o plano deve permanecer apenas na resposta.

## Modelo recomendado de decomposição

### Entrada mínima

Antes de criar tarefas, reunir:

1. objetivo e resultado esperado;
2. fontes de verdade realmente lidas;
3. estado atual comprovado no repositório ou produto;
4. escopo incluído e excluído;
5. usuários, fluxos, dados, estados e invariantes afetados;
6. riscos materiais, decisões pendentes e limitações;
7. comandos oficiais e meios disponíveis de validação.

Quando houver múltiplos briefs, features ou alvos plausíveis, não escolher silenciosamente o arquivo mais recente. A seleção deve vir de uma referência explícita, de uma convenção inequívoca do projeto ou de confirmação do usuário.

### Anatomia de uma tarefa

Cada tarefa de implementação deve conter somente campos que orientem execução e prova:

| Campo | Conteúdo |
|---|---|
| Resultado | Comportamento ou capacidade observável entregue |
| Evidência de origem | Requisito, achado, tela, fluxo, arquivo ou decisão que justifica a tarefa |
| Escopo | Arquivos, componentes, boundaries ou áreas prováveis, sem fingir precisão antes da investigação |
| Estratégia | Reutilizar, alterar ou criar; preservar contratos relevantes |
| Dependências | Bloqueios reais, decisões pendentes e tarefas que podem ocorrer em paralelo |
| Estados e riscos | Casos de falha, extremos, acessibilidade e segurança aplicáveis |
| Critério de pronto | Condições observáveis e mensuráveis |
| Validação | Comando, cenário, captura ou inspeção que comprova cada condição |
| Estado | Pendente, em andamento, bloqueada, validada, validação parcial ou rejeitada |

Não exigir estimativa temporal fictícia, lista antecipada de cada arquivo ou detalhamento de implementação que só poderá ser conhecido durante a tarefa.

### Fatias verticais

Uma boa fatia:

- entrega um fluxo, estado ou controle reconhecível;
- reutiliza a arquitetura existente;
- inclui os testes e validações próprios daquele resultado;
- pode falhar ou ser revertida sem invalidar todo o plano;
- deixa explícito o que ainda não entrega;
- evita dependência artificial em tarefas de “estrutura”, “CSS”, “testes” ou “documentação” isoladas.

Uma tarefa horizontal só é aceitável quando produz um resultado necessário e verificável por si, como uma migração compatível, um token semântico realmente consumido, um contrato de API testado ou uma infraestrutura de teste indispensável. “Preparar a estrutura” sem consumidor imediato não deve entrar.

### Ordenação

Aplicar esta sequência de decisão:

1. respeitar dependências duras;
2. antecipar a hipótese de maior risco ou irreversibilidade;
3. entregar cedo uma fatia representativa que valide direção, arquitetura ou contrato;
4. agrupar tarefas que compartilham causa sem ocultar seus critérios independentes;
5. deixar polimento isolado para depois do comportamento principal;
6. indicar paralelismo apenas quando não houver disputa pelo mesmo contrato, arquivo crítico ou decisão.

Fundação não recebe prioridade automática. Tokens, shells, abstrações e infraestrutura entram cedo somente quando uma fatia imediata prova seu consumo.

### Critério de pronto

Uma tarefa está pronta apenas quando:

- o resultado descrito existe no caminho real;
- os estados e limites aplicáveis foram exercitados;
- a prova foi executada depois da última mudança relevante;
- o uso legítimo continua funcionando;
- o diff está limitado ao resultado;
- limitações e risco residual foram registrados;
- qualquer documentação persistente reflete o estado observado, não intenção futura.

Para UI, incluir viewport e estado; para código, reprodução e regressão; para auditoria, cobertura e disposição; para segurança, teste negativo e positivo; para remediação, status por ID e verificação congelada.

## Matriz comparativa

| Capacidade | Situação no plugin | Onde aparece hoje | Decisão |
|---|---|---|---|
| Ler brief e fontes de verdade antes do plano | Já temos | Design, código, auditoria e segurança | Manter |
| Inspecionar componentes, rotas, tokens, testes e dependências | Já temos | Design e código | Manter e condensar em inventário operacional |
| Classificar cada elemento como reutilizar, alterar, criar ou excluir do escopo | Parcial | Há preservação e inventário, sem classificação obrigatória | Incorporar |
| Criar tarefas como resultados verticais completos | Parcial | Mudança mínima e comportamento/estados existem, mas não há contrato de tarefa | Incorporar |
| Ligar tarefa a requisito, achado ou evidência | Parcial | Auditoria e remediação são fortes; planejamento de design/código é menos explícito | Incorporar |
| Declarar dependências duras, preferenciais e paralelismo seguro | Não temos | Há ordenação por causa/dependência, sem modelo comum | Incorporar |
| Ordenar por caminho crítico e risco de descoberta tardia | Parcial | Segurança e remediação priorizam risco; design prioriza direção | Incorporar |
| Validar cedo uma fatia representativa | Parcial | Contrato de direção e testes focados já apoiam isso | Tornar explícito |
| Definir critério de pronto e prova por tarefa | Parcial | Há critérios globais e por achado, não por tarefa genérica | Incorporar |
| Persistir estado do plano para retomada | Não temos | Relatórios registram estado, mas não um plano de entrega | Incorporar de forma opcional |
| Atualizar o plano a partir de evidência e mudanças de escopo | Parcial | Security atualiza threat model; remediation exige novo gate | Generalizar |
| Criar automaticamente um arquivo de tarefas | Não temos | Modos de planejamento podem ser read-only | Não incorporar como padrão |
| Usar caminho e nome fixos para o arquivo do plano | Não temos | Plugin respeita convenções locais | Não incorporar |
| Escolher automaticamente o brief mais recente | Não temos | Plugin pergunta quando decisão é material | Não incorporar |
| Presumir uma estrutura frontend específica | Não temos | Plugin é portátil entre stacks | Não incorporar |
| Exigir que toda tarefa caiba em uma sessão | Não temos | Mudanças pequenas são exigidas sem unidade temporal fixa | Não incorporar como absoluto |
| Exigir lista plana com profundidade universal | Não temos | O formato varia conforme a tarefa | Não incorporar como absoluto |
| Criar fases fixas de fundação, UI, estados e polimento | Parcial | As áreas existem, mas não como sequência obrigatória | Não incorporar como template universal |
| Encerrar com um comando ou skill de revisão de nome diferente | Não temos | Auditoria e validação já cobrem o handoff | Não incorporar; preservar nomes atuais |

## Recomendações por prioridade

### P0 — Definir um contrato comum de tarefa verificável

- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-code/references/review-workflow.md`
- **Instrução concreta:** adicionar uma seção curta de planejamento que exija resultado, origem, escopo, estratégia reutilizar/alterar/criar, dependências, critério de pronto e validação. Determinar que uma tarefa só seja criada quando estiver ligada a um requisito, achado ou risco observável.
- **Motivo:** fornece uma linguagem comum sem criar nova skill nem duplicar workflows.
- **Risco:** transformar qualquer correção pequena em burocracia.
- **Critério de aceitação:** em um pedido de implementação, cada tarefa planejada identifica um resultado observável e sua prova; campos não aplicáveis são omitidos, e não há tarefas de infraestrutura sem consumidor.

### P0 — Tornar fatias verticais explícitas no planejamento de design

- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md`
- **Instrução concreta:** no modo de planejamento, exigir que entregas combinem estrutura, conteúdo, comportamento, estados e validação apenas na medida necessária ao mesmo fluxo. Proibir a decomposição automática por tecnologia ou disciplina.
- **Motivo:** impede planos do tipo “fazer HTML, depois CSS, depois interação”, que atrasam validação real.
- **Risco:** gerar tarefas grandes demais.
- **Critério de aceitação:** cada fatia pode ser demonstrada isoladamente; quando exceder um fluxo coerente, é dividida por resultado do usuário, não por camada técnica.

### P0 — Acrescentar classificação operacional ao inventário

- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Instrução concreta:** após inventariar telas, rotas, componentes, tokens, mídia e estados, classificar itens relevantes como reutilização direta, alteração necessária, criação, fora de escopo ou desconhecido. Exigir evidência para a classificação.
- **Motivo:** evita criar tarefa para algo que já existe e expõe lacunas antes da implementação.
- **Risco:** inventário excessivo de todo o repositório.
- **Critério de aceitação:** somente elementos alcançáveis pelo escopo são classificados, e cada tarefa referencia pelo menos um item que será alterado ou criado.

### P0 — Preservar os gates da remediação dentro de qualquer plano

- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-remediate/references/remediation-protocol.md`
- **Instrução concreta:** representar cada lote de remediação como uma ou mais fatias ligadas a IDs aprovados, mantendo elegibilidade, plano sem edição, aplicação e verificação congelada. Proibir que uma lista de tarefas seja tratada como nova autorização.
- **Motivo:** um planejador genérico não pode enfraquecer aprovação, escopo ou reprodução.
- **Risco:** agrupar achados diferentes por conveniência.
- **Critério de aceitação:** todo lote mostra IDs, causa compartilhada quando houver, dependências, validação independente e estado final por ID.

### P0 — Incorporar segurança ao critério de pronto, não como fase final

- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-security/SKILL.md`
- **Instrução concreta:** quando uma fatia altera boundary, identidade, tenant, persistência, entrada externa, custo ou operação protegida, anexar desde o planejamento o controle esperado, um cenário adversarial e um cenário legítimo. Atualizar o modelo de ameaça quando a execução revelar mudança material.
- **Motivo:** evita uma tarefa tardia e genérica de “revisar segurança”.
- **Risco:** aplicar checklist de segurança a tarefas sem superfície relevante.
- **Critério de aceitação:** somente fatias com risco aplicável recebem requisitos de segurança, e sua conclusão inclui teste negativo, positivo e risco residual.

### P1 — Registrar dependências com semântica útil

- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-code/references/review-workflow.md`
- **Instrução concreta:** distinguir bloqueio duro, ordem preferencial e paralelismo seguro. Ordenar por caminho crítico, risco de descoberta tardia e valor de uma primeira fatia representativa.
- **Motivo:** “dependência primeiro” é insuficiente quando fundação, risco e feedback visual competem.
- **Risco:** simular precisão sem conhecer implementação.
- **Critério de aceitação:** toda dependência informa o que precisa estar verdadeiro; itens sem relação causal não são marcados como bloqueadores.

### P1 — Converter próximos passos da auditoria em lotes comprováveis

- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-audit/references/report-template.md`
- **Instrução concreta:** ampliar “Próximos passos” com uma tabela opcional contendo IDs, resultado do lote, dependências, risco, critério de aceite e validação proposta, sem alterar o caráter somente leitura.
- **Motivo:** facilita o handoff para remediação sem corrigir nem pré-aprovar achados.
- **Risco:** o relatório sugerir uma implementação única quando existem decisões de produto.
- **Critério de aceitação:** a tabela separa ordem recomendada de autorização e marca alternativas ou decisões pendentes.

### P1 — Tornar a prova parte do estado da tarefa

- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-remediate/references/validation-checklist.md`
- **Instrução concreta:** exigir que uma tarefa só passe de “implementada” para “validada” quando suas evidências forem reexecutadas após a última mudança relevante. Disponibilizar estados separados para bloqueio e validação parcial.
- **Motivo:** evita checklists marcados apenas porque o código foi escrito.
- **Risco:** duplicar o status por ID já existente.
- **Critério de aceitação:** o status da tarefa deriva do status dos IDs e das provas, sem criar uma segunda fonte de verdade conflitante.

### P1 — Planejar acessibilidade por fatia

- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-design/references/accessibility-baseline.md`
- **Instrução concreta:** adicionar orientação para anexar a cada fatia interativa somente os checks acessíveis correspondentes aos widgets e estados que ela introduz ou altera; manter um passe integrado ao final.
- **Motivo:** reduz a chance de acessibilidade virar polimento posterior.
- **Risco:** omitir requisitos transversais ao validar apenas componentes isolados.
- **Critério de aceitação:** cada fatia cobre seu teclado, foco, semântica e mensagens, e o fluxo completo ainda recebe validação integrada.

### P1 — Proibir conclusão horizontal sem consumidor

- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-code/references/architecture-antipatterns.md`
- **Instrução concreta:** registrar como sinal de planejamento frágil uma tarefa de abstração, tokens, configuração, estrutura ou documentação declarada pronta sem consumidor ou comportamento comprovado no mesmo incremento ou no imediatamente dependente.
- **Motivo:** estende o teste de remoção ao planejamento.
- **Risco:** impedir fundação legítima como migração ou contrato compartilhado.
- **Critério de aceitação:** exceções apresentam consumidor conhecido, dependência real e prova própria.

### P2 — Persistir planos sem impor arquivo universal

- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md` e `plugins/anti-ai-craft/skills/anti-ai-code/SKILL.md`
- **Instrução concreta:** permitir salvar um plano apenas quando o usuário pedir ou quando a convenção do projeto autorizar escrita. Usar o caminho já adotado pelo repositório; se não houver convenção, confirmar o destino. Em modo somente leitura, entregar o plano na resposta.
- **Motivo:** possibilita retomada sem violar autorização nem poluir projetos.
- **Risco:** criar documento redundante que diverge de issue tracker ou SDD.
- **Critério de aceitação:** o local e a autoridade do plano ficam explícitos; não existe gravação automática nem caminho presumido.

### P2 — Definir atualização e encerramento do plano

- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-code/references/review-workflow.md`
- **Instrução concreta:** ao surgir nova evidência, atualizar dependências, critérios ou estado; não reescrever silenciosamente tarefas já validadas. Registrar divisão, substituição, bloqueio ou rejeição com motivo. Ao final, reconciliar plano, diff e validações.
- **Motivo:** um checklist estático perde valor assim que a implementação descobre algo novo.
- **Risco:** histórico verboso.
- **Critério de aceitação:** mudanças materiais no plano têm motivo curto; itens obsoletos não permanecem como concluídos.

### P2 — Ajustar os prompts de interface sem renomear skills

- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/*/agents/openai.yaml`
- **Instrução concreta:** somente após os workflows internos serem atualizados, mencionar nos prompts existentes a criação de um plano verificável quando o pedido incluir planejamento. Manter `name`, nomes de invocação e política de chamada explícita.
- **Motivo:** melhora descoberta do novo comportamento sem quebrar compatibilidade.
- **Risco:** prompts curtos ficarem genéricos ou sugerirem edição automática.
- **Critério de aceitação:** cada prompt continua indicando o modo e os limites da skill; nenhuma nova invocação é criada.

## Persistência e continuidade

O plano persistido deve ser uma projeção do trabalho, não uma segunda especificação. Para evitar divergência:

- registrar a fonte de verdade de cada tarefa;
- usar IDs estáveis apenas quando já existirem em requisito ou achado;
- não copiar requisitos extensos para dentro do plano;
- atualizar estado somente após evidência;
- manter decisões pendentes separadas de tarefas executáveis;
- registrar bloqueios com condição de desbloqueio;
- reconciliar o documento com o diff e os comandos antes do handoff;
- arquivar ou marcar como superado quando outro sistema assumir autoridade.

Formato mínimo sugerido:

| Estado | Resultado | Origem | Estratégia | Dependências | Pronto quando | Prova |
|---|---|---|---|---|---|---|
| pendente | comportamento observável | requisito ou ID | reutilizar/alterar/criar | condição real | critérios objetivos | comando ou cenário |

Não adicionar porcentagem de progresso calculada a partir da quantidade de itens. Tarefas variam em risco e escopo, e uma porcentagem assim produz precisão falsa.

## Como evitar planejamento excessivo

Aplicar estes limites:

1. **Planejar até o próximo ponto de decisão.** Detalhar a primeira fatia e as dependências conhecidas; manter o restante no nível necessário para não bloquear escolhas futuras.
2. **Usar orçamento de estrutura.** Se o plano exige mais texto do que a mudança provável, reduzir campos e agrupar somente itens com o mesmo resultado.
3. **Não pré-escrever a implementação.** Evitar nomes de helpers, arquivos ou APIs ainda não verificados.
4. **Não criar tarefa para cada arquivo.** Uma tarefa representa resultado; arquivos são escopo provável.
5. **Não duplicar gates.** Reutilizar critérios de auditoria, código, segurança e remediação já existentes.
6. **Não planejar dívida fora do pedido.** Registrar separadamente sem absorver no caminho crítico.
7. **Não impor cerimônia a mudança trivial.** Para uma correção localizada, uma única tarefa com causa, mudança e prova pode bastar.
8. **Parar diante de decisão material.** Não converter ambiguidade de produto, segurança ou identidade em subtarefas inventadas.

## Como evitar listas sem prova

Uma lista é inválida quando os itens apenas nomeiam atividades: “criar componente”, “adicionar testes”, “melhorar acessibilidade”, “revisar segurança” ou “polir responsividade”. Cada item deve responder:

- qual comportamento ficará diferente;
- qual evidência exige essa mudança;
- que condição observável representa conclusão;
- qual prova pode falhar;
- quais riscos e estados são aplicáveis;
- o que permanece fora do escopo.

Antes de aceitar uma tarefa, aplicar três testes:

1. **Teste de remoção:** se o item desaparecer, algum requisito, achado, risco ou prova fica sem cobertura?
2. **Teste de falsificação:** existe um cenário em que a tarefa parece pronta, mas o critério a reprovaria?
3. **Teste de consumidor:** qualquer fundação criada será usada por um fluxo concreto e próximo?

Se a resposta for “não” aos três, a tarefa provavelmente é decoração de planejamento.

## Compatibilidade e limites

- Manter os cinco nomes atuais e seus modos de invocação.
- Não criar uma invocação nova para planejamento.
- Não mudar skills somente leitura para modo de edição.
- Não tratar um plano como autorização para editar, instalar, fazer commit ou publicar.
- Não impor frontend, framework, estrutura de pastas ou ferramenta de issues.
- Não exigir uma lista completa quando o projeto pede investigação iterativa.
- Não transformar “vertical” em regra que obriga todas as camadas em toda tarefa.
- Não substituir gates de segurança, acessibilidade, auditoria ou remediação por um campo genérico de “QA”.

## Conclusão

A melhor parte da unidade externa é o foco em entregas independentes e verificáveis. O plugin já possui quase toda a disciplina necessária para tornar essa ideia mais segura do que a origem: evidência antes da afirmação, preservação de escopo, validação sensível, estados reais, segurança contextual e remediação por gates.

O trabalho recomendado é conectar essas peças por um contrato enxuto de tarefa e distribuí-lo entre as cinco skills. A prioridade deve ser: fatias verticais, classificação reutilizar/alterar/criar, dependências semânticas, critério de pronto com prova e persistência autorizada. Caminhos fixos, seleção automática do brief mais recente, fases universais e listas baseadas em tempo devem ficar de fora.
