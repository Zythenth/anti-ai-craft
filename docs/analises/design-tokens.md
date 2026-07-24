# Análise da unidade `design-tokens`

## Escopo e método

Esta análise compara integralmente a unidade externa `design-tokens` com as cinco skills atuais do plugin. O objetivo é identificar cobertura, lacunas e melhorias adaptáveis sem copiar texto, impor stack, criar estética automática ou quebrar nomes e compatibilidade.

Nenhum arquivo do plugin foi alterado. Este documento é o único artefato produzido por esta análise.

### Inventário lido

| Unidade | Arquivos examinados integralmente |
|---|---|
| Unidade externa | `design-tokens/SKILL.md` |
| `anti-ai-design` | `SKILL.md`, `agents/openai.yaml`, `references/accessibility-baseline.md`, `references/design-antipatterns.md`, `references/design-principles.md`, `references/direction-contract.md`, `references/review-workflow.md`, `references/sources.md` |
| `anti-ai-code` | `SKILL.md`, `agents/openai.yaml`, `references/architecture-antipatterns.md`, `references/code-antipatterns.md`, `references/debugging-and-evidence.md`, `references/review-workflow.md`, `references/sources.md`, `references/testing-antipatterns.md` |
| `anti-ai-audit` | `SKILL.md`, `agents/openai.yaml`, `references/audit-checklist.md`, `references/report-template.md`, `references/severity-model.md` |
| `anti-ai-remediate` | `SKILL.md`, `agents/openai.yaml`, `references/approval-gates.md`, `references/remediation-protocol.md`, `references/validation-checklist.md` |
| `anti-ai-security` | `SKILL.md`, `agents/openai.yaml`, `references/remediation-workflow.md`, `references/security-checklist.md`, `references/sources.md`, `references/validation-and-severity.md` |

## Inventário da proposta externa

A unidade externa concentra-se em criar ou completar a fundação visual de um projeto. Suas ideias podem ser agrupadas em oito blocos:

1. descobrir variáveis, configurações de framework, providers de tema, arquivos de tokens e dependências de UI;
2. estender um sistema existente em vez de substituí-lo;
3. ler um brief visual antes de escolher valores;
4. escolher o formato de saída conforme o stack;
5. organizar cores, tipografia, espaço, layout, forma, elevação, movimento e breakpoints;
6. produzir variantes claras e escuras;
7. fazer componentes consumirem tokens em vez de valores soltos;
8. salvar o resultado na localização adequada e explicar decisões.

O valor principal está no processo operacional de descoberta e na abrangência do inventário. As partes que não devem ser trazidas literalmente são os defaults obrigatórios: tema escuro em todo projeto, escalas numéricas predeterminadas, breakpoints por classe de aparelho, seleção de brief por data de modificação, dependência de outra unidade estética e escolha automática de CSS quando a arquitetura estiver incerta.

## O que o plugin já possui

### `anti-ai-design`

É a skill com maior cobertura. Ela já:

- lê design system, tokens, componentes, código, assets e regras locais antes de propor estética;
- fixa o mandato de preservar, refinar ou redesenhar;
- organiza tokens em `primitivo → semântico → componente`;
- exige consumidores reais e identifica valores que contornam a cadeia;
- cobre papéis de cor e tipografia, estados, contraste, temas e forced colors;
- escolhe responsividade pela ruptura do conteúdo, não por aparelhos fixos;
- preserva arquitetura, identidade, conteúdo e mídia;
- rejeita números universais de cores, fontes, animações e stacks;
- valida interface real, estados, viewports e acessibilidade.

A lacuna não é conceitual. Falta um procedimento específico para pedidos de tokens: onde procurar, como eleger a fonte autoritativa, como distinguir fonte de arquivo gerado, como registrar aliases e consumidores, quais famílias examinar e qual saída produzir.

### `anti-ai-code`

Já detecta valores mágicos, estilos inline que contornam a arquitetura, configuração excessiva, compatibilidade especulativa e abstrações sem consumidor. Também exige preservação do stack e verificação por build, teste e execução.

Falta explicitar falhas próprias de tokens: alias inexistente ou circular, edição de artefato gerado, valor primitivo consumido onde o projeto exige semântica, branches manuais de tema que duplicam política, token órfão e substituição em massa sem confirmar a função do valor.

