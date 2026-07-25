# Anti-AI Craft

Seis skills para o Codex conduzirem fluxos de design, criarem interfaces, produzirem código, auditarem, corrigirem e analisarem segurança com mais intenção, evidência e controle.

“Anti-AI” não significa detectar autoria ou proibir o uso de IA. O objetivo é reduzir padrões recorrentes de trabalho automático mal conduzido: interfaces genéricas, abstrações desnecessárias, fallbacks silenciosos, mudanças sem evidência, correções fora do escopo e controles de segurança esquecidos.

## O que o plugin oferece

| Skill | Identificador | Ativação | Quando usar |
|---|---|---|---|
| Fluxo de Design Anti-IA | `$anti-ai-design-flow` | Manual | Conduzir uma feature por três ou mais fases, com checkpoints e retomada |
| Design Anti-IA | `$anti-ai-design` | Automática ou manual | Planejar, revisar ou implementar interfaces contextuais, acessíveis, responsivas e orientadas a resultados |
| Código Anti-IA | `$anti-ai-code` | Automática ou manual | Produzir ou revisar código direto, coeso, testável e sem complexidade especulativa |
| Auditoria Anti-IA | `$anti-ai-audit` | Manual | Examinar código e interface por severidade, sem alterar arquivos |
| Remediação Anti-IA | `$anti-ai-remediate` | Manual | Corrigir somente achados confirmados, reproduzíveis e aprovados |
| Segurança Anti-IA | `$anti-ai-security` | Automática ou manual | Modelar ameaças, analisar caminhos de abuso e corrigir riscos autorizados |

Os identificadores permanecem em inglês para serem estáveis em prompts, scripts e documentação. Os nomes e as descrições visíveis estão em português. Design, Código e Segurança podem ser selecionadas automaticamente quando o pedido corresponde aos seus gatilhos; todas também aceitam invocação manual. Fluxo, Auditoria e Remediação exigem o identificador explícito. Pedidos de auditoria ampla ou de aplicação de achados numerados continuam exigindo `$anti-ai-audit` ou `$anti-ai-remediate`.

## Instalação

Pré-requisitos:

- Codex CLI com suporte ao comando `codex plugin`;
- Git disponível no sistema.

Adicione este repositório como um marketplace:

```bash
codex plugin marketplace add Zythenth/anti-ai-craft --ref main
```

Instale o plugin:

```bash
codex plugin add anti-ai-craft@zythenth
```

Abra uma nova tarefa no Codex após a instalação para carregar as seis skills.

Para confirmar que o marketplace foi reconhecido:

```bash
codex plugin list --marketplace zythenth
```

## Como usar

Invoque uma skill pelo seletor de skills ou mencione seu identificador diretamente:

```text
$anti-ai-design-flow conduza esta feature do briefing à revisão e mantenha checkpoints retomáveis

$anti-ai-design revise esta interface antes de alterar o código

$anti-ai-code simplifique este módulo sem mudar o comportamento

$anti-ai-audit audite este repositório sem editar arquivos

$anti-ai-remediate aplique somente os achados que aprovei

$anti-ai-security procure caminhos de abuso e corrija apenas riscos autorizados
```

Não existe um comando como `/anti-ai-craft/design`. Cada skill é invocada pelo próprio identificador.

## Fluxo completo

Use `$anti-ai-design-flow` somente para uma jornada multifase: descoberta e brief, arquitetura da informação, sistema visual/tokens, plano em fatias verificáveis, gate de segurança quando aplicável, implementação autorizada, revisão e remediação opcional.

O fluxo:

- verifica o projeto antes de perguntar;
- reutiliza ou pula fases somente quando a saída existente está atual e comprovada;
- não transforma planejamento em autorização de edição;
- mantém checkpoint de decisões, artefatos, bloqueios e próxima ação;
- invalida somente dependentes de uma decisão alterada;
- preserva auditoria somente leitura e remediação por IDs aprovados.

