# Antipadrões e falsos sinais

## Sumário

- [Regra de interpretação](#regra-de-interpretação)
- [Composição e conteúdo](#composição-e-conteúdo)
- [Estética reflexa](#estética-reflexa)
- [Componentes](#componentes)
- [Movimento e teatro](#movimento-e-teatro)
- [Responsividade superficial](#responsividade-superficial)
- [Falsos sinais de autoria](#falsos-sinais-de-autoria)
- [Perguntas de crítica](#perguntas-de-crítica)

## Regra de interpretação

Não tratar qualquer item isolado como prova de baixa qualidade ou autoria. Procurar combinação, repetição, ausência de justificativa e conflito com tarefa, conteúdo, estado, identidade ou acessibilidade.

Classificar cada ocorrência como:

- defeito funcional ou normativo;
- inconsistência com fonte de verdade;
- padrão genérico contextual;
- heurística;
- preferência subjetiva;
- falso positivo rejeitado.

## Composição e conteúdo

| Sinal | Risco | Decisão contextual |
|---|---|---|
| Hero promocional dentro do produto | desloca a tarefa para marketing | rejeitar salvo onboarding/comunicação real |
| Sidebar + topbar intercambiáveis | produto vira dashboard genérico | adaptar aos destinos, linguagem e frequência reais |
| Cards idênticos | dá peso igual e esconde relações | usar lista, tabela, alinhamento ou cards autônomos |
| Bento escolhido antes do conteúdo | receita governa a informação | aceitar somente overview modular comprovado |
| Card dentro de card | profundidade sem modelo | reduzir níveis ou justificar subgrupo |
| Simetria automática | apaga prioridade | manter apenas para comparação real |
| Assimetria performática | dificulta varredura | exigir ganho informacional |
| Centralização universal | enfraquece leitura e percurso | limitar a estados curtos e locais |
| Espaço uniforme ou vazio cenográfico | relações parecem equivalentes | variar ritmo por item, grupo e seção |
| KPI, gráfico ou atividade fictícia | constrói arquitetura sobre dado falso | remover ou marcar fixture fora de produção |
| Copy promocional em fluxo operacional | ocupa espaço da tarefa | trocar por vocabulário e ação do domínio |
| Happy path sem extremos | interface parece pronta sem funcionar | testar vazio, erro, offline, loading e overflow |

## Estética reflexa

| Sinal | Risco | Falso positivo ou condição |
|---|---|---|
| Gradiente roxo/azul/ciano | paleta substituível | válido se pertence à marca/dado e passa contraste |
| Glassmorphism | contraste e camadas ambíguas | válido em sobreposição controlada e legível |
| Glow, blobs e manchas | atmosfera sem informação | válido quando comunica foco/estado e há pista sólida |
| Radius alto em tudo | hierarquia achatada | formatos arredondados podem pertencer ao sistema |
| Pills em toda ação | botões parecem badges | usar para chip, toggle ou estado curto |
| Sombra e hover lift | “premium” sem modelo | sombra pode comunicar elevação real |
| Dark mode | não é genérico por si | avaliar identidade, contraste e função |
| Tema claro creme/serif/terracota | pode ser novo default | avaliar contexto, não trocar um preset por outro |
| Acid-on-black ou broadsheet | pode performar diferença | exigir vínculo com domínio e legibilidade |
| Mono integral | fadiga e “terminal cosplay” | útil para código, dados e metadados |
| Serif editorial | pode virar template | válida para leitura/voz quando suportada |
| Caixa alta e tracking | ruído e baixa leitura | aceitável em códigos e rótulos curtos |
| Sparkle ou emoji | ícone genérico/ambíguo | conteúdo do usuário ou símbolo ensinado pode ser válido |

## Componentes

| Sinal | Risco | Decisão contextual |
|---|---|---|
| Kebab em toda linha/card | ação vira caça e repetição | consolidar ações e manter frequentes visíveis |
| Reticências com uma ação | overflow sem necessidade | mostrar a ação diretamente |
| Salvar/confirmar/executar oculto | baixa descoberta e eficiência | manter visível |
| Excluir crítico oculto | risco e falta de clareza | expor com hierarquia e confirmação apropriada |
| Ícone sem label/nome | ambiguidade e barreira de acesso | adicionar texto, tooltip e nome acessível conforme o caso |
| Tabela convertida em cards | comparação fica difícil | preservar relação bidimensional |
| Componente genérico para dados incompatíveis | estrutura apaga semântica | criar variação com propósito ou composição específica |
| Modal visual sem comportamento modal | foco escapa e fundo opera | implementar padrão completo ou usar página |
| Tabs visuais sem semântica | teclado e relação quebrados | implementar padrão ou usar navegação |
| Tooltip com ação essencial | inacessível em touch/teclado | mover ação para controle persistente |

## Movimento e “teatro”

- Animação em cascata escolhida por default.
- Partículas, fundo animado, parallax ou glitch sem função.
- Hover que desloca layout.
- Loading teatral, delay artificial ou porcentagem inventada.
- Typewriter que retarda acesso ao conteúdo.
- Confete ou celebração sem adequação ao resultado.

Perguntar: a função permanece clara sem o movimento? O backend mede esse progresso? O usuário consegue reduzir, pausar ou interromper?

## Responsividade superficial

- Empilhar todas as colunas sem reordenar prioridade.
- Transportar sidebar/topbar inteira para mobile.
- Ocultar estado crítico por posição fixa.
- Cortar texto ou ação para preservar card.
- Criar rolagem horizontal global.
- Escolher breakpoints por modelo de aparelho, sem testar conteúdo.

## Falsos sinais de autoria

Rejeitar inferências como:

- “usa cards, então foi feito por IA”;
- “usa dark mode/ciano/serif/mono, então foi feito por IA”;
- “tem menu de três pontos, então foi feito por IA”;
- “é polido ou simétrico, então foi feito por IA”;
- “tem um bug, então foi gerado”;
- “segue um design system, então não é autoral”.

Relatar somente o efeito observável e a evidência: padrão genérico, decisão sem justificativa funcional, inconsistência, acessibilidade, manutenção visual ou preferência.

## Perguntas de crítica

1. Isto poderia pertencer a qualquer produto do mesmo gênero sem alteração?
2. Existe por conteúdo/tarefa ou porque o componente estava disponível?
3. A hierarquia continua clara sem efeitos, bordas e cards?
4. O conteúdo é real e cobre estados extremos?
5. A interação funciona por teclado, touch e tecnologia assistiva?
6. O mobile reprioriza ou apenas empilha?
7. A regra vem do projeto, de requisito normativo, guidance ou gosto?
