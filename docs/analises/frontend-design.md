# Análise da unidade `frontend-design`

## Escopo e método

Esta análise compara integralmente a unidade externa `frontend-design/SKILL.md` com as cinco skills atuais do plugin:

- `anti-ai-design`: `SKILL.md`, `agents/openai.yaml` e seis referências;
- `anti-ai-code`: `SKILL.md`, `agents/openai.yaml` e seis referências;
- `anti-ai-audit`: `SKILL.md`, `agents/openai.yaml` e três referências;
- `anti-ai-remediate`: `SKILL.md`, `agents/openai.yaml` e três referências;
- `anti-ai-security`: `SKILL.md`, `agents/openai.yaml` e quatro referências.

O plugin não foi alterado. A comparação considera a intenção da regra, não semelhança textual. As ideias aproveitáveis abaixo foram reformuladas para preservar o modelo atual: contexto antes de estética, evidência antes de alegação, edição somente quando autorizada, acessibilidade aplicável e ausência de stack ou estilo obrigatório.

## Inventário da unidade externa

A unidade contém um único `SKILL.md`, sem referências auxiliares ou configuração de agente própria. Seu conteúdo se divide em:

1. exemplos de pedidos de criação de interface;
2. inspeção do projeto antes de escrever código;
3. entendimento de problema, público, tom e restrições;
4. escolha explícita de direção estética;
5. catálogo de oito filosofias visuais com prescrições de tipografia, cor, composição, espaçamento, movimento e acabamento;
6. orientações de implementação visual;
7. regras obrigatórias de mobile-first;
8. geração de tema escuro e redução de movimento.

### Pontos fortes

- Exige olhar o projeto antes de gerar componentes.
- Procura componentes, tokens, temas, fontes, padrões de layout e dependências já existentes.
- Prefere composição ou extensão de componentes a duplicação.
- Obriga a declarar uma direção visual em vez de misturar estilos por impulso.
- Trata tipografia, cor, layout, espaçamento, movimento e detalhes como um conjunto coerente.
- Chama atenção para toque, largura de leitura, navegação compacta, contraste entre temas e redução de movimento.

### Limitações

- Converte várias escolhas contextuais em regras universais.
- Mistura descoberta de arquitetura com suposições sobre pastas, frameworks e bibliotecas específicas.
- O catálogo estético pode virar um seletor de presets e produzir outra forma de homogeneização.
- Prescreve famílias tipográficas, paletas, durações, efeitos e tipos de navegação sem comprovar vínculo com produto ou marca.
- Recomenda carregamento remoto de fontes por padrão, sem considerar política do projeto, privacidade, CSP, disponibilidade, performance ou funcionamento offline.
- Declara mobile-first obrigatório mesmo quando a tarefa, o público ou a superfície predominante podem exigir outra estratégia.
- Obriga tema escuro mesmo quando não existe requisito, design system ou capacidade de manter dois temas corretamente.
- A validação é menor que a do plugin atual: não exige execução real, screenshots comparáveis, estados extremos, foco completo, zoom, reflow, text spacing, leitor de tela ou gates de aprovação.
- Não trata hierarquia de ações nem o uso reflexo de kebab/reticências.

## Avaliação por área

### Pré-implementação

O plugin já exige leitura de fontes de verdade, classificação da superfície, mandato de preservar/refinar/redesenhar, inventário de telas, rotas, componentes, estados e mídia, além de critérios de aceitação. A unidade externa acrescenta uma lista operacional útil de lugares onde procurar componentes, tokens, temas, histórias, fontes e dependências.

O ganho real não está em fixar nomes de pastas ou frameworks, mas em tornar o preflight verificável: para o escopo relevante, registrar componente candidato, API pública, estados, consumidores de tokens, fonte do tema, exemplos executáveis e dependências visuais. Exigir a listagem de todos os componentes de um repositório grande seria caro e desproporcional.

### Reuso

O plugin já preserva arquitetura, tokens e componentes locais e proíbe dependência, framework ou refatoração sem necessidade. Falta apenas tornar explícita a decisão entre reutilizar, compor, estender ou criar para os componentes diretamente afetados.

Esse registro reduz duplicação e também combate um padrão anti-IA comum: gerar um novo botão, card, modal ou sistema de tokens porque o modelo não procurou o equivalente existente. Ele deve ser proporcional ao escopo, não um censo completo do repositório.

### Responsividade

O plugin atual é mais seguro: usa composições adaptativas, breakpoints determinados por conteúdo, reflow em 320 CSS px, zoom, text spacing, strings longas, orientação, safe areas, teclado virtual e ausência de hover. A obrigação externa de começar sempre em 375 px e usar apenas media queries de crescimento não deve ser incorporada.

