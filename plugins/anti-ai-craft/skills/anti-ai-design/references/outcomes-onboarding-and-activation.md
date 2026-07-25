# Onboarding, ativação e primeiro valor

## Sumário

- [ADO-033 — Definir o evento de ativação](#ado-033--definir-o-evento-de-ativação)
- [ADO-034 — Entregar valor antes de instruir em excesso](#ado-034--entregar-valor-antes-de-instruir-em-excesso)
- [ADO-035 — Não entregar uma tela inicial sem rumo](#ado-035--não-entregar-uma-tela-inicial-sem-rumo)
- [ADO-036 — Usar evidência da jornada real](#ado-036--usar-evidência-da-jornada-real)
- [ADO-037 — Separar fricção útil de burocracia](#ado-037--separar-fricção-útil-de-burocracia)
- [ADO-038 — Fazer a primeira tarefa parecer possível](#ado-038--fazer-a-primeira-tarefa-parecer-possível)
- [ADO-039 — Tornar orientação uma ação, não um tour passivo](#ado-039--tornar-orientação-uma-ação-não-um-tour-passivo)
- [ADO-040 — Revelar valor progressivamente](#ado-040--revelar-valor-progressivamente)
- [ADO-041 — Personalizar com intenção declarada](#ado-041--personalizar-com-intenção-declarada)
- [ADO-042 — Usar exemplos claramente identificados](#ado-042--usar-exemplos-claramente-identificados)
- [ADO-043 — Tornar progresso e recuperação verdadeiros](#ado-043--tornar-progresso-e-recuperação-verdadeiros)
- [ADO-044 — Celebrar conquista sem simular sucesso](#ado-044--celebrar-conquista-sem-simular-sucesso)
- [ADO-045 — Escolher padrão de onboarding pelo contexto](#ado-045--escolher-padrão-de-onboarding-pelo-contexto)

## ADO-033 — Definir o evento de ativação

**Força.** obrigatório

**Aplicar quando.** o produto possui cadastro, avaliação, primeiro uso ou fluxo que antecede retenção e pagamento.

**Decisão.** identificar a ação ou resultado observável que diferencia pessoas que obtêm valor das que abandonam. Projetar o caminho inicial para essa ação e medir tempo até ela, repetição pertinente e retorno posterior.

**Prova.** relacionar o evento a telemetria, pesquisa, entrevistas, suporte ou análise de coortes; documentar a definição e suas limitações em vez de usar cadastro como substituto.

**Evitar.** chamar abertura de conta, visualização de tutorial ou clique em botão de ativação sem demonstrar que eles predizem valor real.

## ADO-034 — Entregar valor antes de instruir em excesso

**Força.** obrigatório

**Aplicar quando.** o fluxo inicial pede configuração, dados, integrações, convites ou aprendizado antes de qualquer resultado perceptível.

**Decisão.** reordenar o fluxo para chegar a uma primeira consequência útil o mais cedo possível. Ensinar somente o necessário para a próxima ação e revelar detalhes adicionais no ponto em que passam a ser necessários.

**Prova.** medir a sequência real, o tempo até o primeiro resultado compreensível e os pontos de desistência; confirmar que o valor exibido é produzido ou claramente rotulado como exemplo.

**Evitar.** tour longo, manual obrigatório, pedir toda configuração antecipadamente, promessa de resultado que aparece só após trabalho desproporcional ou reduzir controles de segurança necessários.

## ADO-035 — Não entregar uma tela inicial sem rumo

**Força.** obrigatório

**Aplicar quando.** uma pessoa chega a dashboard, lista, espaço de trabalho ou área recém-criada sem dados próprios.

**Decisão.** explicar o estado, apontar uma próxima ação concreta, comunicar o benefício de realizá-la e, quando útil, oferecer exemplo ou modelo explicitamente identificado. Priorizar um caminho inicial em vez de muitas opções equivalentes.

**Prova.** testar se alguém sem conhecimento prévio identifica o que fazer, por que fazer e como recuperar-se após erro ou interrupção.

**Evitar.** painel vazio tratado como neutro, métricas fictícias sem rótulo, checklist burocrático, múltiplos CTAs concorrentes e orientação dependente de tooltip invisível.

## ADO-036 — Usar evidência da jornada real

**Força.** obrigatório

**Aplicar quando.** houver hipótese de que onboarding, trial ou primeira sessão está falhando.

**Decisão.** comparar o fluxo desenhado com comportamento real em sessões, entrevistas, tickets e dados de funil. Transformar divergências em hipóteses priorizadas, sem atribuir intenção à pessoa usuária.

**Prova.** registrar origem das observações, segmento, momento da jornada, evidência contrária e severidade do impacto antes de alterar a interface.

**Evitar.** redesenhar pelo mapa interno, usar uma sessão isolada como regra, coletar conteúdo pessoal além do necessário ou confundir gravação incompleta com prova de compreensão.

## ADO-037 — Separar fricção útil de burocracia

**Força.** padrão

**Aplicar quando.** houver debate sobre remover campos, criar qualificação, solicitar configuração ou exigir uma etapa inicial.

**Decisão.** manter esforço apenas quando ele protege a pessoa, cumpre requisito legítimo, permite personalização de valor ou produz compromisso consciente. Cortar, adiar ou automatizar coleta administrativa que não muda a experiência imediata.

**Prova.** para cada passo, descrever o valor para a pessoa, a necessidade do sistema, o risco de removê-lo e a alternativa menos intrusiva.

**Evitar.** usar dificuldade para prender a pessoa, pedir dados sensíveis sem finalidade, tratar opt-in como obrigatório ou eliminar consentimento, segurança e conformidade em nome de conversão.

## ADO-038 — Fazer a primeira tarefa parecer possível

**Força.** heurística

**Aplicar quando.** a primeira ação exige importação, criação, convite, publicação, integração ou outra tarefa percebida como grande.

**Decisão.** dividir a entrada em uma unidade honesta e pequena, mostrar o que já foi concluído e deixar claro o próximo passo. Priorizar a menor ação que produz consequência útil, não a menor ação possível sem valor.

**Prova.** verificar esforço percebido em teste de uso, taxa de início, conclusão, abandono e tempo até valor; confirmar que qualquer progresso exibido corresponde a trabalho real.

**Evitar.** porcentagem fabricada, metas artificialmente baixas que não levam a nada, checklist infinito ou ocultar esforço futuro relevante.

## ADO-039 — Tornar orientação uma ação, não um tour passivo

**Força.** padrão

**Aplicar quando.** a proposta é usar tooltips, walkthrough, vídeo, documentação ou uma sequência guiada no primeiro acesso.

**Decisão.** converter orientação em passos contextualizados que permitem executar uma ação real e observar efeito. O conteúdo de apoio deve ser dispensável, recuperável e compatível com teclado, leitor de tela e redução de movimento.

**Prova.** verificar que cada passo habilita uma tarefa, pode ser ignorado e retomado sem perda de estado, e não bloqueia quem já sabe operar o produto.

**Evitar.** sequência que exige leitura sem ação, modal impossível de fechar, foco perdido, vídeo com informação exclusiva sem alternativa textual ou tour que reaparece após rejeição.

## ADO-040 — Revelar valor progressivamente

**Força.** padrão

**Aplicar quando.** o produto tem superfície extensa, recursos avançados, custo de erro alto ou muitas possibilidades logo no início.

**Decisão.** mostrar primeiro a capacidade necessária para a tarefa atual e apresentar recursos adicionais quando houver contexto de necessidade. Manter caminhos de descoberta, busca e ajuda para quem precisa ir além.

**Prova.** mapear qual recurso é necessário em cada etapa, verificar descobribilidade posterior e acompanhar se o ocultamento reduziu erro sem criar dependência de suporte.

**Evitar.** esconder controles críticos, tornar recursos pagos ou de segurança invisíveis, usar progressão como desculpa para limitar autonomia ou assumir que todas as pessoas seguem a mesma sequência.

## ADO-041 — Personalizar com intenção declarada

**Força.** padrão

**Aplicar quando.** o produto atende perfis com objetivos, maturidade, função ou fluxos iniciais diferentes.

**Decisão.** pedir uma declaração de objetivo curta e explicada apenas quando ela altera recomendação, conteúdo, ordem ou rota de forma percebida. Permitir corrigir a escolha posteriormente.

**Prova.** demonstrar como cada resposta muda a experiência, registrar finalidade e retenção do dado, e validar se a personalização reduz esforço ou melhora o primeiro resultado.

**Evitar.** questionário longo, segmentação opaca, dados sensíveis sem necessidade, personalização que limita opções sem aviso ou escolha que não pode ser alterada.

## ADO-042 — Usar exemplos claramente identificados

**Força.** padrão

**Aplicar quando.** um espaço vazio precisa demonstrar o resultado possível antes de a pessoa inserir dados próprios.

**Decisão.** oferecer exemplos, modelos ou dados de demonstração que se pareçam com o domínio, estejam visivelmente rotulados e possam ser substituídos, ocultados ou removidos. Distinguir exemplo de dado observado.

**Prova.** confirmar que nenhum gráfico, atividade, indicador ou registro demonstra fato inexistente; testar se a pessoa entende a origem do conteúdo e consegue iniciar com dados próprios.

**Evitar.** números que parecem reais, exemplo misturado à produção, dados pessoais, screenshot como substituto de interação ou estado vazio sem saída clara.

## ADO-043 — Tornar progresso e recuperação verdadeiros

**Força.** obrigatório

**Aplicar quando.** a jornada inclui etapas, processamento, importação, aprovação, falha, pausa ou retorno posterior.

**Decisão.** apresentar progresso somente quando o sistema conhece estágio ou consequência correspondente; informar o que ocorreu, o que falta, o que permanece salvo e como retomar ou desfazer. Preservar estado com segurança.

**Prova.** testar interrupção, recarregamento, erro, permissão insuficiente, conexão instável e retorno ao fluxo; revisar mensagens com tecnologias assistivas.

**Evitar.** barra simulada, sucesso antes da confirmação, perda silenciosa de dados, erro genérico, recomeço obrigatório sem necessidade ou recuperação que dependa de suporte para casos comuns.

## ADO-044 — Celebrar conquista sem simular sucesso

**Força.** heurística

**Aplicar quando.** a pessoa conclui uma ação de esforço relevante ou alcança um primeiro resultado útil.

**Decisão.** dar feedback que reconheça a conquista, explique seu efeito e apresente uma próxima ação opcional. Calibrar movimento, cor e intensidade ao contexto, respeitando preferência de movimento reduzido.

**Prova.** verificar que a conquista existe, que o feedback não interrompe tarefa crítica e que a pessoa entende o estado sem depender de animação, cor ou som.

**Evitar.** confete automático, linguagem exagerada, tratar configuração incompleta como vitória, recompensas que pressionam continuidade ou animação que bloqueia a próxima ação.

## ADO-045 — Escolher padrão de onboarding pelo contexto

**Força.** obrigatório

**Aplicar quando.** for escolhido modal de boas-vindas, checklist, tour, tooltip, modelo, exemplo, definição de objetivo ou demonstração.

**Decisão.** selecionar o padrão conforme familiaridade da pessoa, complexidade, risco de erro, valor da primeira tarefa, variedade de rotas e necessidade de acessibilidade. Combinar padrões somente se cada um tiver papel distinto e percurso recuperável.

**Prova.** documentar o problema que cada padrão resolve, seus estados, critérios de saída, alternativa acessível e resultado esperado; validar em pessoas novatas e experientes quando ambas existirem.

**Evitar.** adotar componente porque é tendência, checklist para tarefas sem sequência real, tooltip como única instrução, modal aninhado, onboarding que bloqueia uso normal ou uma única jornada imposta a todos.
