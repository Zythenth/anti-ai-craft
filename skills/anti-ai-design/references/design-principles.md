# Princípios de design contextual

## Sumário

- [Modelo de decisão](#modelo-de-decisão)
- [Briefing e fontes de verdade](#briefing-e-fontes-de-verdade)
- [Identidade e composição](#identidade-e-composição)
- [Densidade, cards e bento](#densidade-cards-e-bento)
- [Estrutura de aplicativo](#estrutura-de-aplicativo)
- [Menu de três pontos](#menu-de-três-pontos)
- [Linguagem visual](#linguagem-visual)
- [Conteúdo, microcopy e estados](#conteúdo-microcopy-e-estados)
- [Responsividade](#responsividade)
- [Critérios mensuráveis portáveis](#critérios-mensuráveis-portáteis)

## Modelo de decisão

Exigir que toda decisão relevante responda a pelo menos um destes fatores:

1. usuário;
2. tarefa;
3. domínio;
4. dados e conteúdo;
5. estado;
6. identidade;
7. hierarquia;
8. restrição funcional, técnica ou normativa.

Se a única justificativa for “é moderno”, “parece premium”, “o componente existe” ou “é o padrão do gerador”, tratar como default provável e reavaliar.

## Briefing e fontes de verdade

- Formular a tarefa principal, tarefas secundárias, frequência, risco de erro e definição de sucesso.
- Identificar públicos, contexto de uso, dispositivos, input, idioma, localização e necessidades de acesso.
- Ler design guide, design system, tokens, componentes, README, especificação, código, assets, testes e decisões do usuário.
- Inventariar dados mínimos, máximos, ausentes, lentos, inválidos, não autorizados e offline.
- Preservar padrões locais válidos. Não importar identidade de referências externas.
- Usar uma referência dominante apenas para direção; registrar quais características são adotadas, adaptadas e rejeitadas.

## Identidade e composição

- Derivar identidade de vocabulário, conteúdo, materiais, relações de informação e comportamento do produto.
- Separar assinatura de ornamento. Uma assinatura pode ser uma composição, tipografia, ritmo, representação de dados ou interação que pertença ao domínio.
- Tornar a tarefa principal identificável rapidamente.
- Fazer área, posição, contraste, escala e proximidade refletirem importância e relação.
- Preferir reconhecimento a memorização: manter opções, estado, contexto e próximos passos visíveis ou recuperáveis no ponto de uso. Não exigir que a pessoa recorde códigos, caminhos, convenções ocultas ou informações de outra tela.
- Usar assimetria para prioridade e simetria para comparação; nenhuma é default universal.
- Usar espaço para leitura, toque e agrupamento, não para vazio cenográfico.
- Fazer a hierarquia sobreviver sem glow, gradiente, sombra, bordas e cor.

## Densidade, cards e bento

- Escolher densidade pelo volume, frequência, ambiente e precisão exigida.
- Preferir proximidade, alinhamento, divisores, listas, tabelas e summary lists antes de caixas.
- Usar card quando o conteúdo for unidade autônoma, tiver ação/estado próprio ou precisar mover-se como conjunto.
- Aplicar o teste sem caixa: retirar a borda; se a relação continuar clara e a caixa não tiver função, removê-la.
- Usar bento somente para overview modular real, com hierarquia e ordem mobile comprovadas.
- Evitar card dentro de card e níveis de superfície sem modelo de profundidade.

## Estrutura de aplicativo

### Sidebar e topbar

- Usar sidebar para destinos persistentes e frequentes, não para simular dashboard.
- Usar topbar para navegação, busca, ação ou contexto real; não criar uma faixa de métricas decorativas.
- Manter nomes, localização, estado ativo, teclado e foco consistentes.

### Hero

- Reservar hero para comunicação ou onboarding que realmente precise de uma proposição dominante.
- Não inserir hero promocional em fluxo operacional, painel denso ou ferramenta sem justificativa.

### Tabelas e listas

- Usar tabela para comparação bidimensional.
- Usar lista para registros homogêneos e summary list para pares rótulo/valor.
- Preservar headers, contexto, semântica, ordenação e overflow local quando a bidimensionalidade for necessária.

### Formulários

- Agrupar por tarefa, não por cardização.
- Usar label persistente; placeholder é exemplo.
- Preservar valores após erro e oferecer recuperação objetiva.
- Manter ação primária visível e nomeada por verbo concreto.

### Modais

- Usar para tarefa curta, focada e bloqueante.
- Evitar para leitura longa, comparação, navegação principal, formulário complexo ou modal aninhado.
- Implementar nome, foco inicial, contenção, Escape, fechamento visível, fundo inerte e retorno de foco.

### Abas

- Usar para painéis irmãos no mesmo contexto quando comparação simultânea não for necessária.
- Não disfarçar destinos principais como tabs.
- Implementar relação tab–painel, estado, roving tabindex e teclas do padrão da plataforma.

### Menus, busca e overflow

- Usar busca somente com dados reais e estados distintos: vazio inicial, zero resultado, loading, erro e indisponível.
- Usar menus para conjuntos coerentes de ações; evitar submenus profundos.
- Tratar tooltip como explicação, nunca como único acesso a ação ou informação essencial.

## Menu de três pontos

Antes de criar um kebab, reticências ou coluna genérica de “ações”, inventariar todas as ações do objeto e sua frequência. Adotar overflow somente quando houver duas ou mais ações realmente secundárias, pouco frequentes e relacionadas, ou uma restrição de espaço comprovada. Com uma única ação, exibi-la diretamente. Se editar, salvar, executar ou outra ação frequente estiver no menu, reprojetar a hierarquia antes de aceitar o componente.

Um kebab ou menu de reticências:

- não é proibido e não prova autoria;
- serve a ações secundárias relacionadas ao mesmo objeto;
- não deve aparecer em cada linha ou card por reflexo;
- não deve ser copiado por um `map` para todo item sem um modelo de ações e estados por item;
- não substitui hierarquia;
- não deve conter apenas uma ação;
- não deve esconder salvar, editar, confirmar, executar ou excluir crítico sem justificativa;
- mantém ações primárias e frequentes visíveis;
- usa trigger nomeado e estado expandido;
- suporta teclado, foco inicial, setas conforme o padrão, Escape e retorno de foco.

Na revisão, contar ocorrências, abrir exemplos reais e verificar quantos menus contêm zero, uma ou ações repetidas. Não aprovar o padrão apenas porque economiza largura ou já existe no kit de componentes.

## Linguagem visual

### Tokens e consumidores

- Organizar tokens em camadas explícitas: `primitivo → semântico → componente`.
- Usar primitivos para valores brutos, semânticos para intenção e tokens de componente apenas quando houver variação local justificável.
- Fazer componentes reais consumirem tokens semânticos ou de componente; não manter uma taxonomia decorativa enquanto o código usa hex, espaçamento ou radius soltos.
- Verificar estados como hover, focus, disabled, erro, sucesso, contraste e tema. Um token sem consumidor ou um consumidor que contorna a cadeia deve ser removido, conectado ou justificado.

### Tipografia

- Escolher famílias por voz, legibilidade, idiomas, performance e papéis.
- Limitar papéis, não impor número universal de fontes.
- Usar mono para código/dados quando servir à leitura; evitar mono integral por estética reflexa.
- Limitar caixa alta e tracking a conteúdo curto que continue legível.

### Cor

- Mapear cada cor a papel semântico ou identitário.
- Não depender apenas de cor.
- Usar gradiente, glass, glow, textura e sombra somente quando tiverem função explicável.
- Tratar sombra como relação de elevação, não como acabamento “premium”.

### Bordas, radius e ícones

- Usar borda para grupo, campo, estado, foco ou separação.
- Variar ou limitar radius conforme forma e hierarquia; não arredondar tudo automaticamente.
- Usar conjunto coerente de ícones; fornecer label ou nome acessível; ocultar ícones decorativos.
- Não usar emoji ou sparkle como sistema de ícones por default.

### Movimento

- Usar movimento para relação espacial, mudança de estado ou feedback.
- Evitar cascata, bounce, partículas, hover lift, fundo animado e atraso teatral sem função.
- Respeitar reduced motion e manter a função compreensível sem animação.

## Conteúdo, microcopy e estados

- Usar conteúdo e dados reais cedo.
- Não inventar KPI, gráfico, atividade, telemetria, depoimento ou estado para preencher layout.
- Rotular fixture, exemplo, placeholder e indisponibilidade.
- Preferir reconhecimento a memorização: mostrar contexto, escolhas e consequências no momento da decisão.
- Escrever com os termos usados pelas pessoas e pelo domínio, em voz ativa e com verbos concretos.
- Manter o mesmo nome para a mesma ação no botão, título, confirmação, estado de progresso, resultado, erro, documentação e evento relacionado.
- Usar microcopy operacional: o que ocorreu, efeito atual e próxima ação recuperável.
- Usar numeração como recurso estrutural somente quando representar ordem, prioridade ou sequência reais. Dados quantitativos continuam sendo exibidos conforme o domínio; para conjuntos sem ordem, usar lista não numerada ou estrutura adequada.
- Evitar slogan, adjetivo promocional e mensagem genérica em superfícies operacionais.
- Cobrir default, hover, focus, active, selected, disabled, read-only, loading, empty, success, warning, error, offline e permissão quando aplicáveis.
- Não simular duração, porcentagem ou etapas que o sistema não conhece.

## Responsividade

- Adaptar prioridade, navegação, densidade, comparação e ação por espaço disponível.
- Tratar desktop, tablet e mobile como composições relacionadas, não como dispositivos rígidos.
- Não resolver mobile apenas empilhando o desktop.
- Definir breakpoints quando conteúdo, leitura, toque ou navegação deixam de funcionar.
- Preservar acesso imediato a estado crítico e ação principal.

## Critérios mensuráveis portáveis

- WCAG 2.2 nível AA aplicável.
- Sem rolagem horizontal global a 320 CSS px, salvo conteúdo genuinamente bidimensional com overflow local.
- Texto a 200% e zoom a 400% sem perda aplicável.
- Alvo mínimo WCAG AA de 24×24 CSS px ou exceção; adotar meta maior da plataforma/produto quando apropriado.
- Zero ação primária escondida sem justificativa.
- Zero dado de produção inventado.
- Cem por cento das cores e superfícies com papel explicável.
- Estados críticos comunicados por mais de um canal.
- Revisão real em viewport estreito, intermediário e amplo.