Há duas melhorias úteis:

- em superfícies de leitura, validar medida de linha e ritmo em cada composição relevante, sem transformar uma faixa numérica em norma universal;
- em formulários mobile, verificar se o foco provoca zoom, clipping ou perda de contexto e se a ação principal continua disponível com o teclado virtual.

O alvo de toque deve continuar seguindo o baseline normativo e a meta maior da plataforma ou do produto. Um número único não deve substituir contexto, espaçamento entre alvos e exceções aplicáveis.

### Acessibilidade

A cobertura atual é substancialmente superior. Ela inclui WCAG aplicável, semântica, teclado, foco, modal, abas, menus, formulários, live regions, contraste, forced colors, reflow, zoom, text spacing, touch, movimento e matriz manual.

Da unidade externa, apenas o lembrete de validar redução de movimento junto do tema merece reforço operacional. As regras numéricas ou escolhas de navegação não devem substituir o baseline já existente.

### Temas

Esta é a principal lacuna aproveitável. O plugin testa light/dark e forced colors e possui uma cadeia de tokens, mas não define um contrato completo para temas.

Quando o produto já oferece ou exige mais de um tema, o workflow deve registrar:

- fonte de verdade e camadas de tokens;
- temas e preferências realmente suportados;
- precedência entre sistema, configuração do produto e escolha manual;
- persistência e comportamento antes da hidratação;
- papéis semânticos em superfícies, texto, bordas, foco e estados;
- comportamento de imagens, ícones, formulários nativos, overlays e sombras;
- contraste e legibilidade em cada estado;
- relação com forced colors e reduced motion.

O plugin não deve gerar tema escuro automaticamente. Adicionar um tema duplica a superfície de manutenção e exige autorização quando amplia identidade ou escopo.

### Estética

O contrato de direção atual já é mais robusto porque parte de tarefa, identidade, conteúdo, estado e invariantes. O catálogo externo pode servir somente como exemplo de que uma direção precisa formar um sistema coerente.

A melhoria adaptável é ampliar o contrato de direção para registrar, quando relevantes:

- tipografia;
- papéis de cor;
- composição e grid;
- densidade e espaçamento;
- movimento;
- superfícies e detalhes;
- mídia e iconografia.

Não incorporar catálogos fechados, fontes obrigatórias, paletas prontas, tempos fixos, proibições de famílias populares ou obrigação de assimetria, ruído, gradiente, textura ou ornamentação. Essas prescrições podem trocar um default genérico por outro.

### Componentes

O plugin já tem cobertura detalhada para tabelas, listas, formulários, modais, abas, menus, busca, tooltips, cards e bento. Também liga estrutura visual a semântica, teclado e estados.

A unidade externa não melhora esse conjunto, mas reforça a necessidade de localizar APIs e exemplos dos componentes existentes antes de criar outro. Esse ponto deve entrar no preflight e na evidência de reuso.

#### Kebab e reticências

A unidade externa não aborda hierarquia de ações. O plugin atual deve ser preservado:

- kebab/reticências não são proibidos nem indicam autoria;
- servem a duas ou mais ações realmente secundárias, relacionadas e pouco frequentes, ou a uma restrição de espaço comprovada;
- uma única ação deve aparecer diretamente;
- ações primárias ou frequentes continuam visíveis;
- o controle precisa de nome acessível, estado expandido, teclado, foco, Escape e retorno de foco;
- a revisão deve contar ocorrências e inspecionar conteúdos reais, em vez de aceitar uma coluna de ações repetida por conveniência.

Esse tratamento contextual é mais forte que qualquer proibição estética.

### Mídia

O plugin atual também é superior: preserva asset, slot, proporção, crop, texto alternativo, legenda, estado de carregamento e integridade do conteúdo. A sugestão externa de criar atmosfera com fundos, texturas e gradientes não deve virar obrigação.

Uma melhoria transversal é proibir a introdução automática de fonte, imagem, script ou stylesheet remoto. Quando um recurso externo for realmente necessário, a decisão deve passar por arquitetura local, política do projeto, origem, privacidade, CSP, performance, cache, fallback, integridade e disponibilidade offline aplicáveis.

### Movimento

O plugin já exige função, interrupção e alternativa reduzida, e rejeita cascata, bounce, partículas, hover lift, fundo animado e atraso teatral sem motivo.

Pode ficar mais verificável classificando cada movimento relevante como:

- feedback de estado;
- relação espacial ou transição;
- orientação;
- decorativo ou ambiental.

