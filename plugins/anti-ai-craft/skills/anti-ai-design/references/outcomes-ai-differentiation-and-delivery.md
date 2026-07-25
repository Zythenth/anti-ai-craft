# Diferenciação e entrega responsável com IA

## Sumário

- [ADO-095 — Trocar velocidade de entrega por clareza de chegada](#ado-095--trocar-velocidade-de-entrega-por-clareza-de-chegada)
- [ADO-096 — Tornar resultados gerados inspecionáveis e corrigíveis](#ado-096--tornar-resultados-gerados-inspecionáveis-e-corrigíveis)
- [ADO-097 — Graduar autonomia pelo risco da decisão](#ado-097--graduar-autonomia-pelo-risco-da-decisão)
- [ADO-098 — Comprimir abundância gerada em hierarquia útil](#ado-098--comprimir-abundância-gerada-em-hierarquia-útil)
- [ADO-099 — Demonstrar capacidade com cenário falsificável](#ado-099--demonstrar-capacidade-com-cenário-falsificável)
- [ADO-100 — Manter a direção visual e a implementação sincronizadas](#ado-100--manter-a-direção-visual-e-a-implementação-sincronizadas)
- [ADO-101 — Humanizar a automação nos momentos que importam](#ado-101--humanizar-a-automação-nos-momentos-que-importam)

## ADO-095 — Trocar velocidade de entrega por clareza de chegada

**Força.** padrão

**Aplicar quando.** geração assistida reduz o tempo de construir telas, mas pessoas ainda não entendem a primeira tarefa, o resultado prometido ou o próximo passo.

**Decisão.** avaliar a entrega pelo tempo, esforço e compreensão necessários para alcançar um primeiro resultado útil; investir em sequência, conteúdo, estados e recuperação antes de ampliar a superfície.

**Prova.** a primeira tarefa e sua conclusão são reproduzíveis para uma pessoa nova, com dados representativos, caminho de erro e critério observável de entendimento.

**Evitar.** usar quantidade de telas, velocidade de código ou aparência de completude como substituto de valor entregue.

## ADO-096 — Tornar resultados gerados inspecionáveis e corrigíveis

**Força.** obrigatório

**Aplicar quando.** o produto gera recomendação, texto, mídia, classificação ou decisão por um processo probabilístico ou por contexto incompleto.

**Decisão.** permitir inspecionar entrada, contexto, limites e origem quando forem relevantes; oferecer edição, nova tentativa, comparação, reversão ou relato antes de um uso consequente.

**Prova.** testes representativos incluem saída correta, saída plausível porém errada, recusa e informação desatualizada; a pessoa consegue identificar e corrigir o resultado sem reiniciar todo o trabalho.

**Evitar.** apresentar saída como autoridade, esconder contexto decisivo, substituir revisão humana por um selo de confiança ou tornar a automação irreversível.

## ADO-097 — Graduar autonomia pelo risco da decisão

**Força.** obrigatório

**Aplicar quando.** uma automação recomenda ou executa ações que afetam dinheiro, dados, acesso, comunicação, reputação, segurança ou outras pessoas.

**Decisão.** aumentar confirmação, explicação, pré-visualização, limites, registro e reversibilidade conforme consequência e dificuldade de recuperação. Manter aprovação humana significativa nos pontos de risco elevado.

**Prova.** a matriz de ações relaciona nível de risco, autorização, informação exibida, responsável, log, cancelamento e recuperação; limites são testados com abuso e erro plausíveis.

**Evitar.** executar porque a tecnologia permite, usar confirmação ritual que ninguém consegue avaliar ou ocultar qual ação foi tomada e por quem.

## ADO-098 — Comprimir abundância gerada em hierarquia útil

**Força.** padrão

**Aplicar quando.** geração rápida produz muitas sugestões, rascunhos, alertas, variações ou resultados concorrentes.

**Decisão.** agrupar duplicações, ordenar pelo objetivo da tarefa, revelar o critério de seleção e preservar acesso a detalhe, filtro e refinamento. Tratar volume como matéria-prima, não como valor entregue.

**Prova.** pessoas encontram o resultado pertinente, reconhecem itens críticos e entendem por que algo recebeu prioridade; a avaliação inclui omissões e falsos destaques.

**Evitar.** despejar todas as saídas, usar novidade como prioridade, esconder diversidade útil ou apresentar ordenação opaca como verdade objetiva.

## ADO-099 — Demonstrar capacidade com cenário falsificável

**Força.** padrão

**Aplicar quando.** uma página, demonstração ou onboarding precisa explicar o que uma capacidade automatizada realmente faz.

**Decisão.** mostrar um cenário representativo com entrada, saída, tempo, papel humano, dependências, limites e recuperação. Identificar claramente se a experiência é ao vivo, gravada, simulada ou hipotética.

**Prova.** o cenário pode ser reproduzido na versão atual ou possui dados e condições documentados; falhas conhecidas aparecem junto da capacidade que qualificam.

**Evitar.** animação teatral apresentada como produto, latência ou progresso inventado, resultado escolhido sem condições ou demonstração que depende de intervenção oculta.

## ADO-100 — Manter a direção visual e a implementação sincronizadas

**Força.** obrigatório

**Aplicar quando.** protótipos, geração visual, design system e código evoluem por ferramentas ou pessoas diferentes.

**Decisão.** definir fonte de verdade, cadeia de tokens e componentes, responsáveis por atualização e validação de consumidores reais; alterar a menor camada que expresse a intenção.

**Prova.** componentes e estados implementados usam a cadeia prevista, mudanças têm origem rastreável, build não contém divergência conhecida e a revisão compara runtime com direção vigente.

**Evitar.** manter cópias concorrentes de estilo, ajustar valores soltos para imitar um protótipo, importar biblioteca visual sem necessidade ou tratar screenshot como especificação completa.

## ADO-101 — Humanizar a automação nos momentos que importam

**Força.** padrão

**Aplicar quando.** uma interação automatizada confirma, falha, recusa, orienta recuperação ou representa uma consequência que pode afetar confiança.

**Decisão.** usar linguagem direta, feedback proporcional, expectativa explícita e próximo passo recuperável; antecipar erros previsíveis sem ocultar limites, incerteza ou decisão humana necessária.

**Prova.** mensagens explicam o que ocorreu, efeito atual, dados envolvidos quando relevante, opções seguras e como obter ajuda; os mesmos estados funcionam sem animação, cor isolada ou hover.

**Evitar.** simular compreensão humana, inventar progresso, usar celebração desproporcional, culpar a pessoa pelo erro ou ocultar que uma decisão foi automatizada.
