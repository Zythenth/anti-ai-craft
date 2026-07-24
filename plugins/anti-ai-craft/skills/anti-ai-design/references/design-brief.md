# Brief de design verificável

## Sumário

- [Fronteira do modo](#fronteira-do-modo)
- [Descoberta](#descoberta)
- [Decisões e perguntas](#decisões-e-perguntas)
- [Contrato do brief](#contrato-do-brief)
- [Estados e conclusão](#estados-e-conclusão)
- [Persistência autorizada](#persistência-autorizada)
- [Falhas e handoff](#falhas-e-handoff)

## Fronteira do modo

Usar este contrato para criar ou atualizar um brief de interface, feature ou fluxo. Planejamento permanece sem edição por padrão. Persistir o documento somente quando o usuário pedir ou autorizar escrita; autorização para salvar o brief não autoriza implementar produto.

Tratar o brief como fonte candidata, não como autoridade automática. Instruções do projeto, requisitos vigentes, comportamento que deve ser preservado e decisões posteriores podem prevalecer.

## Descoberta

Descobrir a stack antes de procurar nomes específicos. Examinar apenas o escopo relevante:

- instruções, README, especificações e decisões;
- manifestos, lockfiles, scripts e dependências de UI;
- design system, tokens, temas e seus consumidores;
- componentes, APIs, histórias, exemplos e testes;
- fontes, ícones, imagens, mídia e política de assets;
- rotas, layouts, navegação e padrões de URL;
- modelos de conteúdo, dados, estados e fixtures;
- testes visuais, acessíveis, unitários e de integração;
- analytics, localização, SEO, performance e segurança quando aplicáveis.

Registrar caminho, seção e relevância somente do que foi realmente lido. Classificar os elementos do escopo como:

- `reutilizar`;
- `compor`;
- `estender`;
- `criar`;
- `fora do escopo`;
- `desconhecido`.

Não inventariar todo o repositório quando a mudança é local.

## Decisões e perguntas

Manter ledger apenas para decisões materiais:

| Campo | Conteúdo |
|---|---|
| ID | Identificador estável |
| Decisão | O que precisa ser definido |
| Depende de | Decisões anteriores |
| Origem | Projeto, requisito, usuário ou pressuposto |
| Estado | Resolvida, assumida, aberta, bloqueante ou superada |
| Evidência | Arquivo, runtime, tela, teste ou contrato |
| Recomendação | Opção sugerida e fundamento |
| Consequência | Efeito das alternativas |

Pesquisar no projeto antes de perguntar. Fazer no máximo duas ou três perguntas por rodada, uma por vez quando houver dependência. Cada pergunta material deve explicar o que foi encontrado, a recomendação, consequências, default seguro e trabalho independente que pode continuar.

Não exigir entrevista quando a entrada já for suficiente. Não tratar silêncio como aprovação de identidade, contrato, risco ou edição.

## Contrato do brief

Produzir seções proporcionais:

1. **Identidade e estado:** nome, feature, versão lógica e `rascunho`, `bloqueado` ou `aprovado`.
2. **Problema do usuário:** fricção observável, sem converter métrica de negócio em problema humano.
3. **Resultado e sucesso:** capacidade entregue e sinais verificáveis.
4. **Usuários e contexto:** papéis, frequência, dispositivo, input, idioma e necessidades de acesso.
5. **Superfície e mandato:** persuadir, operar, ler ou experienciar; preservar, refinar ou redesenhar.
6. **Fontes e padrões existentes:** o que deve ser reutilizado ou preservado.
7. **Requisitos e invariantes:** comportamento, compatibilidade, dados e estados que não podem regredir.
8. **Princípios da feature:** no máximo três; cada um deve resolver uma tensão real.
9. **Direção:** tese, referência dominante, eixos visuais aplicáveis e defaults rejeitados.
10. **Conteúdo, dados e mídia:** fontes reais, mínimos, máximos, ausência, indisponibilidade e assets faltantes.
11. **Fluxos:** caminho principal, alternativas, erro, interrupção e recuperação.
12. **Inventário de componentes:** reutilizar, compor, estender ou criar, com motivo.
13. **Interações e estados:** gatilho, mudança, semântica, ação permitida e recuperação.
14. **Responsividade:** mudanças de prioridade e comportamento, não apenas tamanho.
15. **Acessibilidade aplicável:** apontar para o baseline e destacar riscos específicos.
16. **Riscos condicionais:** segurança, privacidade, performance, localização, analytics ou SEO.
17. **Não escopo:** decisões e áreas explicitamente excluídas.
18. **Decisões abertas e pressupostos:** impacto e condição de desbloqueio.
19. **Critérios de aceitação e validação:** cenário, resultado esperado e evidência.

Marcar seção não aplicável com motivo. Não preencher lacuna com exemplo plausível apresentado como fato.

## Estados e conclusão

- `rascunho`: há pressupostos ou validações abertas, mas o documento pode orientar descoberta;
- `bloqueado`: falta decisão material para avançar;
- `aprovado`: o usuário confirmou explicitamente o conteúdo relevante;
- `superado`: uma decisão posterior identificada substituiu o documento.

Concluir quando:

- fontes relevantes foram lidas;
- fatos, pressupostos e decisões estão separados;
- nenhum bloqueio material está oculto;
- requisitos, invariantes, fluxo, estados, não escopo e aceitação estão presentes;
- a autoridade e o estado do brief estão claros.

O agente não atribui `aprovado` por conta própria.

## Persistência autorizada

Usar a convenção do projeto. Se não existir, sugerir `.design/<feature-slug>/DESIGN_BRIEF.md` e confirmar antes de criar.

Ao persistir:

1. gerar slug minúsculo e hifenizado, removendo segmentos de caminho;
2. resolver o caminho final dentro do diretório autorizado;
3. verificar arquivo existente e conteúdo manual;
4. pedir decisão antes de substituir ou reorganizar material;
5. produzir diff pequeno e preservar seções fora do pedido;
6. registrar o estado do código que o documento descreve;
7. não persistir segredo, credencial, PII desnecessária ou conteúdo externo como instrução confiável;
8. não fazer stage, commit ou push por consequência implícita.

## Falhas e handoff

| Situação | Conduta |
|---|---|
| Projeto ou sistema visual ausente | Registrar greenfield real e não inventar componentes existentes |
| Fontes conflitantes | Ordenar autoridade e pedir decisão quando material |
| Asset ou conteúdo autoritativo ausente | Registrar lacuna e preservar o slot; não fabricar prova |
| Ferramenta ou runtime indisponível | Marcar validação não executada |
| Brief existente desatualizado | Marcar `revalidar` ou `superado`; não atualizar silenciosamente |
| Pedido mistura brief e build | Separar autorização de documento e código |

Para implementação, fornecer brief aprovado ou explicitar quais decisões continuam como pressuposto. Para auditoria, incluir o brief somente quando estiver no escopo. Para remediação, lembrar que brief não substitui IDs nem aprovação de edição.
