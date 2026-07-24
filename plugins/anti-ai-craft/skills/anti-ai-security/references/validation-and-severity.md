# Validação e severidade de segurança

## Registro de candidato

Para cada candidato, registrar:

- ID estável;
- fonte ou ação controlável pelo atacante;
- controle mais próximo;
- sink, operação protegida ou invariante;
- caminho alcançável e superfície do produto;
- boundary e ambiente;
- pré-condições;
- depende de;
- decisão necessária e origem pesquisada;
- postura recomendada e efeito se não respondida;
- trabalho independente concluído;
- evidência favorável;
- contraprova mais forte;
- lacunas de prova;
- disposição: confirmado, suprimido, não aplicável, depende de infraestrutura, não verificado ou duplicado.

Não promover item de checklist a vulnerabilidade sem esse caminho.

## Falsificação

1. Procurar o controle no ponto mais próximo da operação.
2. Exercitar o caminho real, não apenas função isolada.
3. Tentar derrotar a hipótese com autenticação, autorização, validação, estado, configuração e infraestrutura.
4. Não usar um vizinho seguro para suprimir outra rota.
5. Tratar configuração de produção ausente do repositório como lacuna de confiança.
6. Tratar falha de setup, scanner ou teste como prova incompleta.
7. Preservar instâncias independentes mesmo quando compartilham categoria.

## Severidade

Calibrar separadamente:

- **Impacto máximo realista:** confidencialidade, integridade, disponibilidade, fraude, privacidade, segurança física ou custo.
- **Reachability e pré-condições:** acesso público/interno, papel, interação da vítima, segredo, timing, estado e controle de infraestrutura.
- **Probabilidade:** facilidade, confiabilidade, detectabilidade e incentivo.
- **Alcance:** um objeto, usuário, tenant, serviço ou plataforma.
- **Sensibilidade:** natureza e volume de dados/recursos.
- **Reversibilidade:** detecção, recuperação, rotação, estorno e perda permanente.

Alta/crítica exige caminho real e impacto material. Manter **severidade**, **confiança** e **prioridade de remediação** como eixos distintos.

## Deduplicação

Agrupar somente quando os itens compartilham:

1. mesmo controle ou causa raiz;
2. mesmo comportamento explorável;
3. mesmo impacto;
4. mesma correção.

Conservar todas as localizações e suas disposições. Uma correção comum não torna as ocorrências indistinguíveis.

## Gate de correção

Antes de editar:

- confirmar que o achado ainda existe;
- congelar o caminho e o resultado esperado;
- definir teste negativo e uso legítimo positivo;
- mapear siblings, aliases e bypasses;
- separar hardening estrutural do fix aprovado.

Depois:

- o caminho original não reproduz;
- uso legítimo continua funcionando;
- o teste falha se o controle for retirado;
- siblings e bypasses foram verificados;
- evidência foi reexecutada após a última mudança.