### `anti-ai-audit`

Já audita papéis de tipografia, cor, sombra, borda, radius, ícones e movimento, além de carregar diretamente os princípios de design. A disciplina de evidência e falsificação evita transformar preferência visual em defeito.

Falta uma trilha auditável específica para tokens: fonte autoritativa, camadas, aliases, consumidores, hardcodes, modos, estados, arquivos gerados e efeito observável. Hoje a cobertura existe em alto nível, mas pode ser concluída sem examinar a implementação do sistema de tokens.

### `anti-ai-remediate`

Já preserva design system, identidade, arquitetura e trabalho preexistente; exige comparação antes/depois, validação por viewport e aprovação para mudança visual ampla.

Falta orientar correções de tokens: alterar a fonte autoritativa, regenerar saídas pelo comando oficial, limitar substituições a consumidores comprovados, validar todos os modos afetados e tratar mudança global de token como alteração potencialmente ampla mesmo quando o diff é pequeno.

### `anti-ai-security`

Tokens de design estáticos não pertencem ao núcleo desta skill. A cobertura atual de entrada não confiável, sinks, configuração e conteúdo externo já é suficiente para a maioria dos projetos.

Existe apenas uma extensão condicional: quando temas ou tokens são aceitos de usuário, tenant, CMS, arquivo remoto ou integração, eles passam a cruzar uma fronteira de confiança. Nesse caso, nomes, tipos, valores, referências a recursos e mecanismo de aplicação precisam de validação. Sem entrada externa controlável e sem sink relevante, isso não deve gerar achado de segurança.

## Análise por dimensão

### Hierarquia e ciclo de vida

O plugin já possui a hierarquia correta e a exigência de consumidores reais. A melhoria necessária é operacionalizar o ciclo:

1. localizar a fonte autoritativa;
2. identificar arquivos derivados e o comando que os gera;
3. resolver aliases e dependências;
4. mapear tokens a consumidores e estados;
5. alterar a menor camada capaz de expressar a intenção;
6. regenerar, validar e revisar o diff;
7. remover apenas órfãos criados ou comprovadamente sem consumidores.

Uma taxonomia completa no papel não é suficiente. Também devem ser tratados como falha: alias não resolvido, ciclo, tipo incompatível, unidade inválida para o consumidor, divergência entre fonte e saída gerada, token declarado sem consumidor e consumidor que ignora a camada semântica estabelecida.

### Temas e modos

O plugin já testa light/dark e forced colors quando presentes, mas corretamente não exige dark mode em todo produto. A regra adaptada deve ser:

- preservar o mecanismo de tema já adotado;
- gerar somente modos exigidos pelo produto ou já suportados;
- manter paridade semântica e de estados entre os modos existentes;
- respeitar preferência do sistema e escolha manual apenas se esse contrato já existir ou for solicitado;
- não introduzir simultaneamente seletores, providers e media queries concorrentes;
- tratar tema, marca, contraste elevado e densidade como eixos independentes quando o projeto realmente os modelar.

O ponto de validação não é “há duas paletas”, mas “cada papel semântico continua legível, distinguível e funcional em todos os modos suportados”.

### Tipografia

O plugin já decide famílias por voz, leitura, idiomas, performance e função. Falta pedir um inventário de tokens tipográficos e verificar:

- família, fallback e disponibilidade;
- papéis de texto em vez de uma coleção arbitrária de tamanhos;
- tamanho, peso, altura de linha e tracking como conjunto;
- legibilidade com zoom, text spacing, tradução, strings longas e scripts suportados;
- distinção entre texto de leitura, display, dados e código;
- consumo real pelos componentes.

Não deve existir número obrigatório de famílias, passos ou pesos. A escala deve estender o sistema local ou ser derivada do conteúdo e dos papéis necessários.

### Cor

O plugin já exige papel semântico ou identitário, contraste e comunicação além da cor. A melhoria é tornar explícito o mapa mínimo aplicável:

- superfícies e fundos;
- texto e ícones;
- bordas e separadores;
- ação e foco;
- estados de interação;
- sucesso, aviso, erro e informação;
- overlay e elevação quando existirem.

Esse mapa é uma lista de verificação, não uma obrigação de criar todos os tokens. Estados ausentes só são lacuna quando existe um consumidor ou contrato correspondente. Nomes devem expressar intenção; nomes baseados no valor podem permanecer na camada primitiva, não na API semântica.

