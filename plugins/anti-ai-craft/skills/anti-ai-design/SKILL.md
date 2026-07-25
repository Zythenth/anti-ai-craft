---
name: anti-ai-design
description: "Pesquisar, criar brief, planejar arquitetura da informação ou tokens, revisar, implementar ou refatorar interfaces sem recorrer automaticamente a composição genérica. Usar quando o pedido envolver screenshots, wireframes, frontend, componentes visuais, fluxos de interface delimitados, navegação, design system, acessibilidade ou responsividade; não usar para orquestrar uma jornada completa ou multifase, como do briefing à revisão, nem em código sem componente visual. Ler fontes do projeto e visuais fornecidos, produzir direção ou revisão com evidência e editar apenas quando o usuário autorizar."
---

# Design Anti-IA

Tratar “anti-AI” como disciplina de projeto, não como detector de autoria. Nunca afirmar que uma pessoa ou modelo escreveu uma interface. Avaliar se decisões de composição, componentes, conteúdo e decoração respondem ao usuário, à tarefa, ao domínio, aos dados, ao estado, à identidade, à hierarquia e às restrições do produto.

## Preparar o trabalho

1. Confirmar o escopo: pesquisa, análise, planejamento, revisão ou implementação.
2. Ler as fontes de verdade disponíveis antes de propor estética: design guide, design system, README, especificação, código, assets, testes e decisões do usuário.
3. Classificar a superfície predominante: **persuadir**, **operar**, **ler** ou **experienciar**. Uma aplicação operacional não deve receber automaticamente a composição de uma landing page.
4. Fixar o mandato: **preservar**, **refinar** ou **redesenhar**. Ausência de `DESIGN.md` não significa greenfield; polimento local não autoriza rebranding.
5. Identificar usuários, tarefas críticas, dispositivos, conteúdo representativo ou autoritativo, estados e requisitos de acessibilidade.
6. Registrar apenas decisões materiais e suas dependências. Resolver fatos no projeto antes de perguntar; em rodadas de no máximo duas ou três questões, incluir recomendação, fundamento, consequências e o trabalho independente que pode continuar. Declarar pressupostos de baixo risco; não inventar produto, dados ou identidade.
7. Classificar os elementos relevantes do escopo como `reutilizar`, `compor`, `estender`, `criar`, `fora do escopo` ou `desconhecido`, citando componentes, APIs, estados e consumidores reais.
8. Preservar regras específicas do projeto. Fazer requisitos funcionais e WCAG aplicáveis prevalecerem sobre heurísticas estéticas.
9. Quando o pedido for uma jornada completa, multifase e retomável, orientar a invocação explícita de `$anti-ai-design-flow`; manter esta skill adequada a trabalho visual delimitado.

## Carregar referências por necessidade

- Ler [design-principles.md](references/design-principles.md) para briefing, composição, componentes, linguagem visual, conteúdo, estados e responsividade.
- Ler [design-brief.md](references/design-brief.md) ao criar ou atualizar um brief.
- Ler [information-architecture.md](references/information-architecture.md) para navegação, rotas, hierarquia, persistência ou fluxo entre superfícies.
- Ler [design-tokens.md](references/design-tokens.md) para tokens, temas, paleta, tipografia, escala ou design system.
- Ler [design-antipatterns.md](references/design-antipatterns.md) ao detectar defaults prováveis ou revisar aparência genérica.
- Ler [accessibility-baseline.md](references/accessibility-baseline.md) em toda criação, refação ou auditoria de interface.
- Ler [direction-contract.md](references/direction-contract.md) antes de criar, refinar ou redesenhar uma interface.
- Ler [review-workflow.md](references/review-workflow.md) ao implementar, capturar screenshots ou comparar antes/depois.
- Ler [design-review-template.md](references/design-review-template.md) ao produzir revisão formal ou handoff de achados.
- Ler [sources.md](references/sources.md) quando precisar justificar uma regra, resolver conflito ou distinguir requisito, guidance e heurística.

## Executar o workflow

