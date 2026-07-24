# Antipadrões de código e correção

## Sumário

- [Taxonomia](#taxonomia)
- [Contratos inventados](#contratos-inventados)
- [Certeza fabricada](#certeza-fabricada)
- [Erros escondidos e falso sucesso](#erros-escondidos-e-falso-sucesso)
- [Estado, persistência e transações](#estado-persistência-e-transações)
- [Concorrência e async](#concorrência-e-async)
- [Validação, autorização e segurança](#validação-autorização-e-segurança)
- [Qualidade local](#qualidade-local)
- [Interseção entre código e UI](#interseção-entre-código-e-ui)

## Taxonomia

1. **Defeito funcional confirmado:** reprodução, contrato ou teste demonstra comportamento errado.
2. **Vulnerabilidade:** caminho de impacto e controle ausente são demonstráveis.
3. **Smell tradicional:** eleva custo/risco, mas não prova bug.
4. **Padrão genérico contextual:** combinação observável sem justificativa na tarefa, no domínio ou na arquitetura.
5. **Heurística comunitária:** hipótese para investigar.
6. **Preferência estilística:** não reportar como defeito.
7. **Evidência insuficiente ou falso positivo:** rejeitar.

## Contratos inventados

- API, método, parâmetro, evento ou endpoint inexistente.
- Dependência/pacote inexistente, desatualizado, incompatível ou fora do lockfile.
- Import quebrado, nome indefinido ou feature não disponível na versão instalada.
- Configuração, variável de ambiente, flag ou arquivo fictício.
- Versão, comando, citação, estatística ou comportamento de biblioteca afirmado sem verificação.
- README/docstring que promete feature não implementada.
- Stub, placeholder ou mock deixado em caminho de produção.
- Caminho absoluto, host ou segredo embutido.

Verificar existência, versão, assinatura, licença/política local e uso real. Não instalar pacote apenas porque o nome parece plausível.

## Certeza fabricada

- apresentar inferência como fato observado;
- completar requisito ausente com comportamento plausível;
- citar documentação que existe, mas não sustenta a afirmação;
- inventar fonte, autor, número, versão ou resultado de benchmark;
- defender uma afirmação anterior em vez de revalidá-la;
- dizer que comando, teste, build ou revisão passou sem execução e saída.

Rotular fato, inferência e desconhecido. Verificar detalhes voláteis ou precisos na fonte primária. Quando não houver evidência suficiente, pedir contexto ou declarar a limitação.

## Erros escondidos e falso sucesso

- catch amplo que ignora exceção relevante;
- retorno vazio/default após falha sem distinguir erro legítimo;
- log e continuação quando a operação deveria falhar;
- mensagem genérica que perde causa e próxima ação;
- status de sucesso antes de concluir side effects;
- retry infinito ou sem idempotência;
- fallback que muda semântica silenciosamente;
- teste contornado por branch exclusivo de ambiente;
- erro substituído por placeholder fictício.

Exigir contrato explícito: propagar, traduzir com causa, recuperar com estado observável ou compensar. Preservar stack/cause quando a linguagem permitir.

Não proibir `??`, `||`, valores padrão ou `try/catch` por sintaxe. Reportar somente quando o fallback mascara violação de contrato ou o catch apaga uma falha que deveria permanecer observável.

## Estado, persistência e transações

- mutação parcial antes de validação;
- gravações relacionadas fora de transação;
- rollback que cobre apenas parte dos side effects;
- cache atualizado antes da fonte de verdade;
- evento emitido sem commit ou duplicado em retry;
- estado impossível representável sem validação;
- valores sentinela/magic strings que misturam estados;
- leitura-modificação-gravação sem controle de concorrência;
- operação não idempotente repetida após timeout.

Traçar estados inicial, intermediários, terminal e falhas. Confirmar atomicidade, compensação e invariantes.

## Concorrência e async

- promise/coroutine criada sem await, join ou owner;
- callback executado depois de objeto/escopo invalidado;
- listener/timer registrado mais de uma vez;
- task sem cancelamento, timeout ou tratamento de falha;
- lock ausente, largo demais ou adquirido em ordem inconsistente;
- variável compartilhada sem sincronização;
- resposta enviada antes de persistência/processamento;
- chamada bloqueante em caminho async;
- race entre validação e uso;
- concorrência adicionada sem medição ou requisito.

Reproduzir com interleavings relevantes, não apenas leitura superficial.

## Validação, autorização e segurança

- validar formato sem validar semântica/faixa;
- confiar em dado de cliente, header ou UI;
- autenticar sem autorizar o recurso/ação;
- autorização somente no frontend;
- objeto acessado por ID sem verificar ownership/tenant;
- input concatenado em SQL, shell, HTML, URL, path ou template;
- segredo, token, chave ou PII em código/log;
- permissões excessivas e default allow;
- criptografia caseira ou uso inseguro de primitive;
- dependência não auditada;
- mensagem que expõe detalhe sensível.

Separar claramente validação, autenticação e autorização. Usar padrões oficiais do stack; não improvisar segurança.

## Qualidade local

- magic number/string sem domínio explícito;
- nomes genéricos como data, item, handler ou manager quando ocultam propósito;
- comentário que repete sintaxe;
- docstring promocional que afirma robustez, produção ou performance sem evidência;
- código morto, branch impossível ou compatibilidade especulativa;
- duplicação que já divergiu;
- função/bloco grande com responsabilidades concretamente distintas;
- fragmentação em helpers triviais que obriga saltos sem reduzir complexidade.
- wrapper, facade ou service que só encaminha argumentos;
- tipo intermediário convertido imediatamente para outro tipo idêntico;
- opções, callbacks ou hooks públicos sem consumidor;
- tratamento “defensivo” duplicado depois de uma fronteira que já validou o dado;
- comentário de cabeçalho para cada função óbvia;
- branch de compatibilidade sem versão suportada, teste ou prazo de remoção.
- tabela de retornos ou casos especiais ajustada apenas aos exemplos/testes conhecidos, sem regra de domínio que generalize.

Não transformar preferência de nome/tamanho em achado sem impacto verificável. Preferir remover volume sem função, mas preservar abstrações que concentrem política, invariantes, boundaries, reuso real ou test seams.

## Interseção entre código e UI

- kebab repetido em toda linha/card sem modelo de ações;
- ícone sem label ou nome acessível;
- ação primária escondida;
- cards produzidos por map sem hierarquia ou semântica;
- componente genérico aplicado a dados incompatíveis;
- estado fictício embutido no HTML;
- loading teatral, delay artificial ou progresso inventado;
- animação sem função ou reduced motion;
- estilo inline usado para contornar arquitetura sem justificativa;
- responsividade resolvida apenas empilhando;
- listener duplicado, ID frágil ou estado DOM desincronizado;
- foco e teclado ausentes;
- modal visual sem comportamento modal;
- tabs visuais sem semântica;
- erro real substituído por placeholder.
- alias de token ausente/circular, tipo ou unidade incompatível;
- output de tokens editado manualmente em vez da fonte;
- hardcode que contorna a camada semântica existente;
- branch de tema duplicada, token sem consumidor ou substituição textual sem confirmar função;
- rota que perde filtro, página, retorno ou autorização em link direto/refresh;

Analisar como decisão de implementação e comportamento, nunca como prova de autoria.