### Espaçamento, dimensão, forma e elevação

Espaçamento é a maior lacuna direta. O plugin discute ritmo, agrupamento, densidade, alvos e radius, mas não descreve como auditar ou criar a escala.

A regra adaptada deve:

- descobrir e estender a escala existente;
- derivar passos de agrupamentos, densidade, toque e layout reais;
- evitar duplicatas quase idênticas sem função;
- permitir exceções locais justificadas;
- não substituir dimensões intrínsecas, proporções de mídia ou cálculos de layout por tokens artificiais;
- ligar radius e sombra a forma, estado ou elevação, não a acabamento genérico.

Uma base fixa e multiplicadores universais não devem ser incorporados.

### Movimento

O plugin já possui a orientação funcional correta e reduced motion. Pode melhorar ao distinguir:

- duração;
- curva;
- atraso;
- distância ou intensidade;
- variante reduzida;
- consumidor e transição de estado.

Só vale tokenizar valores repetidos que representam uma linguagem de transição. Não criar uma escala completa para uma única animação, não adotar bounce como default e não transformar duração em regra universal. A validação deve confirmar interrupção, estado final, ausência de atraso teatral e alternativa reduzida.

### Breakpoints e layout

A abordagem atual do plugin é superior à proposta externa: breakpoints devem surgir quando conteúdo, interação, leitura ou navegação deixam de funcionar. Não devem ser nomeados como aparelhos rígidos nem receber valores universais.

Breakpoints podem integrar o sistema quando o stack os trata como configuração compartilhada, mas não devem ser forçados ao mesmo formato de cores ou espaçamento. A saída deve respeitar a capacidade do stack; por exemplo, uma fonte de tokens não deve prometer consumo em um contexto no qual aquele tipo de variável não é resolvido.

### Formatos e saídas

O plugin preserva arquitetura, mas não oferece um mapa operacional para tokens. A melhoria deve identificar, sem impor:

- variáveis e camadas de estilo;
- configuração de framework;
- objetos de tema;
- arquivos estruturados de tokens;
- recursos nativos de plataforma;
- arquivos gerados e ferramentas de transformação.

Quando houver pipeline, editar somente a fonte e executar o gerador oficial. Quando houver mais de uma fonte, resolver autoridade por documentação, imports, scripts e consumidores; não eleger pelo nome do arquivo. Quando a arquitetura continuar ambígua, pedir decisão em vez de criar um novo `tokens.css`.

A saída ideal inclui:

- inventário e fonte autoritativa;
- modos e famílias aplicáveis;
- tokens preservados, adicionados, alterados e rejeitados;
- consumidores atingidos;
- arquivo fonte e arquivos regenerados;
- comandos e validações;
- desvios e decisões pendentes.

### Detecção do sistema existente

A detecção externa é útil, mas deve ser ampliada e tornada independente de nomes específicos. Procurar:

- definições, imports e consumidores de variáveis;
- configurações e dependências do stack;
- providers, contextos, atributos e preferências de tema;
- arquivos estruturados e scripts de geração;
- recursos nativos e bibliotecas de componentes;
- valores repetidos ou hardcoded;
- aliases, referências e outputs gerados;
- testes visuais, documentação e ferramentas de design;
- múltiplas marcas, temas ou plataformas.

Classificar o resultado como:

- inexistente;
- informal, com valores repetidos;
- parcial, com alguma semântica ou geração;
- estabelecido, com fonte, camadas e consumidores;
- fragmentado, com fontes concorrentes.

Essa classificação determina se a ação correta é criar, estender, consolidar, conectar consumidores ou apenas documentar.

## Matriz de cobertura e decisão

