# Análise da unidade `information-architecture`

## Resumo executivo

A unidade externa trata arquitetura da informação como a camada estrutural entre a definição do produto e o desenho visual. O material é útil principalmente por tornar explícitos o mapa de superfícies, o modelo de navegação, a hierarquia de conteúdo, os fluxos, o vocabulário, o reaproveitamento estrutural, o crescimento do conteúdo e as regras de URL.

O plugin atual já cobre parte relevante dessa disciplina, sobretudo em `anti-ai-design`: ele exige leitura do projeto, inventário de telas e rotas, identificação de usuários e tarefas, preservação da navegação existente, contratos de estado, prioridade responsiva e validação no produto real. `anti-ai-audit`, `anti-ai-remediate`, `anti-ai-code` e `anti-ai-security` complementam essa base com evidência, controle de mudanças, persistência e fronteiras de confiança.

A lacuna não justifica uma sexta skill. A recomendação é incorporar uma referência curta de arquitetura da informação à `anti-ai-design` e propagar somente os controles necessários às outras quatro skills. Isso preserva os cinco identificadores públicos, os nomes visíveis e o comportamento de invocação explícita.

## Inventário do que foi analisado

### Unidade externa

| Área | O que a unidade pretende produzir ou decidir |
|---|---|
| Momento do trabalho | Estrutura do produto antes do detalhamento visual e da decomposição em tarefas |
| Entrada de produto | Brief, público, objetivo e estrutura existente |
| Descoberta no repositório | Rotas, componentes de navegação, layouts, páginas, padrões de URL e camada de conteúdo/dados |
| Decisões humanas | Tarefas prioritárias, profundidade aceitável, crescimento do conteúdo, públicos distintos e superfície de uso dominante |
| Mapa | Árvore de páginas ou views com seus caminhos |
| Navegação | Destinos primários, navegação local, utilidades e adaptação móvel |
| Hierarquia | Ordem de conteúdo e justificativa por página |
| Fluxos | Caminhos críticos com bifurcações e destinos |
| Linguagem | Vocabulário consistente para conceitos e ações |
| Reuso | Layouts, containers e elementos estruturais compartilhados |
| Crescimento | Busca, filtros, paginação, arquivo e expansão futura |
| URL | Segmentos, parâmetros e convenções de construção |
| Persistência do artefato | Documento estrutural salvo junto do brief |

### Cobertura atual do plugin

| Skill | Cobertura relacionada |
|---|---|
| `anti-ai-design` | Usuários, tarefas, telas, rotas, conteúdo, estados, fluxos, hierarquia, navegação, responsividade, nomes de ações, URL como estado, retorno de foco e preservação de estrutura |
| `anti-ai-code` | Entradas, transformações, efeitos, persistência, saídas, APIs, estados, concorrência, idempotência, integração e preservação da arquitetura local |
| `anti-ai-audit` | Escopo, usuários, tarefas, dados, estados, superfícies, cobertura de requisitos, evidência por caminho e fechamento de candidatos |
| `anti-ai-remediate` | Mudança por ID aprovado, preservação de comportamento e arquitetura, gates de aprovação, regressão, rollback e comparação antes/depois |
| `anti-ai-security` | Superfícies, endpoints, papéis, tenants, fronteiras, rotas alternativas, URLs controláveis, cache, storage, filas, sessão, autorização e fluxos fora de ordem |

## Modelo adaptado de entradas e saídas

### Entradas mínimas

1. Objetivo do produto ou da mudança.
2. Público e tarefas que realmente precisam ser concluídas.
3. Escopo autorizado: planejar, revisar ou implementar.
4. Fontes de verdade existentes.
5. Rotas, layouts, navegação, modelos de conteúdo e persistência já implementados.
6. Estados de autenticação, autorização, tenant e disponibilidade pertinentes.
7. Restrições de compatibilidade, acessibilidade, SEO, analytics e plataforma.

Não se deve exigir um brief em um caminho fixo. Quando ele existir, deve ser tratado como uma fonte de verdade entre outras. Quando não existir, a análise pode partir do pedido, do README, da especificação e do código. Perguntas são necessárias apenas quando a resposta alterar materialmente a estrutura.

### Saída proporcional ao escopo

Uma análise completa pode conter:

