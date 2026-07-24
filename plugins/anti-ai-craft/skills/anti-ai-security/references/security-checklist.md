# Checklist de segurança contextual

## Sumário

- [Modelo de ameaça e superfícies](#modelo-de-ameaça-e-superfícies)
- [Autenticação e sessão](#autenticação-e-sessão)
- [Autorização e isolamento](#autorização-e-isolamento)
- [Rate limiting e recursos](#rate-limiting-e-recursos)
- [Entrada, saída e execução](#entrada-saída-e-execução)
- [Navegador e cliente](#navegador-e-cliente)
- [Uploads, arquivos e conteúdo ativo](#uploads-arquivos-e-conteúdo-ativo)
- [Segredos, criptografia e configuração](#segredos-criptografia-e-configuração)
- [Dependências e cadeia de suprimentos](#dependências-e-cadeia-de-suprimentos)
- [Logging, monitoramento e privacidade](#logging-monitoramento-e-privacidade)
- [Fluxos e concorrência](#fluxos-e-concorrência)
- [Sistemas que usam modelos ou agentes](#sistemas-que-usam-modelos-ou-agentes)
- [Temas ou tokens externos](#temas-ou-tokens-externos)
- [Testes mínimos por risco](#testes-mínimos-por-risco)

Usar somente as categorias aplicáveis. Marcar `confirmado`, `presente`, `não aplicável`, `depende de infraestrutura` ou `não verificado`; nunca converter item não verificado diretamente em vulnerabilidade.

## Modelo de ameaça e superfícies

- [ ] Ativos, dados sensíveis, atores, papéis e tenants identificados.
- [ ] Processos, datastores, fluxos, entidades externas e fronteiras diagramados na profundidade proporcional ao risco.
- [ ] Produção, CI/build, local, exemplos, testes e conteúdo gerado estão separados.
- [ ] Entradas controláveis por atacante, operador, desenvolvedor e provedor foram distinguidas.
- [ ] Entradas públicas, administrativas, internas, assíncronas e de terceiros inventariadas.
- [ ] Fronteiras de confiança e credenciais entre componentes registradas.
- [ ] Abusos de negócio e impactos de confidencialidade, integridade, disponibilidade e custo considerados.
- [ ] Controles existentes foram localizados antes de declarar ausência.
- [ ] Histórias de ataque realistas e itens fora de escopo estão registrados.
- [ ] O modelo de ameaça foi atualizado depois de qualquer descoberta ou mudança em arquitetura, fluxo, ativo, ator, fronteira, integração ou ambiente.
- [ ] Mudança de arquitetura da informação que criou entrada, papel, ação, estado, integração, exposição de dado ou operação cara acionou revalidação; troca apenas estética não acionou revisão ampla.
- [ ] Hosts públicos, internos, beta/staging, versões antigas, endpoints admin/debug e schemas/documentação expostos estão inventariados.
- [ ] Plano de desativação de versões e uso de dados reais fora de produção estão verificados.
- [ ] Serviços terceiros e dados compartilhados com eles estão no inventário.

## Autenticação e sessão

- [ ] Senhas usam primitive apropriada do stack, política coerente e comparação segura.
- [ ] Login, MFA, OTP, reset e recuperação resistem a enumeração, replay e brute force.
- [ ] Tokens têm audience, issuer, expiração, assinatura e algoritmo validados conforme o protocolo.
- [ ] Cookies sensíveis usam `Secure`, `HttpOnly` e `SameSite` apropriados.
- [ ] Sessão é renovada após autenticação/elevação e invalidada em logout, revogação e mudança crítica.
- [ ] Erros não revelam se conta, email, telefone ou tenant existe sem necessidade.

## Autorização e isolamento

- [ ] Matriz ator × entrada × ação × recurso × propriedade × tenant × estado foi exercitada.
- [ ] Toda ação protegida valida autorização no servidor.
- [ ] IDs controlados pelo cliente passam por autorização de objeto e tenant.
- [ ] Campos de leitura e escrita sensíveis usam allowlist; sem mass assignment.
- [ ] Papéis baixos não acessam funções administrativas por URL, método alternativo ou API direta.
- [ ] Queries, cache keys, filas, storage paths e eventos preservam tenant/ownership.
- [ ] RLS, ACL, IAM ou policy externa está comprovada e testada, não apenas presumida.
- [ ] Role e owner de tabelas não contornam RLS inesperadamente.
- [ ] Serviços preservam a identidade original e não viram confused deputy.
- [ ] Revogação, cache/token stale, onboarding, offboarding, exportação e exclusão preservam isolamento.
- [ ] Todas as versões, jobs, webhooks, filas, busca e ferramentas internas equivalentes foram inventariadas.
- [ ] Testes cobrem usuário A/B, tenant A/B, papéis e objetos inexistentes.

## Rate limiting e recursos

- [ ] Camada, rotas, métodos, versões, aliases, batch/GraphQL e endpoints internos estão cobertos.
- [ ] A chave do limite corresponde ao abuso: identidade, token, tenant, endpoint, IP confiável ou combinação.
- [ ] Proxies confiáveis e headers de IP estão configurados sem permitir spoofing.
- [ ] Burst e taxa sustentada são limitados com armazenamento coerente em múltiplas instâncias.
- [ ] Operações do store compartilhado são atômicas e a política de falha do limiter é explícita.
- [ ] Login, OTP, reset, convite, cadastro e operações pagas têm limites próprios.
- [ ] Body, string, array, upload, batch, paginação, GraphQL e exportação têm máximos.
- [ ] Há timeout, cancelamento, backpressure, concorrência e retry finitos.
- [ ] Jobs e filas têm deduplicação/idempotência e limite de crescimento.
- [ ] Integrações cobradas têm orçamento, cota ou alerta de custo.
- [ ] Noisy neighbor foi exercitado: um usuário ou tenant não degrada pools, filas, CPU, memória, conexões, storage, cotas ou orçamento dos demais.
- [ ] Isolamento, fairness, prioridade, backpressure e limites por tenant/usuário existem onde recursos são compartilhados.
- [ ] Resposta de excesso é consistente (`429` quando aplicável), observável e não cria bypass.
- [ ] Limiares vêm de capacidade, custo, UX e ameaça; valores arbitrários estão marcados como decisão pendente.

## Entrada, saída e execução

- [ ] Entrada valida tipo, formato, faixa, tamanho, semântica e campos inesperados.
- [ ] SQL/ORM usa parâmetros; shell evita concatenação; template/HTML aplica encoding contextual.
- [ ] Paths são normalizados, confinados e não aceitam traversal.
- [ ] URLs de saída restringem esquema, host, redirects, DNS/rebinding e redes internas conforme o caso.
- [ ] Desserializadores e parsers estão em modo seguro e com limites.
- [ ] Content-Type, método HTTP e tamanho são allowlisted.
- [ ] Saídas não expõem campos internos, segredo, stack trace ou PII desnecessária.

## Navegador e cliente

- [ ] CORS usa origens, métodos e credentials deliberados; não reflete origem cegamente.
- [ ] Operações com sessão por cookie têm proteção CSRF aplicável.
- [ ] CSP e demais headers são coerentes com a aplicação, sem copiar configuração que quebre o produto.
- [ ] Segredo e autorização real não dependem de bundle, local storage, route guard ou botão oculto.
- [ ] Redirects e links externos são validados.
- [ ] Mapa de UI e inventário de endpoints concordam; rota direta, link antigo, refresh e restauração de estado revalidam autenticação, autorização e tenant.
- [ ] URL, histórico, cache e armazenamento do cliente não carregam segredo ou dado sensível desnecessário.

## Uploads, arquivos e conteúdo ativo

- [ ] Extensão, tipo real, tamanho, nome e conteúdo são verificados por allowlist/contexto.
- [ ] Arquivo é armazenado fora do webroot ou servido por handler autorizado.
- [ ] Nome/path é gerado pelo servidor e não sobrescreve arquivo arbitrário.
- [ ] Processadores resistem a arquivo comprimido/bomba e têm tempo/memória limitados.
- [ ] Download revalida autorização e usa headers seguros.

## Segredos, criptografia e configuração

- [ ] Nenhum segredo aparece em código, cliente, log, fixture, imagem ou erro.
- [ ] Segredos têm privilégio mínimo, rotação, revogação, expiração e separação por ambiente.
- [ ] Para segredo já exposto, remoção do código não foi tratada como resolução; alcance, contenção e revogação/rotação foram exigidos e seu estado foi confirmado ou escalado.
- [ ] TLS é exigido onde dados/credenciais cruzam rede não confiável.
- [ ] Criptografia usa biblioteca e algoritmo aprovados pelo stack; chaves não ficam junto do ciphertext sem modelo justificável.
- [ ] Debug, default password, endpoint administrativo e storage público estão desativados/restritos por padrão.
- [ ] Config ausente falha de modo explícito e seguro, sem default allow silencioso.

## Dependências e cadeia de suprimentos

- [ ] Pacotes sugeridos existem, são necessários e correspondem ao nome/registry correto.
- [ ] Manifest e lockfile concordam; resolução não depende de versão flutuante perigosa.
- [ ] Alertas existentes, versões vulneráveis e software não mantido foram considerados.
- [ ] Build/CI não executa input não confiável com segredo ou permissão excessiva.
- [ ] O diff foi revisado para nova execução de rede ou shell em build, install, geração, teste, CI e deploy.
- [ ] Cada nova execução de rede/shell tem necessidade, origem, versão/integridade, argumentos, privilégios, credenciais e comportamento de falha verificados.
- [ ] Artefatos e imagens têm origem, integridade e atualização verificáveis quando o projeto exigir.
- [ ] Nova fonte, imagem, stylesheet, script ou biblioteca visual externa tem necessidade, origem, privacidade, CSP, integridade, performance, cache, fallback e comportamento degradado avaliados.

## Logging, monitoramento e privacidade

- [ ] Falhas de autenticação, autorização, validação e rate limit geram eventos úteis.
- [ ] Logs têm correlação, ator/tenant apropriado e proteção contra log injection.
- [ ] Tokens, senhas, chaves, conteúdo sensível e PII desnecessária não são registrados.
- [ ] Alertas têm consumidor e limiar; logging não é ruído sem ação.
- [ ] Retenção, exclusão, exportação e minimização de dados seguem requisito aplicável.

## Fluxos e concorrência

- [ ] Ordem de estados é validada no servidor.
- [ ] Preço, desconto, ownership, papel e permissão são recalculados no servidor.
- [ ] Operações financeiras, crédito, estoque, convite e confirmação resistem a replay e dupla submissão.
- [ ] Um passe de usuário desonesto tentou mentir sobre identidade, tenant, estado, quantidade, preço, elegibilidade, sequência e sucesso anterior para obter benefício.
- [ ] Etapas puladas, repetidas, fora de ordem e TOCTOU foram exercitadas.
- [ ] Funções que dispensam valor têm limite por fluxo de negócio, não apenas limite genérico de endpoint.
- [ ] Idempotency key é vinculada a ator, operação e payload quando usada.
- [ ] Transações, locks, unique constraints ou compare-and-set protegem invariantes concorrentes.
- [ ] Falha parcial tem rollback ou compensação observável.

## Sistemas que usam modelos ou agentes

- [ ] Conteúdo externo é tratado como dado, não como instrução confiável.
- [ ] Issues, PRs, README, logs, páginas e respostas de ferramentas não podem redefinir instruções persistentes silenciosamente.
- [ ] Ferramentas, arquivos, rede e segredos seguem privilégio mínimo.
- [ ] Saída do modelo é validada antes de SQL, shell, HTML, URL, parser ou ação externa.
- [ ] Aprovação humana existe para ações destrutivas ou de alto impacto.
- [ ] Custos, tokens, concorrência e tamanho de contexto têm limites.
- [ ] Pacotes inventados/typosquatting, mudanças em configuração de agentes, CI e scripts de instalação/deploy foram revisados.
- [ ] Testes removidos, asserts enfraquecidos, mocks substitutivos e mudanças fora do escopo foram procurados.
- [ ] Saída de subagente foi revalidada por evidência independente.
- [ ] Briefs, planos e checkpoints persistidos não contêm segredo, PII desnecessária, conteúdo de cliente ou instrução externa tratada como autoridade.
- [ ] Feature sensível inclui atores, fronteiras, abuso plausível e testes negativos desde o planejamento, sem transformar feature comum em checklist cego.

## Temas ou tokens externos

Aplicar somente quando tema ou token vier de usuário, tenant, CMS, arquivo remoto ou integração:

- [ ] Nomes e propriedades seguem allowlist.
- [ ] Tipos, unidades, faixas e tamanho são validados.
- [ ] URLs e referências a recursos passam pelos controles de saída aplicáveis.
- [ ] O valor alcança apenas o sink de estilo previsto, sem conteúdo ativo ou quebra de isolamento.
- [ ] Cache, persistência e escopo por tenant não vazam configuração entre usuários.

Tokens locais de build não geram achado de segurança sem entrada controlável, caminho alcançável, controle ausente e impacto.

## Testes mínimos por risco

- [ ] Sem credencial, credencial inválida e sessão expirada.
- [ ] Papel inferior, objeto de outro usuário e outro tenant.
- [ ] Input vazio, limite, acima do limite, tipo errado e campo inesperado.
- [ ] Burst, taxa sustentada, batch, página/upload grandes e operação cara.
- [ ] Repetição, replay, concorrência e ordem de etapas inválida.
- [ ] Dependência/serviço externo lento, indisponível ou malformado.
- [ ] Usuário/tenant ruidoso consumindo recursos compartilhados enquanto outro uso legítimo continua operando.
- [ ] Logs e respostas revisados para vazamento.
