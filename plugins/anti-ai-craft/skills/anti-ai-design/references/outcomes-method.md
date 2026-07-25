# Método de design orientado a resultados

## Escopo

Usar esta biblioteca somente quando a interface tiver objetivo explícito de aquisição, compreensão da proposta, ativação, adoção, monetização, continuidade ou diferenciação de produto. Não aplicar linguagem de funil a uma superfície operacional apenas porque ela contém botões, métricas ou usuários pagantes.

O resultado da pessoa e o resultado da organização devem ser compatíveis. Quando houver conflito, preservar autonomia, acessibilidade, segurança, privacidade, informação material e saída compreensível. Uma métrica comercial não substitui a tarefa do usuário.

## Autoridade e força

Interpretar os cartões assim:

- **obrigatório:** proteção de verdade, autonomia, acesso, segurança, compatibilidade ou evidência; só afastar por requisito superior explícito e registrar a decisão;
- **padrão:** escolha inicial recomendada; adaptar quando a fonte de verdade do projeto ou a evidência contextual apontar outra direção;
- **heurística:** hipótese útil para pesquisa ou experimento; nunca apresentar como garantia causal.

A ordem de autoridade é: requisito legal ou normativo aplicável; contrato e invariantes do projeto; decisão explícita do usuário; evidência observável; guidance; heurística; preferência.

## Cartão de decisão

Cada princípio possui ID estável e cinco campos:

- **Força.** quanto a regra admite variação;
- **Aplicar quando.** gatilho e contexto relevante;
- **Decisão.** ação concreta ou pergunta de projeto;
- **Prova.** evidência que sustenta, valida ou derrota a decisão;
- **Evitar.** abuso, falso positivo ou aplicação fora do contexto.

Selecionar somente os IDs necessários ao problema atual. Em uma mesma decisão, usar no máximo três princípios candidatos antes de sintetizar; mais regras não significam melhor projeto.

## Roteamento

| Problema predominante | Referência |
|---|---|
| Resultado, estágio, superfície, custo e estratégia | [outcomes-context-and-strategy.md](outcomes-context-and-strategy.md) |
| Público, posicionamento, promessa e diferenciação verbal | [outcomes-positioning-and-promise.md](outcomes-positioning-and-promise.md) |
| Aquisição, página de entrada, proposta, prova e CTA | [outcomes-acquisition-and-landing.md](outcomes-acquisition-and-landing.md) |
| Primeiro uso, ativação, onboarding, trial e estados vazios | [outcomes-onboarding-and-activation.md](outcomes-onboarding-and-activation.md) |
| Escopo, hierarquia, dashboards, descoberta e adoção de features | [outcomes-product-structure-and-features.md](outcomes-product-structure-and-features.md) |
| Planos, preço, cobrança, trial, limites e upgrade | [outcomes-pricing-and-monetization.md](outcomes-pricing-and-monetization.md) |
| Continuidade, ciclo de vida, cancelamento, exportação e suporte | [outcomes-retention-and-offboarding.md](outcomes-retention-and-offboarding.md) |
| Defaults, persuasão, fricção, urgência e prova social | [outcomes-ethical-choice-architecture.md](outcomes-ethical-choice-architecture.md) |
| Instrumentação, métricas, pesquisa e experimentos | [outcomes-metrics-and-experimentation.md](outcomes-metrics-and-experimentation.md) |
| Produtos gerados com IA, identidade, confiança e entrega | [outcomes-ai-differentiation-and-delivery.md](outcomes-ai-differentiation-and-delivery.md) |

## Workflow de geração

1. Confirmar tarefa, público, estágio da relação, superfície e decisão que a pessoa precisa tomar.
2. Registrar promessa, evidência disponível, restrições, conteúdo real, estados e consequências materiais.
3. Escolher a referência temática e os IDs aplicáveis; rejeitar os que dependem de fatos ausentes.
4. Traduzir cada princípio selecionado em conteúdo, ordem, hierarquia, interação ou estado observável.
5. Definir resultado para a pessoa, indicador principal, métricas de proteção, contraprova e condição de reversão.
6. Projetar caminho principal, alternativa, recusa, erro, interrupção, retomada e saída.
7. Verificar acessibilidade, privacidade, segurança, responsividade e coerência com o sistema existente.
8. Implementar somente com autorização e validar na interface real quando possível.

## Workflow de revisão

Separar:

- defeito funcional, normativo ou de acessibilidade;
- inconsistência com promessa, tarefa ou fonte de verdade;
- hipótese de resultado ainda não testada;
- preferência estética;
- tática rejeitada por risco à autonomia ou à confiança.

Para cada achado orientado a resultado, registrar IDs usados, baseline, segmento, comportamento esperado, dano possível, evidência atual, contraprova e validação necessária. Não afirmar aumento de conversão, retenção ou receita a partir de screenshot, gosto ou benchmark externo.

## Proibições

Nunca fabricar ou disfarçar:

- escassez, urgência, disponibilidade ou fila;
- depoimento, avaliação, logotipo, caso, número ou resultado;
- progresso, etapa, duração, atividade ou telemetria;
- consentimento, renovação, custo, limite, elegibilidade ou consequência;
- dado de demonstração como produção.

Não dificultar cancelamento, recusa, exportação, exclusão, comparação ou acesso à informação material. Não explorar compulsão, vulnerabilidade, medo ou confusão como estratégia de crescimento. Não usar defaults, destaque visual ou fricção para obter uma escolha que não seja defensável para a própria pessoa.

## Contrato de saída

Para geração ou plano orientado a resultado, entregar:

- público, tarefa, estágio e superfície;
- resultado da pessoa e resultado da organização;
- IDs selecionados e motivo de aplicabilidade;
- decisões de conteúdo, fluxo, hierarquia e estado;
- prova existente, hipótese e desconhecidos;
- indicador principal, métricas de proteção e contraprova;
- riscos de autonomia, acesso, privacidade, segurança e confiança;
- validação e condição de reversão.
