# Resultado do agente 2 — método de ensino

## Escopo examinado

O agente analisou como a coleção externa ensina, roteia e aplica seus princípios,
incluindo o documento principal, os capítulos temáticos, instruções auxiliares,
scripts de manutenção e convenções de atualização.

## Padrões pedagógicos úteis

- começar por um problema reconhecível, não por uma lista indiscriminada;
- fornecer uma ação operacional após a explicação;
- manter capítulos temáticos curtos e carregados sob demanda;
- permitir consulta por unidade sem exigir leitura linear;
- usar evidência para transformar conselho abstrato em decisão verificável.

## Limitações encontradas

- o formato não informava com consistência quando uma recomendação deveria ser
  rejeitada;
- força normativa, convenção e opinião apareciam próximas demais;
- a presença de uma fonte podia ser confundida com prova de aplicabilidade local;
- o processo de atualização era maior do que o necessário para uma skill local;
- nenhum requisito de TDD existia no material de design, portanto essa obrigação
  não deveria ser inventada durante a integração;
- automatizar cópia ou atualização criaria dependência e risco desnecessários.

## Método melhorado incorporado

O novo método começa por tarefa, público, estágio, superfície e decisão. Em
seguida:

1. separa resultado da pessoa e resultado da organização;
2. seleciona somente o capítulo pertinente;
3. escolhe no máximo três IDs aplicáveis;
4. traduz cada ID em conteúdo, hierarquia, interação ou estado observável;
5. define indicador, métricas de proteção, contraprova e reversão;
6. verifica autonomia, acessibilidade, privacidade e segurança;
7. implementa somente quando houver autorização.

Esse método também define autoridade entre normas, contrato do projeto, decisão do
usuário, evidência, orientação, heurística e preferência. Uma recomendação externa
é tratada como hipótese até encontrar apoio no contexto real.

## Cobertura produzida pelo agente

- `ADO-001` a `ADO-010`: contexto e estratégia;
- `ADO-011` a `ADO-020`: posicionamento e promessa.

Na consolidação final, princípios semanticamente próximos foram reescritos para
cobrir fato versus hipótese, cadeia entre ação e valor, não escopo, categoria,
mecanismo de valor, ordem da mensagem, vocabulário, evidência, elegibilidade e
coerência entre canais.
