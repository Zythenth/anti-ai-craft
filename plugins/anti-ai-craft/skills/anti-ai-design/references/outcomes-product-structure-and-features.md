# Estrutura de produto e foco de funcionalidades

## Sumário

- [ADO-046 — Tratar cada funcionalidade como compromisso contínuo](#ado-046--tratar-cada-funcionalidade-como-compromisso-contínuo)
- [ADO-047 — Justificar escopo pelo valor sustentado](#ado-047--justificar-escopo-pelo-valor-sustentado)
- [ADO-048 — Projetar descoberta no ponto de necessidade](#ado-048--projetar-descoberta-no-ponto-de-necessidade)
- [ADO-049 — Distinguir abertura de uso recorrente](#ado-049--distinguir-abertura-de-uso-recorrente)
- [ADO-050 — Dar precedência visual ao caminho de valor](#ado-050--dar-precedência-visual-ao-caminho-de-valor)
- [ADO-051 — Fazer a complexidade pagar seu custo cognitivo](#ado-051--fazer-a-complexidade-pagar-seu-custo-cognitivo)
- [ADO-052 — Reduzir superfície sem retirar autonomia](#ado-052--reduzir-superfície-sem-retirar-autonomia)
- [ADO-053 — Preservar hábitos validados durante mudanças](#ado-053--preservar-hábitos-validados-durante-mudanças)
- [ADO-054 — Fechar o ciclo de vida da funcionalidade](#ado-054--fechar-o-ciclo-de-vida-da-funcionalidade)
- [ADO-055 — Mudar para resolver fricção demonstrada](#ado-055--mudar-para-resolver-fricção-demonstrada)
- [ADO-056 — Distinguir demanda, ativação, adoção e continuidade](#ado-056--distinguir-demanda-ativação-adoção-e-continuidade)
- [ADO-057 — Transformar painéis em orientação acionável](#ado-057--transformar-painéis-em-orientação-acionável)
- [ADO-058 — Usar o comportamento da interface como evidência](#ado-058--usar-o-comportamento-da-interface-como-evidência)

## ADO-046 — Tratar cada funcionalidade como compromisso contínuo

**Força.** padrão

**Aplicar quando.** uma funcionalidade nova parece pequena, mas adiciona conceitos, estados, suporte, documentação ou permissão ao produto.

**Decisão.** avaliar a proposta pelo benefício duradouro, pelo público que a usará, pelo custo de aprendizagem, pelos estados necessários e pela manutenção futura; preferir a menor versão que permita verificar a hipótese.

**Prova.** há uma tarefa identificável, usuário ou segmento definido, fluxo completo, estados de erro e recuperação previstos, além de critério observável de adoção ou sucesso.

**Evitar.** aceitar funcionalidades apenas porque são fáceis de implementar, foram pedidas isoladamente ou tornam uma demonstração mais impressionante.

## ADO-047 — Justificar escopo pelo valor sustentado

**Força.** heurística

**Aplicar quando.** for preciso priorizar entre várias melhorias, integrações ou variações de uma mesma capacidade.

**Decisão.** comparar contribuição para a tarefa principal, especificidade para o público, esforço de entrega e custo de operação; tratar a priorização como hipótese explícita, não como fórmula automática.

**Prova.** a escolha registra qual resultado do usuário ela melhora, qual alternativa foi adiada e quais sinais poderão invalidar a prioridade.

**Evitar.** converter pontuações em autoridade falsa, ignorar requisitos normativos ou sacrificar acessibilidade, segurança e compatibilidade por uma estimativa de retorno.

## ADO-048 — Projetar descoberta no ponto de necessidade

**Força.** padrão

**Aplicar quando.** uma capacidade relevante existe, mas as pessoas não a encontram durante a tarefa em que ela seria útil.

**Decisão.** tornar a capacidade recuperável no contexto de uso, com estado vazio orientador, sugestão contextual ou próximo passo visível; preservar opção de dispensar a orientação.

**Prova.** o ponto de necessidade, a ação que a antecede e o caminho de retorno estão documentados; usuários conseguem descobrir e compreender a capacidade sem depender de anúncio externo.

**Evitar.** bloquear a tarefa com tours longos, repetir avisos ignorados, usar badges permanentes ou confundir descoberta com pressão para adoção.

## ADO-049 — Distinguir abertura de uso recorrente

**Força.** heurística

**Aplicar quando.** a equipe usa cliques, visitas ou abertura de menu como prova de que uma funcionalidade criou valor.

**Decisão.** definir uso significativo conforme a tarefa, sua frequência esperada e o resultado produzido; analisar recorrência, abandono e necessidade de assistência junto da simples exposição.

**Prova.** a métrica ou estudo diferencia curiosidade, teste pontual e conclusão de uma tarefa útil, com período e população declarados.

**Evitar.** impor uma frequência universal, tratar telemetria incompleta como comportamento humano completo ou coletar dados além do necessário.

## ADO-050 — Dar precedência visual ao caminho de valor

**Força.** padrão

**Aplicar quando.** uma tela organiza muitas informações, mas não deixa claro qual ação ou informação permite avançar na tarefa principal.

**Decisão.** usar posição, sequência, contraste, agrupamento e linguagem para distinguir contexto, ação dominante, informação de apoio e detalhes progressivos; manter alternativas importantes acessíveis.

**Prova.** a hierarquia continua perceptível sem cor decorativa ou efeitos, e usuários conseguem identificar o próximo passo sem memorizar caminhos ocultos.

**Evitar.** fazer uma ação dominante parecer obrigatória quando há escolhas legítimas, esconder consequências materiais ou reduzir todas as opções secundárias a menus opacos.

## ADO-051 — Fazer a complexidade pagar seu custo cognitivo

**Força.** heurística

**Aplicar quando.** a superfície acumula opções, campos, configurações ou módulos que tornam a tarefa mais difícil de compreender.

**Decisão.** manter complexidade apenas quando ela sustentar uma necessidade real; agrupar por intenção, revelar detalhe conforme a tarefa e oferecer rotas avançadas sem degradar o fluxo frequente.

**Prova.** cada grupo, escolha ou configuração tem finalidade, público e estado definidos; testes ou evidências de uso mostram que a organização reduz erro ou esforço.

**Evitar.** aplicar limite numérico de recursos, esconder controles necessários para especialistas ou transformar simplificação em perda de poder e transparência.

## ADO-052 — Reduzir superfície sem retirar autonomia

**Força.** padrão

**Aplicar quando.** dados de uso indicam que partes da interface são raramente usadas, confusas ou competem com a tarefa principal.

**Decisão.** considerar simplificar, reordenar, tornar progressivo ou mover o acesso para contexto apropriado; preservar uma rota encontrável para capacidades ainda necessárias a grupos menores.

**Prova.** a decisão identifica quem será afetado, como a capacidade continua acessível, que documentação ou migração é necessária e como reversões serão tratadas.

**Evitar.** remover comportamento sem evidência, esconder configurações críticas, quebrar links ou fluxos de pessoas experientes e tratar baixa frequência como ausência de valor.

## ADO-053 — Preservar hábitos validados durante mudanças

**Força.** padrão

**Aplicar quando.** uma parte frequente e reconhecida do produto será reorganizada, renomeada ou receberá novo padrão de interação.

**Decisão.** preservar invariantes úteis, introduzir transição proporcional e testar o percurso de quem já usa a área; mudar o mapa mental apenas quando o ganho demonstrado superar o custo de reaprendizagem.

**Prova.** há evidência de frequência, comportamento atual e motivo da mudança; navegação, atalhos, foco, URLs e retorno continuam coerentes ou têm migração clara.

**Evitar.** redesenhar por novidade, chamar preferência interna de melhoria ou presumir que familiaridade é resistência irracional.

## ADO-054 — Fechar o ciclo de vida da funcionalidade

**Força.** obrigatório

**Aplicar quando.** uma funcionalidade será criada, modificada, descontinuada ou removida.

**Decisão.** projetar introdução, descoberta, permissões, estados, manutenção, migração, descontinuação, remoção e recuperação. Definir desde o início qual evidência sustentará expansão, correção ou encerramento.

**Prova.** o plano identifica responsáveis, consumidores, dados, estados, dependências, política de compatibilidade e condição de saída; remoções preservam trabalho e oferecem caminho verificável.

**Evitar.** tratar lançamento como fim do trabalho, manter opção sem dono, retirar capacidade silenciosamente ou deixar dados e navegação órfãos.

## ADO-055 — Mudar para resolver fricção demonstrada

**Força.** obrigatório

**Aplicar quando.** houver vontade de refatorar ou redesenhar uma interface que já funciona.

**Decisão.** declarar a fricção de usuário, requisito ou falha observável que a mudança resolve e delimitar os invariantes que não podem regredir; preferir refinamento verificável a substituição cosmética.

**Prova.** a proposta aponta comportamento anterior, evidência, resultado esperado, risco de regressão e validação proporcional antes da implementação.

**Evitar.** justificar trabalho amplo por cansaço visual, tendência de mercado, disponibilidade de componente ou promessa vaga de modernização.

## ADO-056 — Distinguir demanda, ativação, adoção e continuidade

**Força.** padrão

**Aplicar quando.** uma métrica de abertura, cadastro, clique ou uso é apresentada como prova de que uma funcionalidade gera valor.

**Decisão.** separar interesse inicial, primeiro resultado, incorporação ao trabalho e continuidade útil. Projetar e avaliar cada etapa com sinais próprios sem presumir que avanço em uma garante as seguintes.

**Prova.** a análise usa coortes compatíveis e mostra transições entre etapas, tempo, abandono e valor percebido; a ausência de instrumentação aparece como lacuna.

**Evitar.** chamar clique de adoção, confundir curiosidade com demanda ou celebrar uso recorrente de uma tarefa que não beneficia a pessoa.

## ADO-057 — Transformar painéis em orientação acionável

**Força.** padrão

**Aplicar quando.** um dashboard, relatório ou página inicial concentra métricas, tabelas e alertas sem orientar o que a pessoa pode fazer em seguida.

**Decisão.** priorizar a pergunta que a superfície ajuda a responder, destacar informação interpretável no contexto e conectar desvios relevantes a uma próxima ação segura; manter dados detalhados disponíveis para investigação.

**Prova.** cada visualização tem público, decisão apoiada, origem dos dados, estado vazio/erro e limite de interpretação; a ação relacionada respeita permissões e não produz efeito sem confirmação apropriada.

**Evitar.** converter todo número em CTA, inventar causalidade, esconder dados brutos necessários ou usar cor e urgência para simular gravidade.

## ADO-058 — Usar o comportamento da interface como evidência

**Força.** obrigatório

**Aplicar quando.** uma decisão visual, estrutural ou de fluxo pretende melhorar resultado de usuário ou produto.

**Decisão.** formular uma hipótese falsificável, escolher evidência proporcional — pesquisa, observação, suporte, acessibilidade, telemetria minimizada ou experimento — e registrar a condição que mostraria que a hipótese falhou.

**Prova.** baseline, segmento, período, limitação, efeito esperado e possível dano são declarados; resultados não confundem correlação, preferência interna e causalidade.

**Evitar.** usar métricas de vaidade, declarar êxito sem comparação adequada, coletar telemetria sensível sem necessidade ou manter uma mudança que prejudica acesso e autonomia.
