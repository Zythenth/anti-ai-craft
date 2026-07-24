# Análise unitária: `grill-me`

## Escopo e conclusão

Esta análise compara a unidade `grill-me` com as cinco skills atuais do plugin. O plugin não foi alterado.

A contribuição mais útil da unidade é um protocolo de decisão orientado por dependências:

1. descobrir no repositório tudo que for verificável;
2. separar fatos de escolhas que pertencem ao usuário;
3. perguntar somente sobre decisões materiais ainda abertas;
4. incluir uma recomendação fundamentada em cada pergunta;
5. continuar trabalhando nos ramos independentes;
6. encerrar quando as decisões necessárias estiverem resolvidas, assumidas de forma segura ou registradas como bloqueio real.

O plugin já aplica grande parte dos passos 1 e 2 e contém gates fortes de evidência, escopo e autorização. A principal lacuna é tornar explícitos a árvore de decisões, a dependência entre perguntas, a origem de cada resposta e o critério de encerramento. Não é recomendável importar uma entrevista ilimitada ou transformar todas as cinco skills em interrogatórios.

## Inventário completo

### Unidade analisada

| Arquivo | Papel |
|---|---|
| unidade externa `grill-me/SKILL.md` | Metadados de ativação, exemplos de uso e instruções do fluxo de entrevista |

Não há `agents/openai.yaml`, `references/`, `scripts/` ou `assets/` nessa unidade.

### Plugin atual

#### `anti-ai-design`

| Arquivo | Papel observado |
|---|---|
| `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md` | Escopo, preparação, workflow, modos e contrato de saída |
| `plugins/anti-ai-craft/skills/anti-ai-design/agents/openai.yaml` | Nome, descrição curta, prompt padrão e invocação explícita |
| `plugins/anti-ai-craft/skills/anti-ai-design/references/accessibility-baseline.md` | Baseline normativo e matriz manual de acessibilidade |
| `plugins/anti-ai-craft/skills/anti-ai-design/references/design-antipatterns.md` | Sinais contextuais, falsos positivos e perguntas de crítica |
| `plugins/anti-ai-craft/skills/anti-ai-design/references/design-principles.md` | Modelo de decisão, composição, componentes, linguagem, conteúdo e responsividade |
| `plugins/anti-ai-craft/skills/anti-ai-design/references/direction-contract.md` | Mandato, tese, invariantes, referências, mídia, estados e produção |
| `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md` | Preflight, passes, captura, comparação, gate humano e relatório |
| `plugins/anti-ai-craft/skills/anti-ai-design/references/sources.md` | Hierarquia de evidência e critérios de aplicação |

#### `anti-ai-code`

| Arquivo | Papel observado |
|---|---|
| `plugins/anti-ai-craft/skills/anti-ai-code/SKILL.md` | Revisão e implementação delimitadas, evidência, validação e saída |
| `plugins/anti-ai-craft/skills/anti-ai-code/agents/openai.yaml` | Nome, descrição curta, prompt padrão e invocação explícita |
| `plugins/anti-ai-craft/skills/anti-ai-code/references/architecture-antipatterns.md` | Abstração, fragmentação, compatibilidade, API, performance e observabilidade |
| `plugins/anti-ai-craft/skills/anti-ai-code/references/code-antipatterns.md` | Contratos, falhas, estado, concorrência, segurança e UI implementada |
| `plugins/anti-ai-craft/skills/anti-ai-code/references/debugging-and-evidence.md` | Hipóteses falsificáveis, mudança/prova, oráculos e verificação de APIs |
| `plugins/anti-ai-craft/skills/anti-ai-code/references/review-workflow.md` | Gates de escopo, modelo do sistema, descoberta, correção, validação e relatório |
| `plugins/anti-ai-craft/skills/anti-ai-code/references/sources.md` | Regras de evidência e critérios de aplicação |
| `plugins/anti-ai-craft/skills/anti-ai-code/references/testing-antipatterns.md` | Sensibilidade dos testes, mocks, esperas, snapshots e execução honesta |

#### `anti-ai-audit`