| Ideia avaliada | Estado | Situação atual e decisão |
|---|---|---|
| Ler design system, tokens, código e componentes antes de agir | Já temos | Coberto na preparação de design e nas regras de preservação. |
| Estender sistema existente em vez de substituir | Já temos | Coberto pelo mandato de preservar/refinar e pelo workflow visual. |
| Hierarquia `primitivo → semântico → componente` | Já temos | Está explícita em princípios e contrato de direção. |
| Exigir consumidores reais e detectar bypass da camada semântica | Já temos | Está explícito, embora possa ganhar verificações operacionais. |
| Preservar stack, identidade e arquitetura | Já temos | Coberto nas cinco skills conforme o modo. |
| Papéis semânticos de cor e tipografia | Já temos | Cobertura conceitual forte; falta inventário de tokens por família. |
| Contraste, estados, forced colors e reduced motion | Já temos | Coberto em design e acessibilidade. |
| Breakpoints derivados de ruptura do conteúdo | Já temos | A regra atual é preferível a presets por aparelho. |
| Detectar formatos, providers, arquivos estruturados e dependências | Parcial | Há leitura geral do projeto, mas não um procedimento específico e verificável. |
| Distinguir fonte autoritativa de artefato gerado | Não temos | Deve ser incluído para evitar editar o arquivo errado. |
| Resolver aliases, ciclos, tipos e unidades | Não temos | Falha técnica de tokens ainda não aparece no checklist. |
| Mapear tokens a consumidores, estados e modos | Parcial | Consumidores e estados existem, mas sem formato de inventário. |
| Escala tipográfica baseada em papéis | Parcial | Critérios de família e legibilidade existem; escala e validação conjunta não. |
| Escala de espaçamento contextual | Não temos | Ritmo e densidade existem, mas não criação/auditoria da escala. |
| Tokens de forma, elevação e layout | Parcial | Papéis são discutidos, mas não o processo de tokenização. |
| Tokens de duração, curva e variante reduzida | Parcial | Movimento funcional está coberto; sistema de valores não. |
| Paridade entre temas ou modos já suportados | Parcial | Há testes por tema, mas não matriz token × modo × estado. |
| Saída compatível com o stack e pipeline | Parcial | Preservação existe; mapeamento de formatos e geração oficial não. |
| Relatório de tokens preservados, alterados e rejeitados | Parcial | O contrato geral de saída cobre decisões, não um inventário próprio. |
| Auditoria de hardcodes, órfãos e divergência de geração | Não temos | Deve ser adicionada com exigência de impacto e consumidor real. |
| Correção pela fonte autoritativa e regeneração oficial | Não temos | Falta no protocolo de remediação. |
| Tema claro e escuro obrigatórios em qualquer projeto | Não incorporar | Impõe produto, manutenção e estética sem requisito. |
| Valores fixos de espaçamento, tipografia, movimento ou breakpoints | Não incorporar | Números devem vir do sistema, conteúdo, capacidade e acessibilidade. |
| Escolher brief pelo arquivo modificado mais recentemente | Não incorporar | Data de arquivo não estabelece autoridade nem intenção. |
| Delegar filosofia visual a outra unidade obrigatória | Não incorporar | Cria acoplamento e pode substituir a direção do projeto. |
| Criar CSS por default quando o stack estiver incerto | Não incorporar | A incerteza deve ser resolvida por evidência ou decisão do usuário. |
| Aplicar simultaneamente preferência do sistema e seletor manual | Não incorporar como default | Só adotar se o contrato de tema e a arquitetura exigirem ambos. |
| Transformar todo valor visual em token | Não incorporar | Valores únicos, intrínsecos ou calculados podem permanecer locais quando justificados. |
| Nova skill ou renomeação das cinco skills | Não incorporar | O conteúdo cabe nas skills existentes e os nomes devem permanecer compatíveis. |

## Recomendações adaptadas

### DT-01 — Procedimento central de design tokens

- **Prioridade:** P0
- **Arquivo-alvo:** novo `plugins/anti-ai-craft/skills/anti-ai-design/references/design-tokens.md`
- **Instrução:** criar uma referência operacional com descoberta, classificação do sistema, fonte autoritativa, arquivos gerados, hierarquia, aliases, famílias aplicáveis, modos, consumidores, implementação mínima, validação e contrato de saída. Toda regra numérica deve ser derivada do projeto ou marcada como decisão pendente.
- **Motivo:** concentra as lacunas sem inflar o `SKILL.md` nem duplicar princípios gerais.
- **Risco:** virar catálogo obrigatório ou competir com o design system local.
- **Aceitação:** a referência distingue criar, estender, consolidar e apenas conectar consumidores; proíbe substituir formato/namespace sem autorização; não obriga dark mode, stack, número de passos ou valores fixos; registra fonte e outputs gerados.

