# Arquitetura da informação contextual

## Sumário

- [Quando usar](#quando-usar)
- [Entradas e profundidade](#entradas-e-profundidade)
- [Mapa de superfícies](#mapa-de-superfícies)
- [Navegação e hierarquia](#navegação-e-hierarquia)
- [Fluxos, URLs e persistência](#fluxos-urls-e-persistência)
- [Crescimento e edge cases](#crescimento-e-edge-cases)
- [Critérios de aceitação](#critérios-de-aceitação)

## Quando usar

Executar a etapa completa para produto com múltiplas superfícies, mudança de navegação, rotas públicas, vários papéis ou tenants, conteúdo crescente, onboarding, deep links, retomada, compartilhamento, SEO ou redesign estrutural.

Usar mini-contrato para uma tela que altere prioridade, ação, overlay recuperável, filtro/aba na URL ou rascunho persistente:

- entrada;
- tarefa;
- caminho;
- estado persistido;
- retorno, erro e recuperação.

Não criar documento completo para ajuste puramente visual que preserve hierarquia, rótulos, ações, rotas e estado.

## Entradas e profundidade

Ler:

- brief ou requisito vigente;
- rotas, layouts e componentes de navegação;
- modelos de conteúdo, APIs e persistência;
- papéis, permissões e tenants;
- convenções de URL, analytics, SEO e integrações;
- comportamento real de link direto, refresh, back/forward e retorno.

Não exigir brief em caminho fixo nem escolher silenciosamente o mais recente. Respeitar a convenção documental do projeto; sem autorização de escrita, entregar a arquitetura na resposta.

## Mapa de superfícies

Incluir apenas superfícies alcançáveis ou planejadas com base verificável:

| Campo | Controle |
|---|---|
| Identidade | Nome estável |
| Caminho | Rota e entradas alternativas |
| Público | Papel, tenant e estado de acesso |
| Tarefa | Resultado concluído na superfície |
| Conteúdo | Fonte e autoridade dos dados |
| Estado | Variações que mudam estrutura ou ação |
| Saída | Destino, retorno e recuperação |
| Persistência | O que sobrevive a refresh, retorno ou sessão |

Não espelhar cegamente a árvore de arquivos. Uma rota pode conter várias superfícies funcionais e várias rotas podem compartilhar estrutura.

## Navegação e hierarquia

Distinguir:

- global: destinos recorrentes;
- local: opções dentro da área;
- contextual: ações ligadas ao objeto e estado;
- utilitária: conta, ajuda e administração;
- localização e retorno: breadcrumb, histórico e origem;
- adaptativa: acesso equivalente sob restrição de espaço, input e tarefa.

Não impor quantidade de itens, sidebar, topbar, tabs, hamburger ou bottom navigation. Escolher por frequência, hierarquia, volume, comparação e plataforma.

Para cada superfície, ordenar conforme o estado:

1. contexto que permite reconhecimento;
2. ação ou decisão dominante;
3. informação que sustenta a decisão;
4. ações secundárias;
5. detalhe progressivo;
6. ajuda e recuperação.

Loading, vazio, erro, permissão negada e recurso removido podem substituir toda a hierarquia e precisam de próximo passo próprio.

Manter glossário de conceitos e ações. Usar o mesmo nome no destino, título, botão, confirmação, progresso, resultado, erro, documentação e evento relacionado.

## Fluxos, URLs e persistência

Cada fluxo relevante registra:

1. ator e estado inicial;
2. ponto de entrada;
3. objetivo;
4. superfícies e ações;
5. decisões e condições;
6. dados lidos ou gravados;
7. URL e histórico;
8. falhas e recuperação;
9. estado terminal;
10. retorno ou retomada.

Cobrir, conforme aplicável:

- principal;
- papel ou origem alternativos;
- erro, timeout, offline e indisponibilidade;
- autenticação, expiração e retorno ao destino;
- autorização sem vazamento;
- interrupção, refresh, back/forward e múltiplas abas;
- ciclo de vida, administração e offboarding.

### URL

Decidir deliberadamente:

- segmentos estáticos e dinâmicos;
- identificador, slug e aliases;
- filtro, ordenação, paginação, aba e busca compartilháveis;
- locale, versão, workspace ou tenant;
- canonical, redirects e links antigos;
- recursos removidos;
- dados sensíveis que nunca devem ir para URL.

URL é contrato de localização, histórico e integração; não precisa copiar a hierarquia visual.

### Persistência

Classificar estado:

| Tipo | Exemplos | Regra |
|---|---|---|
| Servidor autoritativo | recurso, permissão, progresso | Reconsultar e invalidar coerentemente |
| URL | busca, filtro, página, aba | Suportar link direto e histórico |
| Sessão de navegação | origem, scroll, etapa | Preservar quando o retorno exigir |
| Dispositivo | preferência não sensível | Não usar como fonte crítica |
| Efêmero | menu, hover, animação | Não persistir sem necessidade |
| Rascunho | formulário longo | Definir duração, conflito, limpeza e privacidade |

Registrar chave/escopo, duração, expiração, versão, invalidação, conflito, logout/revogação, sensibilidade e fallback observável.

## Crescimento e edge cases

Examinar:

- zero, um, muitos e volume extremo;
- strings longas, localização e caracteres especiais;
- paginação após redução do conjunto;
- item removido entre lista e detalhe;
- conteúdo parcial, desatualizado ou duplicado;
- busca sem resultado ou indisponível;
- link direto sem histórico;
- sessão expirada e papel insuficiente;
- recurso de outro usuário ou tenant;
- request lento, repetido ou fora de ordem;
- dupla submissão, conflito de edição e atualização otimista rejeitada;
- cache obsoleto, offline, reconexão, cota e rate limit;
- teclado virtual, safe area, ausência de hover, zoom e retorno de foco.

## Critérios de aceitação

- Tarefa crítica possui entrada e saída alcançáveis.
- Rótulos e conceitos permanecem consistentes.
- Deep link, refresh e retorno funcionam quando fazem parte do contrato.
- Não há beco sem saída; erro e bloqueio oferecem próximo passo seguro.
- Estado é preservado ou descartado deliberadamente.
- Rotas públicas, aliases e integrações preservam compatibilidade ou migração aprovada.
- Navegação móvel mantém descoberta e operação equivalentes.
- UI e endpoint aplicam autorização coerente; ocultar navegação não é controle.
- Cobertura por superfície e fluxo registra `coberto`, `parcial`, `bloqueado`, `não exercitado` ou `não aplicável`.
- Nenhum número universal de cliques, itens ou profundidade substitui cenários reais.