| Arquivo | Papel observado |
|---|---|
| `plugins/anti-ai-craft/skills/anti-ai-audit/SKILL.md` | Auditoria estritamente somente leitura, baseline, cobertura e achados |
| `plugins/anti-ai-craft/skills/anti-ai-audit/agents/openai.yaml` | Nome, descrição curta, prompt padrão e invocação explícita |
| `plugins/anti-ai-craft/skills/anti-ai-audit/references/audit-checklist.md` | Cobertura por evidência, área e família |
| `plugins/anti-ai-craft/skills/anti-ai-audit/references/report-template.md` | Estrutura de achados, fechamento, cobertura, validações e próximos passos |
| `plugins/anti-ai-craft/skills/anti-ai-audit/references/severity-model.md` | Severidade, confiança, prioridade, classificação e calibragem |

#### `anti-ai-remediate`

| Arquivo | Papel observado |
|---|---|
| `plugins/anti-ai-craft/skills/anti-ai-remediate/SKILL.md` | Elegibilidade, planejamento, aplicação, verificação e saída por ID |
| `plugins/anti-ai-craft/skills/anti-ai-remediate/agents/openai.yaml` | Nome, descrição curta, prompt padrão e invocação explícita |
| `plugins/anti-ai-craft/skills/anti-ai-remediate/references/approval-gates.md` | Ações permitidas, nova aprovação, interrupção e conclusão |
| `plugins/anti-ai-craft/skills/anti-ai-remediate/references/remediation-protocol.md` | Protocolo completo e rollback |
| `plugins/anti-ai-craft/skills/anti-ai-remediate/references/validation-checklist.md` | Validação geral, dados, UI e handoff |

#### `anti-ai-security`

| Arquivo | Papel observado |
|---|---|
| `plugins/anti-ai-craft/skills/anti-ai-security/SKILL.md` | Modos, modelo de ameaça, descoberta, validação, correção e saída |
| `plugins/anti-ai-craft/skills/anti-ai-security/agents/openai.yaml` | Nome, descrição curta, prompt padrão e invocação explícita |
| `plugins/anti-ai-craft/skills/anti-ai-security/references/remediation-workflow.md` | Correção por boundary, rate limiting, preservação e validação |
| `plugins/anti-ai-craft/skills/anti-ai-security/references/security-checklist.md` | Controles contextuais e testes mínimos por risco |
| `plugins/anti-ai-craft/skills/anti-ai-security/references/sources.md` | Limites de evidência e corpus de controles |
| `plugins/anti-ai-craft/skills/anti-ai-security/references/validation-and-severity.md` | Registro, falsificação, severidade, deduplicação e gate de correção |

## Comportamento da unidade analisada

### Ativação

A unidade foi feita para situações em que o usuário pede contestação ou estresse de uma ideia, plano ou design. Seu foco é descoberta de decisões, não implementação, auditoria normativa ou correção.

### Fluxo observado

1. Receber uma ideia ou plano ainda incompleto.
2. Decompor o assunto em decisões relacionadas.
3. Percorrer os ramos em uma ordem que respeite dependências.
4. Investigar o projeto quando a resposta estiver em código, componentes, estilos ou tokens.
5. Perguntar ao usuário somente quando a decisão não puder ser resolvida pelo material existente.
6. Acompanhar cada pergunta com uma recomendação.
7. Continuar até haver entendimento suficiente entre usuário e agente.

### Árvore de decisão implícita

```text
decisão pendente
├─ a resposta é verificável no projeto?
│  ├─ sim → investigar e registrar a evidência
│  └─ não
├─ a resposta depende de outra decisão?
│  ├─ sim → resolver primeiro a dependência
│  └─ não
├─ a decisão muda materialmente produto, risco ou direção?
│  ├─ sim → perguntar com recomendação
│  └─ não → adotar pressuposto seguro e declará-lo
└─ há outros ramos independentes?
   ├─ sim → continuar enquanto aguarda ou registra a decisão
   └─ não → encerrar ou declarar bloqueio preciso
```

A unidade original contém os princípios centrais dessa árvore, mas não formaliza estados, formato do ledger, critério verificável de encerramento nem tratamento de bloqueios.

### Tipos de pergunta

