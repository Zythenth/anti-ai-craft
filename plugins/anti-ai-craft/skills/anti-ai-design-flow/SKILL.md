---
name: anti-ai-design-flow
description: "Orquestrar uma jornada completa e retomável de produto, do briefing à arquitetura da informação, sistema visual, plano de build, implementação autorizada, revisão e handoff de achados. Usar somente quando invocada explicitamente para conduzir três ou mais fases, coordenar duas ou mais skills Anti-IA, começar uma feature do zero ou retomar um fluxo persistido; não usar para componente isolado, correção visual local, auditoria, código ou threat model avulsos."
---

# Fluxo de Design Anti-IA

Orquestrar fases e handoffs sem substituir os contratos especializados. Tratar o fluxo como máquina de estados adaptativa, não como ritual linear. Planejamento não autoriza edição; uma autorização não atravessa silenciosamente fases, skills ou ações externas.

## Preparar o fluxo

1. Confirmar feature, objetivo, escopo, definição de sucesso e se o usuário quer apenas planejar ou também implementar e revisar.
2. Ler instruções, README, especificações, design system, código, testes, configurações, assets e histórico pertinente antes de perguntar.
3. Localizar convenções de planejamento já existentes. Não criar `.design/` nem outro diretório se o projeto já define fonte de verdade.
4. Ler integralmente [flow-state.md](references/flow-state.md) e criar o registro de execução.
5. Classificar cada fase como `executar`, `reusar`, `atualizar` ou `não aplicável`, citando a evidência. Arquivo existente não comprova fase concluída.
6. Resolver primeiro fatos verificáveis no projeto. Para decisão material ainda aberta, perguntar em rodada curta com recomendação, fundamento, consequência e trabalho que pode continuar.
7. Solicitar autorização separada antes de criar ou atualizar artefatos persistentes. Sem autorização, manter o checkpoint na resposta e declarar que a retomada entre tarefas depende desse registro.

## Consultar contratos especializados

Os arquivos irmãos são referências internas deste fluxo; lê-los não ativa outra
skill e não deve ser descrito como se ela tivesse sido invocada. Ler somente o
contrato aplicável à fase:

- `../anti-ai-design/SKILL.md` para briefing, estrutura, tokens, direção, acessibilidade e revisão visual;
- `../anti-ai-security/SKILL.md` quando dados, identidade, papéis, tenants, custo, integração, upload, automação ou operação protegida mudarem;
- `../anti-ai-code/SKILL.md` para implementação delimitada e prova por tarefa;
- `../anti-ai-audit/SKILL.md` para revisão independente e estritamente somente leitura;
- `../anti-ai-remediate/SKILL.md` somente para preparar o handoff de IDs confirmados e aprovados.

Quando uma fase exigir o modo ou a autoridade própria de outra skill — auditoria
independente, threat model completo ou remediação — entregar a entrada necessária
e pedir sua invocação explícita. Não ativar, simular nem afirmar que outra skill
foi executada. Não copiar versões resumidas desses contratos para esta skill.

## Executar fases adaptativas

### 1. Descoberta e brief

- Construir ledger de decisões materiais.
- Identificar problema, usuários, tarefa, contexto, superfície, mandato, requisitos, invariantes, conteúdo, dados, estados, riscos, não escopo e critérios de aceitação.
- Usar o contrato de brief de `anti-ai-design` como referência interna.
- Marcar a saída como `rascunho`, `bloqueado` ou `aprovado`; somente confirmação explícita do usuário permite `aprovado`.

**Pronto quando:** as decisões necessárias à próxima fase estão confirmadas, assumidas com baixo risco ou bloqueadas com condição precisa; nenhum requisito material foi inventado.

### 2. Arquitetura da informação

- Executar quando houver múltiplas superfícies, navegação, rotas, conteúdo crescente, papéis, retomada ou fluxo de várias etapas.
- Mapear pontos de entrada, tarefas, hierarquia, navegação, URLs, persistência, fluxo principal, alternativas, erro e recuperação.
- Cruzar UI, dados e autorização. Não tratar navegação escondida como controle de segurança.

**Pronto quando:** superfícies e fluxos no escopo têm entrada, saída, estados, contrato de localização e critérios verificáveis; compatibilidade material está preservada ou aprovada.

### 3. Sistema visual e tokens

- Reusar a fonte autoritativa do projeto.
- Distinguir fonte de outputs gerados, resolver aliases e mapear consumidores.
- Criar ou ampliar somente famílias necessárias ao escopo.
- Não obrigar dark mode, stack, escala, breakpoint ou formato.

