# Análise da unidade `design-review`

## Escopo e método

Esta análise compara integralmente a unidade externa `design-review` com as cinco skills atuais do plugin e todas as referências e configurações de interface associadas. O objetivo é identificar capacidades já cobertas, lacunas reais e melhorias adaptáveis sem copiar texto, alterar identificadores públicos ou misturar revisão com edição.

Nenhum arquivo do plugin foi alterado nesta etapa. Este documento é somente um relatório de pesquisa.

## Inventário examinado

### Unidade externa

| Artefato | Função observada |
|---|---|
| `design-review/SKILL.md` | Define uma crítica estruturada baseada em brief, código e screenshots; propõe cobertura responsiva, estados, acessibilidade, severidade e um relatório persistente. |

### Plugin atual

| Skill | Papel relevante para esta análise | Cobertura lida |
|---|---|---|
| `anti-ai-design` | Direção, revisão e implementação visual contextual | Contrato principal, configuração do agente e seis referências |
| `anti-ai-code` | Inspeção e mudança de código delimitada | Contrato principal, configuração do agente e seis referências |
| `anti-ai-audit` | Auditoria ampla estritamente somente leitura | Contrato principal, configuração do agente e três referências |
| `anti-ai-remediate` | Aplicação de achados confirmados e aprovados | Contrato principal, configuração do agente e três referências |
| `anti-ai-security` | Análise e correção de caminhos de abuso | Contrato principal, configuração do agente e quatro referências |

Também foram considerados o README, o manifesto do plugin e a entrada do marketplace para verificar nomes, invocação, compatibilidade e promessas públicas.

## Conclusão executiva

O plugin já contém a parte mais valiosa de uma revisão de design: fontes de verdade, mandato de preservar/refinar/redesenhar, screenshots reais, inspeção de código, três faixas de viewport, estados críticos, acessibilidade, passes visual e técnico separados, evidência rastreável e aprovação antes de mudanças amplas.

As principais lacunas não estão no checklist visual. Estão na operação da revisão:

1. falta um contrato explícito de suficiência de evidência para distinguir revisão de app em execução, screenshot fornecido e inspeção apenas de código;
2. falta uma matriz formal de cobertura por rota, estado, viewport e tema;
3. falta um template específico de design review com IDs estáveis, severidade, confiança, prioridade e gate de entrega separados;
4. falta definir onde screenshots podem ser armazenados sem transformar uma revisão em edição silenciosa;
5. falta um handoff explícito dos achados aprovados para remediação.

A unidade externa também contém regras rígidas que não devem ser transplantadas. Obrigar captura própria em todo caso, escrever artefatos no projeto sem autorização, impor tamanhos de viewport como universais ou tratar uma estratégia CSS como requisito confundiria método, evidência e permissão.

## Modos de revisão recomendados

O plugin deve manter os modos existentes e tornar explícitos quatro perfis de evidência dentro do modo **Revisão**:

| Perfil | Entrada suficiente | Alegações permitidas | Limites obrigatórios |
|---|---|---|---|
| Runtime completo | Aplicação executável, rotas acessíveis e ferramenta de navegador | Resultado visual, comportamento responsivo, interação, estados observados e causas confirmadas no código | Registrar ambiente, dados, viewport, tema e estados realmente exercitados |
| Runtime parcial | Parte do app executável, mas com rotas, credenciais ou dados indisponíveis | Alegações somente sobre superfícies alcançadas | Listar lacunas por rota/estado e não marcar o restante como aprovado |
| Artefato visual | Screenshots ou vídeo fornecidos pelo usuário | Hierarquia, composição e defeitos visíveis no quadro fornecido | Não inferir foco, teclado, responsividade, transição, semântica ou estados ausentes |
| Código apenas | Código, diff ou componentes sem execução confiável | Estrutura, tokens, semântica potencial, cobertura implementada e riscos técnicos | Não afirmar qualidade visual renderizada; rotular conclusões visuais como não verificadas |

Esses perfis não criam novas skills nem mudam a invocação. Apenas impedem que evidência parcial produza uma conclusão total.

## Evidência visual e evidência de código

### Princípio de suficiência

Cada afirmação deve usar o tipo de evidência adequado:

- screenshot ou observação no runtime demonstra o sintoma renderizado, não necessariamente a causa;
- código e árvore de acessibilidade ajudam a localizar a causa, mas não demonstram por si sós o resultado visual;
- teste automatizado detecta regras programadas, mas não substitui inspeção visual, teclado ou tecnologia assistiva;
- screenshot fornecido demonstra apenas o estado, viewport e momento representados;
- diff indica o que mudou, mas não limita automaticamente todas as superfícies afetadas;
- falha de ambiente não confirma defeito no produto.