| Tipo | Tratamento adequado |
|---|---|
| Fato do repositório | Ler arquivos, histórico, componentes, configuração, testes ou runtime; não perguntar |
| Convenção existente | Localizar precedentes e consumidores reais; não pedir preferência abstrata |
| Ambiguidade de baixo risco | Escolher o default mais coerente, declarar a suposição e continuar |
| Decisão de produto ou identidade | Perguntar, apresentar recomendação, alternativas e consequências |
| Contrato, segurança ou compatibilidade material | Perguntar antes de uma mudança que possa quebrar ou expor o sistema |
| Autorização para efeito externo ou destrutivo | Bloquear somente a ação dependente até autorização explícita |
| Informação externa indisponível | Registrar lacuna e continuar o que não depende dela |

### Saída atual

A unidade não define um artefato final estruturado. O resultado esperado é entendimento compartilhado obtido durante a conversa. Faltam campos para:

- decisões resolvidas;
- origem da resposta;
- dependências entre decisões;
- recomendação e alternativa;
- suposições adotadas;
- ramos ainda abertos;
- impacto do não esclarecimento;
- próximo passo executável;
- condição de encerramento.

### Limites atuais

Não estão explícitos:

- quantidade máxima de perguntas por rodada;
- diferença entre pergunta necessária e curiosidade;
- permissão para continuar em ramos independentes;
- critério para não repetir pergunta já respondida;
- limite de escopo da entrevista;
- tratamento de conflito entre repositório e declaração do usuário;
- diferença entre recomendação objetiva e preferência;
- proteção dos modos somente leitura;
- gates de autorização para edição, commit, push ou ações externas.

## Matriz comparativa

| Capacidade | Estado no plugin | Evidência atual | Decisão |
|---|---|---|---|
| Investigar o repositório antes de perguntar | **Já temos** | As cinco `SKILL.md` exigem leitura de fontes e estado pertinentes | Preservar |
| Examinar componentes, estilos e tokens antes de pedir direção visual | **Já temos** | `anti-ai-design` faz inventário e lê design system, tokens, código e assets | Preservar |
| Perguntar somente quando a resposta muda materialmente o resultado | **Já temos** | `anti-ai-design` limita perguntas materiais; `anti-ai-code` separa ambiguidade de baixo e alto risco | Generalizar com linguagem consistente |
| Resolver dependências entre decisões antes de perguntar | **Parcial** | Gates de remediação e modelo de ameaça têm ordem, mas não há árvore ou dependências registradas | Incorporar |
| Fornecer recomendação em cada pergunta material | **Não temos** | Há alternativas e trade-offs, mas não um contrato obrigatório por pergunta | Incorporar de forma fundamentada |
| Registrar origem da resposta: projeto, usuário, requisito ou suposição | **Parcial** | Há separação entre fato, inferência e desconhecido e rastreabilidade de fontes | Acrescentar origem e confiança ao ledger |
| Continuar ramos independentes sem esperar resposta | **Parcial** | A auditoria exige cobertura completa e código aceita suposições de baixo risco, mas o comportamento não é comum às cinco skills | Incorporar |
| Critério explícito de encerramento da entrevista | **Não temos** | Gates de conclusão existem por tarefa, não por saturação das decisões | Incorporar |
| Evitar repetir pergunta já resolvida | **Parcial** | O estado atual é revalidado em remediação e segurança, mas não existe registro conversacional uniforme | Incorporar |
| Manter perguntas e decisões no relatório | **Parcial** | Auditoria separa decisões pendentes; outras saídas citam aprovações e limitações | Incorporar somente quando houver decisões materiais |
| Entrevista persistente e sem limite | **Não incorporar** | Conflita com autonomia, economia de contexto e limite de duas ou três perguntas de design | Substituir por rodadas curtas e orientadas por impacto |
| Fazer perguntas sobre fatos já presentes no projeto | **Não incorporar** | Contradiz todas as cinco skills e as instruções do repositório | Investigar diretamente |
| Ativar implicitamente ao detectar uma ideia vaga | **Não incorporar** | As cinco skills preservam invocação explícita | Não mudar a política |
| Criar uma sexta skill ou renomear as cinco existentes | **Não incorporar** | O valor cabe como protocolo transversal; nova skill fragmentaria o fluxo | Preservar nomes, caminhos e compatibilidade |
| Exigir resposta do usuário antes de qualquer progresso | **Não incorporar** | Muitos ramos podem ser verificados ou executados de forma independente | Bloquear somente a ação dependente |
| Recomendar mesmo quando não há evidência suficiente | **Não incorporar** | Conflita com evidência, segurança e anti-alucinação | Recomendar apenas com base e confiança declaradas |