- mapa de superfícies;
- modelo de navegação;
- hierarquia por superfície;
- fluxos principais, alternativos e de recuperação;
- estratégia de URL;
- modelo de persistência do estado de interface;
- vocabulário de conceitos e ações;
- mapa de reuso estrutural;
- plano de crescimento de conteúdo;
- edge cases e estados terminais;
- decisões preservadas, alteradas e rejeitadas;
- critérios de aceitação e plano de validação.

Uma mudança local não precisa gerar um documento extenso. Nesse caso, basta registrar a estrutura afetada, os invariantes, o fluxo, a persistência e os critérios que impedem regressão.

### Destino do artefato

Não fixar `INFORMATION_ARCHITECTURE.md` nem uma pasta única como regra universal. Respeitar a convenção do projeto. Se o usuário pedir apenas planejamento na conversa, não criar arquivo. Se autorizar persistência e não houver convenção, sugerir um caminho previsível, como `docs/architecture/information-architecture.md`, antes de gravar.

## Mapas necessários

### Mapa de superfícies

O mapa deve incluir apenas superfícies alcançáveis ou planejadas com base verificável:

- páginas e views;
- layouts persistentes;
- overlays que representam etapas reais;
- rotas públicas, autenticadas, administrativas e internas;
- entradas alternativas por link direto, notificação, busca, convite ou retomada;
- estados de recurso inexistente, removido, inacessível ou indisponível;
- variações relevantes por papel, tenant, idioma ou versão.

Cada item deve registrar, quando aplicável:

| Campo | Pergunta de controle |
|---|---|
| Identidade | Qual é o nome estável da superfície? |
| Caminho | Como ela é alcançada no produto e por link direto? |
| Público | Quem pode vê-la e em qual estado? |
| Tarefa | O que a pessoa consegue concluir ali? |
| Conteúdo | Qual fonte alimenta a superfície? |
| Estado | Quais estados mudam a estrutura ou a ação disponível? |
| Saída | Para onde a pessoa segue, volta ou se recupera? |
| Persistência | O que sobrevive a refresh, retorno ou nova sessão? |

O mapa não deve espelhar cegamente a árvore de arquivos. Uma rota pode ter várias superfícies funcionais, e várias rotas podem compartilhar uma única estrutura.

### Mapa de navegação

O modelo deve distinguir:

- **global:** destinos recorrentes entre áreas;
- **local:** opções dentro do contexto atual;
- **contextual:** links e ações dependentes do objeto ou estado;
- **utilitária:** conta, ajuda, preferências e operações administrativas;
- **retorno e localização:** breadcrumb, histórico, “voltar” e trilha de origem;
- **mobile/adaptativa:** acesso equivalente com prioridade adequada ao espaço e à tarefa.

Não impor quantidade fixa de itens, sidebar, topbar, hamburger ou tabs. A escolha deve responder à frequência, à hierarquia, ao volume, ao papel do usuário e à necessidade de comparação. A navegação móvel não pode simplesmente esconder destinos sem demonstrar que continuam descobríveis e operáveis.

### Mapa de conteúdo

Para cada superfície principal, ordenar:

1. informação necessária para reconhecer o contexto;
2. ação ou decisão dominante;
3. dados que sustentam a decisão;
4. ações secundárias;
5. detalhes progressivos;
6. ajuda e recuperação.

A ordem deve variar por tarefa e estado. Loading, erro, vazio, permissão negada ou recurso removido não são apenas mensagens: podem substituir a hierarquia e o próximo passo.

### Mapa de reuso

Registrar layouts e padrões compartilhados somente quando existir reuso real. Para cada elemento:

- superfícies consumidoras;
- comportamento comum;
- variações legítimas;
- estado e responsabilidade;
- limites de acoplamento.

O mapa não deve induzir a criação de abstrações. Ele descreve reuso comprovado e ajuda a detectar divergência; não obriga a extrair componente.

## Navegação, URLs e compatibilidade

### Regras de URL

Uma estratégia completa deve decidir, conforme o produto:

- segmento estático e dinâmico;
- identificador versus slug legível;
- filtro, ordenação, paginação, aba e busca que precisam sobreviver no endereço;
- fragmento para localização dentro do conteúdo;
- locale, versão, workspace ou tenant quando fizerem parte do contrato;
- URL canônica e aliases existentes;
- encoding, caixa, separadores e trailing slash conforme a convenção local;
- comportamento de links antigos, redirects e recursos removidos;
- páginas que podem ser abertas diretamente e restaurar o contexto;
- dados que nunca podem aparecer na URL por sensibilidade.

