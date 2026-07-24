# Análise da unidade `design-brief`

## Escopo e decisão

Esta análise compara integralmente a unidade externa `design-brief` com as cinco skills atuais do plugin. O plugin não foi alterado. A recomendação é absorver somente o contrato de brief e a persistência controlada, mantendo os nomes públicos, a invocação explícita e a separação já existente entre design, código, auditoria, remediação e segurança.

A unidade analisada é útil como fluxo de descoberta e como formato de documento, mas não deve ser incorporada literalmente. Seu questionário sem limite, sua gravação automática e suas buscas orientadas a stacks específicas conflitam com controles mais fortes já presentes no plugin.

## Inventário completo

### Unidade externa examinada

- unidade externa `design-brief/SKILL.md`
  - Define ativação por pedido de brief, planejamento de página ou funcionalidade e direção de interface.
  - Parte de uma descrição dada pelo usuário.
  - Explora tokens, temas, bibliotecas de componentes, catálogos de componentes, dependências de UI, fontes, rotas e layouts.
  - Conduz entrevista sobre usuário, trabalho a realizar, sucesso, tom, referências, restrições e conteúdo.
  - Produz um Markdown por funcionalidade em uma pasta persistente.
  - Oferece um modelo com problema, solução, princípios, direção estética, padrões existentes, componentes, interações, responsividade, acessibilidade e itens fora do escopo.

Não há, nessa unidade, arquivos auxiliares, configuração de interface ou referências adicionais.

### `anti-ai-design`

- `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md`
  - Escopo, mandato de preservar/refinar/redesenhar, descoberta, contrato de direção, modos de operação, validação e contrato de saída.
- `plugins/anti-ai-craft/skills/anti-ai-design/agents/openai.yaml`
  - Nome público, descrição curta, prompt padrão e invocação implícita desativada.
- `plugins/anti-ai-craft/skills/anti-ai-design/references/accessibility-baseline.md`
  - Semântica, teclado, foco, menus, modais, abas, formulários, mensagens, contraste, reflow, movimento e matriz manual.
- `plugins/anti-ai-craft/skills/anti-ai-design/references/design-antipatterns.md`
  - Sinais contextuais de composição genérica, estética reflexa, controles, movimento e responsividade; inclui rejeição de inferência de autoria.
- `plugins/anti-ai-craft/skills/anti-ai-design/references/design-principles.md`
  - Modelo de decisão, briefing, identidade, composição, componentes, overflow, tokens, escrita, estados, responsividade e critérios portáveis.
- `plugins/anti-ai-craft/skills/anti-ai-design/references/direction-contract.md`
  - Superfície, mandato, tese, invariantes, referências, mídia, estados e verificações de produção.
