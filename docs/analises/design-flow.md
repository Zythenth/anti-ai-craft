# Análise da unidade `design-flow`

## Escopo e método

Esta análise compara o fluxo externo de design com as cinco skills públicas atuais do plugin. O objetivo não é copiar sua redação, mas identificar mecanismos úteis, lacunas e integrações — inclusive avaliar uma orquestradora adicional — sem quebrar invocações, caminhos ou contratos já publicados.

O passe considerou:

- a sequência completa proposta pela unidade externa;
- as entradas, saídas, estados, gates, transições e falhas implícitas desse fluxo;
- a cobertura direta e transversal das cinco skills atuais;
- os controles atuais de autorização, evidência, acessibilidade, segurança, auditoria e remediação;
- compatibilidade com os nomes públicos `$anti-ai-design`, `$anti-ai-code`, `$anti-ai-audit`, `$anti-ai-remediate` e `$anti-ai-security`.

## Inventário completo do que foi lido

### Unidade externa

- unidade externa `design-flow/SKILL.md`

### Arquivos transversais externos

- documentação pública da unidade externa
- política de segurança da unidade externa
- manifesto da unidade externa
- entrada de marketplace da unidade externa

### Empacotamento público atual consultado para comparação

- `README.md`
- `plugins/anti-ai-craft/.codex-plugin/plugin.json`
- `.agents/plugins/marketplace.json`

### `anti-ai-design`