## Protocolo melhorado de perguntas não bloqueantes

### 1. Construir o ledger antes de perguntar

Registrar apenas decisões materiais:

| Campo | Conteúdo |
|---|---|
| ID | Identificador estável da decisão |
| Decisão | O que precisa ser definido |
| Depende de | IDs que precisam ser resolvidos antes |
| Origem possível | Projeto, requisito, usuário, ambiente externo ou suposição |
| Estado | Resolvida, assumida, aberta, bloqueante, não aplicável ou superada |
| Evidência | Arquivo, linha, comando, teste, tela ou contrato |
| Recomendação | Opção sugerida e motivo |
| Consequência | O que muda se outra opção for escolhida |
| Próximo passo | Trabalho que pode continuar agora |

Não registrar preferências triviais ou perguntas de curiosidade.

### 2. Pesquisar na ordem mais barata e confiável

1. instruções do projeto e pedido atual;
2. README, especificação e documentação;
3. configuração, manifestos e lockfiles;
4. código, componentes, tokens e callers;
5. testes e fixtures;
6. histórico Git quando esclarece intenção;
7. runtime ou comando somente leitura;
8. documentação oficial da versão exata, quando necessária;
9. usuário, apenas se a decisão continuar materialmente aberta.

### 3. Perguntar em rodada curta

Fazer uma pergunta por vez quando uma resposta muda a pergunta seguinte. Agrupar no máximo duas ou três quando forem independentes e o usuário puder respondê-las em conjunto.

Formato recomendado:

```text
Decisão:
O que encontrei:
Minha recomendação:
Alternativas e consequências:
Default seguro se você não tiver preferência:
O que consigo continuar sem esta resposta:
```

Não apresentar uma preferência como recomendação técnica. Quando a evidência for insuficiente, indicar confiança e explicar o que falta.

### 4. Não bloquear trabalho independente

- continuar leitura, inventário, diagnóstico e validação que não dependam da resposta;
- em análise, registrar a lacuna sem interromper toda a cobertura;
- em implementação, pausar apenas os arquivos ou comportamentos afetados;
- em remediação, não editar um ID bloqueado, mas continuar IDs aprovados e independentes;
- em segurança, marcar controle externo como dependente de infraestrutura e continuar outras superfícies;
- nunca usar silêncio do usuário como autorização para ação destrutiva, externa ou materialmente incompatível.

### 5. Encerrar com condição verificável

Encerrar o protocolo quando:

- toda decisão material estiver resolvida, assumida explicitamente, superada ou classificada como bloqueio;
- nenhuma pergunta restante mudar critérios de aceitação, segurança, compatibilidade, identidade, escopo ou autorização;
- o próximo passo puder ser executado e validado sem inventar requisito;
- o relatório indicar claramente qualquer risco residual.

## Recomendações por arquivo

### GRM-01 — Tornar explícito o gate de decisão no design

- **Prioridade:** P0
- **Arquivo atual exato:** `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md`
- **Instrução concreta:** ampliar o passo 6 de “Preparar o trabalho” para exigir um ledger curto das decisões materiais, pesquisar primeiro no projeto, ordenar perguntas por dependência, incluir recomendação e consequência e continuar ramos independentes. Manter o máximo atual de duas ou três perguntas por rodada.
- **Motivo:** design é a aplicação mais direta do protocolo e hoje controla a quantidade de perguntas, mas não sua estrutura nem dependência.
- **Risco:** aumentar o preâmbulo e tornar tarefas simples burocráticas.
- **Critério de aceitação:** em um projeto com tokens e componentes definidos, a skill não pergunta por paleta ou biblioteca; diante de conflito real de identidade, faz no máximo três perguntas, cada uma com evidência, recomendação, impacto e default seguro.