### Manifesto mínimo de evidência

Para cada captura usada em um achado, registrar:

- identificador ou caminho da captura;
- rota ou superfície;
- estado e dados;
- largura, altura e escala;
- tema e preferências relevantes;
- navegador ou ambiente;
- origem: capturada na execução ou fornecida;
- momento da comparação, quando houver antes/depois.

Para cada causa atribuída ao código, registrar componente, arquivo, linha quando estável, caminho de execução e a relação entre a implementação e o sintoma visual.

### Armazenamento

Uma revisão sem autorização de edição não deve criar pastas permanentes no repositório. Capturas podem permanecer em diretório temporário ou ser apresentadas na conversa. Persistir screenshots ou um relatório dentro do projeto deve exigir autorização explícita e usar o caminho já adotado pelo repositório. A ausência de uma pasta específica nunca autoriza criar uma convenção nova.

## Cobertura de rotas, estados, viewports e temas

### Inventário de superfícies

Antes das capturas, listar:

- rotas e variantes relevantes;
- shell compartilhado, navegação e overlays;
- componentes reutilizados em várias rotas;
- papéis e permissões;
- estados de dados e de rede;
- temas e preferências de acessibilidade;
- fluxos críticos e recuperação.

Em revisão de mudança, o inventário deve partir do escopo solicitado e dos arquivos alterados, mas incluir consumidores e superfícies alcançáveis afetados. Quando o alvo for branch ou diff, o baseline deve ser documentado, não presumido.

### Matriz de cobertura

O relatório deve conter uma matriz semelhante a:

| Superfície | Criticidade | Estados exercitados | Viewports | Tema/input | Evidência | Estado |
|---|---|---|---|---|---|---|
| rota ou componente | crítica, importante ou auxiliar | normal, loading, vazio, erro, permissão etc. | estreito, intermediário, amplo | claro/escuro, teclado/touch etc. | captura, execução, código | coberto, parcial, bloqueado ou não aplicável |

A matriz não exige o produto cartesiano de todas as combinações. A seleção deve ser orientada por risco, reutilização e criticidade. Um componente compartilhado pode reduzir repetição, desde que variações por rota, conteúdo e estado sejam verificadas.

### Viewports

Os breakpoints do projeto e as falhas reais do conteúdo têm precedência. Na ausência de critérios definidos, podem ser usados como sondas iniciais:

- estreito: `375 × 812`;
- intermediário: `768 × 1024`;
- amplo: `1280 × 800`;
- reflow adicional: `320 CSS px`, quando aplicável.

Essas medidas são defaults operacionais, não requisitos universais. O objetivo é encontrar pontos em que hierarquia, leitura, navegação, toque ou ação deixam de funcionar. Para antes/depois, manter dados, estado, viewport, escala e tema equivalentes.

### Estados

Selecionar conforme o componente e o fluxo:

- normal, hover, foco, ativo, selecionado, expandido e desabilitado;
- vazio, carregando, parcial, sucesso, aviso, erro, offline e sem permissão;
- strings longas, conteúdo mínimo/máximo, mídia ausente e dados extremos;
- modal, menu, drawer, tooltip, tabs e formulários em estados significativos;
- retorno de foco, interrupção, retry, undo e recuperação;
- redução de movimento, forced colors e tema escuro quando suportados.

Estado não aplicável deve ser marcado como tal, não omitido silenciosamente.

## Severidade, confiança, prioridade e gate

A unidade externa agrupa itens como obrigação, recomendação e polimento. Essa estrutura é útil para leitura, mas mistura impacto com ordem de trabalho. O plugin já possui um modelo melhor e deve reutilizá-lo:

- **severidade:** consequência observável do problema;
- **confiança:** força da evidência;
- **prioridade:** ordem recomendada de correção;
- **gate:** passar, passar com ressalvas, bloquear ou decisão humana.

Para design, a calibração deve considerar:

- bloqueio da tarefa principal ou da recuperação;
- falha normativa de acessibilidade aplicável;
- ação primária invisível ou inalcançável;
- perda de informação, foco, estado ou conteúdo;
- alcance por rotas, papéis, dispositivos e componentes compartilhados;
- frequência da tarefa;
- reversibilidade e custo de erro;
- evidência de runtime versus hipótese de código.

Preferência estética sem dano observável permanece como observação ou decisão pendente. Não deve ser elevada artificialmente a defeito.

## Relatório recomendado

Um relatório específico de design review deve incluir:

