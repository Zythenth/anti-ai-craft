# Template de revisão de design

Usar somente os campos aplicáveis. Entregar na resposta por padrão; salvar arquivo ou capturas permanentes apenas com autorização.

## Resumo

- Escopo:
- Mandato:
- Fontes de verdade:
- Estado do código/baseline:
- Perfil de evidência:
- Ambiente/runtime:
- Gate: passar / passar com ressalvas / bloquear / decisão humana
- Cobertura:
- Limitações:
- Risco residual:

## Perfis de evidência

| Perfil | Evidência | Alegações permitidas |
|---|---|---|
| Runtime completo | App executável e superfícies acessíveis | Resultado renderizado, interação e estados exercitados |
| Runtime parcial | Apenas parte alcançável | Somente superfícies e estados observados |
| Artefato visual | Screenshot ou vídeo fornecido | Aparência visível naquele quadro |
| Código apenas | Código/diff sem execução confiável | Estrutura, implementação potencial e risco técnico |

Não declarar qualidade visual renderizada com código apenas. Não inferir teclado, semântica, responsividade ou estados ausentes de uma captura isolada.

## Manifesto de evidência

| ID/arquivo | Origem | Superfície | Estado/dados | Dimensões/escala | Tema/input | Ambiente | Comparável a |
|---|---|---|---|---|---|---|---|

Captura prova sintoma, não necessariamente causa. Código pode explicar causa, mas não prova sozinho o resultado visual.

## Matriz de cobertura

| Superfície | Criticidade | Estados | Viewports | Tema/input | Evidência | Disposição |
|---|---|---|---|---|---|---|

Usar amostragem por risco, compartilhamento e criticidade. Registrar `coberto`, `parcial`, `bloqueado`, `não exercitado` ou `não aplicável`. Não exigir produto cartesiano de todas as combinações.

## Decisão preservada

| Elemento | Evidência | Por que funciona | Invariante |
|---|---|---|---|

Não preencher com elogio genérico. Se nada foi comprovado, omitir.

## Achados

### ADR-001 — Título

- Feature/fase:
- Artefato vigente:
- Área:
- Classificação:
- Severidade:
- Confiança:
- Prioridade:
- Gate:
- Superfície/rota:
- Estado/viewport/tema:
- Arquivo/linha/componente:
- Evidência visual:
- Evidência técnica:
- Controle ou causa:
- Ator e pré-condições:
- Contraprova mais forte:
- Lacuna de prova:
- Impacto:
- Justificativa:
- Regra ou contrato:
- Correção sugerida:
- Risco da correção:
- Critérios de aceitação:
- Validação necessária:

Repetir somente para achados sustentados. Preferência estética e decisão de produto ficam separadas.

## Coerência do fluxo

| ID relacionado | Decisão/requisito | Feature/fase | Artefato vigente | Implementação/runtime | Disposição | Evidência |
|---|---|---|---|---|---|---|

Classificar divergência como defeito, decisão posterior válida, artefato superado, ambiguidade ou lacuna de prova.

## Candidatos e falsos positivos

| Candidato | Evidência examinada | Disposição | Motivo |
|---|---|---|---|

## Falhas e áreas não testadas

Registrar runtime indisponível, rota bloqueada, credencial/dado ausente, captura falha, asset externo, comparação inválida, ambiente divergente e testes insuficientes. Falha operacional não é automaticamente defeito do produto.

## Plano opcional de aplicação

| ID | Resultado esperado | Dependências | Risco | Aceitação | Prova |
|---|---|---|---|---|---|

O plano não autoriza edição. Solicitar seleção explícita dos IDs e encaminhar preferencialmente para `$anti-ai-remediate`.
