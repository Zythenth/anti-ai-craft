# Workflow de remediação de segurança

## 1. Fixar evidência e escopo

Registrar:

- ativo e boundary;
- ator e pré-condição;
- caminho controlável;
- controle atual e bypass;
- impacto;
- evidência reproduzível segura;
- arquivos/configurações autorizados;
- teste que deve falhar antes da correção.

Se a proteção puder estar em gateway, WAF, IAM, RLS, service mesh ou plataforma externa não fornecida, não afirmar ausência. Pedir configuração ou relatar `depende de infraestrutura`.

## 2. Escolher o boundary correto

- Autorização: servidor e acesso ao recurso, não apenas rota/UI.
- Isolamento: query/policy/storage/cache/evento, não filtro posterior.
- Validação: antes do sink ou mudança de confiança.
- Rate limit: próximo da superfície de abuso, com chave e storage coerentes com a implantação.
- Segredo: secret manager/configuração segura, não ofuscação.
- Estado: transação, constraint, idempotência ou máquina de estados, não flag visual.

Se um segredo já foi exposto, removê-lo do código impede novas exposições, mas não invalida cópias existentes. Registrar alcance e janela, bloquear novo uso quando autorizado e exigir revogação ou rotação confirmada. Não executar rotação real, alteração de produção ou revogação sem autorização específica; escalar como risco residual até a confirmação.

## 3. Corrigir rate limiting e consumo

Antes de implementar, definir:

1. ação protegida e custo;
2. ator/chave do limite;
3. burst, janela e taxa sustentada;
4. comportamento em múltiplas instâncias;
5. resposta e retry;
6. observabilidade;
7. impacto em NAT, proxies, acessibilidade e usuários legítimos;
8. limites complementares de payload, batch, paginação, timeout, concorrência, fila e gasto.

Preferir mecanismo já adotado no gateway/framework. Um contador em memória local não protege implantação com múltiplas instâncias e reinicia com o processo. Não copiar `100 requests/minute` como valor universal. Se produto/capacidade não definir limiar, implementar estrutura configurável somente quando a necessidade for real e registrar o valor como decisão pendente.

Testar pelo menos: abaixo do limite, no limite, acima do limite, recuperação após janela, chaves distintas, concorrência e bypass por header/endpoint alternativo.

## 4. Preservar função e usabilidade

- Não remover código funcional apenas para silenciar scanner.
- Não bloquear todo usuário para impedir abuso de poucos.
- Não transformar falha de autorização em vazamento por mensagens diferentes.
- Não degradar criptografia, validação ou teste para recuperar compatibilidade.
- Não introduzir dependência sem verificar existência, versão, manutenção e arquitetura local.

## 5. Validar em camadas

1. teste negativo específico;
2. teste positivo que preserva uso legítimo;
3. regressão da área;
4. análise estática/configuração já adotada pelo projeto;
5. revisão manual do diff e do caminho de dados;
6. verificação de logs, erros e telemetria;
7. suíte proporcional ao impacto.

Atualizar o modelo de ameaça se a correção alterar arquitetura, fluxo, ativo, ator, fronteira, integração ou ambiente. Para controles de consumo compartilhado, validar também noisy neighbor e uso legítimo concorrente.

Scanner limpo não encerra o trabalho. Resultado de scanner precisa de validação manual; ausência de alerta não cobre lógica de negócio, autorização contextual, tenant, rate limit externo ou concorrência.

## 6. Relatar

Por achado, informar:

- causa e risco;
- controle implementado;
- arquivo/configuração;
- teste antes/depois;
- comandos e resultados;
- comportamento legítimo preservado;
- limitações e dependências externas;
- risco residual e monitoramento;
- aprovação adicional necessária.
