# Antipadrões de arquitetura e manutenção

## Sumário

- [Preservar antes de expandir](#preservar-antes-de-expandir)
- [Abstração sem valor](#abstração-sem-valor)
- [Fragmentação e volume](#fragmentação-e-volume)
- [Prolixidade e superengenharia](#prolixidade-e-superengenharia)
- [Compatibilidade e configuração especulativas](#compatibilidade-e-configuração-especulativas)
- [Duplicação e inconsistência](#duplicação-e-inconsistência)
- [API e contrato](#api-e-contrato)
- [Performance, cache e concorrência](#performance-cache-e-concorrência)
- [Logging e observabilidade](#logging-e-observabilidade)
- [Documentação e comentários](#documentação-e-comentários)
- [Falsos sinais](#falsos-sinais)

## Preservar antes de expandir

Ler a arquitetura existente e distinguir dívida real de preferência. Uma correção localizada não autoriza redesenho amplo.

## Abstração sem valor

- helper de uma linha que só renomeia operação clara;
- wrapper que replica interface sem adaptar, proteger ou observar;
- factory para construção única e invariável;
- interface/protocolo com uma implementação sem necessidade de teste ou fronteira;
- strategy/adapter/repository introduzido por “profissionalismo” genérico;
- classe para estado que uma função/estrutura simples representa;
- genericidade para casos hipotéticos;
- configuração que substitui código claro por strings;
- base class com hooks nunca usados;
- camadas que apenas encaminham parâmetros.

Perguntar: qual variação, invariante, boundary, test seam ou política a abstração concentra? Se não houver resposta concreta, simplificar.

## Fragmentação e volume

- dezenas de arquivos pequenos sem ownership ou coesão;
- função dividida em helpers que exigem navegação constante;
- módulo “utils/common/helpers” sem domínio;
- tipo por operação simples;
- boilerplate maior que a lógica;
- duplicação de DTOs/mappers sem fronteira real;
- bloco enorme com responsabilidades realmente distintas.

O alvo é coesão e compreensão, não número universal de linhas ou arquivos.

## Prolixidade e superengenharia

- validação repetida em várias camadas sem mudança de confiança;
- objeto de opções para dois parâmetros estáveis sem evolução real;
- enum, DTO, mapper e service que apenas renomeiam os mesmos campos;
- pipeline de handlers para uma sequência curta e fixa;
- guard clauses redundantes depois de tipos ou invariantes já comprovados;
- comentário, docstring e log repetindo a mesma informação;
- duas implementações equivalentes mantidas por compatibilidade imaginária;
- arquitetura “enterprise” aplicada a script, endpoint ou fluxo local simples.
- tarefa de abstração, tokens, configuração, estrutura ou documentação declarada pronta sem consumidor conhecido ou comportamento verificável no mesmo incremento ou no dependente imediato.

Aplicar o teste de remoção: retirar a estrutura suspeita e comparar contrato, legibilidade, testes, reuso e limites arquiteturais. Se nada material for perdido, escolher a implementação menor. Não usar contagem de linhas como objetivo e não esconder domínio complexo em código compacto demais.

Fundação horizontal pode ser legítima quando possui consumidor confirmado, dependência real e prova própria, como migração compatível, contrato compartilhado ou token semântico consumido. Não rejeitar por formato; exigir valor observável.

## Compatibilidade e configuração especulativas

- feature flag sem rollout, experimento ou rollback;
- compatibilidade com versão/plataforma não suportada;
- branches para config inexistente;
- fallback para API antiga sem teste;
- opção exposta e nunca usada;
- migração parcialmente implementada;
- versão duplicada em múltiplos registries;
- default silencioso que esconde configuração ausente.

Exigir consumidor, cronograma, teste e remoção.

## Duplicação e inconsistência

- copiar implementação em vez de usar padrão local;
- validação/autorização divergente entre caminhos;
- nomes iguais com semântica diferente;
- error model diferente sem boundary;
- serialização duplicada;
- lógica repetida que já divergiu.

Não abstrair duas coincidências cegamente. Primeiro confirmar regra comum e direção de mudança.

## API e contrato

- alterar API pública sem migração/justificativa;
- aceitar parâmetros ignorados;
- retorno polimórfico não documentado;
- null/exception/status usados de forma inconsistente;
- comportamento default inventado;
- side effect surpreendente;
- contrato documentado sem implementação.

Preservar compatibilidade válida e tornar mudança explícita.

## Performance, cache e concorrência

- otimização sem perfil ou requisito;
- cache sem invalidação, ownership ou limite;
- memoization de dado mutável/sensível;
- paralelismo para operação pequena;
- batch que muda semântica;
- pooling/retry sem backpressure;
- índice ou denormalização sem query medida;
- logging em loop quente.

Medir baseline, definir métrica e validar antes/depois.

## Logging e observabilidade

- log em cada função/branch;
- mensagem genérica sem contexto acionável;
- segredo/PII em log;
- mesmo erro registrado em todas as camadas;
- catch-log-rethrow que duplica ruído;
- nível incorreto;
- métrica sem consumidor;
- tracing adicionado a caminho fora de escopo.

Registrar boundary, correlação e ação. Logging não substitui tratamento de erro.

## Documentação e comentários

- comentário que narra a próxima linha;
- docstring que promete “robusto”, “escalável” ou “production-ready”;
- exemplo de API inexistente;
- README/CI/config criado automaticamente sem pedido;
- comentário obsoleto após mudança;
- rationale ausente onde decisão não óbvia realmente existe.

Documentar por que, contrato, risco e decisão; deixar o código expressar o como.

## Falsos sinais

Não inferir autoria por:

- muitos ou poucos comentários;
- nomes muito descritivos ou genéricos isolados;
- estilo consistente;
- uso de pattern conhecido;
- número de arquivos/classes;
- código polido ou verboso;
- presença de TODO;
- erro simples.

Reportar apenas impacto e evidência observáveis.