### GRM-02 — Registrar fechamento dos ramos de direção

- **Prioridade:** P1
- **Arquivo atual exato:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Instrução concreta:** acrescentar ao preflight uma tabela opcional de decisões com ID, dependência, origem, estado e evidência; no relatório, exigir somente decisões que alterem direção, produto ou risco. Definir encerramento quando nenhum ramo aberto alterar o contrato de direção ou os critérios de aceitação.
- **Motivo:** o workflow já cobre alternativas e gate humano, mas não mostra por que uma pergunta veio antes de outra nem se um ramo ficou aberto.
- **Risco:** duplicar o contrato de direção.
- **Critério de aceitação:** o ledger referencia o contrato em vez de repeti-lo e permite identificar, em uma leitura, quais decisões vieram do projeto, do usuário ou de uma suposição.

### GRM-03 — Separar descoberta técnica de escolha de contrato

- **Prioridade:** P0
- **Arquivo atual exato:** `plugins/anti-ai-craft/skills/anti-ai-code/SKILL.md`
- **Instrução concreta:** após o passo 4 de “Preparar”, adicionar a regra: fatos verificáveis devem ser investigados; ambiguidades de contrato, compatibilidade, comportamento ou segurança devem virar decisão com recomendação, alternativas e impacto; ambiguidades de baixo risco recebem suposição declarada. Permitir continuar investigação e mudanças independentes.
- **Motivo:** a skill já diferencia ambiguidades, mas ainda não orienta como perguntar nem como evitar que uma dúvida localizada paralise toda a tarefa.
- **Risco:** o agente recomendar uma API ou contrato por preferência.
- **Critério de aceitação:** a recomendação cita evidência local ou requisito; sem evidência suficiente, a skill apresenta a opção como hipótese e não edita o caminho dependente.

### GRM-04 — Ordenar decisões técnicas por dependência

- **Prioridade:** P1
- **Arquivo atual exato:** `plugins/anti-ai-craft/skills/anti-ai-code/references/review-workflow.md`
- **Instrução concreta:** em “Resolver escopo”, registrar decisões abertas e suas dependências; resolver primeiro contrato/invariante, depois boundary/API e somente então implementação. No relatório, listar decisões abertas que impediram prova ou mudança.
- **Motivo:** impede perguntas prematuras sobre implementação quando a decisão real ainda é de contrato.
- **Risco:** excesso de formalidade em correção localizada.
- **Critério de aceitação:** para bug simples sem ambiguidade, nenhum ledger é emitido; para duas interpretações de requisito, o workflow resolve a interpretação antes de discutir arquitetura.

### GRM-05 — Fazer perguntas de auditoria sem interromper cobertura

- **Prioridade:** P0
- **Arquivo atual exato:** `plugins/anti-ai-craft/skills/anti-ai-audit/SKILL.md`
- **Instrução concreta:** adicionar regra de que perguntas sobre produto, infraestrutura ou baseline devem incluir resposta recomendada e efeito sobre severidade/confiança, mas não interrompem famílias independentes. Apenas escopo ausente, alvo impossível de determinar ou autorização necessária para acesso externo podem bloquear a parte dependente.
- **Motivo:** a skill já exige continuar após o primeiro achado; o mesmo princípio deve valer para decisões abertas.
- **Risco:** emitir achado prematuro quando falta resposta.
- **Critério de aceitação:** candidato dependente de infraestrutura permanece como lacuna, enquanto a auditoria conclui outras áreas e não o promove a vulnerabilidade confirmada.

### GRM-06 — Estruturar decisões pendentes no relatório de auditoria

- **Prioridade:** P1
- **Arquivo atual exato:** `plugins/anti-ai-craft/skills/anti-ai-audit/references/report-template.md`
- **Instrução concreta:** transformar “Decisões pendentes e preferências” em tabela com ID, pergunta, origem pesquisada, dependência, recomendação, alternativas, impacto no relatório, estado e trabalho concluído independentemente.
- **Motivo:** o template atual separa decisões, mas não oferece rastreabilidade suficiente para retomar a auditoria sem repetir perguntas.
- **Risco:** confundir decisão pendente com achado.
- **Critério de aceitação:** IDs de decisão usam prefixo distinto dos achados e nunca entram na contagem de severidade.