Não exigir que a URL reproduza a hierarquia visual. A URL é contrato de localização, compartilhamento, histórico e integração; sua forma deve permanecer estável mesmo quando a navegação visual muda.

### Compatibilidade que deve ser preservada

- identificadores públicos das cinco skills;
- nomes visíveis e invocação explícita;
- rotas, slugs, anchors e links existentes, salvo migração aprovada;
- deep links e bookmarks válidos;
- back/forward e refresh;
- parâmetros usados por analytics, integrações, SEO ou suporte;
- autorização e isolamento associados a cada rota;
- estado preexistente que o usuário espera recuperar.

Mudança de URL ou navegação principal deve ser considerada alteração material, não polimento visual.

## Fluxos

### Estrutura mínima de um fluxo

Cada fluxo relevante deve declarar:

1. ator e estado inicial;
2. ponto de entrada;
3. objetivo;
4. sequência de superfícies e ações;
5. decisões e condições;
6. dados lidos ou gravados;
7. mudança de URL e histórico;
8. falhas e recuperação;
9. estado terminal;
10. retorno ou retomada posterior.

### Famílias de fluxo

| Família | Exemplos de controle |
|---|---|
| Principal | A tarefa mais frequente ou valiosa conclui sem desvio desnecessário |
| Alternativo | Outro papel, origem ou tipo de conteúdo chega ao resultado correto |
| Recuperação | Erro, timeout, offline ou entrada inválida mantém contexto e próximo passo |
| Autenticação | Login, expiração e retorno ao destino não quebram o fluxo |
| Autorização | Ausência de permissão não vaza conteúdo e oferece destino coerente |
| Interrupção | Refresh, back, fechamento, mudança de dispositivo ou retomada preservam o necessário |
| Crescimento | Busca, filtro, paginação e arquivo continuam úteis com grande volume |
| Administrativo | Criação, edição, revogação, exclusão e auditoria usam rotas e estados próprios |
| Ciclo de vida | Onboarding, uso recorrente, offboarding e remoção de dados permanecem coerentes |

O “caminho principal” não deve apagar os caminhos de recuperação e abuso. O fluxo de interface, o fluxo de dados e o fluxo de autorização precisam ser comparados.

## Edge cases obrigatórios por aplicabilidade

### Conteúdo e volume

- nenhum item, um item e muitos itens;
- texto longo, idioma expansivo e caracteres especiais;
- ordenação instável ou resultados duplicados;
- página solicitada depois que o conjunto encolheu;
- item removido entre listagem e detalhe;
- conteúdo parcial ou desatualizado;
- busca sem resultado e busca indisponível.

### Identidade e acesso

- pessoa não autenticada;
- sessão expirada durante o fluxo;
- papel insuficiente;
- objeto de outro usuário ou tenant;
- convite vencido;
- conta desativada;
- acesso por link antigo ou compartilhado.

### Navegação e dispositivo

- entrada direta sem histórico anterior;
- back/forward depois de mutação;
- refresh em etapa intermediária;
- múltiplas abas com estados divergentes;
- viewport estreito, teclado virtual e ausência de hover;
- foco restaurado ao fechar overlay ou retornar;
- orientação, safe area e zoom.

### Operação e persistência

- request lento, cancelado, repetido ou concluído fora de ordem;
- dupla submissão;
- atualização otimista rejeitada;
- gravação parcial;
- conflito de edição;
- retry depois de timeout;
- cache obsoleto;
- offline e reconexão;
- limite, quota ou rate limit atingido.

## Persistência do estado

Antes de implementar um fluxo, classificar cada estado:

| Tipo | Exemplos | Regra |
|---|---|---|
| Autoritativo no servidor | recurso, permissão, progresso confirmado | Reconsultar e invalidar de forma coerente |
| Representado na URL | busca, filtro, ordenação, página, tab compartilhável | Suportar link direto, refresh e histórico |
| Sessão de navegação | origem, scroll, etapa temporária | Preservar quando o retorno fizer parte da tarefa |
| Local ao dispositivo | preferência não sensível e não crítica | Não confundir com fonte de verdade |
| Efêmero do componente | menu aberto, hover, animação | Não persistir sem necessidade |
| Rascunho | formulário longo ou criação incompleta | Definir duração, conflito, limpeza e privacidade |

Para cada estado persistido, registrar:

- fonte de verdade;
- chave e escopo por usuário/tenant;
- duração e expiração;
- serialização e versão;
- invalidação;
- conflito entre abas ou dispositivos;
- comportamento em logout, revogação e exclusão;
- sensibilidade e exposição;
- fallback observável quando a restauração falhar.

Filtros e paginação não devem ser mantidos em memória apenas por conveniência se o produto exige compartilhamento ou retorno. Segredos, tokens e dados sensíveis não devem migrar para URL ou armazenamento do cliente para simplificar a implementação.

## Matriz de cobertura

| Capacidade | Estado | Evidência atual ou lacuna | Decisão |
|---|---|---|---|
| Ler estrutura existente antes de propor | Já temos | Preparação e workflow de `anti-ai-design`, `anti-ai-code`, `anti-ai-audit` e `anti-ai-security` | Preservar |
| Inventariar telas, rotas, componentes e fluxos | Já temos | `anti-ai-design` exige o inventário | Preservar e detalhar |
| Identificar usuários, tarefas, dados e estados | Já temos | Contrato compartilhado por design e auditoria | Preservar |
| Preservar navegação e rotas existentes | Já temos | Mandato de preservar/refinar/redesenhar e contrato de direção | Preservar |
| URL refletir filtro, aba ou página quando necessário | Já temos | Checklist de produção da direção | Preservar |
| Reconhecimento em vez de memorização | Já temos | Princípios, conteúdo e passe de revisão | Preservar |
| Termos e nomes de ação consistentes | Já temos | Princípios e passe de conteúdo | Preservar |
| Modelo explícito de navegação global/local/contextual/utilitária | Parcial | Componentes são avaliados, mas o modelo não é solicitado como artefato | Incorporar |
| Mapa hierárquico de superfícies com rotas | Parcial | Existe inventário, sem campos nem cobertura definidos | Incorporar de forma proporcional |
| Hierarquia de conteúdo por superfície | Parcial | Hierarquia é exigida, mas sem vínculo sistemático por tela/estado | Incorporar |
| Fluxos com decisões, falhas e retomada | Parcial | Caminho principal e estados existem, mas não há formato completo | Incorporar |
| Convenções de URL | Parcial | Há preservação e alguns estados na URL, sem estratégia abrangente | Incorporar |
| Deep link, refresh, back e forward | Parcial | Retorno e preservação aparecem, mas não como matriz de fluxo | Incorporar |
| Persistência por tipo de estado | Parcial | Código cobre persistência; design não classifica estado de interface | Incorporar |
| Crescimento de conteúdo | Parcial | Busca, paginação, filtros e dados extremos aparecem isoladamente | Incorporar |
| Mapa de reuso estrutural | Parcial | Componentes e padrões locais são preservados, sem inventário de consumidores | Incorporar com proteção contra abstração prematura |
| Edge cases de recurso removido, link antigo e conflito de abas | Não temos de forma explícita | Estados gerais existem, mas esses casos não são sistemáticos | Incorporar |
| Migração de navegação e URL | Não temos de forma explícita | Há gate humano para navegação, porém sem redirects, aliases e depreciação | Incorporar |
| Cobertura de IA no relatório de auditoria | Não temos | Template não possui seção estrutural específica | Incorporar |
| Critério de aceitação para arquitetura da informação | Não temos | Critérios são gerais e visuais | Incorporar |
| Brief obrigatório em caminho fixo | Não temos | O plugin aceita múltiplas fontes de verdade | Não incorporar |
| Escolher automaticamente o brief mais recente | Não temos | Pode selecionar feature errada | Não incorporar |
| Entrevista obrigatória antes de qualquer trabalho | Não temos | O plugin limita perguntas às decisões materiais | Não incorporar |
| Quantidade fixa de itens ou níveis de navegação | Não temos | O plugin evita universais sem contexto | Não incorporar |
| Hamburger, tabs ou sidebar como solução padrão | Não temos | O plugin exige justificativa contextual | Não incorporar |
| Documento extenso para toda mudança local | Não temos | Saída atual é proporcional ao modo | Não incorporar |
| Criar uma sexta skill de arquitetura da informação | Não temos | Fragmentaria design, auditoria e remediação | Não incorporar |
| Gravar artefato durante planejamento sem autorização | Não temos | Planejamento é não editável por padrão | Não incorporar |
| Fazer a estrutura de URL espelhar a árvore visual | Não temos | Contratos podem exigir URL mais estável que a UI | Não incorporar |