1. Ler o projeto e registrar o estado inicial quando houver código.
2. Identificar a tarefa e os usuários.
3. Localizar regras existentes e ordenar sua autoridade.
4. Inventariar telas, rotas, componentes, conteúdo, mídia, estados e fluxos reais.
5. Quando houver várias superfícies, mapear entradas, navegação, hierarquia, URLs, persistência, caminhos principal/alternativos e recuperação antes da estética.
6. Separar identidade verificável de decoração substituível e registrar o que deve permanecer invariável.
7. Antes do código, escrever um contrato de direção curto: tese, modo, tarefa, primeiro viewport, caminho principal, estrutura, papéis de cor/tipo, assinatura, risco e default da categoria rejeitado.
8. Para tokens, identificar fonte autoritativa, outputs gerados, aliases, consumidores, modos e alcance antes de propor valores.
9. Travar uma referência dominante e limitar fontes secundárias a papéis explícitos; não calcular uma média visual de referências conflitantes.
10. Listar defaults prováveis: composição, componentes, copy, paleta, tipografia, movimento e controles de overflow.
11. Inventariar ações primárias, frequentes, secundárias e destrutivas antes de aceitar kebab, reticências ou menus genéricos.
12. Produzir alternativas somente quando houver decisão material em aberto; comparar consequências, não apenas estilos.
13. Definir estados de componentes por gatilho, alteração visual, estado semântico, ação permitida e recuperação.
14. Ao planejar build, criar fatias verticais por resultado observável com origem, estratégia de reuso, dependências, critérios de pronto e prova; não decompor automaticamente por tecnologia ou arquivo.
15. Implementar apenas quando autorizado, preservando arquitetura, conteúdo essencial e invariantes do produto.
16. Executar a interface real quando o perfil de revisão exigir runtime; calibrar alegações quando houver apenas screenshot ou código.
17. Revisar viewports e estados por criticidade, incluindo teclado, leitor de tela, interrupção e recuperação.
18. Fazer primeiro um passe visual/UX sem consultar detectores; depois um passe técnico/determinístico; sintetizar os dois com evidência.
19. Comparar antes/depois com dados, estados, temas e viewports equivalentes.
20. Produzir IDs estáveis para achados de revisão e solicitar seleção explícita antes de qualquer correção.
21. Solicitar aprovação antes de uma alteração visualmente ampla ou de uma escolha que redefine identidade, navegação, tema ou alcance global de tokens.

## Operar por modo

### Pesquisa ou planejamento

Não editar. Entregar brief, inventário, arquitetura, riscos, direção recomendada, alternativas relevantes, critérios mensuráveis e plano de validação.

### Brief de design

Usar [design-brief.md](references/design-brief.md). Produzir o brief na resposta por padrão. Salvar somente com autorização específica, sem sobrescrever material existente e sem iniciar implementação. Manter o estado `rascunho`, `bloqueado`, `aprovado` ou `superado`.

### Revisão

Não editar por padrão nem criar capturas permanentes sem autorização. Declarar perfil de evidência, cobertura e limitações. Citar screenshot, viewport, componente, arquivo ou linha quando disponível. Separar:

- falha funcional ou normativa;
- inconsistência com fonte de verdade;
- padrão genérico contextual;
- heurística;
- preferência subjetiva;
- falso positivo rejeitado.

### Implementação

Fazer mudança pequena e verificável. Usar conteúdo fiel e dados representativos;
preferir fixtures. Usar dados reais somente quando forem necessários, autorizados,
minimizados e redigidos. Confirmar o ambiente antes de executar a aplicação e não
submeter formulários, enviar mensagens, fazer upload, pagamento, exclusão, escrita
em banco ou chamada externa mutável sem autorização específica. Implementar
estados e comportamento, não apenas aparência. Rodar lint, testes, build e revisão
no navegador conforme o projeto permitir. Informar qualquer validação não executada.

## Contrato de saída

Entregar, conforme o modo:

- contexto e fontes de verdade lidas;
- tarefa, usuários, conteúdo, estados e restrições;
- defaults prováveis e por que se aplicam ou não;
- direção ou achados com nível de evidência;
- contrato de direção e referência dominante quando houver criação ou redesign;
- decisões preservadas, alteradas e rejeitadas;
- arquitetura, tokens, tarefas ou artefatos superados e dependentes a revalidar;
- critérios de aceitação mensuráveis;
- validações executadas e evidência obtida;
- riscos, lacunas e aprovação humana necessária.

Não transformar dark mode, ciano, serif, mono, cards, bordas, radius, simetria ou assimetria em proibições universais. Um sinal isolado não comprova problema nem autoria.
