# Checklist de auditoria

## Sumário

- [Escopo e fontes de verdade](#escopo-e-fontes-de-verdade)
- [Ledger e fechamento](#ledger-e-fechamento)
- [Interface e experiência](#interface-e-experiência)
- [Acessibilidade](#acessibilidade)
- [Código e comportamento](#código-e-comportamento)
- [Arquitetura e manutenção](#arquitetura-e-manutenção)
- [Testes e documentação](#testes-e-documentação)
- [Classificação](#classificação)
- [Evidência por família](#evidência-por-família)

## Escopo e fontes de verdade

- [ ] Tipo de alvo, raiz, escopo, objetivo, autorização e não edição confirmados.
- [ ] Instruções, README, especificação, design/code guides e configs lidos.
- [ ] Se Git existir, branch, HEAD, status, alterações preexistentes, upstream/alvo e `merge-base` exato estão registrados; fora de Git, os campos estão marcados como não aplicáveis.
- [ ] O baseline não foi presumido como `main`, `HEAD^` ou commit anterior; o SHA e o comando usados para o diff foram registrados.
- [ ] Em diff, itens introduzidos/agravados estão separados da dívida preexistente.
- [ ] Usuários, tarefas, dados, estados e invariantes identificados.
- [ ] Artefatos de fluxo relevantes têm estado, autoridade, atualidade e vínculo com o código verificados.
- [ ] Comandos oficiais e ambiente conhecidos.
- [ ] Comandos que escreveriam caches, snapshots, lockfiles, bancos ou artefatos no alvo foram evitados.

## Ledger e fechamento

- [ ] Todo candidato tem ID, localização, família, método de validação, controle examinado e disposição.
- [ ] Disposição é confirmado, suprimido, não aplicável, depende de infraestrutura, não verificado ou duplicado.
- [ ] Contraprova mais forte e lacuna de prova estão registradas.
- [ ] Falha de ambiente/setup não foi usada como contraprova.
- [ ] Um caminho vizinho seguro não suprimiu uma instância independente.
- [ ] Duplicatas compartilham causa/controle, comportamento, impacto e correção.
- [ ] A auditoria continuou por todo o escopo depois do primeiro achado; qualquer corte está registrado como área não auditada.

## Interface e experiência

- [ ] Tarefa principal e hierarquia correspondem ao produto.
- [ ] Composição, densidade, cards, bento, sidebar, topbar e hero têm função.
- [ ] Tabelas, listas, formulários, modais, tabs, menus e busca usam forma adequada.
- [ ] Kebab contém apenas ações secundárias coerentes; primárias ficam visíveis.
- [ ] Conteúdo, microcopy, dados e estados são reais.
- [ ] Tipografia, cor, sombra, borda, radius, ícones e movimento têm papéis.
- [ ] Desktop, tablet e mobile repriorizam corretamente.
- [ ] Antes/depois ou screenshots reais foram comparados quando disponíveis.
- [ ] Perfil de evidência e matriz superfície/rota × estado × viewport × tema/input estão registrados de forma proporcional ao risco.
- [ ] Mapa de superfícies, navegação por papel, deep links, URL/redirects, retorno, crescimento e persistência foram exercitados quando aplicáveis.
- [ ] Duplicação visual ou reuso proposto foi validado contra componente real, API, alcance e limitações; sem inferência apenas por aparência.
- [ ] Fonte autoritativa de tokens, outputs gerados, camadas, aliases, consumidores, hardcodes e paridade entre modos/estados foram examinados quando tokens estavam no escopo.

## Acessibilidade

- [ ] Semântica, nome, role, value e state.
- [ ] Teclado, foco, Escape e retorno de foco.
- [ ] Modal, tabs, menu e tooltip completos.
- [ ] Labels, erros e recuperação de formulário.
- [ ] Contraste, cor não exclusiva e forced colors.
- [ ] Alvos, reflow 320 CSS px, 200%, 400% e text spacing.
- [ ] Reduced motion e conteúdo automático.
- [ ] Status/live regions sem ruído.

## Código e comportamento

- [ ] Requisitos/invariantes ligados a caminhos executáveis.
- [ ] APIs, imports, dependências e configuração existem.
- [ ] Sem falso sucesso, erro engolido ou fallback oculto.
- [ ] Validação, autenticação e autorização corretas.
- [ ] Mutação, transação, rollback e idempotência.
- [ ] Concorrência, async, cancelamento, timeout e listeners.
- [ ] Estado impossível e magic values.
- [ ] Segredos, paths absolutos e dados sensíveis.
- [ ] Performance, cache e logging têm evidência/necessidade.
- [ ] Evidência forma entrada/caminho executável → invariante violada → resultado observável.

## Arquitetura e manutenção

- [ ] Arquitetura e padrões locais preservados.
- [ ] Wrappers/helpers/factories/interfaces agregam valor.
- [ ] Sem abstração prematura ou configuração excessiva.
- [ ] Sem dezenas de arquivos pequenos sem ganho.
- [ ] Duplicação, código morto e compatibilidade especulativa avaliados.
- [ ] API pública não muda silenciosamente.
- [ ] Comentários/docstrings não repetem nem prometem sem evidência.

## Testes e documentação

- [ ] Regressão reproduz o problema.
- [ ] Happy path e falhas/limites pertinentes.
- [ ] Mocks não confirmam a si mesmos.
- [ ] Snapshots são pequenos e semanticamente revisados.
- [ ] Integração cobre wiring/config/serialização/transação relevantes.
- [ ] Comandos realmente executados e resultados registrados.
- [ ] Docs não prometem feature inexistente.

## Classificação

- [ ] Bug confirmado.
- [ ] Acessibilidade.
- [ ] Segurança.
- [ ] Manutenção.
- [ ] Aparência genérica contextual.
- [ ] Inconsistência.
- [ ] Decisão pendente.
- [ ] Preferência subjetiva.
- [ ] Falso positivo rejeitado.

## Evidência por família

- [ ] Correção: entrada/caminho executável → invariante → resultado observável.
- [ ] Segurança: fonte controlável → controle mais próximo → sink/operação → pré-condições → impacto.
- [ ] Acessibilidade: ação/estado → semântica/operação esperada → falha observada.
- [ ] Design: tarefa → ação/hierarquia → viewport/estado → dano concreto.
- [ ] Fluxo de design: decisão/requisito → artefato vigente → implementação/runtime → evidência/disposição.
