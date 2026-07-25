# Revisão final de cobertura

Data: 2026-07-24

Atualização de 2026-07-25: a versão `0.4.0` mantém a ativação híbrida. Design,
Código e Segurança podem ser selecionadas implicitamente pelo contexto; Fluxo,
Auditoria e Remediação permanecem exclusivamente manuais. Esta mudança preserva
as fronteiras de autorização descritas no relatório. A mesma versão amplia Design
Anti-IA com 101 princípios autorais orientados a resultados, carregados por tema e
subordinados à tarefa, à evidência e às proteções de autonomia.

## Veredito

**PASS para o conteúdo commitável.**

As oito unidades foram analisadas integralmente, cada uma possui relatório próprio
e todas as 99 recomendações tituladas foram rechecadas. Noventa e oito foram
incorporadas. Uma permanece adiada de forma deliberada e segura: `DF-23`, porque
o relato privado de vulnerabilidades do repositório foi verificado e está
desativado. Criar `SECURITY.md` antes de existir um canal monitorado produziria
uma promessa falsa.

As cinco skills anteriores mantêm seus identificadores. A única adição pública é
`$anti-ai-design-flow`, explícita e opcional para jornadas com três ou mais fases.

## Artefatos examinados

- os oito relatórios em `docs/analises/`;
- `README.md` e o marketplace;
- manifesto, metadados e contratos das seis skills;
- todas as referências internas das seis skills;
- estado Git e diff completo do repositório.

## Matriz integral das recomendações

`Incorporada` significa que o contrato e a evidência de aceitação estão presentes
no estado final. Os identificadores `BT-*` foram atribuídos apenas nesta revisão,
porque o relatório original de tarefas usa títulos por prioridade em vez de IDs.

### Fluxo de design

| ID | Recomendação | Estado |
|---|---|---|
| DF-01 | Encaminhar o fluxo completo para a orquestradora | Incorporada |
| DF-02 | Formalizar critérios para pular fases | Incorporada |
| DF-03 | Criar checkpoint retomável | Incorporada |
| DF-04 | Definir invalidação entre fases | Incorporada |
| DF-05 | Tornar arquitetura da informação uma saída mínima | Incorporada |
| DF-06 | Definir conclusão para tokens | Incorporada |
| DF-07 | Produzir plano de build verificável | Incorporada |
| DF-08 | Consumir o plano no código | Incorporada |
| DF-09 | Exigir prova antes de concluir tarefa | Incorporada |
| DF-10 | Inserir gate de segurança antes do build | Incorporada |
| DF-11 | Propagar mudanças ao modelo de ameaça | Incorporada |
| DF-12 | Criar gate de prontidão da revisão | Incorporada |
| DF-13 | Validar a cadeia de decisões | Incorporada |
| DF-14 | Fazer auditoria reconhecer artefatos do fluxo | Incorporada |
| DF-15 | Registrar cobertura do fluxo | Incorporada |
| DF-16 | Preservar IDs no handoff de remediação | Incorporada |
| DF-17 | Reconciliar estado após remediação | Incorporada |
| DF-18 | Padronizar pausa e retomada | Incorporada |
| DF-19 | Usar gates materiais, sem confirmação ritual | Incorporada |
| DF-20 | Tornar handoffs explícitos | Incorporada |
| DF-21 | Publicar a nova skill sem alterar as cinco existentes | Incorporada |
| DF-22 | Atualizar a seleção pública | Incorporada |
| DF-23 | Definir divulgação privada de vulnerabilidades | Adiada: depende de canal privado operacional |
| DF-24 | Acrescentar gate de release | Incorporada |
| DF-25 | Explicar o risco de atualização mutável | Incorporada |

### Entrevista e decisões

| ID | Recomendação | Estado |
|---|---|---|
| GRM-01 | Gate de decisão explícito no design | Incorporada |
| GRM-02 | Fechamento dos ramos de direção | Incorporada |
| GRM-03 | Separar descoberta técnica de escolha de contrato | Incorporada |
| GRM-04 | Ordenar decisões por dependência | Incorporada |
| GRM-05 | Perguntar sem interromper cobertura independente | Incorporada |
| GRM-06 | Estruturar decisões pendentes no relatório | Incorporada |
| GRM-07 | Distinguir falta de informação de falta de aprovação | Incorporada |
| GRM-08 | Classificar perguntas nos gates | Incorporada |
| GRM-09 | Tornar o modelo de ameaça rastreável | Incorporada |
| GRM-10 | Registrar dependência e recomendação em segurança | Incorporada |
| GRM-11 | Preservar metadados e compatibilidade | Incorporada |