1. escopo, mandato e fontes de verdade realmente lidas;
2. ambiente, baseline e perfil de evidência;
3. manifesto de capturas;
4. matriz de cobertura;
5. resumo e decisão de gate;
6. achados com IDs estáveis, por exemplo `ADR-001`;
7. por achado: severidade, confiança, prioridade, superfície, estado, viewport, evidência visual, evidência de código, impacto, regra, contraprova, correção sugerida, risco e aceitação;
8. decisões que funcionam e devem ser preservadas;
9. falsos positivos rejeitados e preferências separadas;
10. falhas de ambiente, lacunas e áreas não testadas;
11. plano opcional de aplicação por ID, sem editar;
12. risco residual.

O relatório só deve ser salvo no repositório quando isso tiver sido autorizado. Caso contrário, deve ser entregue na conversa.

## Aplicação opcional e separação de permissões

A revisão termina no relatório. Sugestão de correção não é autorização para alterar arquivos.

Fluxo seguro:

1. produzir achados com IDs e critérios de aceitação;
2. pedir ao usuário que selecione os IDs;
3. encaminhar somente os IDs aprovados para `anti-ai-remediate`, ou entrar no modo de implementação de `anti-ai-design` se o usuário pedir explicitamente;
4. revalidar o estado atual e a evidência;
5. capturar antes/depois com condições equivalentes;
6. solicitar nova aprovação se identidade, navegação, arquitetura, escopo ou risco mudarem.

Capturar uma tela para observação não autoriza corrigir o componente. Salvar captura, criar relatório, instalar dependência, iniciar serviço mutável ou alterar fixture também deve respeitar o escopo e as regras do projeto.

## Tratamento de falhas

| Falha | Conduta recomendada | O que não concluir |
|---|---|---|
| Aplicação não inicia | Registrar comando, saída, ambiente e tentar somente o procedimento oficial e seguro | Não chamar automaticamente de defeito visual |
| Browser ou captura indisponível | Usar artefatos fornecidos ou reduzir o perfil de evidência | Não declarar revisão visual completa |
| Rota exige credencial/dado ausente | Marcar superfície bloqueada e pedir o mínimo necessário | Não inventar fixture ou conta |
| Fonte, imagem ou API externa falha | Distinguir problema ambiental de fallback inadequado do produto | Não atribuir a causa sem traçar rede e código |
| Screenshot diverge por dados/tema/viewport | Invalidar a comparação e recapturar com condições equivalentes | Não declarar melhora ou regressão |
| Teste automatizado passa | Registrar apenas o controle efetivamente testado | Não inferir qualidade visual geral |
| Evidências entram em conflito | Preservar ambas, formular hipótese e executar teste discriminante | Não escolher a evidência mais conveniente |
| Achado exigiria edição para confirmação | Parar no risco e pedir autorização ou outro meio de prova | Não editar silenciosamente |
| Captura exigiria arquivo permanente | Usar temporário ou pedir autorização | Não criar convenção no projeto |
| Escopo fica amplo demais | Registrar corte e risco residual | Não encerrar sem declarar áreas não revisadas |

## Matriz de incorporação