Movimento decorativo ou ambiental deve ter justificativa, contenção e alternativa. Não incorporar bibliotecas, curvas, durações ou estilos de animação como defaults.

### Validação

O plugin atual exige execução real, screenshots, comparação antes/depois, viewports estreito/intermediário/amplo, estados extremos, passes visual e técnico independentes, lint, testes, build e gate humano. A unidade externa não contém equivalentes suficientes.

As adições úteis são:

- registrar a decisão de reuso para componentes do escopo;
- incluir uma matriz de tema quando houver múltiplos temas;
- verificar medida de leitura nas superfícies editoriais;
- testar foco de campos com teclado virtual e comportamento de zoom nos navegadores móveis aplicáveis;
- registrar qualquer nova origem de recurso visual como mudança de dependência ou boundary.

## Matriz de cobertura

| Item avaliado | Estado | Decisão |
|---|---|---|
| Ler o projeto antes de escrever código | já temos | Preservar o workflow atual. |
| Identificar componentes existentes no escopo | já temos | Tornar a evidência de reuso mais explícita. |
| Registrar API, propriedades, eventos e estados dos componentes candidatos | parcial | Adicionar somente para componentes relevantes ao pedido. |
| Examinar tokens e consumidores reais | já temos | A cadeia atual é mais completa. |
| Examinar configuração real de tema | parcial | Expandir para contrato de temas. |
| Procurar histórias, catálogos ou exemplos executáveis | não temos | Incluir como fonte opcional de verdade. |
| Examinar carregamento e fallback de fontes | parcial | Já há fallback; falta inventário explícito e gate para origem remota. |
| Examinar layout, containers e breakpoints existentes | já temos | Preservar. |
| Examinar dependências visuais existentes | parcial | Integrar ao preflight e à checagem de código/segurança. |
| Reutilizar, compor ou estender antes de duplicar | já temos | Registrar a decisão no relatório. |
| Entender problema, público, tom e restrições | já temos | Preservar. |
| Declarar direção antes do código | já temos | O contrato atual é mais verificável. |
| Traduzir direção em eixos visuais coerentes | parcial | Ampliar o contrato sem catálogo fixo. |
| Catálogo fechado de filosofias estéticas | não incorporar | Pode virar seletor de presets e importar identidade. |
| Fontes específicas por filosofia | não incorporar | Voz, idioma, licença, performance e sistema local prevalecem. |
| Banir famílias tipográficas populares por nome | não incorporar | Popularidade isolada não demonstra inadequação. |
| Carregar fontes remotas por padrão | não incorporar | Cria dependência, risco de privacidade, CSP, disponibilidade e performance. |
| Fórmula fixa de cor dominante e acento forte | não incorporar | Papéis semânticos e identidade do produto prevalecem. |
| Assimetria, sobreposição ou quebra de grid por default | não incorporar | Só aceitar com ganho para tarefa e conteúdo. |
| Fundos atmosféricos e texturas por default | não incorporar | Não substituir hierarquia nem mídia real por decoração. |
| Proporcionalidade entre ambição visual e complexidade | parcial | Adotar como gate de custo e manutenção, não como licença para volume. |
| Mobile-first obrigatório em 375 px | não incorporar | Estratégia depende de público, superfície e produto. |
| Media queries de crescimento como única técnica válida | não incorporar | Preservar arquitetura CSS e breakpoints do projeto. |
| Alvo de toque único e universal | parcial | Manter baseline normativo e meta de plataforma/produto. |
| Tamanho tipográfico mobile único e universal | não incorporar | Testar legibilidade e zoom no contexto real. |
| Navegação mobile limitada a três padrões | não incorporar | Escolher pelo modelo de informação e plataforma. |
| Medida de leitura verificada por breakpoint | não temos | Adicionar para superfícies de leitura, sem faixa rígida universal. |
| Mobile como composição repriorizada | já temos | Preservar; é mais forte que apenas empilhar. |
| Gerar tema escuro sempre | não incorporar | Exige requisito, design system, escopo e manutenção. |
| Reusar tokens de tema existentes | já temos | Reforçar fonte de verdade e consumidores. |
| Precedência entre preferência do sistema e escolha manual | não temos | Adicionar quando o produto suportar ambos. |
| Evitar inversão mecânica de cores | parcial | Formalizar por papéis semânticos e estados. |
| Contraste e reduced motion em temas | já temos | Integrar em uma matriz única de validação. |
| Movimento ligado a estado e orientação | já temos | Classificar para facilitar revisão. |
| Biblioteca de animação obrigatória por stack | não incorporar | Reutilizar stack e arquitetura existentes. |
| Duração e easing prescritos por estética | não incorporar | Derivar de função, plataforma e preferência do usuário. |
| Integridade de mídia, proporção, crop e loading | já temos | A cobertura atual é superior. |
| Execução real e screenshots comparáveis | já temos | A cobertura atual é superior. |
| Estados extremos e recuperação | já temos | A cobertura atual é superior. |
| Evidência explícita de decisão de reuso | não temos | Adicionar ao preflight e ao relatório. |
| Matriz de validação por tema | parcial | Consolidar temas, estados, contraste e movimento. |

