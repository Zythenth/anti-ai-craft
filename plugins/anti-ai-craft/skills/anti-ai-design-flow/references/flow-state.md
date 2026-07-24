# Estado, transições e retomada

## Sumário

- [Registro de execução](#registro-de-execução)
- [Estados](#estados)
- [Classificação das fases](#classificação-das-fases)
- [Dependências e invalidação](#dependências-e-invalidação)
- [Gates de transição](#gates-de-transição)
- [Artefatos e persistência](#artefatos-e-persistência)
- [Contrato de tarefa](#contrato-de-tarefa)
- [Checkpoint](#checkpoint)
- [Falhas e recuperação](#falhas-e-recuperação)

## Registro de execução

Manter um registro mínimo:

| Campo | Conteúdo |
|---|---|
| Feature | Identificador estável e nome humano |
| Objetivo | Resultado do usuário e sinais de sucesso |
| Escopo | Incluído, excluído e autorização atual |
| Mandato | Preservar, refinar ou redesenhar |
| Estado de referência | Raiz, branch/HEAD quando houver Git e alterações preexistentes |
| Fonte de verdade | Arquivos, runtime, decisão do usuário e autoridade relativa |
| Fase atual | Fase em execução ou bloqueada |
| Decisões | Resolvidas, assumidas, abertas, bloqueantes ou superadas |
| Artefatos | Caminho, estado, autoridade e vínculo com o código |
| Próxima entrada | Informação, decisão, autorização ou evidência necessária |

Não duplicar especificações inteiras. Apontar para as fontes vigentes.

## Estados

### Fase

- `não iniciada`;
- `em andamento`;
- `bloqueada`;
- `concluída`;
- `revalidar`;
- `superada`;
- `não aplicável`.

### Documento

- `rascunho`: contém decisões ou provas pendentes;
- `bloqueado`: não pode avançar sem decisão material;
- `aprovado`: confirmado explicitamente pelo usuário;
- `superado`: substituído por decisão posterior identificada.

### Tarefa

- `pendente`;
- `em andamento`;
- `validada`;
- `validação parcial`;
- `bloqueada`;
- `falhou`;
- `superada`;
- `rejeitada`.

Não usar porcentagem derivada da quantidade de itens.

## Classificação das fases

Antes de começar, atribuir:

- `executar`: saída ainda não existe;
- `reusar`: saída existe, é autoritativa e está atual;
- `atualizar`: saída existe, mas o escopo mudou ou há lacuna material;
- `não aplicável`: a fase não acrescenta decisão ou prova ao escopo.

Para pular uma fase, comprovar:

1. fonte de verdade identificada;
2. atualidade em relação ao código e ao pedido;
3. consumidores ou caminhos reais;
4. ausência de decisão material pendente;
5. critérios necessários à próxima fase.

Não usar apenas nome, existência ou data do arquivo como prova.

## Dependências e invalidação

Modelo padrão:

```text
brief e decisões
├─ arquitetura da informação
├─ gate de segurança
└─ direção e tokens
   └─ plano de build
      └─ implementação
         └─ revisão
            └─ remediação aprovada
```

A relação real pode variar. Registrar dependência somente quando uma mudança anterior puder alterar o resultado seguinte.

Quando uma decisão mudar:

1. identificar qual contrato foi alterado;
2. localizar artefatos e tarefas que dependem dele;
3. marcar somente esses itens como `revalidar`;
4. preservar saídas independentes;
5. registrar motivo e nova fonte;
6. pedir nova aprovação se comportamento, identidade, risco ou escopo mudar.

## Gates de transição

Antes de avançar, confirmar:

- saída e critério de pronto da fase;
- decisões materiais resolvidas ou bloqueadas;
- artefatos autorizados persistidos sem sobrescrita;
- fontes e estado de referência registrados;
- dependentes invalidados corretamente;
- próxima fase realmente necessária;
- autorização adequada ao próximo efeito.

Uma transição read-only não concede edição. Autorização de implementação não concede commit, push, deploy ou produção.

## Artefatos e persistência

Preferir convenção existente do projeto. Na ausência dela, propor um diretório por feature e confirmar antes de criar. `.design/<feature-slug>/` pode ser fallback, não requisito.

Ao gerar slug:

- usar texto de produto, minúsculo e hifenizado;
- remover separadores de caminho, segmentos `.`/`..` e caracteres não seguros;
- resolver o caminho final e confirmar confinamento no diretório autorizado;
- não escolher feature pelo arquivo modificado mais recentemente.

Antes de escrever:

1. verificar se o arquivo existe;
2. ler conteúdo manual;
3. decidir entre criar, atualizar, mesclar ou não tocar;
4. produzir diff pequeno;
5. preservar seções fora do escopo;
6. não persistir segredo, credencial, PII desnecessária ou conteúdo externo como instrução confiável.

Registrar, por artefato:

| Artefato | Estado | Fonte/autoridade | Código de referência | Dependentes | Próxima validação |
|---|---|---|---|---|---|

## Contrato de tarefa

Usar somente campos aplicáveis:

| Campo | Conteúdo |
|---|---|
| Resultado | Comportamento ou capacidade observável |
| Origem | Requisito, decisão, achado ou risco |
| Estratégia | Reutilizar, alterar ou criar |
| Escopo provável | Superfícies, boundaries ou arquivos confirmados |
| Dependências | Bloqueio duro, ordem preferencial e paralelismo seguro |
| Estados e riscos | Falhas, extremos, acessibilidade e segurança aplicáveis |
| Critério de pronto | Condições observáveis |
| Prova | Comando, cenário, captura ou inspeção |
| Estado | Estado atual e limitação |

Uma fatia vertical atravessa somente as camadas necessárias ao resultado. Não criar tarefas isoladas de “HTML”, “CSS”, “testes”, “segurança” ou “polimento” sem comportamento e consumidor.

Aplicar:

1. teste de remoção: sem a tarefa, qual requisito fica sem cobertura?
2. teste de falsificação: como ela pode parecer pronta e falhar no critério?
3. teste de consumidor: qual fluxo usa a fundação criada?

## Checkpoint

Ao pausar ou concluir uma fase, entregar:

```markdown
## Checkpoint da feature

- Feature:
- Objetivo:
- Escopo/autorização:
- Fase atual:
- Fases: executar / reusar / atualizar / não aplicável
- Saídas concluídas:
- Decisões e pressupostos:
- Bloqueios e condição de desbloqueio:
- Artefatos e estado:
- Código/commit de referência:
- Validações:
- Dependentes a revalidar:
- Próxima ação segura:
```

Se não houver persistência autorizada, manter o checkpoint na resposta e deixar explícita essa limitação.

## Falhas e recuperação

| Falha | Conduta |
|---|---|
| Artefato contraditório | Preservar alternativas, definir autoridade e bloquear só o dependente |
| Artefato desatualizado | Marcar `revalidar`; não atualizar silenciosamente |
| Skill especializada indisponível | Parar a fase e indicar contrato ausente; não improvisar versão reduzida |
| Stack de tokens incerta | Investigar fonte/consumidores ou pedir decisão; não criar formato paralelo |
| Implementação diverge do plano | Determinar se o plano foi superado ou o código desviou antes de editar |
| Validação de tarefa falha | Marcar `falhou` e voltar à hipótese; não empilhar remendos |
| Runtime indisponível | Reduzir nível de evidência e registrar limitação |
| Mudança de escopo | Reclassificar fases e pedir aprovação quando material |
| Conflito com trabalho preexistente | Preservar mudanças e pausar somente a área em colisão |
| Usuário pausa | Emitir checkpoint sem inventar conclusão |
