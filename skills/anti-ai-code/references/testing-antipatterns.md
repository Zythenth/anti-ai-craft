# Antipadrões de testes

## Sumário

- [Teste como evidência](#teste-como-evidência)
- [Falsa confiança](#falsa-confiança)
- [Mocks](#mocks)
- [Esperas](#esperas)
- [Snapshots](#snapshots)
- [Casos necessários](#casos-necessários)
- [Qualidade do oráculo](#qualidade-do-oráculo)
- [Execução honesta](#execução-honesta)

## Teste como evidência

Um teste aprovado demonstra somente os casos e oráculos que contém. Não demonstra correção geral, segurança, performance, ausência de corrida ou conformidade.

Preferir um teste que:

- falha antes da correção pela causa esperada;
- passa depois;
- exerce API/comportamento real;
- verifica efeito e estado persistente;
- cobre limite ou caminho de falha;
- permanece determinístico;
- explica a regressão.

Antes de escrever o corpo, nomear a mutação ou defeito de produção que o teste deve detectar. Derivar o esperado de contrato, regra de domínio ou cálculo independente; não reutilizar helper/builder/algoritmo da unidade como oráculo.

Para correção de bug, preferir a sequência:

1. escrever ou localizar um teste que reproduza;
2. executá-lo contra o comportamento defeituoso e confirmar falha pela causa esperada;
3. aplicar a correção mínima;
4. confirmar que o teste passa;
5. executar regressão proporcional ao risco.

Se o estado anterior não puder ser executado com segurança ou já tiver mudado, registrar essa limitação em vez de simular uma etapa vermelha.

## Falsa confiança

- suíte apenas de happy path;
- assertions fracas, ausentes ou sobre valores constantes;
- teste que só confirma que o mock devolveu o valor configurado;
- mock da unidade sob teste;
- stub tão detalhado que reimplementa a produção;
- snapshot grande aprovado sem revisão semântica;
- teste que passa mesmo removendo a lógica;
- cobertura alta sem branches, limites ou mutation score;
- fixture incompatível com dados reais;
- execução seletiva que ignora falhas;
- retry automático que mascara flakiness;
- teste skipped/xfail sem prazo e motivo;
- teste gerado junto ao bug que codifica o comportamento errado.
- implementação ou fixture codificada como tabela de respostas para satisfazer apenas os exemplos conhecidos.

## Mocks

- Conhecer os side effects que pertencem ao contrato antes de mockar.
- Mockar fronteira lenta, instável ou externa quando necessário.
- Mockar a boundary mais baixa possível e manter efeitos reais necessários.
- Não mockar tipo/contrato que não se compreende.
- Verificar resultado observável antes de sequência interna de chamadas.
- Usar fake/in-memory somente se preservar semântica relevante.
- Manter ao menos um teste de integração para wiring, serialização, transação, autenticação e configuração.
- Não substituir dependência real por mock em produção para “corrigir” teste.
- Expectativas de chamadas do mock não são evidência primária quando existe resultado observável.

## Esperas

- Preferir evento ou condição observável com timeout diagnóstico a `sleep` arbitrário.
- Usar atraso fixo somente quando tempo é parte explícita do contrato.
- Ao estourar o timeout, registrar o estado observado para distinguir lentidão, deadlock e evento ausente.

## Snapshots

- Usar para representação estável que uma pessoa consegue revisar.
- Evitar snapshots enormes, voláteis ou com IDs/timestamps.
- Não atualizar snapshot em massa sem explicar mudança.
- Acrescentar assertions semânticas para propriedades críticas.
- Em UI, não tratar snapshot DOM como substituto de interação, acessibilidade e screenshot real.

## Casos necessários

Selecionar conforme o contrato:

- zero, um, muitos, mínimo, máximo e fora da faixa;
- vazio, null/ausente, inválido e tipo errado;
- duplicação, ordem diferente e dados longos;
- permissão negada, outro usuário/tenant e sessão expirada;
- timeout, indisponibilidade e falha parcial;
- retry, idempotência e rollback;
- concorrência/interleaving;
- encoding, locale, timezone e DST quando pertinentes;
- API/dependência/config real;
- regressão histórica.

## Qualidade do oráculo

- Verificar resposta, side effects, persistência, evento e log somente na medida do contrato.
- Não afirmar apenas que “não lançou exceção”.
- Não usar implementação como oráculo de si mesma.
- Acrescentar entradas não presentes nos exemplos originais quando houver risco de implementação ajustada aos testes.
- Preferir propriedade/invariante quando exemplos isolados são insuficientes.
- Usar mutation testing, fuzzing/property tests ou casos ampliados proporcionalmente ao risco; não exigir por ritual.

## Execução honesta

- Registrar comando exato, código de saída e resumo relevante.
- Distinguir “não executado”, “não disponível”, “falhou por ambiente” e “passou”.
- Não alegar lint/build/typecheck/test sem rodar.
- Não esconder stderr, remover teste, afrouxar assertion ou mudar fixture para eliminar falha sem causa.
- Executar teste focado e depois suíte maior proporcional ao impacto.
