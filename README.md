# Anti-AI Craft

Plugin pessoal e local para conduzir design, programação, auditoria, remediação e segurança com contexto e evidência. “Anti-AI” descreve um workflow de qualidade; o plugin não detecta, classifica nem atribui autoria.

## Limites

- Skill-only: não inclui apps, MCP, hooks, scripts automáticos, telemetria ou acesso a serviços.
- As cinco skills exigem invocação explícita.
- Regras do projeto e requisitos funcionais/normativos prevalecem sobre heurísticas.
- Análise não autoriza edição; remediação exige achados aprovados.
- Nenhuma skill faz commit ou push sem autorização explícita.

## Skills

Os identificadores técnicos permanecem em inglês para não quebrar prompts existentes; nomes visíveis e descrições estão em português.

| Nome visível | Invocação | Finalidade | Edição |
|---|---|---|---|
| Design Anti-IA | `$anti-ai-design` | Pesquisar, planejar, revisar ou implementar interfaces contextuais, acessíveis e responsivas | somente quando autorizada |
| Código Anti-IA | `$anti-ai-code` | Produzir ou revisar código direto, coeso, verificável e sem prolixidade ou abstração especulativa | somente quando autorizada |
| Auditoria Anti-IA | `$anti-ai-audit` | Auditar interface e código por severidade | sempre somente leitura |
| Remediação Anti-IA | `$anti-ai-remediate` | Aplicar somente achados confirmados, aprovados e reproduzíveis | sim, no escopo aprovado |
| Segurança Anti-IA | `$anti-ai-security` | Analisar controles ausentes e corrigir riscos confirmados, incluindo autorização e limites de consumo | somente quando autorizada |

### Qual skill usar

| Se você precisa de… | Use |
|---|---|
| direção visual, UI, responsividade ou acessibilidade | `$anti-ai-design` |
| implementar ou revisar um módulo/diff delimitado | `$anti-ai-code` |
| varrer um escopo amplo sem alterar nada | `$anti-ai-audit` |
| corrigir IDs já confirmados e aprovados | `$anti-ai-remediate` |
| modelar ameaça, validar abuso ou corrigir um risco confirmado | `$anti-ai-security` |

Auditoria ampla de código deve usar `$anti-ai-audit`; segurança deve usar `$anti-ai-security`; correção de achados já numerados deve usar `$anti-ai-remediate`.

## Instalação local

O plugin fica em:

~~~text
$HOME/.agents/plugins/anti-ai-craft/
~~~

O marketplace pessoal fica em:

~~~text
$HOME/.agents/plugins/marketplace.json
~~~

Depois de validar o marketplace, instalar:

~~~text
codex plugin add anti-ai-craft@personal
~~~

Abrir uma nova tarefa após instalar ou atualizar para que a lista de skills seja recarregada.

## Seleção e invocação

Usar /skills, o seletor de skills ou menção explícita com dólar:

~~~text
$anti-ai-design revise esta interface antes de alterar o código

$anti-ai-code analise este módulo e corrija apenas problemas confirmados

$anti-ai-audit audite este repositório sem editar arquivos

$anti-ai-remediate aplique somente os achados que aprovei

$anti-ai-security analise e corrija somente riscos confirmados e autorizados
~~~

Não existe comando inventado como /anti-ai-craft/design.

## Privacidade

As skills contêm somente instruções e referências públicas. Não incluem código de projetos, caminhos pessoais, credenciais, prompts privados, histórico de conversa, screenshots ou conteúdo proprietário. Funcionam sem qualquer projeto de origem disponível.

## Atualização

1. Editar somente a origem local.
2. Validar as cinco skills e o plugin.
3. Atualizar a versão SemVer quando houver release local; durante iteração, usar o fluxo de cachebuster oficial.
4. Reinstalar pelo marketplace pessoal.
5. Abrir uma nova tarefa e repetir os testes de invocação.

## Desinstalação

1. Executar `codex plugin remove anti-ai-craft@personal`.
2. Remover somente a entrada anti-ai-craft do marketplace pessoal.
3. Remover a pasta local do plugin se não for mais necessária.
4. Reiniciar o Codex.

## Validação

- No Windows, validar cada pasta com `python -X utf8 quick_validate.py <pasta-da-skill>`.
- No Windows, validar o plugin com `python -X utf8 validate_plugin.py <pasta-do-plugin>`.
- Validar JSON, YAML, UTF-8, links relativos, arquivos vazios e placeholders.
- Confirmar allow_implicit_invocation: false nas cinco skills.
- Confirmar ausência de apps, MCP, hooks, scripts e dependências externas.
- Confirmar descoberta no marketplace pessoal e testar as cinco menções em uma nova tarefa.