### GRM-07 — Distinguir ausência de informação de ausência de aprovação

- **Prioridade:** P0
- **Arquivo atual exato:** `plugins/anti-ai-craft/skills/anti-ai-remediate/SKILL.md`
- **Instrução concreta:** antes de pedir informação, exigir busca no relatório, estado atual, código, testes e histórico pertinente. Se ainda faltar uma decisão material, perguntar com recomendação, risco e comportamento preservado; bloquear somente os IDs dependentes e continuar IDs aprovados independentes.
- **Motivo:** a remediação exige entrada suficiente, mas pode evitar perguntas redundantes e bloqueio de todo o lote.
- **Risco:** corrigir IDs em ordem que gere conflito com o ID bloqueado.
- **Critério de aceitação:** a skill verifica dependências entre IDs antes de prosseguir; um ID independente pode ser validado e corrigido, enquanto o bloqueado mantém estado explícito e nenhum arquivo relacionado é editado.

### GRM-08 — Classificar perguntas nos gates de aprovação

- **Prioridade:** P1
- **Arquivo atual exato:** `plugins/anti-ai-craft/skills/anti-ai-remediate/references/approval-gates.md`
- **Instrução concreta:** acrescentar três classes: descobrível no alvo, assumível sem alterar contrato e bloqueante por autorização/produto/risco. Exigir recomendação apenas nas classes de decisão; nunca tratar default sugerido como autorização implícita.
- **Motivo:** evita misturar falta de contexto técnico com consentimento necessário.
- **Risco:** uma classificação errada permitir mudança material sem aprovação.
- **Critério de aceitação:** commit, push, mudança destrutiva, migração e alteração ampla continuam bloqueados sem autorização específica, mesmo que exista uma recomendação.

### GRM-09 — Transformar o modelo de ameaça em árvore de decisões rastreável

- **Prioridade:** P0
- **Arquivo atual exato:** `plugins/anti-ai-craft/skills/anti-ai-security/SKILL.md`
- **Instrução concreta:** no modelo de ameaça, relacionar decisões por dependência entre ativo, ator, fronteira, entrada, controle, impacto e ambiente. Para configuração externa ou limiar de produto não verificável, perguntar com postura recomendada, base, impacto e confiança; continuar superfícies independentes.
- **Motivo:** segurança já possui o material mais próximo de uma árvore, mas não registra perguntas e recomendações como decisões retomáveis.
- **Risco:** uma postura conservadora ser apresentada como requisito universal.
- **Critério de aceitação:** a skill distingue requisito normativo, evidência local, hardening e decisão de produto; valores de rate limit não são inventados, e uma lacuna de gateway não encerra a revisão de autorização ou fluxo.

### GRM-10 — Incluir dependência e resposta recomendada no registro de segurança

- **Prioridade:** P1
- **Arquivo atual exato:** `plugins/anti-ai-craft/skills/anti-ai-security/references/validation-and-severity.md`
- **Instrução concreta:** adicionar ao registro de candidato os campos “depende de”, “decisão necessária”, “origem pesquisada”, “postura recomendada”, “efeito se não respondida” e “trabalho independente concluído”. Manter decisão pendente fora de vulnerabilidades confirmadas.
- **Motivo:** melhora retomada, falsificação e handoff sem reduzir o padrão de prova.
- **Risco:** misturar hipótese de controle com recomendação de correção.
- **Critério de aceitação:** todo candidato externo ou dependente de produto mostra claramente se a pergunta afeta confirmação, severidade, prioridade ou apenas hardening.

### GRM-11 — Preservar metadados e compatibilidade

