# Design tokens operacionais

## Sumário

- [Princípio](#princípio)
- [Descoberta e classificação](#descoberta-e-classificação)
- [Fonte, aliases e consumidores](#fonte-aliases-e-consumidores)
- [Famílias](#famílias)
- [Modos e temas](#modos-e-temas)
- [Implementação e validação](#implementação-e-validação)
- [Contrato de saída](#contrato-de-saída)

## Princípio

Organizar a cadeia `primitivo → semântico → componente ou consumidor` quando o projeto adotar essas camadas. Criar somente abstrações e famílias com intenção e consumidor reais. Um catálogo de variáveis sem uso, estados ou modos conectados não constitui sistema concluído.

Não obrigar CSS, framework, tema escuro, escala, breakpoint, quantidade de tokens ou formato.

## Descoberta e classificação

Descobrir:

- definições, imports e consumidores de variáveis;
- configuração, providers, atributos e preferências de tema;
- objetos ou recursos nativos de plataforma;
- arquivos estruturados e scripts de geração;
- bibliotecas de componentes e documentação;
- valores repetidos ou hardcoded;
- aliases, referências e outputs gerados;
- testes visuais e ferramentas de design;
- marcas, temas, densidades ou plataformas.

Classificar o sistema:

- `inexistente`;
- `informal`: valores repetidos sem semântica estável;
- `parcial`: algumas camadas ou geração;
- `estabelecido`: fonte, camadas e consumidores identificados;
- `fragmentado`: fontes concorrentes ou política duplicada.

A classificação determina `criar`, `estender`, `consolidar`, `conectar consumidores` ou `preservar`.

## Fonte, aliases e consumidores

1. Identificar fonte autoritativa por documentação, imports, scripts e consumidores; não pelo nome ou data do arquivo.
2. Distinguir arquivos derivados e comando oficial de geração.
3. Resolver aliases e dependências; procurar referência ausente, ciclo, tipo ou unidade incompatível.
4. Mapear token a consumidores, estados e modos representativos.
5. Alterar a menor camada capaz de expressar a intenção.
6. Regenerar outputs pelo comando oficial.
7. Remover somente órfãos comprovados ou criados pela mudança.

Tratar como candidato técnico:

- alias quebrado ou circular;
- fonte e output divergentes;
- primitivo consumido onde o contrato exige semântico;
- hardcode que contorna política vigente;
- branch manual de tema que duplica provider;
- token órfão;
- substituição textual sem confirmar semântica.

Literal local não é falha por si. Valores intrínsecos, calculados, de mídia ou de terceiros podem permanecer locais com justificativa.

## Famílias

Criar apenas famílias aplicáveis. Para cada token, registrar intenção, nome, tipo/unidade, consumidor, estados, modos e validação.

### Cor

Mapear papéis necessários:

- superfícies e fundos;
- texto e ícones;
- bordas e separadores;
- ação, foco e interação;
- sucesso, aviso, erro e informação;
- overlay e elevação.

Nomes de valor pertencem à camada primitiva; API semântica expressa intenção. Não comunicar estado apenas por cor.

### Tipografia

Definir papéis de leitura, display, dados e código. Tratar família, fallback, tamanho, peso, altura de linha e tracking como conjunto. Validar idioma, scripts suportados, zoom, text spacing, tradução e strings longas.

Não impor número de famílias, passos ou pesos.

### Espaço, dimensão, forma e elevação

- Estender a escala existente.
- Derivar passos de agrupamento, densidade, toque e layout reais.
- Evitar duplicatas quase idênticas sem função.
- Permitir exceção local justificada.
- Não tokenizar proporção de mídia ou cálculo intrínseco apenas por completude.
- Ligar radius e sombra a forma, estado ou elevação.

### Movimento

Tokenizar duração, curva, atraso ou intensidade somente quando representarem linguagem repetida. Registrar consumidor, transição de estado e variante reduzida. Não criar escala para animação única nem adotar bounce ou duração universal.

### Layout e breakpoints

Definir breakpoints quando conteúdo, leitura, navegação ou interação deixarem de funcionar. Respeitar a capacidade do stack; não tratar classes de aparelho como contrato universal.

## Modos e temas

Preservar o mecanismo existente. Criar novo modo apenas por requisito e autorização.

Quando houver múltiplos temas ou modos, registrar:

- fonte de verdade;
- modos realmente suportados;
- precedência entre sistema, produto e escolha manual;
- persistência e estado antes da hidratação;
- paridade dos papéis semânticos;
- assets, controles nativos, overlays e sombras;
- contraste, foco, estados e forced colors;
- relação com reduced motion.

Não combinar provider, atributo e media query concorrentes sem um contrato explícito.

## Implementação e validação

Antes:

- registrar baseline e consumidores;
- delimitar alcance por componentes, marcas, modos e plataformas;
- pedir aprovação quando token global ou pipeline tiver alcance amplo;
- prever rollback ou migração.

Depois:

1. validar aliases, tipos e geração;
2. executar build/lint/testes oficiais pertinentes;
3. comparar consumidores representativos com mesmos dados e estados;
4. cobrir modos, interação, contraste, zoom, strings longas e reduced motion afetados;
5. revisar diff de fonte e outputs;
6. registrar combinações não testadas.

Build não prova resultado visual; screenshot não prova integridade da cadeia.

## Contrato de saída

Entregar:

- classificação do sistema;
- fonte autoritativa e outputs gerados;
- formatos e comandos;
- modos e famílias aplicáveis;
- tokens preservados, adicionados, alterados e rejeitados;
- aliases e consumidores afetados;
- valores que ainda contornam a cadeia;
- alcance e aprovação;
- validações visual e técnica;
- riscos, dívida fora do escopo e decisões pendentes.
