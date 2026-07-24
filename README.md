# Anti-AI Craft

Cinco skills para o Codex produzirem design, código, auditorias, correções e análises de segurança com mais intenção, evidência e controle.

“Anti-AI” não significa detectar autoria ou proibir o uso de IA. O objetivo é reduzir padrões recorrentes de trabalho automático mal conduzido: interfaces genéricas, abstrações desnecessárias, fallbacks silenciosos, mudanças sem evidência, correções fora do escopo e controles de segurança esquecidos.

## O que o plugin oferece

| Skill | Invocação | Quando usar |
|---|---|---|
| Design Anti-IA | `$anti-ai-design` | Planejar, revisar ou implementar interfaces contextuais, acessíveis e responsivas |
| Código Anti-IA | `$anti-ai-code` | Produzir ou revisar código direto, coeso, testável e sem complexidade especulativa |
| Auditoria Anti-IA | `$anti-ai-audit` | Examinar código e interface por severidade, sem alterar arquivos |
| Remediação Anti-IA | `$anti-ai-remediate` | Corrigir somente achados confirmados, reproduzíveis e aprovados |
| Segurança Anti-IA | `$anti-ai-security` | Modelar ameaças, analisar caminhos de abuso e corrigir riscos autorizados |

Os identificadores permanecem em inglês para serem estáveis em prompts, scripts e documentação. Os nomes e as descrições visíveis estão em português.

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

Abra uma nova tarefa no Codex após a instalação para carregar as cinco skills.

Para confirmar que o marketplace foi reconhecido:

```bash
codex plugin list --marketplace zythenth
```

## Como usar

Invoque uma skill pelo seletor de skills ou mencione seu identificador diretamente:

```text
$anti-ai-design revise esta interface antes de alterar o código

$anti-ai-code simplifique este módulo sem mudar o comportamento

$anti-ai-audit audite este repositório sem editar arquivos

$anti-ai-remediate aplique somente os achados que aprovei

$anti-ai-security procure caminhos de abuso e corrija apenas riscos autorizados
```

Não existe um comando como `/anti-ai-craft/design`. Cada skill é invocada pelo próprio identificador.

## Qual skill escolher

| Objetivo | Skill |
|---|---|
| Direção visual, UI, responsividade ou acessibilidade | `$anti-ai-design` |
| Implementação ou revisão de um módulo ou diff delimitado | `$anti-ai-code` |
| Inspeção ampla e somente leitura | `$anti-ai-audit` |
| Correção de achados já numerados e aprovados | `$anti-ai-remediate` |
| Threat model, autorização, isolamento, rate limits ou abuso | `$anti-ai-security` |

Para auditoria ampla, prefira `$anti-ai-audit`. Para riscos de segurança, use `$anti-ai-security`. Para aplicar correções já aprovadas, use `$anti-ai-remediate`.

## Princípios e limites

- As cinco skills exigem invocação explícita.
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
├── plugins/anti-ai-craft/
│   ├── .codex-plugin/plugin.json
│   └── skills/
└── README.md
```

Cada skill mantém seu contrato principal em `SKILL.md` e referências especializadas em sua própria pasta.

## Contribuições

Relatos de comportamento inesperado, sugestões e pull requests são bem-vindos. Ao propor uma mudança, preserve os identificadores públicos das skills, mantenha análise e edição como permissões distintas e inclua uma forma objetiva de verificar o resultado.