### DT-02 — Roteamento explícito para pedidos de tokens

- **Prioridade:** P0
- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md`
- **Instrução:** adicionar o novo documento à seção de referências e incluir no workflow um ramo curto para pedidos de tokens, temas, paleta, escala ou design system. O ramo deve primeiro detectar o sistema existente e só depois propor valores ou arquivos.
- **Motivo:** a skill já é o ponto correto de entrada, mas hoje o pedido pode seguir um fluxo visual genérico.
- **Risco:** sobrecarregar qualquer revisão de interface com uma auditoria completa de tokens.
- **Aceitação:** a leitura da referência ocorre apenas quando o pedido ou o problema envolve tokens; o nome `$anti-ai-design`, a política de invocação e o prompt padrão permanecem compatíveis.

### DT-03 — Auditoria verificável do sistema de tokens

- **Prioridade:** P0
- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-audit/references/audit-checklist.md`
- **Instrução:** acrescentar itens condicionais para identificar fonte autoritativa, outputs gerados, camadas, aliases, consumidores, valores que contornam o sistema, paridade entre modos/estados e divergência entre definição e runtime.
- **Motivo:** transforma a cobertura visual ampla em evidência técnica reproduzível.
- **Risco:** promover pureza taxonômica a achado sem impacto.
- **Aceitação:** um achado exige consumidor alcançável e dano observável, contrato violado ou risco concreto; valor local isolado e justificado não é falha; áreas não aplicáveis são marcadas como tal.

### DT-04 — Famílias de tokens contextuais

- **Prioridade:** P1
- **Arquivo-alvo:** novo `plugins/anti-ai-craft/skills/anti-ai-design/references/design-tokens.md`
- **Instrução:** detalhar cor, tipografia, espaço, dimensão, forma, elevação, movimento e layout como famílias opcionais. Para cada família, exigir intenção, naming, tipo/unidade, consumidores, estados, modos e validação. Escalas devem estender o projeto ou nascer de conteúdo e função.
- **Motivo:** aproveita a abrangência da proposta externa sem importar presets.
- **Risco:** criar tokens sem consumidor ou granularidade excessiva.
- **Aceitação:** cada token novo tem ao menos um consumidor previsto e uma intenção; exceções locais são permitidas e justificadas; não há lista universal obrigatória.

### DT-05 — Validação visual e técnica de tokens

- **Prioridade:** P1
- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Instrução:** no passe técnico, verificar resolução de aliases, fonte versus output, consumidores representativos, estados e todos os modos suportados. No passe visual, comparar os mesmos dados e componentes antes/depois, incluindo contraste, zoom, strings longas e reduced motion quando afetados.
- **Motivo:** build bem-sucedido não prova coerência visual, e screenshot isolado não prova integridade do sistema.
- **Risco:** ampliar demais a validação em mudança localizada.
- **Aceitação:** a matriz de testes é proporcional aos tokens alterados; mudança de cor global verifica combinações e estados afetados, enquanto token local verifica apenas consumidores alcançáveis.

### DT-06 — Antipadrões técnicos de tokens

- **Prioridade:** P1
- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-code/references/code-antipatterns.md`
- **Instrução:** adicionar, na interseção com UI, aliases quebrados/circulares, edição manual de output gerado, hardcode que contorna contrato existente, branch de tema duplicada, token sem consumidor e substituição textual de valores sem confirmar semântica.
- **Motivo:** esses defeitos aparecem como código e podem escapar de uma revisão apenas visual.
- **Risco:** sinalizar qualquer literal de estilo como erro.
- **Aceitação:** cada candidato é avaliado contra fonte de verdade, consumidor, repetição e efeito; valores intrínsecos, calculados, de mídia ou de terceiros podem ser mantidos com justificativa.

### DT-07 — Remediar pela fonte e pelo alcance real

- **Prioridade:** P1
- **Arquivos-alvo:** `plugins/anti-ai-craft/skills/anti-ai-remediate/references/remediation-protocol.md` e `plugins/anti-ai-craft/skills/anti-ai-remediate/references/validation-checklist.md`
- **Instrução:** orientar a edição da fonte autoritativa, a regeneração pelo comando oficial e a verificação dos consumidores. Exigir inventário de alcance antes de alterar token compartilhado e comparação dos modos/estados afetados.
- **Motivo:** uma linha em token global pode alterar muitas telas e marcas.
- **Risco:** mudança pequena no diff causar regressão visual ampla ou sobrescrever output gerado.
- **Aceitação:** o handoff informa fonte editada, arquivos regenerados, consumidores examinados, comandos, antes/depois e modos testados; não há substituição em massa sem mapa de uso.

### DT-08 — Gate para alteração global de tokens

- **Prioridade:** P1
- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-remediate/references/approval-gates.md`
- **Instrução:** tratar troca de token global, namespace, provider, pipeline ou estratégia de tema como materialmente ampla quando atingir múltiplas superfícies, mesmo que envolva poucos arquivos.
- **Motivo:** tamanho do diff não representa alcance visual.
- **Risco:** pedir aprovação para correções locais sem impacto amplo.
- **Aceitação:** o gate usa número e criticidade de consumidores, marcas, modos e plataformas; alias local com alcance comprovadamente restrito não exige nova aprovação.