## Recomendações adaptadas

As recomendações abaixo descrevem mudanças futuras. Este relatório não altera as skills.

### IA-01 — Referência estrutural dentro de design

- **Prioridade:** P0
- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-design/references/information-architecture.md`
- **Mudança concreta:** criar uma referência curta com mapa de superfícies, navegação, hierarquia, fluxos, URLs, crescimento, edge cases e persistência, usando os modelos deste relatório de forma condensada.
- **Razão:** a cobertura está dispersa e depende de a agente inferir a disciplina completa.
- **Risco:** transformar todo trabalho visual em documentação pesada.
- **Mitigação:** exigir profundidade proporcional e permitir saída compacta para mudanças locais.
- **Critério de aceitação:** em uma tarefa com várias rotas, a saída relaciona superfície, público, tarefa, caminho, URL, estados e persistência; em ajuste local, não cria artefato desnecessário.

### IA-02 — Roteamento da referência no contrato principal

- **Prioridade:** P0
- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md`
- **Mudança concreta:** carregar a nova referência quando o pedido envolver estrutura de site/app, navegação, rotas, organização de conteúdo, onboarding, busca, filtros, documentação ou fluxo entre telas.
- **Razão:** uma referência não lida não altera o comportamento.
- **Risco:** acionamento excessivo em tarefa puramente estética.
- **Mitigação:** explicitar os gatilhos estruturais e manter invocação da skill como requisito.
- **Critério de aceitação:** pedidos de arquitetura da informação usam a referência; revisão de cor ou tipografia isolada não é ampliada automaticamente.

### IA-03 — Contrato de direção com invariantes estruturais

- **Prioridade:** P1
- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-design/references/direction-contract.md`
- **Mudança concreta:** acrescentar uma seção compacta para navegação afetada, rotas/URLs, pontos de entrada, estado persistido e compatibilidade de retorno.
- **Razão:** o contrato já protege rotas e navegação, mas não obriga a declarar como o fluxo se conserva.
- **Risco:** duplicação com a nova referência.
- **Mitigação:** manter apenas os campos que funcionam como gate antes do código.
- **Critério de aceitação:** redesign que altera estrutura registra invariantes de deep link, histórico, persistência e migração antes da implementação.

### IA-04 — Passe estrutural na revisão visual

- **Prioridade:** P1
- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Mudança concreta:** inserir, antes da decoração, um passe que compare mapa planejado e runtime: entradas, navegação, rótulos, URL, retorno, estados e recuperação.
- **Razão:** screenshot isolado não demonstra que a arquitetura funciona.
- **Risco:** confundir falha estrutural com preferência.
- **Mitigação:** exigir tarefa, caminho e dano observável.
- **Critério de aceitação:** cada achado estrutural cita o fluxo e a condição em que a pessoa se perde, perde estado ou alcança destino incorreto.

### IA-05 — Cobertura estrutural em auditoria

- **Prioridade:** P1
- **Arquivos-alvo:** `plugins/anti-ai-craft/skills/anti-ai-audit/references/audit-checklist.md` e `plugins/anti-ai-craft/skills/anti-ai-audit/references/report-template.md`
- **Mudança concreta:** adicionar controles para mapa de superfícies, navegação por papel, deep links, URL/canonical/redirect, crescimento, fluxo de erro/retomada e persistência; no relatório, incluir uma matriz de cobertura estrutural.
- **Razão:** o ledger atual é forte, mas não evidencia quais rotas e fluxos foram realmente percorridos.
- **Risco:** inflar relatório de auditorias sem UI.
- **Mitigação:** marcar a seção como aplicável somente a produtos com superfícies navegáveis.
- **Critério de aceitação:** o relatório distingue coberto, parcial, não exercitado e não aplicável por superfície/fluxo.

### IA-06 — Gate de remediação para navegação e URL

- **Prioridade:** P1
- **Arquivos-alvo:** `plugins/anti-ai-craft/skills/anti-ai-remediate/references/approval-gates.md`, `remediation-protocol.md` e `validation-checklist.md`
- **Mudança concreta:** tratar mudança de navegação principal, URL pública, slug, parâmetro persistido ou estratégia de retorno como material; exigir mapa antes/depois, compatibilidade, redirects quando aprovados, testes de deep link, refresh, back/forward e rollback.
- **Razão:** uma correção visual pode quebrar contratos externos sem alterar a tela final.
- **Risco:** bloquear correção pequena por formalidade.
- **Mitigação:** aplicar somente quando o contrato público ou o caminho entre superfícies mudar.
- **Critério de aceitação:** nenhum ID é marcado como corrigido se links existentes ou retomada esperada regressarem.

### IA-07 — Implementação de rotas e estado em código

- **Prioridade:** P1
- **Arquivos-alvo:** `plugins/anti-ai-craft/skills/anti-ai-code/SKILL.md` e `references/review-workflow.md`
- **Mudança concreta:** quando houver frontend roteado, mapear rota, entrada, loaders/actions equivalentes, fonte de verdade, estado na URL, cache, persistência, erro e retorno; exigir teste proporcional de link direto e restauração.
- **Razão:** a skill já traça persistência e efeitos, mas não liga isso ao histórico e à navegação do navegador.
- **Risco:** impor conceitos web a apps nativos, CLI ou backend.
- **Mitigação:** condicionar a superfícies navegáveis e adaptar à plataforma.
- **Critério de aceitação:** mudanças de rota demonstram comportamento correto em entrada direta, refresh e retorno, quando aplicável.

### IA-08 — Segurança da arquitetura da informação

- **Prioridade:** P1
- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-security/references/security-checklist.md`
- **Mudança concreta:** cruzar mapa de UI e inventário de endpoints; verificar autorização em rota direta, dados sensíveis em URL/histórico/log, redirects, recurso removido, cache por tenant e restauração de estado após mudança de identidade.
- **Razão:** esconder um destino na navegação não protege a rota; persistência e URL podem atravessar fronteiras.
- **Risco:** duplicação com os controles existentes de autorização e entrada.
- **Mitigação:** acrescentar a visão de fluxo e localização, sem repetir a taxonomia de vulnerabilidades.
- **Critério de aceitação:** a análise tenta acesso direto e restauração de estado com usuário, papel e tenant diferentes, sem considerar a UI como controle.