- **Prioridade:** P0
- **Arquivos atuais exatos:** `plugins/anti-ai-craft/skills/anti-ai-design/agents/openai.yaml`, `plugins/anti-ai-craft/skills/anti-ai-code/agents/openai.yaml`, `plugins/anti-ai-craft/skills/anti-ai-audit/agents/openai.yaml`, `plugins/anti-ai-craft/skills/anti-ai-remediate/agents/openai.yaml` e `plugins/anti-ai-craft/skills/anti-ai-security/agents/openai.yaml`
- **Instrução concreta:** não alterar nomes, prompts padrão nem `allow_implicit_invocation` por causa desta unidade. O protocolo deve viver no corpo e nas referências das skills já existentes.
- **Motivo:** a melhoria é operacional e não cria uma nova capacidade pública; mudar ativação aumentaria colisões e quebraria expectativas.
- **Risco:** nenhum risco funcional se os metadados permanecerem coerentes com as `SKILL.md`.
- **Critério de aceitação:** os cinco nomes, display names, prompts padrão e política de invocação continuam idênticos após a implementação.

## Adaptação específica por skill

| Skill | O que perguntar | O que descobrir no repositório | O que pode bloquear |
|---|---|---|---|
| `anti-ai-design` | Identidade, mandato, prioridade de produto e trade-off visual material | componentes, tokens, assets, estados, padrões e comportamento responsivo | redesign amplo, identidade, navegação ou alternativa de produto |
| `anti-ai-code` | contrato ambíguo, compatibilidade pública e comportamento esperado | APIs instaladas, callers, testes, invariantes, convenções e histórico | contrato ou segurança que mudem a correção |
| `anti-ai-audit` | alvo/baseline realmente ambíguo e evidência externa necessária | escopo, merge-base, código, testes, runtime e controles locais | apenas a parte que não pode ser auditada com segurança ou evidência |
| `anti-ai-remediate` | IDs aprovados, trade-off de produto, risco e autoridade adicional | causa atual, reprodução, arquivos, regressões e dependências entre IDs | edição do ID dependente ou ação fora da autorização |
| `anti-ai-security` | ativos de negócio, impacto, limiares e controles externos não fornecidos | boundaries, auth, queries, configuração, CI, testes e caminhos de ataque | correção, rotação, produção, teste destrutivo ou confirmação que depende de infraestrutura |

## Regras que não devem ser incorporadas

1. Não entrevistar sem limite.
2. Não perguntar novamente algo já respondido pelo projeto ou pelo usuário.
3. Não transformar pergunta de preferência em bloqueio técnico.
4. Não criar dezenas de decisões para tarefa simples.
5. Não oferecer recomendação sem evidência, premissa e confiança.
6. Não usar default como consentimento para editar, publicar, rotacionar, migrar ou destruir.
7. Não alterar a natureza somente leitura da auditoria.
8. Não permitir que o protocolo de perguntas substitua reprodução, teste, screenshot, trace ou validação.
9. Não criar uma sexta skill, renomear pastas ou alterar gatilhos.
10. Não copiar exemplos, frases ou estrutura externa; manter vocabulário e arquitetura do plugin.

## Ordem recomendada de implementação

1. Aplicar GRM-01, GRM-03, GRM-05, GRM-07 e GRM-09 nas cinco `SKILL.md`.
2. Aplicar GRM-02, GRM-04, GRM-06, GRM-08 e GRM-10 às referências específicas.
3. Confirmar GRM-11 e revisar se nenhum metadata mudou.
4. Validar as cinco skills.
5. Fazer testes de cenário sem revelar ao executor as conclusões deste relatório:
   - resposta já disponível no repositório;
   - duas decisões com dependência;
   - decisão de baixo risco assumível;
   - decisão material realmente bloqueante;
   - dois ramos independentes, um deles bloqueado;
   - configuração externa ausente;
   - pedido de ação que exige autorização específica.
6. Rejeitar a revisão se houver pergunta redundante, bloqueio global desnecessário, recomendação sem base ou alteração de compatibilidade.

## Critério final de completude

A incorporação estará completa quando as cinco skills:

- pesquisarem antes de perguntar;
- perguntarem somente sobre decisão material que não possa ser descoberta;
- apresentarem recomendação, base, consequência e default seguro quando aplicável;
- registrarem dependências e origem da resposta;
- continuarem ramos independentes;
- tiverem condição explícita de encerramento;
- preservarem evidência, escopo, modo read-only e gates de autorização;
- mantiverem nomes, caminhos, prompts e invocação explícita atuais.