### DT-09 — Evidência opcional no relatório de auditoria

- **Prioridade:** P2
- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-audit/references/report-template.md`
- **Instrução:** incluir uma tabela opcional de sistema de tokens com fonte, camada, token/alias, consumidores, modos/estados, evidência e disposição.
- **Motivo:** facilita deduplicação e passagem de achados para remediação.
- **Risco:** tornar o template obrigatório e ruidoso para repositórios sem UI.
- **Aceitação:** a seção é usada apenas quando tokens estão no escopo e pode ser omitida sem deixar campos vazios.

### DT-10 — Tema dinâmico como entrada não confiável

- **Prioridade:** P2, condicional
- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-security/references/security-checklist.md`
- **Instrução:** adicionar uma verificação curta em entrada/saída somente para tokens ou temas fornecidos por usuário, tenant, CMS ou integração. Validar allowlist de nomes, tipo e faixa de valores, referências a recursos e aplicação no sink correto.
- **Motivo:** um sistema visual configurável pode virar entrada de conteúdo ativo ou consumo externo.
- **Risco:** misturar qualidade visual com segurança e criar falso positivo em tokens estáticos.
- **Aceitação:** nenhum achado é criado sem entrada controlável, caminho alcançável, controle ausente e impacto; tokens locais de build permanecem fora desta verificação.

## Ordem recomendada de incorporação

1. Criar a referência central de tokens e roteá-la pela `anti-ai-design`.
2. Tornar a auditoria capaz de inventariar fonte, aliases, consumidores e modos.
3. Adicionar falhas técnicas à `anti-ai-code`.
4. Proteger a correção com fonte autoritativa, regeneração e gate de alcance.
5. Adicionar a verificação de segurança apenas como ramo condicional de tema externo.
6. Validar as cinco skills e revisar se não foram introduzidos números, stacks, temas ou arquivos obrigatórios.

## Critérios globais de conclusão

- Os nomes das cinco skills, diretórios e política de invocação permanecem iguais.
- Não é criada uma sexta skill para tokens.
- O sistema existente é detectado e classificado antes de qualquer geração.
- Fonte autoritativa e outputs gerados são distinguidos.
- Camadas, aliases, consumidores, modos e estados podem ser auditados.
- Tipografia, cor, espaço e movimento são definidos por papéis e contexto, não por presets universais.
- Dark mode só é criado quando solicitado ou exigido pelo produto.
- Breakpoints continuam derivados do conteúdo e do comportamento.
- Mudanças globais recebem validação e aprovação proporcionais ao alcance.
- A segurança só entra quando existe uma fronteira de confiança real.
- O relatório final registra o que foi preservado, alterado, rejeitado, validado e não testado.

## Resumo final

A unidade externa acrescenta valor principalmente como checklist de descoberta e como inventário de famílias de tokens. O plugin atual já possui uma base conceitual mais madura: hierarquia explícita, consumidores reais, direção contextual, acessibilidade, preservação e rejeição de absolutos.

A incorporação recomendada não é copiar uma escala pronta. É criar um procedimento operacional dentro da `anti-ai-design`, refletir esse procedimento na auditoria, no código e na remediação, e manter a segurança condicional a temas externos. Isso melhora as cinco skills sem impor dark mode, stack, estética, valores fixos ou uma nova skill incompatível.
