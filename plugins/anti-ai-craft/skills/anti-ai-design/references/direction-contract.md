# Contrato de direção

## Sumário

- [Classificar a superfície](#1-classificar-a-superfície)
- [Fixar o mandato](#2-fixar-o-mandato)
- [Escrever o contrato](#3-escrever-o-contrato-antes-do-código)
- [Travar referências](#4-travar-referências)
- [Preservar mídia e conteúdo](#5-preservar-mídia-e-conteúdo)
- [Contratar estados](#6-contratar-estados)
- [Checar prontidão da implementação](#7-checar-prontidão-da-implementação)
- [Preservar estrutura, URL e estado](#8-preservar-estrutura-url-e-estado)
- [Contratar temas e recursos externos](#9-contratar-temas-e-recursos-externos)
- [Manter checkpoint e invalidação](#10-manter-checkpoint-e-invalidação)
- [Limites](#limites)

Usar antes de criar, refinar ou redesenhar. O contrato é curto e verificável; não é um manifesto estético.

## 1. Classificar a superfície

- **Persuadir:** explicar valor e conduzir uma decisão. A mensagem e a sequência narrativa dominam.
- **Operar:** executar tarefas repetidas com velocidade, clareza, recuperação e baixa carga de memória.
- **Ler:** sustentar compreensão, navegação e continuidade em conteúdo.
- **Experienciar:** criar presença, exploração ou atmosfera sem esconder a tarefa.

Combinações são possíveis, mas declarar qual modo domina cada viewport ou etapa.

## 2. Fixar o mandato

- **Preservar:** manter identidade, comportamento, copy e estrutura; corrigir somente a falha indicada.
- **Refinar:** manter identidade e produto; melhorar hierarquia, ritmo, estados, acessibilidade e responsividade.
- **Redesenhar:** pode substituir o mundo visual, mas preserva verdade do produto, conteúdo, função, restrições, acessibilidade e integrações.

Mesmo em redesign, não alterar silenciosamente rotas, slugs, anchors, navegação primária, nomes/ordem de campos, eventos analíticos, consentimento, SEO, metadados, dados estruturados ou acessibilidade existente.

## 3. Escrever o contrato antes do código

Registrar:

1. tese de uma frase;
2. modo e tarefa dominante;
3. promessa do primeiro viewport;
4. caminho principal do usuário;
5. estrutura e hierarquia;
6. papéis semânticos de cor e tipografia;
7. uma assinatura significativa;
8. default da categoria conscientemente rejeitado;
9. risco principal e como será testado;
10. elementos que devem permanecer invariáveis.

A assinatura deve servir ao domínio, conteúdo ou interação. Criar uma decisão memorável e manter contenção ao redor costuma produzir mais identidade do que espalhar vários gestos decorativos.

Quando relevantes, transformar a direção em decisões verificáveis por eixo: tipografia, papéis de cor, composição/grid, densidade/espaçamento, movimento, superfícies/detalhes e mídia/iconografia. Omitir eixos não aplicáveis; não preencher com adjetivos vagos ou presets.

## 4. Travar referências

- Eleger uma fonte dominante para composição e linguagem.
- Dar às secundárias papéis limitados, como tipografia, movimento ou densidade.
- Registrar a decisão adotada e a alternativa rejeitada.
- Registrar exatamente quais arquivos, versões, seções, telas ou artefatos foram realmente lidos e qual decisão cada um sustenta. Não citar uma coleção inteira quando apenas um documento foi consultado.
- Preservar a cadeia `token primitivo → token semântico → token de componente ou consumidor real`. Componentes não devem consumir valores primitivos diretamente quando o sistema define uma camada semântica.
- Verificar consumidores reais no código e nos estados da interface; declarar token sem uso ou componente com valor solto como lacuna, não como sistema concluído.
- Preservar relações entre tokens, componentes, conteúdo e mídia; não copiar somente a aparência superficial.
- Quando fontes conflitarem, decidir por tarefa e restrição. Não produzir uma média visual.

Para componentes do escopo, registrar candidato encontrado, API/estados relevantes e decisão `reutilizar`, `compor`, `estender` ou `criar`. Não exigir censo completo do repositório.

## 5. Preservar mídia e conteúdo

Se a direção depende de fotografia, ilustração, vídeo, mapa, diagrama ou screenshot de produto, usar o asset fornecido ou uma alternativa legítima e adequada. Não substituir mídia essencial por gradientes, blobs, cartões vazios ou desenhos CSS genéricos.

Preservar slot, proporção, crop, `alt`, legenda e estado de carregamento. Se o asset não existir, declarar a lacuna; não inventar prova de produto.

## 6. Contratar estados

Para cada componente interativo relevante, definir:

- gatilho;
- alteração visual;
- estado semântico e de acessibilidade;
- ação permitida;
- recuperação ou próxima transição.

Cobrir carregando, vazio, parcial, erro, sucesso, indisponível, somente leitura, foco, seleção, expansão e confirmação quando aplicáveis.

## 7. Checar prontidão da implementação

- Usar `type`, `inputmode`, `autocomplete` e validação coerentes.
- Fazer navegação real funcionar; refletir filtro, aba ou página na URL quando o produto depende disso.
- Preservar scroll, filtros e formulários no retorno quando esperado.
- Testar clipping de overlays, safe areas, orientação, teclado virtual, ponteiro e ausência de hover.
- Reservar proporção de mídia, priorizar imagens críticas e atrasar as demais para evitar layout shift.
- Usar fallback de fonte compatível e conteúdo visível sem depender da animação.
- Tornar movimento interrompível e respeitar preferências de redução.

## 8. Preservar estrutura, URL e estado

Quando a mudança afetar várias superfícies, declarar:

- entradas e destinos;
- navegação global, local, contextual e de retorno;
- rotas, slugs, aliases, parâmetros e deep links;
- comportamento de refresh, back/forward e retomada;
- estado autoritativo, representado na URL, local ou efêmero;
- compatibilidade, redirects ou migração necessários.

Usar [information-architecture.md](information-architecture.md) para o contrato completo. Mudança de navegação ou URL pública é material mesmo quando o diff visual parece pequeno.

## 9. Contratar temas e recursos externos

Quando houver múltiplos temas, registrar fonte de verdade, modos suportados, precedência entre preferência do sistema e escolha manual, persistência, estado antes da hidratação, papéis semânticos, assets, controles nativos, overlays, contraste, forced colors e reduced motion. Não criar tema novo sem requisito ou autorização.

Antes de adicionar fonte, imagem, stylesheet, script ou biblioteca visual externa, procurar alternativa local aprovada e verificar necessidade, origem, política do projeto, privacidade, CSP, integridade, performance, cache, fallback e funcionamento degradado aplicáveis.

## 10. Manter checkpoint e invalidação

No fluxo completo ou retomável, registrar feature, fase, artefatos, decisões, bloqueios, próxima entrada e estado do código usado como referência. Arquivo presente não significa fase concluída.

Dependências usuais:

```text
brief → estrutura e direção → tokens → plano → implementação → revisão
```

Adaptar a relação ao projeto. Quando uma decisão anterior mudar, marcar somente os dependentes reais como `revalidar`; não atualizar silenciosamente nem reescrever todo o conjunto.

## Limites

Não tratar como absolutos: número fixo de cores/fontes, risco visual obrigatório, stack específica, duração universal de animação, aleatoriedade de direção ou obrigação de usar imagens.