## Recomendações adaptadas

As instruções abaixo descrevem comportamento novo em linguagem própria. Não exigem renomear skills, alterar comandos, mudar a política de invocação ou adicionar dependências.

### FD-01 — Inventário de reuso proporcional

- **Prioridade:** P1
- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md`
- **Apoio:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Instrução:** antes de criar um componente, registrar apenas os candidatos relevantes encontrados no design system, diretórios de UI, histórias, exemplos ou testes. Para cada candidato, anotar API pública, estados cobertos e decisão `reutilizar`, `compor`, `estender` ou `criar`, com motivo.
- **Motivo:** reduz componentes duplicados e APIs inventadas sem exigir varredura desproporcional do repositório inteiro.
- **Risco:** transformar tarefas pequenas em documentação excessiva.
- **Critério de aceitação:** toda criação de componente no escopo tem ao menos uma busca registrada e uma decisão de reuso; quando não houver candidato, a lacuna é declarada.

### FD-02 — Perfil de direção por eixos

- **Prioridade:** P1
- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-design/references/direction-contract.md`
- **Apoio:** `plugins/anti-ai-craft/skills/anti-ai-design/references/design-principles.md`
- **Instrução:** ampliar o contrato de direção para registrar somente os eixos relevantes entre tipografia, cor, composição/grid, densidade/espaçamento, movimento, superfícies/detalhes e mídia/iconografia. Cada escolha deve indicar vínculo com tarefa, domínio, identidade ou restrição.
- **Motivo:** transforma uma “vibe” em decisões coerentes sem recorrer a um catálogo estético fixo.
- **Risco:** o contrato ficar longo ou ser preenchido com adjetivos vagos.
- **Critério de aceitação:** cada eixo preenchido possui decisão verificável e justificativa; eixos não aplicáveis podem ser omitidos; nenhuma fonte, paleta, efeito ou layout é escolhido apenas pelo nome de um estilo.

### FD-03 — Contrato condicional de temas

- **Prioridade:** P1
- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-design/references/direction-contract.md`
- **Apoio:** `plugins/anti-ai-craft/skills/anti-ai-design/references/accessibility-baseline.md`
- **Instrução:** quando houver mais de um tema, registrar fonte de verdade, temas suportados, precedência, persistência, estado antes da hidratação, papéis semânticos, assets, controles nativos, overlays, contraste, forced colors e reduced motion. Não criar novo tema sem requisito ou autorização.
- **Motivo:** evita inversão mecânica, flash de tema incorreto, estados ilegíveis e duplicação de valores.
- **Risco:** ampliar escopo de uma correção visual localizada.
- **Critério de aceitação:** todos os temas suportados preservam hierarquia, estados, foco e contraste; escolha manual e preferência do sistema têm comportamento documentado; novo tema só entra com autorização explícita.

### FD-04 — Gate para recursos visuais externos

- **Prioridade:** P1
- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-design/references/direction-contract.md`
- **Apoio:** `plugins/anti-ai-craft/skills/anti-ai-code/references/code-antipatterns.md` e `plugins/anti-ai-craft/skills/anti-ai-security/references/security-checklist.md`
- **Instrução:** antes de adicionar fonte, imagem, stylesheet, script ou biblioteca visual externa, procurar alternativa local aprovada e verificar necessidade, origem, política do projeto, privacidade, CSP, integridade, performance, cache, fallback e funcionamento degradado aplicáveis.
- **Motivo:** uma decisão estética não deve introduzir silenciosamente dependência de rede, nova origem confiável ou risco de supply chain.
- **Risco:** bloquear um asset legítimo por falta de informação.
- **Critério de aceitação:** toda nova origem ou dependência visual tem necessidade e validações registradas; incerteza relevante vira decisão pendente, não instalação automática.

### FD-05 — Validação de leitura e formulário mobile