### Brief de design

| ID | Recomendação | Estado |
|---|---|---|
| DB-01 | Modo de brief com fronteira de escrita | Incorporada |
| DB-02 | Referência dedicada para o brief | Incorporada |
| DB-03 | Descoberta adaptável ao repositório | Incorporada |
| DB-04 | Classificar entradas e perguntas por impacto | Incorporada |
| DB-05 | Schema de brief rastreável | Incorporada |
| DB-06 | Persistência sem sobrescrita silenciosa | Incorporada |
| DB-07 | Estados e falhas do documento | Incorporada |
| DB-08 | Integração segura com implementação | Incorporada |
| DB-09 | Cobertura do brief na auditoria, inclusive não verificável | Incorporada |
| DB-10 | Brief não autoriza remediação | Incorporada |
| DB-11 | Segurança e privacidade condicionais | Incorporada |
| DB-12 | Expor brief sem renomear a skill | Incorporada |

### Arquitetura da informação

| ID | Recomendação | Estado |
|---|---|---|
| IA-01 | Referência estrutural dentro de design | Incorporada |
| IA-02 | Roteamento da referência no contrato principal | Incorporada |
| IA-03 | Invariantes estruturais no contrato de direção | Incorporada |
| IA-04 | Passe estrutural na revisão visual | Incorporada |
| IA-05 | Cobertura estrutural na auditoria | Incorporada |
| IA-06 | Gate de remediação para navegação e URL | Incorporada |
| IA-07 | Rotas e estado no contrato de código | Incorporada |
| IA-08 | Segurança da arquitetura da informação | Incorporada |
| IA-09 | Critérios mensuráveis de arquitetura da informação | Incorporada |
| IA-10 | Preservar metadados públicos existentes | Incorporada |

### Design tokens

| ID | Recomendação | Estado |
|---|---|---|
| DT-01 | Procedimento central de tokens | Incorporada |
| DT-02 | Roteamento explícito para pedidos de tokens | Incorporada |
| DT-03 | Auditoria verificável dos tokens | Incorporada |
| DT-04 | Famílias contextuais | Incorporada |
| DT-05 | Validação visual e técnica | Incorporada |
| DT-06 | Antipadrões técnicos de tokens | Incorporada |
| DT-07 | Remediar pela fonte e alcance real | Incorporada |
| DT-08 | Gate para alteração global | Incorporada |
| DT-09 | Evidência opcional no relatório | Incorporada |
| DT-10 | Tema dinâmico como entrada não confiável | Incorporada |

### Brief para tarefas

| ID | Recomendação | Estado |
|---|---|---|
| BT-01 | Contrato comum de tarefa verificável | Incorporada |
| BT-02 | Fatias verticais no planejamento de design | Incorporada |
| BT-03 | Classificação operacional do inventário | Incorporada |
| BT-04 | Preservar gates da remediação no plano | Incorporada |
| BT-05 | Segurança no critério de pronto | Incorporada |
| BT-06 | Dependências com semântica útil | Incorporada |
| BT-07 | Próximos passos em lotes comprováveis | Incorporada |
| BT-08 | Prova como parte do estado | Incorporada |
| BT-09 | Acessibilidade proporcional por fatia | Incorporada |
| BT-10 | Proibir fundação concluída sem consumidor | Incorporada |
| BT-11 | Persistir planos sem arquivo universal | Incorporada |
| BT-12 | Atualizar e encerrar o plano | Incorporada |
| BT-13 | Ajustar prompts sem renomear skills | Incorporada |

### Frontend

| ID | Recomendação | Estado |
|---|---|---|
| FD-01 | Inventário de reuso proporcional | Incorporada |
| FD-02 | Direção visual por eixos | Incorporada |
| FD-03 | Contrato condicional de temas | Incorporada |
| FD-04 | Gate para recursos visuais externos | Incorporada |
| FD-05 | Validação de leitura e formulário mobile | Incorporada |
| FD-06 | Matriz proporcional de tema | Incorporada |
| FD-07 | Classificação funcional de movimento | Incorporada |
| FD-08 | Evidência de reuso na auditoria | Incorporada |