Para uma tela, componente, screenshot ou ajuste visual delimitado, continue usando `$anti-ai-design`.

## Design orientado a resultados

`$anti-ai-design` inclui um catálogo autoral de 101 princípios para interfaces de
produto. Eles estão organizados em dez áreas: contexto e estratégia; posicionamento
e promessa; aquisição; onboarding e ativação; estrutura e funcionalidades; pricing
e monetização; retenção e offboarding; arquitetura ética de escolha; métricas e
experimentação; diferenciação e entrega com IA.

A skill carrega somente as áreas relevantes e seleciona no máximo três princípios
por decisão. Cada princípio declara quando se aplica, qual decisão orienta, que
prova pode sustentá-lo e que abuso deve ser evitado. Métricas comerciais são
tratadas como hipóteses subordinadas ao resultado da pessoa: o catálogo não
autoriza urgência falsa, prova social fabricada, cancelamento difícil, coleta
desnecessária ou qualquer outro padrão manipulativo.

## Qual skill escolher

| Objetivo | Skill |
|---|---|
| Jornada completa, multifase e retomável | `$anti-ai-design-flow` |
| Direção visual, UI, responsividade ou acessibilidade | `$anti-ai-design` |
| Implementação ou revisão de um módulo ou diff delimitado | `$anti-ai-code` |
| Inspeção ampla e somente leitura | `$anti-ai-audit` |
| Correção de achados já numerados e aprovados | `$anti-ai-remediate` |
| Threat model, autorização, isolamento, rate limits ou abuso | `$anti-ai-security` |

Para auditoria ampla, prefira `$anti-ai-audit`. Para riscos de segurança, use `$anti-ai-security`. Para aplicar correções já aprovadas, use `$anti-ai-remediate`.

## Princípios e limites

- Design, Código e Segurança podem ser selecionadas automaticamente pelo Codex conforme o pedido.
- Fluxo, Auditoria e Remediação exigem invocação explícita.
- Ativação automática não amplia autorização de leitura, edição ou ação externa.
- Regras do projeto e requisitos funcionais ou normativos prevalecem sobre heurísticas.
- Análise não autoriza edição; cada skill preserva o escopo concedido pelo usuário.
- Auditoria é sempre somente leitura.
- Remediação exige achados confirmados e aprovados.
- Nenhuma skill autoriza commit, push ou outra ação externa por conta própria.
- O pacote não inclui apps, MCP, hooks, executáveis, telemetria ou serviços externos.

## Atualização

Atualize o snapshot do marketplace e reinstale o plugin:

```bash
codex plugin marketplace upgrade zythenth
codex plugin add anti-ai-craft@zythenth
```

Depois, abra uma nova tarefa para garantir que o Codex carregue a versão atualizada.

O upgrade do marketplace pode apontar para uma revisão nova do plugin. O caminho
acima continua sendo o mais simples; em ambientes sensíveis, revise as notas da
versão e o diff antes de atualizar. O branch padrão não é uma referência imutável.

## Desinstalação

Remova o plugin:

```bash
codex plugin remove anti-ai-craft@zythenth
```

Se você não utiliza nenhum outro plugin desse marketplace, também pode removê-lo:

```bash
codex plugin marketplace remove zythenth
```

## Estrutura do repositório

```text
.
├── .agents/plugins/marketplace.json
├── docs/analises/
├── plugins/anti-ai-craft/
│   ├── .codex-plugin/plugin.json
│   └── skills/
└── README.md
```

Cada skill mantém seu contrato principal em `SKILL.md` e referências especializadas em sua própria pasta.
Os relatórios em `docs/analises/` registram a avaliação técnica usada para evoluir
o plugin e a revisão final de cobertura.

## Contribuições

Relatos de comportamento inesperado, sugestões e pull requests são bem-vindos. Ao propor uma mudança, preserve os identificadores públicos das skills, mantenha análise e edição como permissões distintas e inclua uma forma objetiva de verificar o resultado.