**Pronto quando:** papéis semânticos e consumidores reais estão identificados, modos e estados aplicáveis foram cobertos e qualquer migração tem alcance delimitado.

### 4. Plano de build

- Decompor em fatias verticais por resultado observável, não por HTML/CSS/JS, arquivo ou disciplina.
- Registrar origem, resultado, estratégia `reutilizar/alterar/criar`, dependências, risco, critério de pronto e prova.
- Distinguir bloqueio duro, ordem preferencial e paralelismo seguro.
- Antecipar dependências duras, hipótese de maior risco e uma primeira fatia representativa.

**Pronto quando:** cada tarefa está ligada a requisito, decisão ou risco; não há infraestrutura sem consumidor nem decisão material escondida em subtarefa.

### 5. Gate de segurança

Executar somente quando houver superfície aplicável. Registrar ativos, atores, dados, fronteiras, tenants, operações caras ou destrutivas, controles esperados e histórias de abuso. Classificar cada ponto como `resolvido`, `decisão pendente`, `depende de infraestrutura` ou `não aplicável`.

**Pronto quando:** decisões que mudariam estrutura ou critérios de conclusão foram resolvidas ou bloqueadas antes do build.

### 6. Implementação autorizada

- Confirmar autorização de edição e escopo de tarefas.
- Implementar uma fatia por vez conforme o contrato interno de `anti-ai-code`, sem alegar que a skill foi invocada.
- Mapear tarefa → arquivos → mudança → prova.
- Não marcar concluída por ter editado; usar `validada`, `validação parcial`, `bloqueada`, `superada` ou `falhou`.
- Revalidar somente artefatos dependentes quando nova evidência mudar decisão anterior.

**Pronto quando:** critérios da fatia foram exercitados depois da última mudança, uso legítimo permaneceu funcional e diff ficou limitado ao resultado.

### 7. Revisão independente

- Executar somente quando houver evidência proporcional ao tipo de revisão.
- Aplicar o contrato interno de revisão visual/técnica. Quando for necessária auditoria independente ampla, preparar o escopo e pedir invocação explícita de `$anti-ai-audit`.
- Comparar tarefa, brief, estrutura, tokens, plano, código e runtime sem presumir que documento ou código é automaticamente a fonte vigente.
- Produzir IDs estáveis; separar severidade, confiança, prioridade, gate, preferências e falsos positivos.

**Pronto quando:** cobertura, evidência, limitações, decisões preservadas e risco residual estão explícitos. Revisão não autoriza correção.

### 8. Remediação opcional

- Aceitar somente IDs selecionados explicitamente.
- Revalidar cada achado no estado atual.
- Preparar um handoff para `$anti-ai-remediate`; aplicar correções somente após essa skill ser invocada explicitamente com os IDs e a autorização.
- Atualizar artefatos de fluxo somente quando autorizado e necessário ao ID.

**Pronto quando:** cada ID tem status e prova; código, evidência, tarefa e artefatos autorizados não se contradizem.

## Transicionar e invalidar

- Avançar entre fases read-only quando a saída estiver suficiente e nenhuma decisão material estiver aberta.
- Pedir confirmação para mudança de identidade, navegação, contrato, escopo, risco, edição, ação externa ou trade-off de produto.
- Não pedir confirmação ritual após cada pergunta, fase ou tarefa.
- Se decisão anterior mudar, marcar apenas dependentes como `revalidar`; não reescrever todo o fluxo.
- Se o usuário pausar, emitir checkpoint com fase, saídas, decisões, bloqueios, arquivos e próxima ação segura.
- Se houver múltiplas features, exigir identificador inequívoco; não escolher silenciosamente pela data de modificação.

## Limites

Não:

- ativar implicitamente ou substituir `$anti-ai-design`;
- impor conjunto fixo de documentos a tarefa pequena;
- herdar autorização para commit, push, deploy, rotação, migração ou produção;
- mover correções para a auditoria;
- considerar arquivo presente, checklist marcado ou build verde como prova suficiente;
- escolher tema, estética, stack, biblioteca ou breakpoint por preset;
- sobrescrever artefato existente ou persistir segredos e dados pessoais;
- tratar preferência visual como defeito ou vulnerabilidade;
- continuar uma fase bloqueada inventando produto, dados, APIs ou comportamento.

## Contrato de saída

Entregar:

- feature e objetivo;
- fase atual e classificação de todas as fases;
- fontes de verdade e estado do código usados;
- decisões, pressupostos, bloqueios e invalidações;
- artefatos produzidos ou atualizados e autorização correspondente;
- tarefas e provas por estado;
- IDs de revisão ou remediação, quando houver;
- validações executadas e não executadas;
- risco residual;
- checkpoint e próxima ação segura.