- `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
  - Preflight, estrutura, conteúdo, alternativas, implementação autorizada, capturas, passes independentes, comparação e gate humano.
- `plugins/anti-ai-craft/skills/anti-ai-design/references/sources.md`
  - Hierarquia de evidência, rastreabilidade e limites das heurísticas.

### `anti-ai-code`

- `plugins/anti-ai-craft/skills/anti-ai-code/SKILL.md`
  - Revisão e implementação delimitadas, leitura do repositório, verificação de APIs, investigação falsificável, mudança mínima e validação honesta.
- `plugins/anti-ai-craft/skills/anti-ai-code/agents/openai.yaml`
  - Nome público, descrição curta, prompt padrão e invocação implícita desativada.
- `plugins/anti-ai-craft/skills/anti-ai-code/references/architecture-antipatterns.md`
  - Abstração, fragmentação, superengenharia, compatibilidade, API, desempenho, observabilidade e documentação.
- `plugins/anti-ai-craft/skills/anti-ai-code/references/code-antipatterns.md`
  - Contratos inventados, certeza fabricada, falhas ocultas, estado, concorrência, segurança, qualidade local e interseção com UI.
- `plugins/anti-ai-craft/skills/anti-ai-code/references/debugging-and-evidence.md`
  - Reprodução, hipótese, experimento, adequação da evidência, oráculos, mocks, tempo e verificação de API.
- `plugins/anti-ai-craft/skills/anti-ai-code/references/review-workflow.md`
  - Escopo, modelo do sistema, descoberta, validação, correção e relatório.
- `plugins/anti-ai-craft/skills/anti-ai-code/references/sources.md`
  - Matriz de evidência e limites de generalização.
- `plugins/anti-ai-craft/skills/anti-ai-code/references/testing-antipatterns.md`
  - Regressão, falsa confiança, mocks, esperas, snapshots, casos, oráculos e execução.

### `anti-ai-audit`

- `plugins/anti-ai-craft/skills/anti-ai-audit/SKILL.md`
  - Auditoria estritamente somente leitura, baseline, ledger, regras de achado e fechamento.
- `plugins/anti-ai-craft/skills/anti-ai-audit/agents/openai.yaml`
  - Nome público, descrição curta, prompt padrão e invocação implícita desativada.
- `plugins/anti-ai-craft/skills/anti-ai-audit/references/audit-checklist.md`
  - Cobertura de escopo, interface, acessibilidade, código, arquitetura, testes, classificação e evidência.
- `plugins/anti-ai-craft/skills/anti-ai-audit/references/report-template.md`
  - Estrutura de resumo, contagem, achados, candidatos, cobertura, falsos positivos e validações.
- `plugins/anti-ai-craft/skills/anti-ai-audit/references/severity-model.md`
  - Severidade, confiança, prioridade, classificação, calibragem e deduplicação.

### `anti-ai-remediate`

- `plugins/anti-ai-craft/skills/anti-ai-remediate/SKILL.md`
  - Entrada aprovada, preparação, gates, correção mínima, limites e status por achado.
- `plugins/anti-ai-craft/skills/anti-ai-remediate/agents/openai.yaml`
  - Nome público, descrição curta, prompt padrão e invocação implícita desativada.
- `plugins/anti-ai-craft/skills/anti-ai-remediate/references/approval-gates.md`
  - Ações permitidas, nova aprovação, interrupção, proibições e conclusão.
- `plugins/anti-ai-craft/skills/anti-ai-remediate/references/remediation-protocol.md`
  - Estado inicial, elegibilidade, plano, aplicação, verificação, validação, handoff e rollback.
- `plugins/anti-ai-craft/skills/anti-ai-remediate/references/validation-checklist.md`
  - Evidência, preservação, regressão, dados, UI e handoff.

### `anti-ai-security`

- `plugins/anti-ai-craft/skills/anti-ai-security/SKILL.md`
  - Modos de análise/correção, ameaça contextual, abuso por usuário autenticado, controles esquecidos, evidência e remediação.
- `plugins/anti-ai-craft/skills/anti-ai-security/agents/openai.yaml`
  - Nome público, descrição curta, prompt padrão e invocação implícita desativada.
- `plugins/anti-ai-craft/skills/anti-ai-security/references/remediation-workflow.md`
  - Evidência, boundary, consumo de recursos, preservação funcional, validação e relatório.
- `plugins/anti-ai-craft/skills/anti-ai-security/references/security-checklist.md`
  - Ameaças, autenticação, autorização, recursos, entradas, cliente, arquivos, segredos, dependências, privacidade, fluxos e agentes.
- `plugins/anti-ai-craft/skills/anti-ai-security/references/sources.md`
  - Fontes usadas para controles e limites de inferência.
- `plugins/anti-ai-craft/skills/anti-ai-security/references/validation-and-severity.md`
  - Registro, falsificação, severidade, deduplicação e gate de correção.

## Funcionamento observado da unidade

### Descoberta do projeto

A descoberta é adequada para aplicações web conhecidas: procura valores visuais, configurações de estilização, temas de bibliotecas, diretórios de componentes, catálogo de componentes, dependências, fontes e páginas existentes. A regra correta é considerar componentes existentes como vocabulário inicial.

As limitações são:

- pressupõe convenções e tecnologias específicas, podendo ignorar stacks diferentes, aplicações nativas ou design systems organizados de outra forma;
- não ordena a autoridade entre instruções do projeto, produto, código, design system, testes e preferência do usuário;
- não exige registrar os arquivos realmente lidos, o que enfraquece rastreabilidade;
- não cobre de forma explícita contratos de dados, conteúdo, estados, mídia, analytics, localização, performance e integrações;
- não define o que fazer quando não existe repositório, quando o projeto está incompleto ou quando fontes entram em conflito.

O plugin já tem uma descoberta mais ampla e uma ordem de autoridade melhor. Vale importar apenas uma lista operacional de onde procurar o sistema visual, de forma heurística e adaptável ao repositório.

### Entradas

As entradas previstas são descrição do que será construído, público, restrições, ideias, referências e respostas da entrevista. Não existe um contrato que diferencie dado obrigatório, opcional, desconhecido ou dependente de decisão.

Também não há:

- mandato explícito de preservar, refinar ou redesenhar;
- classificação da superfície predominante;
- estado do brief, como rascunho, bloqueado ou aprovado;
- autorização explícita para criar ou substituir o arquivo;
- identificação de fontes não confiáveis, dados sensíveis ou segredos que não devem ser persistidos;
- regra para uma solicitação que já traga informação suficiente e dispense entrevista.

### Contrato de saída

O modelo de saída cobre a base de um brief: problema humano, experiência pretendida, poucos princípios, direção, padrões existentes, componentes, interações, responsividade, acessibilidade e não escopo.

Faltam elementos necessários para conectar planejamento a execução verificável:

- fonte e estado de cada afirmação relevante;
- requisitos funcionais e invariantes;
- conteúdo e dados reais, incluindo extremos e indisponibilidade;
- mapa de fluxos e estados por interação;
- critérios de aceitação e plano de validação;
- riscos, decisões em aberto, pressupostos e responsáveis por decisão;
- comportamento que deve permanecer inalterado;
- requisitos condicionais de segurança, privacidade, localização, performance e mídia;
- sinal inequívoco de que o documento está pronto ou ainda é rascunho.

### Persistência

A persistência por funcionalidade evita colisão entre briefs diferentes e cria um ponto de integração para trabalho posterior. Entretanto, gravar automaticamente entra em conflito com o modo de planejamento atual do Design Anti-IA, que não deve editar.

Não há política para:

- autorização de escrita;
- normalização segura do identificador da funcionalidade;
- arquivo já existente;
- atualização incremental versus substituição;
- preservação de conteúdo manual;
- múltiplos briefs para a mesma funcionalidade;
- detecção de versão desatualizada em relação ao código;
- stage, commit ou qualquer outra mutação Git;
- retomada após uma entrevista incompleta.

### Falhas e interrupções

A unidade permite omitir etapas, mas não define falhas. São casos sem tratamento:

- contexto insuficiente ou respostas contraditórias;
- ausência de projeto, componentes ou tokens;
- falta de asset ou conteúdo real;
- acesso negado a arquivo ou ferramenta;
- conflito entre documentação e implementação;
- impossibilidade de validar acessibilidade, responsividade ou runtime;
- colisão de caminho;
- tentativa de sobrescrever brief existente;
- inclusão acidental de segredo, dado pessoal ou conteúdo externo não confiável;
- pedido que combina brief e implementação sem autorização clara para cada parte.

A resposta correta deve ser produzir um rascunho marcado, registrar lacunas e bloquear somente as decisões materiais. Não se deve preencher ausência com detalhes plausíveis.

## Matriz comparativa

| Capacidade | Estado | Onde está hoje | Decisão |
|---|---|---|---|
| Ler o projeto antes de definir direção | Já temos | `anti-ai-design/SKILL.md`, `design-principles.md` | Manter a regra atual. |
| Descobrir tokens, componentes, temas, fontes, rotas e layouts | Parcial | Descoberta ampla existe, mas sem inventário operacional padronizado | Acrescentar uma varredura adaptável, sem amarrar a stacks. |
| Tratar componentes existentes como vocabulário inicial | Já temos | Preservação de arquitetura, tokens, componentes e padrões locais | Tornar explícito no modo brief. |
| Definir usuário, tarefa, contexto, restrições e sucesso | Já temos | Preparação e briefing de design | Reorganizar como entradas do brief, sem duplicar regras. |
| Recomendar respostas durante entrevista | Parcial | A skill recomenda direção e alternativas, mas não define protocolo de perguntas | Oferecer recomendação apenas em decisões materiais, com fundamento e consequência. |
| Entrevista ilimitada e exaustiva | Não incorporar | Conflita com o limite atual de perguntas e pode bloquear trabalho | Usar rodadas curtas por dependência e encerrar quando há informação suficiente. |
| Classificar superfície e mandato | Já temos, superior | `anti-ai-design/SKILL.md` e `direction-contract.md` | Tornar obrigatório no brief. |
| Referência dominante e anti-defaults | Já temos, superior | Contrato de direção | Preservar e registrar no brief quando houver direção visual. |
| Problema humano e experiência pretendida | Parcial | Tarefa, usuário e direção existem, mas não em documento estável | Incluir no template persistente. |
| Limitar princípios de experiência | Não temos como contrato | Há princípios gerais, não seleção curta específica por feature | Adotar até três, cada um resolvendo uma tensão real. |
| Inventário existe/modificar/novo | Parcial | Há inventário de componentes, sem tabela de decisão de brief | Adotar com justificativa e dependências. |
| Contratos detalhados de estado | Já temos, superior | `direction-contract.md` e workflow de design | Referenciar, não criar versão reduzida. |
| Responsividade por mudança de comportamento | Já temos, superior | Princípios e validação por viewports | Registrar decisões específicas da funcionalidade. |
| Acessibilidade | Já temos, muito superior | Baseline completo e validação manual | O brief deve apontar requisitos aplicáveis, não repetir o baseline inteiro. |
| Conteúdo real e distinção de placeholder | Já temos | Princípios, antipadrões e workflow | Registrar fonte, extremos e lacunas no brief. |
| Não escopo explícito | Parcial | Escopo é controlado, mas não há seção obrigatória do brief | Adotar para reduzir expansão durante implementação. |
| Arquivo persistente por funcionalidade | Não temos | Planejamento entrega brief, mas não define arquivo | Adotar somente com autorização de escrita. |
| Política de atualização e colisão | Não temos | Ausente | Adotar antes de qualquer persistência. |
| Estado rascunho/aprovado/bloqueado | Não temos | Ausente | Adotar para impedir que hipótese vire contrato. |
| Critérios de aceitação e validação | Parcial | Contrato de saída já os exige, mas o modelo externo não | Tornar seção obrigatória do brief. |
| Rastreabilidade de fontes consultadas | Já temos | Workflow e matriz de evidência | Levar ao brief como evidência operacional, não como inventário ornamental. |
| Handoff para código | Parcial | Código lê especificação e requisitos, mas não há regra para brief | Tratar somente brief aprovado como fonte, subordinado às autoridades do projeto. |
| Handoff para auditoria | Parcial | Auditoria cobre especificação/SDD | Incluir brief aprovado na cobertura quando estiver no escopo. |
| Handoff para remediação | Parcial | Remediação exige achados e IDs aprovados | Proibir que um brief, sozinho, autorize correções. |
| Segurança e privacidade do documento | Não temos no modo brief | Segurança cobre o projeto, não a persistência do brief | Não persistir segredos/PII; incluir seção condicional de risco. |
| Busca rígida por nomes e frameworks específicos | Não incorporar como regra | Pode produzir falsos negativos e importar arquitetura | Usar como exemplos de pistas, nunca como checklist obrigatório. |
| Gravação automática durante planejamento | Não incorporar | Viola a fronteira de não edição atual | Exigir autorização explícita. |
| Arquivo como barramento obrigatório para skills futuras | Não incorporar | Cria acoplamento e unidade externa pressupõe skills inexistentes | Aceitar o brief como uma fonte opcional, não como dependência obrigatória. |

## Recomendações priorizadas

As instruções abaixo são sínteses novas. Não exigem renomear skills, mudar seus identificadores, permitir invocação implícita ou alterar os comandos públicos atuais.

### DB-01 — Modo de brief com fronteira de escrita

- **Prioridade:** P0.
- **Arquivo-alvo exato:** `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md`.
- **Instrução concreta:** adicionar, em “Operar por modo”, um subtipo “Brief de design”. Ele deve descobrir o projeto, resolver decisões materiais, produzir um documento estruturado e permanecer sem edição por padrão. Persistir somente quando o usuário pedir o arquivo ou autorizar escrita; implementar continua sendo uma autorização separada.
- **Motivo:** permite aproveitar o fluxo sem violar a promessa atual de planejamento sem edição.
- **Risco:** uma formulação ambígua pode fazer a skill gravar ou começar a implementar por inferência.
- **Aceitação:** um pedido “planeje esta tela” retorna o brief na conversa sem mutação; um pedido “salve o brief” cria apenas o documento autorizado; nenhum dos dois altera código de produto.
- **Obrigatoriedade:** obrigatório para habilitar persistência segura.

### DB-02 — Referência dedicada para o contrato do brief

- **Prioridade:** P0.
- **Arquivo-alvo exato:** `plugins/anti-ai-craft/skills/anti-ai-design/references/design-brief.md` (novo).
- **Instrução concreta:** definir entradas, descoberta, entrevista em rodadas, schema de saída, estados do documento, política de persistência, falhas e critérios de conclusão. Reutilizar por referência os baselines atuais de direção, estados, acessibilidade e revisão; não duplicá-los.
- **Motivo:** evita inflar o `SKILL.md` e cria um contrato verificável para criação e atualização de briefs.
- **Risco:** duplicar regras existentes e permitir divergência futura.
- **Aceitação:** toda regra detalhada do brief vive nesse arquivo; o `SKILL.md` apenas define quando carregá-lo; não há cópia concorrente do baseline de acessibilidade ou do contrato de direção.
- **Obrigatoriedade:** obrigatório se o modo for incorporado.

### DB-03 — Inventário de descoberta adaptável ao repositório

- **Prioridade:** P0.
- **Arquivo-alvo exato:** `plugins/anti-ai-craft/skills/anti-ai-design/references/design-brief.md`.
- **Instrução concreta:** orientar a busca por instruções, documentação, tokens/temas, componentes e catálogos, fontes/assets, rotas/layouts, conteúdo/dados, estados, testes visuais e dependências. Nomes de arquivos ou frameworks são pistas condicionais; primeiro descobrir a stack e os comandos reais. Registrar caminho e relevância apenas do que foi lido.
- **Motivo:** torna a exploração repetível sem supor uma tecnologia.
- **Risco:** uma lista longa virar ritual e consumir contexto em arquivos irrelevantes.
- **Aceitação:** em uma stack desconhecida, a varredura parte de manifestos e estrutura; em um projeto sem frontend, itens visuais são marcados não aplicáveis; o brief lista fontes realmente usadas.
- **Obrigatoriedade:** descoberta de fontes e padrões é obrigatória; categorias e tecnologias específicas são condicionais.

### DB-04 — Entradas classificadas e perguntas por impacto

- **Prioridade:** P0.
- **Arquivo-alvo exato:** `plugins/anti-ai-craft/skills/anti-ai-design/references/design-brief.md`.
- **Instrução concreta:** classificar cada entrada como confirmada, pressuposto de baixo risco, decisão aberta ou bloqueio. Perguntar em rodadas de no máximo duas ou três questões somente quando a resposta mudar direção, contrato, segurança ou escopo. Para cada decisão material, apresentar recomendação, fundamento e consequência; aceitar que um pedido completo não precisa de entrevista.
- **Motivo:** combina colaboração útil com a disciplina já existente de não interrogar por ritual.
- **Risco:** perguntar pouco demais e cristalizar requisito incorreto.
- **Aceitação:** lacunas materiais ficam visíveis; pressupostos menores são declarados; nenhuma pergunta é feita sem explicar qual decisão ela destrava.
- **Obrigatoriedade:** classificação e limite são obrigatórios; perguntas são condicionais.

### DB-05 — Schema de brief rastreável

- **Prioridade:** P0.
- **Arquivo-alvo exato:** `plugins/anti-ai-craft/skills/anti-ai-design/references/design-brief.md`.
- **Instrução concreta:** exigir as seções: identidade e estado do documento; problema do usuário; resultado e sinais de sucesso; usuários/contexto; superfície e mandato; fontes e padrões existentes; requisitos/invariantes; até três princípios que resolvam tensões; direção e invariantes; conteúdo/dados/mídia; fluxo principal e alternativos; inventário de componentes; contratos de interação e estado; comportamento responsivo; requisitos aplicáveis de acessibilidade; não escopo; riscos/decisões abertas; critérios de aceitação e plano de validação.
- **Motivo:** conecta intenção a implementação e teste, em vez de produzir apenas direção estética.
- **Risco:** briefs pequenos ficarem burocráticos.
- **Aceitação:** se uma seção não se aplicar, ela é marcada como não aplicável com motivo; se estiver desconhecida e for material, o documento permanece rascunho ou bloqueado; nenhuma seção é preenchida com conteúdo inventado.
- **Obrigatoriedade:** problema, resultado, usuários, mandato, fontes, invariantes, fluxo, estados, não escopo, aceitação e lacunas são obrigatórios; direção estética, mídia, segurança e outras áreas são condicionais.

### DB-06 — Persistência sem sobrescrita silenciosa

- **Prioridade:** P0.
- **Arquivo-alvo exato:** `plugins/anti-ai-craft/skills/anti-ai-design/references/design-brief.md`.
- **Instrução concreta:** quando autorizado, usar `.design/<slug-seguro>/DESIGN_BRIEF.md`. Derivar um identificador minúsculo e hifenizado apenas de texto de produto, remover segmentos de caminho e caracteres não seguros, confirmar a pasta final dentro de `.design`, verificar arquivo existente e pedir decisão antes de substituir conteúdo manual. Atualizações devem produzir diff pequeno e preservar seções não incluídas no pedido.
- **Motivo:** mantém um endereço previsível sem risco de colisão, traversal ou perda.
- **Risco:** adoção rígida da pasta conflitar com uma convenção já existente no projeto.
- **Aceitação:** convenção local documentada prevalece; um arquivo existente nunca é substituído silenciosamente; nenhum stage, commit, push ou alteração de código ocorre como consequência implícita.
- **Obrigatoriedade:** segurança do caminho e não sobrescrita são obrigatórias quando houver persistência; o caminho padrão é condicional à ausência de convenção local.

### DB-07 — Estados e falhas do documento

- **Prioridade:** P0.
- **Arquivo-alvo exato:** `plugins/anti-ai-craft/skills/anti-ai-design/references/design-brief.md`.
- **Instrução concreta:** usar os estados `rascunho`, `bloqueado` e `aprovado`. Registrar motivo, decisões faltantes e validações não executadas. Falhas de ferramenta, acesso, runtime ou contexto devem gerar lacuna explícita; conflito entre fontes deve preservar as alternativas e pedir decisão quando material. Nunca converter ausência em placeholder apresentado como fato.
- **Motivo:** impede que um documento incompleto seja tratado como contrato final.
- **Risco:** o rótulo “aprovado” ser atribuído pelo agente sem decisão humana.
- **Aceitação:** somente confirmação explícita do usuário muda o documento para aprovado; falha externa não é apresentada como reprovação do design; todo bloqueio contém o dado ou decisão necessária para prosseguir.
- **Obrigatoriedade:** obrigatório.

### DB-08 — Integração segura com implementação

- **Prioridade:** P1.
- **Arquivo-alvo exato:** `plugins/anti-ai-craft/skills/anti-ai-code/references/review-workflow.md`.
- **Instrução concreta:** na construção do modelo do sistema, ler o brief apenas quando fornecido, citado pelo projeto ou diretamente relacionado ao escopo. Registrar seu estado e data lógica em relação ao código. Tratar brief aprovado como fonte de requisito, mas subordinado a instruções de maior autoridade e ao comportamento atual que o usuário mandou preservar. Mapear critérios de aceitação a caminhos e testes; um rascunho não autoriza implementação.
- **Motivo:** cria continuidade entre planejamento e código sem acoplamento obrigatório.
- **Risco:** documento obsoleto ser usado contra implementação válida.
- **Aceitação:** divergências são relatadas antes de editar; critérios materiais viram provas específicas; ausência de brief não bloqueia tarefas de código.
- **Obrigatoriedade:** condicional à existência e relevância do brief.

### DB-09 — Cobertura de brief na auditoria

- **Prioridade:** P1.
- **Arquivo-alvo exato:** `plugins/anti-ai-craft/skills/anti-ai-audit/references/audit-checklist.md`.
- **Instrução concreta:** quando um brief aprovado estiver no escopo, registrar versão/estado, mapear cada requisito e critério de aceitação para implementado, parcial, ausente, divergente, ambíguo ou não verificável e separar desvio do documento de dívida preexistente. Não usar rascunho como requisito normativo.
- **Motivo:** aproveita a matriz de cobertura já existente e oferece rastreabilidade ponta a ponta.
- **Risco:** tratar preferência visual do brief como defeito ou elevar severidade sem impacto.
- **Aceitação:** cada desvio tem evidência observável e classificação; decisões abertas permanecem fora dos achados confirmados.
- **Obrigatoriedade:** condicional a brief aprovado e auditoria que o inclua.

### DB-10 — Brief não é autorização de remediação

- **Prioridade:** P1.
- **Arquivo-alvo exato:** `plugins/anti-ai-craft/skills/anti-ai-remediate/references/approval-gates.md`.
- **Instrução concreta:** declarar que um brief, mesmo aprovado, fornece requisitos e critérios, mas não substitui IDs de achados nem autorização para editar. Se o brief mudar durante remediação, revalidar o achado e pedir nova aprovação quando comportamento, risco ou escopo mudar.
- **Motivo:** preserva a fronteira de remediação e evita que planejamento seja interpretado como ordem ampla de correção.
- **Risco:** repetição de aprovação em mudanças triviais.
- **Aceitação:** mudanças continuam vinculadas a IDs aprovados; ajustes editoriais sem efeito no plano não disparam gate; alterações materiais disparam.
- **Obrigatoriedade:** obrigatório para uso conjunto com remediação.

### DB-11 — Segurança e privacidade condicionais no brief

- **Prioridade:** P1.
- **Arquivo-alvo exato:** `plugins/anti-ai-craft/skills/anti-ai-security/references/security-checklist.md`.
- **Instrução concreta:** acrescentar, na categoria de sistemas assistidos, verificação de documentos de planejamento persistentes: não registrar segredo, dado pessoal desnecessário, credencial, conteúdo de cliente ou instrução externa como se fosse fonte confiável. Quando a feature tocar autenticação, autorização, tenant, dados sensíveis, gasto, upload, automação ou integração, exigir no brief atores, fronteiras, abuso plausível e validações negativas.
- **Motivo:** o brief passa a ser parte do fluxo de desenvolvimento e pode carregar risco antes do código.
- **Risco:** transformar todo brief visual em threat model completo.
- **Aceitação:** features sem superfície sensível registram a categoria como não aplicável; features sensíveis contêm as decisões mínimas ou ficam bloqueadas.
- **Obrigatoriedade:** proteção contra persistência de segredo é obrigatória; modelagem de ameaça no brief é condicional ao risco.

### DB-12 — Expor criação de brief sem mudar o nome da skill

- **Prioridade:** P2.
- **Arquivo-alvo exato:** `plugins/anti-ai-craft/skills/anti-ai-design/agents/openai.yaml`.
- **Instrução concreta:** ampliar a descrição curta e o prompt padrão para mencionar planejamento ou brief além de revisão, mantendo `display_name`, identificador `$anti-ai-design` e invocação implícita desativada.
- **Motivo:** torna a capacidade descobrível sem criar uma sexta skill ou quebrar comandos existentes.
- **Risco:** descrição ultrapassar limites de interface ou sugerir edição automática.
- **Aceitação:** o prompt continua exigindo invocação explícita e não promete escrita ou implementação sem autorização.
- **Obrigatoriedade:** opcional; não afeta o contrato interno.

## Obrigatório versus condicional

### Obrigatório para todo brief

- identificar problema, usuário, tarefa, resultado desejado e sinais de sucesso;
- classificar superfície e mandato;
- ler fontes de verdade relevantes e registrar o que foi realmente consultado;
- preservar arquitetura, componentes, conteúdo e identidade válidos;
- distinguir fatos, pressupostos, decisões abertas e bloqueios;
- registrar invariantes, fluxo principal, estados relevantes, não escopo e critérios de aceitação;
- formular no máximo três princípios específicos, somente se cada um resolver uma tensão real;
- declarar status do documento;
- não inventar dados, componentes, assets, APIs, validações ou decisões;
- manter planejamento sem edição até autorização explícita;
- evitar sobrescrita silenciosa e mutações Git implícitas;
- tratar brief aprovado como requisito, não como autorização automática para código ou remediação.

### Condicional ao projeto ou ao risco

- busca por tecnologias, nomes de arquivo e bibliotecas específicas;
- direção estética detalhada e referências visuais;
- catálogo de componentes e screenshots;
- mídia, animação, internacionalização, analytics e SEO;
- testes em navegador e capturas por viewport;
- requisitos ampliados de performance;
- threat model, privacidade e testes adversariais;
- persistência em `.design/<slug>/DESIGN_BRIEF.md`;
- leitura do brief por Código, Auditoria, Remediação e Segurança;
- entrevista com o usuário, quando as entradas já não forem suficientes.

### Não incorporar

- entrevista “até esgotar tudo”;
- uma recomendação obrigatória para toda pergunta;
- gravação automática durante planejamento;
- sobrescrita sem confirmação;
- lista rígida de frameworks como definição de descoberta;
- arquivo persistente como dependência obrigatória entre skills;
- acessibilidade reduzida a poucas verificações no template;
- mudança automática de código após criação do brief;
- aprovação inferida pelo agente;
- detalhes ausentes preenchidos por plausibilidade.

## Ordem recomendada de implementação

1. Implementar DB-01 a DB-07 dentro de Design Anti-IA.
2. Validar o fluxo em três cenários: projeto existente com design system, projeto sem sistema visual explícito e pedido sem repositório.
3. Acrescentar DB-08 a DB-11 para handoff entre skills.
4. Aplicar DB-12 somente se a interface pública continuar clara dentro dos limites de texto.
5. Rodar a validação estrutural das cinco skills e revisar o diff para confirmar que nomes, identificadores e política de invocação não mudaram.

## Resumo

A unidade externa acrescenta duas ideias úteis que ainda não estão completas no plugin: um documento de brief por funcionalidade e um inventário operacional de descoberta visual. O restante já existe, em geral de forma mais forte, nas cinco skills. A melhor evolução é um modo de brief dentro de `anti-ai-design`, com template próprio, escrita opt-in, status explícito, falhas rastreáveis e handoff condicional. Não é necessário criar nova skill, renomear as existentes ou acoplar o plugin a um único caminho ou stack.
