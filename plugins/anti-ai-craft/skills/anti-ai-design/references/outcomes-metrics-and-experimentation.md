# Métricas, pesquisa e experimentação

## Sumário

- [ADO-087 — Ligar a métrica a um resultado do usuário](#ado-087--ligar-a-métrica-a-um-resultado-do-usuário)
- [ADO-088 — Registrar baseline antes de declarar melhora](#ado-088--registrar-baseline-antes-de-declarar-melhora)
- [ADO-089 — Separar sinal inicial de resultado duradouro](#ado-089--separar-sinal-inicial-de-resultado-duradouro)
- [ADO-090 — Definir métricas de proteção](#ado-090--definir-métricas-de-proteção)
- [ADO-091 — Instrumentar eventos com semântica e minimização](#ado-091--instrumentar-eventos-com-semântica-e-minimização)
- [ADO-092 — Planejar o experimento antes de observar o resultado](#ado-092--planejar-o-experimento-antes-de-observar-o-resultado)
- [ADO-093 — Usar pesquisa qualitativa quando o volume não prova causalidade](#ado-093--usar-pesquisa-qualitativa-quando-o-volume-não-prova-causalidade)
- [ADO-094 — Comparar segmentos e coortes compatíveis](#ado-094--comparar-segmentos-e-coortes-compatíveis)

## ADO-087 — Ligar a métrica a um resultado do usuário

**Força.** obrigatório

**Aplicar quando.** Uma decisão de design é justificada por cadastro, clique, tempo, visita, receita ou outra métrica agregada.

**Decisão.** Explicar qual tarefa ou valor humano o indicador representa, em que janela e para qual população. Se a relação for indireta, rotular a métrica como proxy e buscar evidência complementar.

**Prova.** O contrato liga evento, comportamento, resultado percebido e consequência de negócio sem confundir correlação com causa.

**Evitar.** Otimizar volume vazio, tempo de tela sem utilidade, clique acidental, receita sem qualidade ou métrica escolhida apenas porque já existe no dashboard.

## ADO-088 — Registrar baseline antes de declarar melhora

**Força.** obrigatório

**Aplicar quando.** Uma tela, fluxo ou mensagem será comparada como antes/depois.

**Decisão.** Capturar estado inicial, período, segmento, definição do evento, qualidade dos dados e fatores externos relevantes antes da mudança. Preservar a comparação equivalente.

**Prova.** Baseline e resultado usam a mesma definição, população, janela e instrumentação, ou a diferença está declarada como limitação.

**Evitar.** Comparar semanas sazonais, públicos distintos, eventos redefinidos, screenshot com dados diferentes ou ausência de medição como se fosse zero.

## ADO-089 — Separar sinal inicial de resultado duradouro

**Força.** padrão

**Aplicar quando.** Uma alteração aumenta atenção, cadastro, início de fluxo, uso inicial ou compra, mas seu efeito posterior ainda é desconhecido.

**Decisão.** Acompanhar indicador de entrada junto de ativação, conclusão útil, retorno, suporte, reembolso, cancelamento ou outro resultado tardio aplicável.

**Prova.** O plano diferencia métricas antecedentes e posteriores e define por quanto tempo a leitura precisa continuar.

**Evitar.** Chamar curiosidade de adoção, cadastro de retenção, compra de satisfação ou aumento momentâneo de clique de sucesso sustentável.

## ADO-090 — Definir métricas de proteção

**Força.** obrigatório

**Aplicar quando.** Uma hipótese busca elevar conversão, uso, velocidade, receita, adoção ou retenção.

**Decisão.** Definir sinais que não podem piorar: erro, abandono involuntário, acessibilidade, suporte, privacidade, reclamação, reembolso, cancelamento, tempo da tarefa ou satisfação, conforme o risco.

**Prova.** Critérios de aprovação e reversão incluem o indicador principal e os limites de proteção, com responsável e janela de observação.

**Evitar.** Declarar vitória por uma métrica isolada enquanto custos, dano, exclusão ou dificuldade de saída aumentam.

## ADO-091 — Instrumentar eventos com semântica e minimização

**Força.** obrigatório

**Aplicar quando.** A validação depende de analytics, logs de interação, replay, experimento ou segmentação.

**Decisão.** Nomear eventos pelo comportamento do domínio, documentar gatilho e propriedades, coletar somente o necessário e respeitar consentimento, retenção, redação e acesso. Testar duplicação, perda e mudança de versão.

**Prova.** Existe dicionário de eventos, exemplo verificável, política de dados e teste que relaciona a emissão ao estado real da interface.

**Evitar.** Captura indiscriminada, PII desnecessária, evento que mede renderização como conclusão, propriedades ambíguas ou telemetria inventada para preencher relatório.

## ADO-092 — Planejar o experimento antes de observar o resultado

**Força.** obrigatório

**Aplicar quando.** A equipe pretende usar teste controlado para escolher entre alternativas.

**Decisão.** Definir hipótese, unidade de análise, população, métrica, efeito mínimo relevante, tamanho ou duração adequados, regra de parada e tratamento de múltiplas leituras antes de iniciar.

**Prova.** O plano é revisável sem conhecer o vencedor e registra desvios, falhas de exposição e qualidade da amostra.

**Evitar.** Encerrar ao primeiro número favorável, testar muitas mudanças sem diagnóstico, ignorar poder estatístico ou apresentar associação como causalidade.

## ADO-093 — Usar pesquisa qualitativa quando o volume não prova causalidade

**Força.** padrão

**Aplicar quando.** O tráfego, a frequência ou o número de usuários não sustenta experimento quantitativo confiável.

**Decisão.** Usar observação de tarefa, entrevista, teste de compreensão, análise de suporte, revisão de sessões autorizadas ou protótipo comparativo para descobrir mecanismos e falhas. Registrar alcance e não generalizar além da amostra.

**Prova.** Há protocolo, participantes compatíveis, notas ligadas a comportamentos e hipóteses que podem ser confirmadas ou rejeitadas depois.

**Evitar.** Chamar cinco opiniões de taxa universal, conduzir respostas, usar colega interno como único usuário ou inventar precisão estatística.

## ADO-094 — Comparar segmentos e coortes compatíveis

**Força.** padrão

**Aplicar quando.** O resultado varia por origem, experiência, plano, dispositivo, papel, mercado, período ou versão.

**Decisão.** Separar populações com contexto materialmente diferente e comparar coortes equivalentes. Investigar se uma média agregada esconde benefício para um grupo e dano para outro.

**Prova.** Segmentação possui motivo anterior à leitura, tamanho suficiente ou limitação declarada e não usa característica sensível sem base legítima.

**Evitar.** Misturar tráfego conhecido com público novo, comparar clientes maduros com recém-chegados, escolher segmento depois do resultado ou transformar benchmark externo em meta universal.