### IA-09 — Critérios mensuráveis de arquitetura da informação

- **Prioridade:** P2
- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-design/references/information-architecture.md`
- **Mudança concreta:** definir critérios portáveis: tarefa crítica alcançável; rótulos consistentes; entradas diretas recuperáveis; ausência de becos sem saída; estado preservado ou descartado deliberadamente; fluxos de erro com próximo passo; cobertura registrada.
- **Razão:** sem critério, o documento vira descrição sem poder de validação.
- **Risco:** criar números universais falsos.
- **Mitigação:** medir por cenários e contratos, não por limite fixo de cliques ou itens.
- **Critério de aceitação:** cada decisão estrutural relevante tem cenário verificável e resultado esperado.

### IA-10 — Não alterar metadados públicos

- **Prioridade:** P0 de compatibilidade
- **Arquivos-alvo:** todos os `agents/openai.yaml` e frontmatters das cinco `SKILL.md`
- **Mudança concreta:** manter `anti-ai-design`, `anti-ai-code`, `anti-ai-audit`, `anti-ai-remediate` e `anti-ai-security`, seus nomes visíveis e `allow_implicit_invocation: false`.
- **Razão:** arquitetura da informação é capacidade interna de design e revisão, não um novo contrato de invocação.
- **Risco:** nenhum risco funcional; apenas menor descoberta por quem procura uma skill separada.
- **Mitigação:** mencionar arquitetura da informação nos gatilhos descritivos de `anti-ai-design` sem renomear a skill.
- **Critério de aceitação:** prompts e scripts existentes continuam funcionando sem migração.

## O que não copiar

1. Dependência obrigatória de um arquivo de brief em pasta específica.
2. Escolha silenciosa do arquivo mais recente quando houver mais de um contexto possível.
3. Entrevista ritual antes de toda tarefa.
4. Máximo universal de itens ou profundidade de navegação.
5. Solução móvel predeterminada.
6. Hierarquia de URL derivada mecanicamente da árvore visual.
7. Documento completo para mudança de uma única superfície.
8. Gravação automática de artefato durante análise.
9. Extração de componente porque duas superfícies parecem semelhantes.
10. Presunção de que a página mais usada concentra uma porcentagem fixa do tempo.

Esses pontos podem servir como perguntas, nunca como regra sem contexto e evidência.

## Quando a arquitetura da informação é necessária ou exagerada

### Aplicar a etapa completa

Usar análise estrutural completa quando houver pelo menos um destes sinais:

- produto novo com mais de uma superfície;
- mudança de navegação principal;
- criação, remoção ou migração de rotas públicas;
- múltiplos papéis, tenants ou pontos de entrada;
- conteúdo que crescerá e exigirá busca, filtro, paginação ou arquivo;
- onboarding ou fluxo de várias etapas;
- exigência de deep link, retomada, compartilhamento ou SEO;
- inconsistência de nomes, caminhos ou hierarquia entre áreas;
- redesign que pode alterar estrutura, não apenas aparência;
- histórico de pessoas se perderem ou não encontrarem conteúdo;
- risco de segurança ligado a rota, URL, estado ou acesso direto.

### Aplicar versão compacta

Usar somente um mini-contrato quando:

- a mudança afeta uma tela, mas altera prioridade, ação ou estado;
- um modal/drawer introduz etapa recuperável;
- um filtro ou tab passa a precisar de URL;
- um formulário longo precisa preservar rascunho;
- um componente muda a forma de retornar ao contexto anterior.

O mini-contrato pode caber em cinco campos: entrada, tarefa, caminho, estado persistido e critério de retorno/erro.

### Considerar exagero

Não exigir artefato completo quando:

- a correção é puramente visual e não muda hierarquia, rótulo, ação, rota ou estado;
- há uma única superfície simples e o fluxo já está explícito;
- o pedido é correção de contraste, foco ou semântica local;
- o sistema não tem navegação nem conteúdo crescente;
- o documento repetiria integralmente rotas e contratos já mantidos por uma fonte autoritativa;
- a estrutura não está em decisão e a tarefa é apenas implementar um achado aprovado.

Mesmo nesses casos, preservar os invariantes existentes continua obrigatório.

## Quando usar inteligência artificial para esta etapa

Para evitar ambiguidade, arquitetura da informação e inteligência artificial não são a mesma coisa.

### Uso justificável

A assistência de um modelo ajuda quando é necessário:

- inventariar muitas rotas, layouts, papéis e estados;
- cruzar código, documentação e testes para encontrar divergências;
- gerar perguntas de decisão a partir de lacunas concretas;
- comparar alternativas com critérios explícitos;
- construir uma primeira matriz de cobertura para revisão humana;
- encontrar edge cases e caminhos alternativos que depois serão testados.

### Uso excessivo

É exagero usar um modelo para:

- inventar páginas ou fluxos sem requisito;
- substituir observação de usuários, analytics ou decisão de produto;
- produzir mapa extenso de um fluxo trivial;
- impor padrões de navegação por frequência em exemplos de treinamento;
- declarar que a estrutura funciona sem executar links e fluxos;
- criar abstrações ou arquivos apenas para aparentar completude;
- decidir sozinho mudança material de navegação, URL pública ou identidade.

Toda saída assistida deve ser reconciliada com código, runtime, regras do projeto e decisão humana. O modelo pode organizar e testar hipóteses; não se torna fonte de verdade.

## Plano recomendado de incorporação

1. Criar a referência de arquitetura da informação em `anti-ai-design`.
2. Roteá-la no contrato principal somente por gatilhos estruturais.
3. Adicionar o passe estrutural e os critérios de aceitação.
4. Estender auditoria com matriz de cobertura.
5. Estender remediação com compatibilidade e testes de navegação/URL.
6. Acrescentar integrações mínimas em código e segurança.
7. Validar as cinco skills e revisar se houve repetição, expansão de escopo ou alteração de identificadores.

## Checklist final desta análise

- [x] A unidade externa foi lida integralmente.
- [x] As cinco skills atuais, suas referências e seus `agents/openai.yaml` foram lidos integralmente.
- [x] Entradas e saídas foram comparadas.
- [x] Mapas, navegação, URLs, fluxos, edge cases e persistência foram cobertos.
- [x] O que já existe, existe parcialmente, falta ou não deve ser incorporado foi separado.
- [x] Cada recomendação tem prioridade, arquivo-alvo, mudança, razão, risco e critério de aceitação.
- [x] Regras de proporcionalidade e de uso de inteligência artificial foram registradas.
- [x] Nomes públicos e compatibilidade foram preservados.
- [x] Nenhum arquivo do plugin foi alterado por esta análise.
