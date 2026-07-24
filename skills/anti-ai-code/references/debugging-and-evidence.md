# Depuração e evidência

## Ciclo de investigação

1. Ler o erro e a stack completos.
2. Reproduzir com o menor caso fiel.
3. Conferir mudanças recentes e um caminho vizinho que funciona.
4. Traçar o valor incorreto até sua origem, atravessando boundaries.
5. Formular **uma** hipótese falsificável.
6. Executar o menor experimento que separa essa hipótese das alternativas.
7. Se falhar, isolar ou desfazer o experimento antes do próximo. Falhas repetidas exigem revisar o modelo mental, não declarar automaticamente que toda a arquitetura está errada.

Evitar patches sucessivos sem nova evidência, alterações simultâneas que impedem atribuir causa e explicações depois do fato.

## Mudança e prova

Cada passo não trivial deve formar um par:

- mudança observável;
- prova específica executada depois dela.

Congelar a alegação antes de escolher o comando. Exemplos:

| Alegação | Evidência mínima adequada |
|---|---|
| bug corrigido | reprodução original deixa de falhar e regressão passa |
| API compatível | tipo/assinatura da versão exata e execução ou build |
| código compila | build/typecheck real |
| requisito atendido | cenário de aceitação exercitado |
| refactor sem mudança | caracterização antes e suíte proporcional depois |
| espera robusta | evento/condição observável e timeout diagnóstico |

Teste não prova build, lint não prova runtime e suíte verde não prova um requisito ausente do oráculo.

## Gate do oráculo

Antes do corpo de um teste não trivial:

1. nomear a mutação ou defeito de produção que ele deveria detectar;
2. derivar o resultado esperado de contrato, regra de domínio ou cálculo independente;
3. evitar usar o mesmo helper, builder ou algoritmo da unidade testada para construir o esperado;
4. testar comportamento, efeito, saída ou exit code, não presença textual por `grep`.

Se retirar o controle relevante e o teste continuar verde, o teste não prova aquele controle.

## Mocks e efeitos

- Identificar efeitos que fazem parte do contrato antes de mockar.
- Mockar a boundary externa/lenta mais baixa possível.
- Preservar efeitos reais necessários e a estrutura real dos dados.
- Não usar expectativas do mock como principal prova de correção.
- Preferir integração quando wiring, serialização, transação ou persistência fazem parte do risco.

## Tempo, concorrência e refactor

Substituir `sleep` arbitrário por espera de evento ou condição com timeout que explique o estado observado. Atraso fixo só é adequado quando tempo é parte explícita do contrato.

Antes de refatorar comportamento sem proteção, criar testes de caracterização. Fazer passos pequenos e provar ausência de mudança após cada um.

## Escada contra API inventada

Verificar, em ordem:

1. repositório, lockfile, imports e tipos;
2. pacote/CLI realmente instalado e `--help`;
3. documentação oficial da versão exata;
4. release notes ou repositório oficial.

Uma assinatura semelhante em outra versão, linguagem ou SDK não é prova. Se a evidência terminar, declarar o desconhecido.
