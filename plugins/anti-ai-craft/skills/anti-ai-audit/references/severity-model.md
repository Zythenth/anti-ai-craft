# Modelo de severidade e confiança

## Severidade

### Crítica

Exploração provável com impacto grave; perda/corrupção ampla; exposição sensível; controle crítico ausente; uso essencial bloqueado para muitos usuários. Exigir caminho demonstrável, não hipótese abstrata.

### Alta

Função principal quebrada, autorização incorreta, regressão de acessibilidade importante, mutação/rollback perigoso, ação crítica oculta ou arquitetura que causa falha concreta.

### Média

Comportamento secundário incorreto, manutenção materialmente frágil, teste com falsa confiança, responsividade/estado incompleto ou padrão genérico que prejudica tarefa/hierarquia.

### Baixa

Problema localizado, risco limitado, inconsistência menor ou refinamento com impacto observável pequeno.

### Observação

Decisão pendente, oportunidade, preferência, dívida sem falha atual ou informação insuficiente. Não apresentar como defeito.

## Confiança

- **Alta:** reproduzido; contrato claro; caminho e impacto demonstrados.
- **Média:** caminho plausível e evidência forte, mas ambiente/estado impede reprodução completa.
- **Baixa:** heuristicamente suspeito; falta condição material. Manter fora dos achados principais ou como pergunta.

## Prioridade de remediação

Prioridade não é sinônimo de severidade. Considerar dependências, recorrência, custo de oportunidade, disponibilidade de correção segura, exigência normativa e janela operacional. Um achado de alta severidade pode aguardar uma decisão crítica de produto; um achado médio recorrente pode ser corrigido primeiro por reduzir vários riscos.

## Classificação do achado

- defeito funcional confirmado;
- vulnerabilidade;
- acessibilidade;
- code smell tradicional;
- padrão genérico contextual;
- heurística comunitária;
- preferência;
- decisão do produto;
- evidência insuficiente ou falso positivo rejeitado.

## Regras de calibragem

- Impacto sem alcançabilidade não define severidade.
- Complexidade estética não aumenta severidade.
- Um smell não vira bug sem comportamento.
- Vulnerabilidade exige boundary, controle ausente e impacto.
- Falha WCAG aplicável pode bloquear entrega mesmo sem crash.
- Várias baixas repetidas podem formar problema sistêmico; registrar relação sem inflar cada item.
- Confiança e severidade são eixos separados.
- Calibrar impacto máximo realista, alcançabilidade/pré-condições, probabilidade, alcance, sensibilidade e reversibilidade.
- Reportar severidade, confiança e prioridade em campos separados.
