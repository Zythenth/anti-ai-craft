---
name: anti-ai-design
description: "Pesquisar, planejar, revisar, criar ou refatorar interfaces de produto sem recorrer automaticamente a composição genérica. Usar somente quando invocada explicitamente para screenshots, wireframes, frontend, acessibilidade ou responsividade; não usar em tarefas de código sem componente visual. Ler fontes do projeto e visuais fornecidos, produzir direção ou revisão com evidência e editar apenas quando o usuário autorizar."
---

# Design Anti-IA

Tratar “anti-AI” como disciplina de projeto, não como detector de autoria. Nunca afirmar que uma pessoa ou modelo escreveu uma interface. Avaliar se decisões de composição, componentes, conteúdo e decoração respondem ao usuário, à tarefa, ao domínio, aos dados, ao estado, à identidade, à hierarquia e às restrições do produto.

## Preparar o trabalho

1. Confirmar o escopo: pesquisa, análise, planejamento, revisão ou implementação.
2. Ler as fontes de verdade disponíveis antes de propor estética: design guide, design system, README, especificação, código, assets, testes e decisões do usuário.
3. Classificar a superfície predominante: **persuadir**, **operar**, **ler** ou **experienciar**. Uma aplicação operacional não deve receber automaticamente a composição de uma landing page.
4. Fixar o mandato: **preservar**, **refinar** ou **redesenhar**. Ausência de `DESIGN.md` não significa greenfield; polimento local não autoriza rebranding.
5. Identificar usuários, tarefas críticas, dispositivos, conteúdo real, estados e requisitos de acessibilidade.
6. Perguntar no máximo duas ou três questões quando as respostas mudarem materialmente a direção. Declarar pressupostos de baixo risco; não inventar produto, dados ou identidade.
7. Preservar regras específicas do projeto. Fazer requisitos funcionais e WCAG aplicáveis prevalecerem sobre heurísticas estéticas.

## Carregar referências por necessidade

- Ler [design-principles.md](references/design-principles.md) para briefing, composição, componentes, linguagem visual, conteúdo, estados e responsividade.
- Ler [design-antipatterns.md](references/design-antipatterns.md) ao detectar defaults prováveis ou revisar aparência genérica.
- Ler [accessibility-baseline.md](references/accessibility-baseline.md) em toda criação, refação ou auditoria de interface.
- Ler [direction-contract.md](references/direction-contract.md) antes de criar, refinar ou redesenhar uma interface.
- Ler [review-workflow.md](references/review-workflow.md) ao implementar, capturar screenshots ou comparar antes/depois.
- Ler [sources.md](references/sources.md) quando precisar justificar uma regra, resolver conflito ou distinguir requisito, guidance e heurística.

## Executar o workflow

1. Ler o projeto e registrar o estado inicial quando houver código.
2. Identificar a tarefa e os usuários.
3. Localizar regras existentes e ordenar sua autoridade.
4. Inventariar telas, rotas, componentes, conteúdo, mídia, estados e fluxos reais.
5. Separar identidade verificável de decoração substituível e registrar o que deve permanecer invariável.
6. Antes do código, escrever um contrato de direção curto: tese, modo, tarefa, primeiro viewport, caminho principal, estrutura, papéis de cor/tipo, assinatura, risco e default da categoria rejeitado.
7. Travar uma referência dominante e limitar fontes secundárias a papéis explícitos; não calcular uma média visual de referências conflitantes.
8. Listar defaults prováveis: composição, componentes, copy, paleta, tipografia, movimento e controles de overflow.
9. Inventariar ações primárias, frequentes, secundárias e destrutivas antes de aceitar kebab, reticências ou menus genéricos.
10. Produzir alternativas somente quando houver decisão material em aberto; comparar consequências, não apenas estilos.
11. Definir estados de componentes por gatilho, alteração visual, estado semântico, ação permitida e recuperação.
12. Implementar apenas quando autorizado, preservando arquitetura, conteúdo essencial e invariantes do produto.
13. Executar a interface real e capturar telas reais; não validar apenas pelo código.
14. Revisar desktop, tablet e mobile como composições adaptativas e testar estados extremos, teclado, leitor de tela, interrupção e recuperação.
15. Fazer primeiro um passe visual/UX sem consultar detectores; depois um passe técnico/determinístico; sintetizar os dois com evidência.
16. Comparar antes/depois com dados, estados, temas e viewports equivalentes.
17. Solicitar aprovação antes de uma alteração visualmente ampla ou de uma escolha que redefine a identidade.

## Operar por modo

### Pesquisa ou planejamento

Não editar. Entregar brief, inventário, riscos, direção recomendada, alternativas relevantes, critérios mensuráveis e plano de validação.

### Revisão

Não editar por padrão. Citar screenshot, viewport, componente, arquivo ou linha quando disponível. Separar:

- falha funcional ou normativa;
- inconsistência com fonte de verdade;
- padrão genérico contextual;
- heurística;
- preferência subjetiva;
- falso positivo rejeitado.

### Implementação

Fazer mudança pequena e verificável. Usar conteúdo e dados reais. Implementar estados e comportamento, não apenas aparência. Rodar lint, testes, build e revisão no navegador conforme o projeto permitir. Informar qualquer validação não executada.

## Contrato de saída

Entregar, conforme o modo:

- contexto e fontes de verdade lidas;
- tarefa, usuários, conteúdo, estados e restrições;
- defaults prováveis e por que se aplicam ou não;
- direção ou achados com nível de evidência;
- contrato de direção e referência dominante quando houver criação ou redesign;
- decisões preservadas, alteradas e rejeitadas;
- critérios de aceitação mensuráveis;
- validações executadas e evidência obtida;
- riscos, lacunas e aprovação humana necessária.

Não transformar dark mode, ciano, serif, mono, cards, bordas, radius, simetria ou assimetria em proibições universais. Um sinal isolado não comprova problema nem autoria.