| Capacidade observada | Estado no plugin | Decisão |
|---|---|---|
| Ler brief, design system, código, assets e regras do projeto | Já temos | Manter |
| Comparar implementação com direção e tarefa | Já temos | Manter |
| Mandato preservar, refinar ou redesenhar | Já temos | Manter |
| Inventariar telas, rotas, componentes, conteúdo e estados | Já temos | Manter |
| Inspecionar tokens, componentes duplicados e padrões locais | Já temos | Manter |
| Executar a interface e usar screenshots reais | Já temos | Manter |
| Revisar faixas estreita, intermediária e ampla | Já temos | Manter |
| Exercitar estados críticos, teclado, leitor de tela e recuperação | Já temos | Manter |
| Comparar antes/depois com condições equivalentes | Já temos | Manter |
| Separar passe visual/UX de passe técnico | Já temos | Manter |
| Citar screenshot, viewport, componente, arquivo ou linha | Já temos | Manter |
| Separar falha normativa, inconsistência, heurística e preferência | Já temos | Manter |
| Não editar durante auditoria e pedir aprovação para implementação | Já temos | Manter |
| Continuar cobertura depois do primeiro achado | Já temos na auditoria | Repetir explicitamente na revisão de design |
| Cobertura formal rota × estado × viewport × tema | Parcial | Incorporar com amostragem por risco |
| Perfil de evidência para runtime, screenshot fornecido e código | Parcial | Incorporar |
| Defaults de viewport quando o projeto não define breakpoints | Parcial | Incorporar como sondas, não como norma |
| Manifesto de screenshots com ambiente e origem | Parcial | Incorporar |
| Tema escuro e preferências de acessibilidade | Parcial | Tornar dimensão explícita quando suportada |
| Inventário exato de arquivos alterados e consumidores afetados | Parcial | Incorporar em revisão de diff |
| Defeitos de renderização como fonte ausente, clipping, overflow e sobreposição | Parcial | Explicitar no passe runtime |
| Registro do que funciona e deve ser preservado | Parcial | Incorporar com evidência |
| Template dedicado de design review | Não temos | Criar sem mudar a interface pública |
| IDs estáveis para handoff de achados visuais | Não temos | Incorporar |
| Regras para armazenamento temporário ou permanente de capturas | Não temos | Incorporar |
| Taxonomia de falhas de captura e ambiente | Não temos | Incorporar |
| Gate final separado de severidade e prioridade | Não temos de forma explícita no design | Incorporar |
| Obrigação de capturar a aplicação em toda revisão, inclusive de imagem isolada | Não incorporar | Evidência deve acompanhar o escopo real |
| Bloquear toda revisão até o usuário fornecer três screenshots | Não incorporar | Permitir relatório parcial com lacunas claras |
| Criar sempre uma pasta de design e salvar capturas | Não incorporar | Viola convenções locais e pode constituir edição |
| Salvar sempre um relatório no projeto | Não incorporar | Exige autorização de escrita |
| Tamanhos fixos de viewport como requisito universal | Não incorporar | Breakpoints dependem do conteúdo e do produto |
| `44 × 44` como mínimo normativo universal | Não incorporar | Preservar a distinção entre requisito aplicável e meta de plataforma |
| Exigir estratégia mobile-first baseada em um tipo específico de media query | Não incorporar | Avaliar comportamento, não preferência de implementação |
| Exigir tema escuro em produto que não o possui | Não incorporar | Testar somente suporte e requisitos reais |
| Exigir uma filosofia estética nomeada | Não incorporar | Tarefa, identidade e fontes existentes podem ser suficientes |
| Aplicar automaticamente a lista de refinamentos | Não incorporar | Revisão e edição permanecem permissões diferentes |

## Recomendações priorizadas

### ADR-R01 — Formalizar perfis de evidência

- **Prioridade:** P0
- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Instrução:** adicionar os quatro perfis de revisão e limitar as alegações ao que cada perfil consegue demonstrar.
- **Motivo:** hoje a skill pede captura real, mas não define como proceder de forma calibrada quando runtime, rota ou navegador não estão disponíveis.
- **Risco:** tornar o processo burocrático para revisões pequenas.
- **Aceitação:** qualquer relatório identifica o perfil usado, diferencia observado de não verificado e não declara revisão visual completa com código apenas.

### ADR-R02 — Criar matriz de cobertura por risco

- **Prioridade:** P0
- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Instrução:** exigir inventário de superfícies e matriz com rota/componente, criticidade, estados, viewports, tema/input, evidência e disposição.
- **Motivo:** “estreito, intermediário e amplo” não garante que rotas e estados importantes tenham sido cobertos.
- **Risco:** explosão combinatória.
- **Aceitação:** a instrução permite amostragem justificada, registra cortes e impede que uma superfície não testada seja marcada como aprovada.

### ADR-R03 — Definir política de capturas e escrita

- **Prioridade:** P0
- **Arquivos-alvo:** `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md` e `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Instrução:** declarar que revisão não edita por padrão; capturas permanentes e relatório em arquivo exigem autorização, enquanto evidência temporária pode ficar fora do alvo.
- **Motivo:** a captura de screenshots pode criar arquivos e contradizer a separação entre análise e edição.
- **Risco:** perder artefatos úteis ao fim da tarefa.
- **Aceitação:** sem autorização, nenhum arquivo permanente é criado; com autorização, o caminho segue a convenção existente e aparece no relatório.

### ADR-R04 — Adicionar template específico de design review

- **Prioridade:** P0
- **Arquivos-alvo:** novo `plugins/anti-ai-craft/skills/anti-ai-design/references/design-review-template.md` e link em `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md`
- **Instrução:** criar template com escopo, perfil de evidência, manifesto de capturas, cobertura, gate, IDs `ADR-*`, achados completos, decisões preservadas, falsos positivos, lacunas e plano opcional.
- **Motivo:** o contrato atual descreve campos gerais, mas não garante um relatório visual consistente nem um handoff por ID.
- **Risco:** duplicação com o template da auditoria.
- **Aceitação:** o novo template reutiliza severidade e campos de evidência existentes, acrescentando apenas dimensões próprias de UI.

### ADR-R05 — Separar severidade, confiança, prioridade e gate

- **Prioridade:** P1
- **Arquivos-alvo:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md` e o novo template
- **Instrução:** referenciar o modelo de severidade existente e definir um gate de entrega independente.
- **Motivo:** listas de “corrigir agora/depois/polir” confundem impacto com ordem e decisão de release.
- **Risco:** categorias demais em um achado simples.
- **Aceitação:** cada achado principal contém os quatro eixos ou explica por que um deles não se aplica; preferência estética não recebe severidade inflada.