- `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md`
- `plugins/anti-ai-craft/skills/anti-ai-design/agents/openai.yaml`
- `plugins/anti-ai-craft/skills/anti-ai-design/references/accessibility-baseline.md`
- `plugins/anti-ai-craft/skills/anti-ai-design/references/design-antipatterns.md`
- `plugins/anti-ai-craft/skills/anti-ai-design/references/design-principles.md`
- `plugins/anti-ai-craft/skills/anti-ai-design/references/direction-contract.md`
- `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- `plugins/anti-ai-craft/skills/anti-ai-design/references/sources.md`

### `anti-ai-code`

- `plugins/anti-ai-craft/skills/anti-ai-code/SKILL.md`
- `plugins/anti-ai-craft/skills/anti-ai-code/agents/openai.yaml`
- `plugins/anti-ai-craft/skills/anti-ai-code/references/architecture-antipatterns.md`
- `plugins/anti-ai-craft/skills/anti-ai-code/references/code-antipatterns.md`
- `plugins/anti-ai-craft/skills/anti-ai-code/references/debugging-and-evidence.md`
- `plugins/anti-ai-craft/skills/anti-ai-code/references/review-workflow.md`
- `plugins/anti-ai-craft/skills/anti-ai-code/references/sources.md`
- `plugins/anti-ai-craft/skills/anti-ai-code/references/testing-antipatterns.md`

### `anti-ai-audit`

- `plugins/anti-ai-craft/skills/anti-ai-audit/SKILL.md`
- `plugins/anti-ai-craft/skills/anti-ai-audit/agents/openai.yaml`
- `plugins/anti-ai-craft/skills/anti-ai-audit/references/audit-checklist.md`
- `plugins/anti-ai-craft/skills/anti-ai-audit/references/report-template.md`
- `plugins/anti-ai-craft/skills/anti-ai-audit/references/severity-model.md`

### `anti-ai-remediate`

- `plugins/anti-ai-craft/skills/anti-ai-remediate/SKILL.md`
- `plugins/anti-ai-craft/skills/anti-ai-remediate/agents/openai.yaml`
- `plugins/anti-ai-craft/skills/anti-ai-remediate/references/approval-gates.md`
- `plugins/anti-ai-craft/skills/anti-ai-remediate/references/remediation-protocol.md`
- `plugins/anti-ai-craft/skills/anti-ai-remediate/references/validation-checklist.md`

### `anti-ai-security`

- `plugins/anti-ai-craft/skills/anti-ai-security/SKILL.md`
- `plugins/anti-ai-craft/skills/anti-ai-security/agents/openai.yaml`
- `plugins/anti-ai-craft/skills/anti-ai-security/references/remediation-workflow.md`
- `plugins/anti-ai-craft/skills/anti-ai-security/references/security-checklist.md`
- `plugins/anti-ai-craft/skills/anti-ai-security/references/sources.md`
- `plugins/anti-ai-craft/skills/anti-ai-security/references/validation-and-severity.md`

## Implicações transversais relevantes

### Processo

- O conjunto externo confirma que a orquestração é uma capacidade distinta das fases individuais. Isso favorece uma entrada explícita para a jornada completa em vez de fazer qualquer invocação de design percorrer todas as etapas.
- Persistência por feature resolve colisão e retomada, mas uma pasta fixa não deve prevalecer sobre convenções existentes do projeto. A necessidade real é um identificador estável e artefatos não sobrescritos.
- A detecção de design system, tokens, temas, componentes e dependências antes de criar UI coincide com o modelo atual e deve continuar central.
- “Mobile primeiro” com uma largura fixa, tema escuro obrigatório e seleção automática de uma filosofia visual são defaults prescritivos. O plugin atual está correto ao derivar breakpoints do conteúdo, exigir contexto para tema e usar direção dominante sem catálogo estético obrigatório.
- Uma lista de estilos nomeados pode ajudar conversa exploratória, mas não deve escolher identidade pelo usuário nem substituir evidência do produto.
- O fluxo externo permite uso individual das fases e uso orquestrado. A mesma separação deve ser preservada: jornada completa opt-in, skills especializadas utilizáveis de forma independente.

### Segurança

- Skills são dependências de instrução executadas por agentes locais. Mudanças nelas podem ampliar leitura, escrita, execução ou ações externas mesmo sem binário próprio; revisão de diff e validação de release são controles de cadeia de suprimentos.
- Atualizações não devem ser tratadas como confiáveis apenas por virem do branch padrão. O pacote público precisa de versão verificável, changelog objetivo e revisão antes de atualizar um ambiente sensível.
- Relatos de comportamento que possam induzir exfiltração, bypass de consentimento, ação destrutiva ou exposição de segredos precisam de um canal privado. O repositório atual não contém `SECURITY.md`; issue pública não é canal adequado para vulnerabilidade ainda não corrigida.
- Relatórios de segurança devem pedir apenas reprodução mínima e nunca solicitar segredo real. Material sensível deve ser reduzido, redigido e tratado fora de artefatos públicos.
- Limitações genéricas de modelos não são corrigidas por uma skill. O escopo do projeto deve ser comportamento de instruções, empacotamento e integrações que ele controla.
- A proteção atual por invocação explícita deve permanecer. Uma descrição boa para descoberta não deve ativar automaticamente um fluxo longo ou com escrita.

### Empacotamento

- O conjunto externo lista cada unidade separadamente no manifesto. O pacote atual aponta para o diretório de skills, o que reduz duplicação; se uma nova skill for criada, a descoberta pode continuar pelo diretório, mas README, versão, descrições e testes precisam refletir a sexta unidade.
- Metadados duplicados em manifesto e marketplace podem divergir. O marketplace atual mantém apenas descoberta e política, enquanto o manifesto carrega a descrição do pacote; essa separação é preferível.
- O manifesto atual e o README afirmam “cinco skills”. Criar `anti-ai-design-flow` exigiria atualizar ambos na mesma mudança e validar que o pacote realmente expõe seis skills.
- O repositório atual não possui arquivo de licença. Uma licença não deve ser copiada do conjunto externo; publicação e reutilização precisam de uma decisão própria do mantenedor.
- A atualização atual é manual, o que é mais seguro que seguir silenciosamente a revisão mais recente. Para releases públicas, um tag ou referência imutável melhora reprodução, mas a documentação não deve prometer pinning sem testar o fluxo real do Codex.
- A criação de uma orquestradora não requer novo app, MCP, hook, executável ou serviço. Qualquer uma dessas capacidades seria expansão separada de risco e escopo.

## Modelo da unidade externa

### Intenção

A unidade coordena uma jornada de design do esclarecimento inicial até a construção. Ela não tenta resolver cada disciplina internamente; em vez disso, encadeia capacidades especializadas e usa seus artefatos como memória entre fases.

### Entradas

Entradas explícitas ou pressupostas:

- pedido para começar um produto ou feature do zero;
- intenção de percorrer o processo completo;
- contexto do projeto;
- decisão sobre fases que podem ser puladas;
- feature em foco;
- artefatos de fases anteriores, se existirem;
- stack do projeto, necessária para materializar tokens;
- autorização para construir;
- aplicação executável e evidência visual, necessárias para a revisão final.

Entradas materiais não formalizadas:

- definição de pronto por fase;
- fonte de verdade que vence em caso de conflito;
- versão ou estado Git a que cada artefato se refere;
- critérios de segurança e acessibilidade antes da construção;
- política para artefato desatualizado;
- comportamento quando uma fase produz dúvidas que invalidam uma fase anterior.

### Sequência

O fluxo externo é uma máquina de estados linear com desvios controlados:

1. esclarecer decisões;
2. registrar intenção;
3. organizar informação e navegação;
4. estabelecer linguagem visual;
5. decompor a construção;
6. implementar em ordem;
7. revisar separadamente quando houver produto construído.

As fases de 1 a 6 formam a execução principal. A revisão é deliberadamente separada e depende de algo executável.

### Saídas

Saídas previstas:

- entendimento compartilhado, sem arquivo na primeira fase;
- documento de intenção;
- documento de arquitetura da informação;
- tokens no formato da stack;
- checklist ordenado de implementação;
- componentes e páginas construídos;
- relatório de revisão;
- screenshots por viewport, tema, página, componente e estado.

### Estado persistente

O estado é inferido pela existência de arquivos em uma pasta por feature. Os elementos essenciais são:

- identificador curto da feature;
- fases concluídas;
- artefatos presentes;
- dúvidas abertas;
- próxima fase;
- tarefas marcadas;
- existência de build revisável;
- revisão pedida ou não;
- evidência visual capturada.

Esse modelo permite retorno posterior, mas a conclusão é deduzida por nomes de arquivos. Não há metadado formal para distinguir arquivo iniciado, concluído, bloqueado, desatualizado ou substituído.

### Gates

Gates úteis:

- apresentar a jornada antes de começar;
- permitir saltos justificados;
- declarar a saída esperada antes de cada fase;
- concluir uma fase antes da próxima;
- verificar se uma saída altera a interpretação da fase seguinte;
- permitir pausa e retomada;
- implementar tarefas em ordem;
- não executar revisão final sem algo construído;
- pedir escolha da feature quando houver mais de uma.

Gates frágeis ou incompletos:

- confirmação humana antes de cada fase, independentemente do risco;
- confirmação humana após cada tarefa, independentemente do impacto;
- “arquivo existe” como substituto de critério de conclusão;
- inexistência de gate explícito de autorização antes da primeira edição;
- inexistência de gate de segurança antes de congelar arquitetura;
- inexistência de teste de atualidade entre artefato e código;
- inexistência de validação técnica antes de marcar tarefa como concluída;
- inexistência de tratamento para contradição entre brief, arquitetura, tokens e tarefas.

### Transições

Cada fase deveria receber a saída validada da anterior. As transições materiais são:

- entendimento → intenção registrada;
- intenção → estrutura e navegação;
- estrutura + identidade → tokens;
- intenção + estrutura + tokens → plano de build;
- plano aprovado → implementação;
- implementação verificável → revisão independente;
- revisão com achados → remediação aprovada.

O fluxo externo menciona a necessidade de observar efeitos da fase anterior, mas não define como invalidar, atualizar ou versionar saídas dependentes.

### Falhas e recuperação

Falhas tratadas:

- usuário pausa: resumir posição e próxima fase;
- múltiplas features: pedir qual deve ser retomada;
- revisão sem build: adiar;
- ausência de navegador: usar alternativa disponível ou solicitar evidência manual.

Falhas não tratadas de forma suficiente:

- skill de fase inexistente ou indisponível;
- artefato incompleto ou contraditório;
- artefato antigo em relação ao código;
- token incompatível com a stack;
- tarefa marcada como pronta sem build, teste ou execução;
- implementação que diverge do contrato aprovado;
- alteração arquitetural que invalida modelo de ameaça;
- falha parcial durante a escrita de um artefato;
- mudança de escopo no meio do fluxo;
- conflito com alterações preexistentes;
- ausência de conteúdo ou dados reais;
- build que passa, mas interface real não abre;
- screenshot sem rota, estado, viewport ou tema reproduzível.

## Comparação de cobertura

| Capacidade observada | Estado | Onde está hoje | Avaliação |
|---|---|---|---|
| Leitura do projeto antes de decidir | Já temos | As cinco `SKILL.md` | A cobertura atual é mais forte, pois inclui instruções, código, configuração, histórico e estado preexistente. |
| Esclarecer decisões materiais | Já temos | `anti-ai-design/SKILL.md`, `anti-ai-code/SKILL.md` | Já diferencia dúvidas materiais de pressupostos de baixo risco. |
| Contrato de direção antes do código | Já temos | `anti-ai-design/references/direction-contract.md` | É mais rigoroso que um brief genérico e inclui mandato, invariantes, mídia, estados e produção. |
| Jornada completa visível ao usuário | Parcial | `anti-ai-design/SKILL.md` | Há workflow interno, mas não um mapa de fases, estado atual, entrada, saída e definição de pronto. |
| Escolha de fases que podem ser puladas | Parcial | Modos e carregamento por necessidade | As referências são condicionais, porém não há gate explícito para pular fase com evidência suficiente. |
| Registro persistente de intenção | Parcial | Contrato de saída do design | O conteúdo é exigido, mas caminho, estado e retomada não são definidos. |
| Arquitetura da informação como entrega verificável | Parcial | Inventário de telas, rotas, fluxos e estrutura | Os elementos existem, mas não há artefato ou seção mínima que preserve mapa, entradas, saídas e navegação. |
| Tokens da stack como fase | Parcial | Cadeia `primitivo → semântico → componente` | A regra técnica é forte, mas não há saída de fase, migração, estado nem definição de pronto. |
| Plano ordenado de construção | Não temos | — | Não existe contrato mínimo de tarefas com dependências, aceite e prova. |
| Construção guiada por tarefas aprovadas | Parcial | Implementação autorizada em design e código | Há escopo e mudança mínima, mas não rastreabilidade entre tarefa de design e diff. |
| Marcar tarefa somente após prova | Parcial | Ciclo `mudança → prova` em código e remediação | A evidência existe, mas não está conectada a um estado persistente da tarefa. |
| Pausa e retomada | Não temos | — | Não há checkpoint com fase, artefatos, dúvidas, bloqueio e próxima entrada. |
| Múltiplas features independentes | Não temos | — | Não há política de seleção ou namespacing de artefatos de design. |
| Revisão de produto construído | Já temos | `anti-ai-design/references/review-workflow.md` | A cobertura atual é mais completa: runtime, viewports, estados, dois passes e gate humano. |
| Revisão separada da implementação | Parcial | Passes separados e `$anti-ai-audit` | Existe separação metodológica, mas o handoff após build não é explícito. |
| Screenshots rastreáveis | Parcial | Workflow visual e relatório de auditoria | Registra viewport, estado e tema, mas não estabelece convenção de localização ou índice de evidência. |
| Revisão somente quando existe evidência adequada | Parcial | Captura real exigida | Ainda falta distinguir formalmente crítica de plano, protótipo e validação final de runtime. |
| Acessibilidade em todas as fases | Já temos | Baseline de acessibilidade e workflows | Muito mais completa que a unidade externa. |
| Segurança antes e depois de decisões arquiteturais | Parcial | `anti-ai-security/SKILL.md` | O modelo de ameaça é forte, mas não está conectado aos gates do fluxo de design. |
| Auditoria read-only com IDs | Já temos | `anti-ai-audit` | Mais robusta que uma revisão apenas visual. |
| Remediação apenas de achados aprovados | Já temos | `anti-ai-remediate` | Mais segura que corrigir itens diretamente a partir do review. |
| Preservação de trabalho preexistente e Git | Já temos | Código, auditoria e remediação | Ausente no fluxo externo e bem coberta no plugin. |
| Falsificação e rejeição de falso positivo | Já temos | Auditoria, código e segurança | Cobertura atual superior. |
| Atualidade do artefato contra o código | Não temos | — | Nenhuma skill exige vínculo do artefato de design ao estado que ele descreve. |
| Invalidação de saídas dependentes | Não temos | — | Uma mudança no contrato não marca arquitetura, tokens ou tarefas como possivelmente obsoletos. |
| Gate de aprovação em toda transição | Não incorporar | — | Confirmação ritual em cada fase ou tarefa gera atrito e conflita com autonomia proporcional ao risco. |
| Dependência de várias skills externas com nomes fixos | Não incorporar | — | Criaria referências quebradas e alteraria o modelo público de cinco skills. |
| Estrutura fixa obrigatória para todo trabalho de design | Não incorporar | — | Componentes pequenos e manutenção local não precisam de um diretório documental completo. |
| Revisão visual restrita apenas a build final | Não incorporar | — | Wireframes e screenshots também podem ser revisados, desde que não sejam apresentados como prova de runtime. |
| Formato único de token | Não incorporar | — | A saída deve seguir a stack existente. |
| Browser específico como requisito | Não incorporar | — | A validação deve usar a capacidade real disponível e declarar limitações. |

## Decisão: incorporar ou criar `anti-ai-design-flow`

### Opção A — Incorporar tudo à `$anti-ai-design`

Vantagens:

- nenhum novo nome público;
- nenhuma nova pasta de skill;
- menor mudança de documentação e empacotamento;
- adequada se o fluxo continuar limitado a planejamento e execução de interface em uma única tarefa.

Desvantagens:

- mistura criação/revisão local com orquestração de longa duração;
- aumenta uma skill que já cobre pesquisa, planejamento, revisão e implementação;
- torna o gatilho ambíguo: “revisar uma tela” e “conduzir produto do zero à remediação” passam a compartilhar o mesmo contrato;
- dificulta coordenar segurança, código, auditoria e remediação sem transformar `$anti-ai-design` em dona das outras quatro skills;
- aumenta o risco de ativar fases, artefatos ou perguntas desnecessários em tarefas pequenas.

### Opção B — Criar `$anti-ai-design-flow`

Vantagens:

- torna a jornada completa explicitamente opt-in;
- preserva o foco e o comportamento das cinco skills atuais;
- oferece lugar próprio para estado, transições, retomada e handoffs;
- pode ler e aplicar os contratos atuais sem duplicar suas regras;
- permite evoluir o fluxo sem alterar o uso rotineiro de `$anti-ai-design`.

Desvantagens:

- adiciona uma sexta skill pública;
- exige atualizar README, versão, descrição do manifesto e validação de empacotamento;
- pode duplicar conteúdo se reescrever as cinco skills em vez de orquestrá-las;
- exige regras claras para não herdar autorização, não invocar implicitamente edições e não transformar toda tarefa em workflow.

### Recomendação

**Criar uma nova `$anti-ai-design-flow`, sem renomear ou substituir nenhuma skill existente.**

A razão decisiva é que o fluxo completo atravessa design, segurança, código, auditoria e remediação, enquanto `$anti-ai-design` deve continuar adequada a uma tela, revisão ou implementação visual delimitada. A nova skill deve conter somente a máquina de estados e os contratos de transição; as regras especializadas permanecem nas cinco skills atuais.

### Gatilhos da nova skill

Ativar somente por invocação explícita ou pedido inequívoco como:

- conduzir o fluxo completo de design;
- começar uma feature do zero e ir até implementação e revisão;
- retomar um fluxo de design persistido;
- coordenar direção, estrutura, build e validação de uma mesma feature.

Não ativar para:

- revisão de screenshot;
- correção visual local;
- criação de um componente isolado;
- revisão de código;
- auditoria ampla;
- correção de IDs;
- threat model isolado.

O arquivo `agents/openai.yaml` da nova skill deve manter `allow_implicit_invocation: false`.

### Limites da nova skill

- Planejamento não autoriza edição.
- Uma autorização não atravessa silenciosamente fases, skills ou ações externas.
- O fluxo lê cada contrato especializado necessário; não os resume em versões paralelas.
- Pular fase exige saída existente e atual, não apenas preferência.
- Checkpoint persistente é obrigatório somente no fluxo completo.
- Confirmação humana fica reservada a trade-off material, mudança de escopo, identidade, navegação, risco, edição ou ação externa.
- Auditoria continua read-only.
- Segurança não corrige sem autorização.
- Remediação continua dependente de IDs aprovados.
- Commit, push, deploy, rotação de segredo e mudança de produção continuam fora do fluxo sem autorização específica.
- A pasta `.design/` pode ser fallback, nunca imposição contra convenção existente.

### Critério de necessidade

Criar a nova skill quando o produto público pretende suportar pelo menos uma destas situações:

- retomada em outra tarefa ou sessão;
- três ou mais fases encadeadas;
- coordenação de duas ou mais skills atuais;
- múltiplas features com artefatos separados;
- handoff formal de implementação para auditoria e remediação.

Se o objetivo fosse apenas adicionar um checklist curto antes de implementar uma interface na mesma tarefa, a nova skill não seria necessária; uma seção interna em `$anti-ai-design` bastaria. Para o fluxo analisado, os requisitos de retomada e coordenação satisfazem o critério de criação.

### Arquivos previstos, sem criação nesta análise

- `plugins/anti-ai-craft/skills/anti-ai-design-flow/SKILL.md`
- `plugins/anti-ai-craft/skills/anti-ai-design-flow/agents/openai.yaml`
- referência própria de estado/transições somente se o `SKILL.md` ficar grande demais;
- atualizações em `README.md` e `plugins/anti-ai-craft/.codex-plugin/plugin.json`.

## Recomendações

Prioridades:

- **P0:** corrige lacuna de contrato, segurança ou rastreabilidade que pode produzir trabalho errado.
- **P1:** melhora continuidade, verificação ou integração sem alterar o propósito da skill.
- **P2:** melhora clareza operacional ou consistência do handoff.

### DF-01 — Encaminhar o fluxo completo para a orquestradora

- **Prioridade:** P0
- **Arquivo atual exato a alterar:** `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md`
- **Instrução concreta:** manter os modos atuais e acrescentar somente um handoff: quando o pedido for conduzir uma jornada completa e retomável, orientar a invocação explícita de `$anti-ai-design-flow`; não executar a máquina de estados inteira dentro de `$anti-ai-design`.
- **Motivo:** evita duplicar a orquestração e preserva o contrato enxuto da skill visual.
- **Risco:** criar dependência de uma skill ainda não instalada em versões antigas.
- **Critério de aceitação:** o handoff só aparece quando a nova skill existe no mesmo pacote; instalações anteriores continuam operando com os modos atuais.

### DF-02 — Formalizar critérios para pular fases

- **Prioridade:** P0
- **Arquivo previsto a criar:** `plugins/anti-ai-craft/skills/anti-ai-design-flow/SKILL.md`
- **Instrução concreta:** definir que uma fase pode ser pulada apenas quando sua saída necessária já existir, tiver fonte de verdade identificada e estiver atual para o escopo. Exigir leitura e validação leve do artefato existente; “já temos tokens” não basta se os componentes os contornam.
- **Motivo:** evita repetir trabalho sem aceitar como pronta uma base inexistente ou decorativa.
- **Risco:** o passe de validação virar auditoria completa antes de qualquer tarefa.
- **Critério de aceitação:** o registro de execução informa `executar`, `reusar`, `atualizar` ou `não aplicável` para cada fase e a evidência que sustenta a decisão.

### DF-03 — Criar um checkpoint retomável no contrato de direção

- **Prioridade:** P0
- **Arquivo atual exato a alterar:** `plugins/anti-ai-craft/skills/anti-ai-design/references/direction-contract.md`
- **Instrução concreta:** adicionar uma seção opcional de checkpoint com identificador de feature, escopo, mandato, fase atual, fases concluídas, artefatos, decisões, dúvidas abertas, bloqueio, próxima entrada necessária e estado do código usado como referência. Usar estados explícitos como `não iniciada`, `em andamento`, `bloqueada`, `concluída` e `superada`.
- **Motivo:** existência de arquivo não comprova conclusão e não permite saber se ele ainda descreve o código atual.
- **Risco:** gerar documentação administrativa para uma mudança pequena.
- **Critério de aceitação:** o checkpoint é obrigatório apenas no modo de fluxo completo ou quando o usuário pede retomada; ao reabrir o trabalho, a próxima fase pode ser determinada sem adivinhação.

### DF-04 — Definir invalidação entre fases

- **Prioridade:** P0
- **Arquivo atual exato a alterar:** `plugins/anti-ai-craft/skills/anti-ai-design/references/direction-contract.md`
- **Instrução concreta:** declarar dependências entre contrato, estrutura, tokens, plano e implementação. Quando uma decisão anterior muda, marcar as saídas dependentes como “revalidar” em vez de atualizá-las silenciosamente ou considerá-las concluídas.
- **Motivo:** uma alteração de navegação ou de identidade pode invalidar tarefas e tokens mesmo que os arquivos continuem presentes.
- **Risco:** cascata de revalidação maior que a mudança real.
- **Critério de aceitação:** toda mudança material registra quais artefatos foram afetados e limita a revalidação às dependências reais.

### DF-05 — Tornar a arquitetura da informação uma saída mínima

- **Prioridade:** P1
- **Arquivo atual exato a alterar:** `plugins/anti-ai-craft/skills/anti-ai-design/references/direction-contract.md`
- **Instrução concreta:** adicionar ao contrato, quando o escopo tiver mais de uma tela, rota ou estado navegável, uma seção estrutural com pontos de entrada, destinos, tarefas, relações, navegação, estados sem acesso e fluxo de recuperação. Permitir arquivo separado apenas quando o volume justificar.
- **Motivo:** o inventário atual localiza telas e rotas, mas não preserva a lógica que liga estrutura à tarefa.
- **Risco:** duplicar documentação de rotas já existente.
- **Critério de aceitação:** a saída referencia a fonte de verdade existente e documenta apenas decisões ou lacunas não representadas no código/configuração.

### DF-06 — Especificar uma definição de pronto para tokens

- **Prioridade:** P1
- **Arquivo atual exato a alterar:** `plugins/anti-ai-craft/skills/anti-ai-design/references/design-principles.md`
- **Instrução concreta:** complementar a seção de tokens com um gate de conclusão: formato compatível com a stack, papéis semânticos definidos, consumidores reais identificados, estados críticos cobertos, valores soltos conhecidos, migração delimitada e verificação em tema/contraste. Não exigir arquivo novo se o sistema atual já for a fonte de verdade.
- **Motivo:** a cadeia técnica existente é boa, porém não diz quando a fase está pronta para alimentar o plano de build.
- **Risco:** transformar refino de um componente em migração completa de tokens.
- **Critério de aceitação:** o gate declara cobertura do escopo e dívida fora dele; não exige eliminar todo valor legado.

### DF-07 — Produzir plano de build verificável

- **Prioridade:** P0
- **Arquivo atual exato a alterar:** `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md`
- **Instrução concreta:** quando o usuário pedir um plano de build ou a orquestradora encaminhar essa fase, exigir unidades pequenas com objetivo, dependências, arquivos ou superfícies prováveis, comportamento preservado, critério de aceitação, prova esperada e risco. Não começar a editar se o plano depender de decisão material em aberto.
- **Motivo:** a principal lacuna entre direção e implementação é a ausência de uma decomposição rastreável.
- **Risco:** antecipar arquivos antes de compreender a arquitetura real.
- **Critério de aceitação:** itens podem apontar superfícies em vez de arquivos quando ainda não confirmados; nenhum caminho é inventado e cada tarefa possui uma prova independente.

### DF-08 — Consumir o plano de design no código

- **Prioridade:** P0
- **Arquivo atual exato a alterar:** `plugins/anti-ai-craft/skills/anti-ai-code/SKILL.md`
- **Instrução concreta:** quando a mudança vier de um fluxo de design, localizar e ler o contrato, a estrutura, os tokens e o plano aprovados; mapear cada alteração ao item e critério correspondente. Se o código atual contradisser o artefato, parar a implementação daquele item e registrar a divergência em vez de escolher silenciosamente um lado.
- **Motivo:** fecha a transição entre decisão visual e implementação verificável.
- **Risco:** confiar em documento desatualizado.
- **Critério de aceitação:** o relatório final lista tarefa → arquivos alterados → evidência; divergências foram resolvidas ou permanecem bloqueadas.

### DF-09 — Não concluir tarefa apenas porque o código foi escrito

- **Prioridade:** P0
- **Arquivo atual exato a alterar:** `plugins/anti-ai-craft/skills/anti-ai-code/references/review-workflow.md`
- **Instrução concreta:** adicionar um gate para tarefas de fluxo: marcar concluída somente depois de prova proporcional, revisão do diff e confirmação de que os critérios de design e comportamento aplicáveis foram exercitados. Falha de ambiente deve resultar em validação parcial, não em conclusão plena.
- **Motivo:** o fluxo externo acompanha tarefas, mas não define um gate técnico de conclusão; o plugin já possui os controles necessários.
- **Risco:** bloquear progresso por validações externas indisponíveis.
- **Critério de aceitação:** cada tarefa termina em `validada`, `validação parcial`, `bloqueada`, `superada` ou `falhou`, com comando/evidência ou limitação.

### DF-10 — Adicionar gate de segurança antes de congelar estrutura

- **Prioridade:** P0
- **Arquivo atual exato a alterar:** `plugins/anti-ai-craft/skills/anti-ai-security/SKILL.md`
- **Instrução concreta:** acrescentar um modo de apoio a planejamento que, quando explicitamente invocado durante o fluxo, produza um checkpoint mínimo de ativos, dados, atores, tenants, fronteiras, operações caras, ações destrutivas e histórias de abuso antes de aprovar estrutura e tarefas. Reusar o modelo completo atual quando o risco exigir.
- **Motivo:** autorização, isolamento, privacidade e custo são decisões de arquitetura, não acabamentos a descobrir depois do build.
- **Risco:** converter todo projeto visual em revisão de segurança ampla.
- **Critério de aceitação:** o checkpoint usa apenas categorias aplicáveis e separa `resolvido`, `decisão pendente`, `depende de infraestrutura` e `não aplicável`.

### DF-11 — Propagar mudanças de design ao modelo de ameaça

- **Prioridade:** P0
- **Arquivo atual exato a alterar:** `plugins/anti-ai-craft/skills/anti-ai-security/references/security-checklist.md`
- **Instrução concreta:** incluir no gatilho de atualização do modelo de ameaça mudanças em arquitetura da informação que criem nova entrada, papel, ação, estado, integração, exposição de dado ou operação cara. Uma troca apenas estética não deve acionar revisão ampla.
- **Motivo:** o modelo atual já exige atualização por mudanças arquiteturais; falta tornar explícita a origem em decisões de produto e fluxo.
- **Risco:** falsos gatilhos para alterações puramente visuais.
- **Critério de aceitação:** o checklist distingue mudança cosmética de mudança que altera superfície, boundary, ator, ativo ou custo.

### DF-12 — Criar gate de prontidão para revisão final

- **Prioridade:** P0
- **Arquivo atual exato a alterar:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Instrução concreta:** antes de apresentar uma revisão como validação final, exigir alvo executável, rota ou entrada conhecida, estado/dados reproduzíveis, viewport/tema definidos e critérios anteriores disponíveis. Se faltar algo, classificar o passe como revisão de plano, estática ou de protótipo e declarar o que ele não prova.
- **Motivo:** impede que screenshot isolado ou inspeção de código seja tratado como evidência de runtime.
- **Risco:** reduzir a utilidade de feedback precoce.
- **Critério de aceitação:** feedback precoce continua permitido, mas o relatório identifica claramente o nível de evidência e não emite conclusão de runtime sem execução.

### DF-13 — Validar a cadeia de decisões na revisão

- **Prioridade:** P1
- **Arquivo atual exato a alterar:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Instrução concreta:** adicionar um passe de coerência entre tarefa, contrato, estrutura, tokens, plano e implementação. Para cada desvio, determinar se é defeito, decisão posterior válida, artefato superado ou lacuna de prova.
- **Motivo:** comparar apenas “antes e depois” não detecta deriva entre as fases.
- **Risco:** reportar documentação antiga como falha do produto.
- **Critério de aceitação:** toda divergência recebe disposição e a fonte de verdade vigente é explicitada.

### DF-14 — Fazer a auditoria reconhecer artefatos do fluxo

- **Prioridade:** P0
- **Arquivo atual exato a alterar:** `plugins/anti-ai-craft/skills/anti-ai-audit/SKILL.md`
- **Instrução concreta:** quando houver artefatos de design, tratá-los como fontes candidatas, verificar autoridade e atualidade, e construir uma matriz requisito/decisão → implementação → evidência. Não presumir que o artefato vence o código nem que um arquivo presente está concluído.
- **Motivo:** a auditoria é o melhor ponto de revisão independente entre build e remediação.
- **Risco:** ampliar escopo de auditorias que não são visuais.
- **Critério de aceitação:** a leitura de artefatos só ocorre quando eles intersectam o escopo e o relatório diferencia desvio de implementação, documento superado e ambiguidade.

### DF-15 — Registrar cobertura do fluxo no relatório

- **Prioridade:** P1
- **Arquivo atual exato a alterar:** `plugins/anti-ai-craft/skills/anti-ai-audit/references/report-template.md`
- **Instrução concreta:** adicionar uma seção opcional com feature, fase alegada, artefatos examinados, estado de cada um, vínculo com código e áreas do fluxo não verificadas.
- **Motivo:** o relatório atual registra cobertura técnica, mas não deixa evidente se brief, estrutura, tokens e tarefas foram realmente comparados.
- **Risco:** tornar o template maior em auditorias sem design.
- **Critério de aceitação:** a seção é omitida ou marcada não aplicável quando não há fluxo de design no escopo.

### DF-16 — Preservar IDs de revisão no handoff de remediação

- **Prioridade:** P0
- **Arquivo atual exato a alterar:** `plugins/anti-ai-craft/skills/anti-ai-remediate/SKILL.md`
- **Instrução concreta:** aceitar achados de revisão visual que usem o mesmo contrato de IDs da auditoria e exigir vínculo com fase, artefato, viewport/estado e critério de aceitação. Não atualizar artefatos de design automaticamente; fazê-lo somente se estiver dentro do ID aprovado ou for consequência necessária declarada.
- **Motivo:** conecta revisão a correção sem transformar recomendações abertas em edições automáticas.
- **Risco:** duplicar IDs ou misturar preferência visual com defeito aprovado.
- **Critério de aceitação:** cada ID preserva classificação, evidência e status; preferência continua fora da remediação automática.

### DF-17 — Verificar consistência do estado após a remediação

- **Prioridade:** P1
- **Arquivo atual exato a alterar:** `plugins/anti-ai-craft/skills/anti-ai-remediate/references/validation-checklist.md`
- **Instrução concreta:** adicionar, quando houver fluxo de design, verificação de que código, evidência, status da tarefa e artefatos afetados não se contradizem. Se atualizar documentação não estiver autorizada, registrar a pendência sem editar.
- **Motivo:** corrigir o código e deixar a tarefa como bloqueada ou o contrato como incompatível prejudica a retomada.
- **Risco:** expandir uma correção pequena para documentação ampla.
- **Critério de aceitação:** somente artefatos diretamente afetados são considerados; alterações fora do escopo viram pendência explícita.

### DF-18 — Padronizar o handoff de pausa e retomada

- **Prioridade:** P1
- **Arquivo previsto a criar:** `plugins/anti-ai-craft/skills/anti-ai-design-flow/SKILL.md`
- **Instrução concreta:** quando o usuário parar no modo de fluxo completo, entregar um checkpoint curto com fase atual, saídas concluídas, decisões, perguntas abertas, bloqueios, arquivos relevantes e próxima ação segura.
- **Motivo:** permite continuar sem reler ou reinterpretar todo o histórico da conversa.
- **Risco:** o resumo se tornar outra fonte de verdade divergente.
- **Critério de aceitação:** o checkpoint aponta para os artefatos vigentes e não duplica seu conteúdo integral.

### DF-19 — Usar gates materiais, não confirmação ritual

- **Prioridade:** P1
- **Arquivo previsto a criar:** `plugins/anti-ai-craft/skills/anti-ai-design-flow/SKILL.md`
- **Instrução concreta:** pedir confirmação apenas para mudança material de direção, identidade, navegação, escopo, autorização de edição ou trade-off de produto. Entre fases sem decisão pendente, avançar e relatar o checkpoint; entre tarefas, executar a prova prevista sem interromper por ritual.
- **Motivo:** preserva controle humano onde ele importa sem tornar um fluxo longo impraticável.
- **Risco:** avançar além da expectativa do usuário em tarefas abertas.
- **Critério de aceitação:** toda transição que pode causar mudança externa continua exigindo autorização aplicável; passos read-only ou já autorizados não pedem consentimento repetido.

### DF-20 — Tornar o handoff entre as cinco skills explícito

- **Prioridade:** P2
- **Arquivo previsto a criar:** `plugins/anti-ai-craft/skills/anti-ai-design-flow/SKILL.md`
- **Instrução concreta:** no encerramento de cada fase, emitir um mapa opcional de próximos modos: implementação delimitada em `$anti-ai-code`, revisão independente em `$anti-ai-audit`, avaliação de abuso em `$anti-ai-security` e correção de IDs aprovados em `$anti-ai-remediate`. Não invocar automaticamente skills com política explícita de ativação.
- **Motivo:** o conjunto já possui especialização forte, mas o usuário precisa saber qual contrato inicia a próxima etapa.
- **Risco:** parecer que todas as cinco skills são obrigatórias.
- **Critério de aceitação:** o handoff recomenda apenas a capacidade aplicável, informa a entrada necessária e respeita invocação explícita.

### DF-21 — Publicar a nova skill sem alterar as cinco existentes

- **Prioridade:** P0
- **Arquivo atual exato a alterar:** `plugins/anti-ai-craft/.codex-plugin/plugin.json`
- **Instrução concreta:** somente no mesmo commit que criar `$anti-ai-design-flow`, incrementar a versão, substituir as afirmações de “cinco” por “seis” e incluir o fluxo completo na descrição e nos exemplos de prompt. Manter `skills` apontando para o diretório e validar a descoberta real da nova pasta.
- **Motivo:** o manifesto atual ficaria factualmente incorreto mesmo que a descoberta por diretório funcionasse.
- **Risco:** anunciar a skill antes de ela estar empacotada ou quebrar consumidores por mudar identificadores existentes.
- **Critério de aceitação:** as cinco invocações atuais continuam idênticas, a sexta é listada pelo plugin instalado e a versão pública coincide com o conteúdo.

### DF-22 — Atualizar a documentação pública de seleção

- **Prioridade:** P0
- **Arquivo atual exato a alterar:** `README.md`
- **Instrução concreta:** adicionar `$anti-ai-design-flow` às tabelas de oferta e seleção, explicar que é opt-in para jornadas completas/retomáveis e manter `$anti-ai-design` como escolha para trabalho visual delimitado. Atualizar contagem, exemplos e estrutura do repositório na mesma mudança.
- **Motivo:** evita que usuários invoquem a orquestradora para tarefas pequenas ou não saibam que ela existe.
- **Risco:** documentação prometer um fluxo ainda não validado.
- **Critério de aceitação:** cada uma das seis skills possui fronteira de uso distinta e os exemplos usam identificadores realmente instaláveis.

### DF-23 — Definir divulgação privada de vulnerabilidades

- **Prioridade:** P0
- **Arquivo previsto a criar:** `SECURITY.md`
- **Instrução concreta:** publicar política curta que delimite versões mantidas, comportamentos de instrução e empacotamento em escopo, canal privado, informação mínima de reprodução e proibição de enviar segredos reais. Não copiar licença, identidade ou contatos do conjunto externo.
- **Motivo:** o repositório público atual convida contribuições, mas não separa vulnerabilidade não corrigida de issue comum.
- **Risco:** oferecer canal que o mantenedor não monitora ou prometer prazo de resposta irreal.
- **Critério de aceitação:** existe um canal privado operacional, o texto não pede dados sensíveis e nenhuma promessa não sustentada é feita.

### DF-24 — Acrescentar gate de release para skills

- **Prioridade:** P1
- **Arquivo atual exato a alterar:** `README.md`
- **Instrução concreta:** na seção de contribuição ou manutenção, exigir validação das skills e do manifesto, revisão de diff para novas capacidades, confirmação de que nenhuma política de invocação mudou silenciosamente e teste de instalação/listagem antes de publicar versão.
- **Motivo:** skill é dependência de instrução; um diff textual pode alterar permissões e comportamento com impacto semelhante ao de código.
- **Risco:** documentar comandos que não existem ou não foram testados.
- **Critério de aceitação:** a documentação registra somente comandos executáveis no ambiente atual e separa validação obrigatória de passos opcionais.

### DF-25 — Não seguir atualização mutável sem transparência

- **Prioridade:** P1
- **Arquivo atual exato a alterar:** `README.md`
- **Instrução concreta:** explicar que atualizar o marketplace carrega uma revisão nova do plugin e recomendar revisão das notas/diff em ambientes sensíveis. Se referências imutáveis forem documentadas, testar previamente a instalação por tag; não afirmar reprodutibilidade apenas por usar o branch padrão.
- **Motivo:** o fluxo público atual ensina atualização, mas não explicita a mudança de confiança entre versões.
- **Risco:** complicar a instalação comum ou prometer suporte a tag sem prova.
- **Critério de aceitação:** o caminho simples continua disponível, e o caminho de maior garantia só aparece se tiver sido validado.

## Integração recomendada entre as cinco skills

### Fluxo principal

1. **`$anti-ai-design`** organiza descoberta, contrato, estrutura, sistema visual e plano. Ele pode implementar somente quando isso estiver autorizado, mas deve produzir critérios consumíveis por código e revisão.
2. **`$anti-ai-security`** entra como gate explícito quando estrutura ou tarefa afeta dados, identidade, tenants, operações destrutivas, integrações, custo ou superfície pública. Sua saída é um checkpoint de risco ou achados com IDs, não uma estética paralela.
3. **`$anti-ai-code`** implementa itens delimitados, lê as decisões vigentes, preserva arquitetura e só conclui uma tarefa depois da prova adequada.
4. **`$anti-ai-audit`** revisa de forma independente e somente leitura. Compara contrato, estrutura, tokens, plano, código e runtime dentro do escopo, fecha falsos positivos e emite IDs sustentados.
5. **`$anti-ai-remediate`** recebe apenas IDs aprovados, revalida o estado atual, corrige uma causa por vez e mantém evidência e status consistentes.

### Contratos de handoff

| Origem | Destino | Entrada mínima do destino | Saída esperada |
|---|---|---|---|
| Design | Segurança | ativos, atores, dados, fronteiras, ações e arquitetura proposta | decisões de risco, lacunas ou IDs confirmados |
| Design | Código | contrato vigente, estrutura, tokens aplicáveis, tarefas e critérios | diff delimitado e prova por tarefa |
| Código | Design | implementação executável, estados, rotas e limitações | revisão visual/técnica com evidência |
| Design/Código/Segurança | Auditoria | escopo, fontes de verdade e estado comparável | achados com IDs, disposições e cobertura |
| Auditoria/Segurança | Remediação | IDs aprovados, evidência, escopo e aceite | status e prova por ID |
| Remediação | Auditoria ou Design | diff, comandos, screenshots e risco residual | rechecagem independente quando solicitada |

### Regras de integração

- Uma skill não deve alegar que outra foi executada sem invocação e evidência.
- Artefatos são entradas verificáveis, não autoridade automática.
- O nome da feature deve ser estável dentro do fluxo, mas seu armazenamento não precisa seguir uma pasta obrigatória quando o projeto já possui convenção própria.
- Mudança no contrato pode exigir revalidação; não autoriza reescrever todas as fases.
- Aprovação para planejar não é aprovação para editar.
- Aprovação para implementar não é aprovação para commit, push, deploy ou alteração de produção.
- Revisão de design pode gerar recomendação; somente achado sustentado e aprovado entra em remediação.
- Achado de segurança não deve ser reduzido a ajuste visual.
- Uma tarefa visual que altera comportamento deve cumprir tanto critérios de design quanto de código.

## Armadilhas

### Transformar sequência em burocracia

Uma jornada longa pode gerar arquivos sem valor, perguntas repetidas e checkpoints que envelhecem rapidamente. O fluxo completo deve ser opt-in e proporcional ao escopo.

### Confundir arquivo com progresso

Arquivo presente pode estar vazio, parcialmente preenchido, bloqueado ou superado. Estado e critério de conclusão precisam ser explícitos.

### Tratar linearidade como verdade

Design real é iterativo. Uma descoberta de conteúdo, segurança ou implementação pode exigir voltar a uma decisão anterior. A volta deve invalidar somente dependências afetadas.

### Ocultar autorização dentro do fluxo

“Continuar” uma fase de planejamento não concede permissão para editar, instalar, criar dependência, executar ação externa, commit ou push.

### Fazer documentação competir com o repositório

Rotas, tokens e componentes que já possuem fonte de verdade não devem ser duplicados integralmente. O artefato deve registrar decisão, lacuna e vínculo.

### Planejar arquivos inventados

O plano de build não deve afirmar caminhos, APIs ou componentes antes de ler a arquitetura. Quando ainda incerto, deve apontar superfície e decisão a localizar.

### Usar revisão como aprovação automática

Um passe visual não prova runtime, acessibilidade, segurança, performance ou integração. Os níveis de evidência devem permanecer separados.

### Corrigir durante auditoria

O fluxo não pode enfraquecer o contrato read-only de `$anti-ai-audit`. A revisão produz IDs; a remediação aplica somente os aprovados.

### Transformar preferência em defeito

Direção, composição e estética continuam dependentes do produto. A existência de uma etapa de review não muda a taxonomia atual.

### Considerar tokens concluídos sem consumidores

Uma tabela de variáveis sem componentes reais, estados e temas conectados não constitui sistema visual pronto.

### Adiar segurança para o fim

Autorização, isolamento, custo e privacidade podem mudar a arquitetura da informação e as tarefas. Descobri-los somente após o build encarece e fragiliza a correção.

### Atualizar tudo após qualquer mudança

Rastreabilidade não significa reescrever todo o conjunto. Somente artefatos dependentes da decisão modificada devem ser revalidados.

## Regras que devem ser rejeitadas

- Não renomear a nova skill para `design-flow` genérico nem fazê-la substituir `$anti-ai-design`; o nome recomendado é `$anti-ai-design-flow`.
- Não criar a sexta skill se o produto desistir de retomada, múltiplas fases ou coordenação entre skills; nesse caso, manter somente um checklist curto em `$anti-ai-design`.
- Não renomear nenhuma das cinco skills existentes.
- Não mudar os gatilhos públicos ou permitir invocação implícita como efeito colateral.
- Não exigir uma coleção fixa de documentos para componente, correção local ou revisão pequena.
- Não obrigar confirmação humana antes de toda fase ou depois de toda tarefa.
- Não usar o número de fases como medida de qualidade.
- Não considerar fase concluída apenas porque um arquivo foi criado.
- Não marcar tarefa como concluída apenas porque houve edição.
- Não depender de nomes de skills externas que não existem no plugin.
- Não exigir ferramenta de navegador específica.
- Não limitar revisão a screenshot ou a código; o tipo de evidência deve ser declarado.
- Não apresentar revisão estática como validação de runtime.
- Não criar tokens paralelos quando o projeto já possui uma fonte de verdade.
- Não impor CSS, Tailwind, tema ou qualquer formato universal.
- Não criar pasta de design se a convenção do projeto já define outra localização.
- Não sobrescrever artefato de outra feature por reutilizar um nome genérico.
- Não atualizar automaticamente um artefato superado sem confirmar a fonte de verdade.
- Não pular segurança porque a feature “é só frontend” quando ela altera dado, papel, fluxo, custo ou boundary.
- Não mover correções para `$anti-ai-audit`; preservar seu modo estritamente read-only.
- Não fazer `$anti-ai-remediate` corrigir recomendações não aprovadas.
- Não promover preferência visual a ID de vulnerabilidade ou defeito.
- Não herdar autorização de uma fase para commit, push, deploy ou mudança de produção.

## Ordem sugerida de incorporação

1. Implementar DF-01, DF-02, DF-03 e DF-04 para criar o contrato de fluxo e retomada.
2. Implementar DF-07, DF-08 e DF-09 para fechar a ligação planejamento → código → prova.
3. Implementar DF-10 e DF-11 para antecipar decisões de segurança.
4. Implementar DF-12, DF-13, DF-14 e DF-15 para tornar a validação independente e rastreável.
5. Implementar DF-16 e DF-17 para preservar o contrato de remediação.
6. Implementar DF-05, DF-06, DF-18, DF-19 e DF-20 como refinamentos operacionais.
7. Implementar DF-21 e DF-22 no mesmo commit da nova skill; adicionar DF-23 antes de promover o repositório para uso sensível.
8. Aplicar DF-24 e DF-25 somente com comandos de release e atualização já verificados.

## Conclusão

A melhor contribuição da unidade externa é o modelo de jornada com artefatos encadeados, pausa, retomada e uma revisão posterior ao build. As cinco skills atuais já são mais fortes em evidência, autorização, falsificação, acessibilidade, segurança e remediação; portanto, não devem ser substituídas por uma sequência rígida.

A melhoria correta, diante da autorização para criar novas skills e do requisito de retomada transversal, é adicionar `$anti-ai-design-flow` como orquestradora explícita. Ela deve conectar as saídas aos contratos já existentes das cinco skills e concentrar apenas estado, transições, definição de pronto, invalidação e handoffs. Isso preserva todos os nomes públicos atuais e a compatibilidade, reduz trabalho ritual e acrescenta rastreabilidade onde hoje existe a principal lacuna.