- **Prioridade:** P2
- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-design/references/accessibility-baseline.md`
- **Apoio:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Instrução:** para superfícies de leitura, verificar medida de linha, ritmo e continuidade nos viewports pertinentes. Para formulários mobile, testar foco, zoom do navegador, teclado virtual, safe area, clipping e acesso à ação principal.
- **Motivo:** cobre problemas reais levantados pela unidade externa sem impor largura, tamanho de fonte ou dispositivo universal.
- **Risco:** tratar uma preferência editorial como falha normativa.
- **Critério de aceitação:** o relatório separa legibilidade observada de requisito normativo e registra navegador, viewport e estado; nenhum campo ou ação essencial fica inacessível durante entrada.

### FD-06 — Matriz de validação de tema

- **Prioridade:** P2
- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Apoio:** `plugins/anti-ai-craft/skills/anti-ai-audit/references/audit-checklist.md`
- **Instrução:** quando múltiplos temas fizerem parte do escopo, cruzar tema com estados críticos e ao menos um viewport estreito e um amplo; incluir foco, erro, disabled, loading, overlays, mídia, forced colors e reduced motion quando aplicáveis.
- **Motivo:** “possui dark mode” não demonstra que o tema funciona fora do estado ideal.
- **Risco:** explosão combinatória.
- **Critério de aceitação:** a matriz é proporcional ao risco, cobre estados que mudam semântica ou contraste e declara combinações não testadas.

### FD-07 — Classificação funcional de movimento

- **Prioridade:** P2
- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-design/references/design-principles.md`
- **Apoio:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Instrução:** classificar movimentos relevantes como feedback, transição espacial, orientação ou decoração/ambiente. Exigir função observável para os três primeiros e justificativa, contenção e alternativa para o último.
- **Motivo:** facilita distinguir movimento útil de microinterações espalhadas por reflexo.
- **Risco:** burocratizar transições triviais.
- **Critério de aceitação:** movimentos materiais têm categoria e comportamento em reduced motion; animações removidas não podem esconder conteúdo ou estado.

### FD-08 — Evidência de reuso na auditoria

- **Prioridade:** P2
- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-audit/references/audit-checklist.md`
- **Instrução:** ao reportar duplicação visual ou componente genérico, verificar primeiro o componente existente, sua API, alcance e limitações. Não declarar duplicação apenas por aparência.
- **Motivo:** conecta o inventário de pré-implementação ao padrão de evidência da auditoria.
- **Risco:** um componente semelhante pode ter contrato incompatível.
- **Critério de aceitação:** o achado identifica candidato real de reuso e demonstra compatibilidade ou descreve por que extensão/composição é viável.

## Decisões de não incorporação

Não incorporar:

- catálogo de estéticas como menu obrigatório;
- associação rígida entre estética e fontes, cores, formas, grids ou animações;
- proibição de fontes, gradientes, sombras, simetria, cards ou dark mode por aparência isolada;
- obrigação de assimetria, sobreposição, ruído, textura ou “ousadia”;
- geração automática de tema escuro;
- carregamento remoto de fontes por padrão;
- mobile-first universal, viewport inicial único ou técnica CSS única;
- tamanho tipográfico, alvo de toque, medida de linha, duração ou easing como números universais;
- hamburger, tabs inferiores ou drawer como únicas soluções mobile;
- complexidade maior apenas para sinalizar autoria ou criatividade.

Esses itens entram em conflito com a própria missão do plugin: impedir que uma receita substitua tarefa, evidência, identidade e restrições reais.

## Compatibilidade

As recomendações preservam:

- os cinco nomes de skill e suas formas de invocação;
- descrições e política de invocação explícita;
- separação entre design, código, auditoria, remediação e segurança;
- auditoria somente leitura;
- remediação limitada a achados aprovados;
- proibição de stack, dependência, identidade ou tema novo sem necessidade e autorização;
- regra contextual para kebab/reticências;
- baseline de acessibilidade e validação já existente.

Nenhuma recomendação exige alteração de manifesto, estrutura pública, nome de arquivo, comando de instalação ou API do plugin.

## Resumo

A unidade externa confirma que inspeção prévia, reuso e direção visual explícita são importantes, mas o plugin atual já as implementa com mais evidência, acessibilidade e segurança. As melhores melhorias são operacionais: inventário proporcional de componentes e APIs, perfil de direção por eixos, contrato condicional de temas, gate para recursos externos, validação mobile de leitura/formulários, matriz de temas e evidência de reuso.

O catálogo estético e as regras universais de fonte, cor, layout, mobile, tema e movimento não devem ser incorporados. Eles poderiam recriar exatamente o comportamento anti-IA que o plugin procura evitar: escolher uma receita visual pronta antes de compreender o produto.