### ADR-R06 — Tornar a evidência bidirecional

- **Prioridade:** P1
- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Instrução:** ligar sintoma visual a causa de código e exigir contraprova; impedir que screenshot isolado prove causa ou que código isolado prove resultado renderizado.
- **Motivo:** reduz diagnósticos plausíveis, porém não demonstrados.
- **Risco:** aumentar o custo de achados óbvios.
- **Aceitação:** achados de alta severidade têm evidência visual e técnica quando ambas são alcançáveis; limitações são explícitas quando uma delas falta.

### ADR-R07 — Padronizar sondas de viewport sem torná-las universais

- **Prioridade:** P1
- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Instrução:** usar primeiro breakpoints do projeto e, se ausentes, sugerir `375 × 812`, `768 × 1024` e `1280 × 800`, mantendo `320 CSS px` como teste de reflow aplicável.
- **Motivo:** facilita reprodutibilidade sem substituir decisões responsivas do produto.
- **Risco:** agentes tratarem defaults como lista ritual.
- **Aceitação:** o texto chama as medidas de sondas iniciais, exige adaptação ao conteúdo e registra as dimensões realmente usadas.

### ADR-R08 — Explicitar falhas de ambiente e cobertura

- **Prioridade:** P1
- **Arquivo-alvo:** `plugins/anti-ai-craft/skills/anti-ai-design/references/review-workflow.md`
- **Instrução:** incluir disposições para runtime indisponível, rota bloqueada, credencial ausente, captura falha, asset externo, comparação inválida e teste automatizado insuficiente.
- **Motivo:** impede que incapacidade de observar seja confundida com aprovação ou defeito.
- **Risco:** relatórios mais longos.
- **Aceitação:** cada falha operacional aparece como limitação, bloqueio ou lacuna; não vira achado do produto sem caminho causal.

### ADR-R09 — Handoff explícito para aplicação opcional

- **Prioridade:** P1
- **Arquivos-alvo:** `plugins/anti-ai-craft/skills/anti-ai-design/SKILL.md` e o novo template
- **Instrução:** encerrar revisão com IDs e oferecer aplicação apenas após seleção explícita, preferencialmente por `anti-ai-remediate`.
- **Motivo:** alinha design ao protocolo já adotado por auditoria e remediação.
- **Risco:** fricção em tarefas em que o usuário já pediu revisão e correção conjuntamente.
- **Aceitação:** pedido somente de revisão não edita; pedido conjunto mantém uma fase de achados antes da aplicação e registra quais IDs foram autorizados.

### ADR-R10 — Registrar decisões preservadas

- **Prioridade:** P2
- **Arquivo-alvo:** novo `plugins/anti-ai-craft/skills/anti-ai-design/references/design-review-template.md`
- **Instrução:** incluir uma seção curta de elementos eficazes, cada um apoiado por evidência e marcado como invariante de futura remediação.
- **Motivo:** uma correção visual segura precisa saber não apenas o que mudar, mas o que não pode regredir.
- **Risco:** elogio genérico usado como preenchimento.
- **Aceitação:** cada item cita superfície/evidência e explica o comportamento ou decisão que deve permanecer; seção vazia é permitida quando nada foi comprovado.

## Ordem de implementação sugerida

1. ADR-R01, ADR-R02 e ADR-R03 para fechar permissão, evidência e cobertura.
2. ADR-R04 e ADR-R05 para estabilizar o formato do relatório.
3. ADR-R06, ADR-R07 e ADR-R08 para melhorar reprodutibilidade e tratamento de falhas.
4. ADR-R09 para integrar revisão e remediação sem aplicação automática.
5. ADR-R10 como refinamento de preservação.

## Critério final desta análise

A melhor incorporação não é tornar toda revisão mais rígida. É tornar cada conclusão proporcional à evidência, cada superfície rastreável, cada falha explícita e cada edição dependente de autorização. Os nomes públicos `anti-ai-design`, `anti-ai-audit`, `anti-ai-remediate`, `anti-ai-code` e `anti-ai-security` devem permanecer inalterados.