### Revisão de design

| ID | Recomendação | Estado |
|---|---|---|
| ADR-R01 | Perfis de evidência | Incorporada |
| ADR-R02 | Matriz de cobertura por risco | Incorporada |
| ADR-R03 | Política de capturas e escrita | Incorporada |
| ADR-R04 | Template próprio de design review | Incorporada |
| ADR-R05 | Separar severidade, confiança, prioridade e gate | Incorporada |
| ADR-R06 | Evidência bidirecional | Incorporada |
| ADR-R07 | Sondas condicionais e reproduzíveis de viewport | Incorporada |
| ADR-R08 | Falhas de ambiente e cobertura | Incorporada |
| ADR-R09 | Handoff explícito para aplicação | Incorporada |
| ADR-R10 | Decisões preservadas | Incorporada |

## Correções da auditoria independente

A primeira auditoria final encontrou oito lacunas P1. Todas foram corrigidas e
reauditadas com resultado `8/8 PASS`. Um passe adicional de segurança encontrou
mais uma lacuna P1, também corrigida e revalidada:

1. referências internas não simulam invocação das outras skills;
2. execução e screenshots dependem do perfil de evidência;
3. acessibilidade e UI usam matriz proporcional, não ritual universal;
4. achados visuais preservam feature, fase, artefato e estado;
5. estados documentais foram normalizados;
6. o passe estrutural cobre entrada, navegação, URL, retorno e recuperação;
7. sondas de viewport são fallbacks condicionais, não breakpoints impostos;
8. a auditoria representa explicitamente o estado `não verificável`.
9. runtime visual exige ambiente conhecido, autorização para efeitos externos,
   preferência por fixtures e redação de segredos, PII e conteúdo de cliente.

## Regras deliberadamente rejeitadas

Não foram incorporados:

- tema escuro, mobile-first, stack, framework, escala ou breakpoint universais;
- TDD, commit, push, instalação, remediação ou escrita automáticos;
- perguntas, confirmações ou fases como ritual;
- seleção silenciosa do documento mais recente;
- persistência em caminho fixo;
- screenshot, navegador, leitor de tela ou matriz cartesiana obrigatórios sem
  relação com escopo e risco;
- ocultação universal de ações em menu de reticências;
- inferência de autoria por IA a partir de um padrão visual.

## Testes comportamentais

### Revisão delimitada

Um teste com uma única ação `Editar` escondida em menu de reticências:

- permaneceu no componente solicitado;
- declarou o perfil e a limitação de evidência;
- tratou o menu como heurística contextual, não prova de autoria;
- produziu um único achado rastreável;
- não iniciou o fluxo completo.

### Fluxo novo

Um teste de onboarding B2B multitenant:

- manteve a etapa inicial somente leitura;
- separou planejamento de autorização de edição;
- acionou gate condicional de segurança para papéis, tenants e convites;
- não impôs tema escuro;
- fez apenas três perguntas materiais;
- produziu fases, estados e checkpoint sem persistência automática.

## Validação técnica

- seis `SKILL.md` aprovados pelo validador oficial;
- manifesto aprovado pelo validador oficial de plugins;
- todos os links Markdown locais das skills resolvem;
- três políticas `allow_implicit_invocation: true` e três `false`, conforme o modo híbrido;
- cada prompt de interface menciona o identificador correto;
- README, manifesto e diretórios concordam em seis skills e versão `0.4.0`;
- nenhuma citação, URL, autoria ou nome dos repositórios-base permanece;
- nenhuma fonte temporária de pesquisa permanece no working tree;
- `git diff --check` passou imediatamente antes do commit.

## Pendência externa segura

`DF-23` não é uma lacuna a preencher com texto fictício. A configuração do
repositório oferece a opção de habilitar relatos privados, mas ela estava
desativada na verificação. A ação correta para uma versão futura é:

1. o mantenedor habilitar e assumir o monitoramento do canal privado;
2. confirmar o fluxo de envio;
3. só então publicar `SECURITY.md` com escopo, versões mantidas, informação mínima
   e proibição de enviar segredos reais.

Essa configuração não foi alterada nesta tarefa.
