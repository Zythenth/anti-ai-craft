# Baseline de acessibilidade

## Sumário

- [Autoridade](#autoridade)
- [Semântica e estrutura](#semântica-e-estrutura)
- [Teclado e foco](#teclado-e-foco)
- [Menus e overflow](#menus-e-overflow)
- [Modais](#modais)
- [Abas](#abas)
- [Formulários e erros](#formulários-e-erros)
- [Estados e mensagens](#estados-e-mensagens)
- [Contraste, cor e alvos](#contraste-cor-e-alvos)
- [Reflow, zoom e texto](#reflow-zoom-e-texto)
- [Movimento](#movimento)
- [Matriz manual mínima](#matriz-manual-mínima)

## Autoridade

Usar WCAG 2.2 A/AA aplicável como baseline normativo para web. Tratar WAI-ARIA APG, GOV.UK, Carbon, Material, Fluent, Apple HIG, Xbox XAG, MDN e NN/g como guidance ou heurística. Preferir HTML nativo. Testar padrões ARIA nas combinações reais de navegador e tecnologia assistiva.

## Semântica e estrutura

- Preservar ordem de leitura, DOM e foco.
- Usar landmarks, headings, listas, tabelas, links, buttons e campos conforme sua finalidade.
- Expor nome, role, value, state e relationships.
- Fazer o nome acessível conter o texto visível.
- Não comunicar informação apenas por cor, posição, forma ou movimento.

## Teclado e foco

- Tornar toda funcionalidade operável por teclado, sem timing específico.
- Evitar tabindex positivo.
- Manter foco visível, lógico e não totalmente encoberto.
- Não mover foco por atualização comum.
- Após remoção de um trigger, enviar foco ao próximo ponto lógico.
- Testar Tab, Shift+Tab, Enter, Space, setas, Home, End e Escape conforme o widget.

## Menus e overflow

- Usar button como trigger, com nome e estado expandido.
- Ao abrir, mover foco segundo o padrão escolhido.
- Navegar itens por setas; ativar por teclado; fechar com Escape.
- Devolver foco ao trigger ou contexto lógico.
- Manter alternativa de touch e voz; não depender de hover.
- Manter ações primárias/frequentes fora do overflow.

## Modais

- Fornecer título/nome e fechamento visível.
- Tornar o fundo realmente inerte.
- Definir foco inicial pela tarefa.
- Conter Tab e Shift+Tab.
- Fechar diálogo comum com Escape.
- Devolver foco ao invocador ou próximo ponto lógico.
- Preferir ação menos destrutiva como foco inicial em confirmação irreversível.

## Abas

- Relacionar tab e tabpanel.
- Manter apenas a tab ativa na sequência de Tab.
- Usar setas para navegação interna.
- Usar ativação automática somente sem latência perceptível; caso contrário, ativação manual.
- Não quebrar tabs em múltiplas linhas sem padrão acessível.

## Formulários e erros

- Fornecer label persistente e associada.
- Não usar placeholder como label.
- Associar hint e erro ao campo.
- Identificar o erro em texto e sugerir correção quando conhecida.
- Preservar dados e permitir colar/gerenciador de senhas.
- Em formulários extensos, combinar mensagens inline e resumo navegável.
- Em operações relevantes, oferecer reversão, revisão ou confirmação apropriada.

## Estados e mensagens

- Expor selected, checked, expanded, disabled, read-only, busy e invalid programaticamente.
- Explicar indisponibilidade quando necessário; disabled não é explicação.
- Anunciar status sem mover foco.
- Reservar alert/assertive para urgência real.
- Não anunciar página inteira ou histórico como atualização.

## Contraste, cor e alvos

- Texto normal: 4,5:1; texto grande: 3:1.
- Componentes e indicadores essenciais: 3:1.
- Foco visível precisa sobreviver a temas e forced colors.
- Alvo mínimo WCAG 2.2 AA: 24×24 CSS px ou exceção normativa.
- Usar meta maior da plataforma/produto para ações frequentes e mobile.
- Não converter dp, pt e CSS px como equivalentes.

## Reflow, zoom e texto

- Testar reflow em 320 CSS px sem rolagem bidimensional, salvo conteúdo essencialmente 2D.
- Testar texto a 200% e zoom a 400% quando aplicável.
- Testar override de text spacing, strings longas, tradução e RTL.
- Permitir overflow local para tabelas/mapas genuínos, preservando headers e contexto.

## Movimento

- Permitir pausar, parar ou ocultar conteúdo automático quando WCAG exigir.
- Não exceder limites de flashes.
- Respeitar prefers-reduced-motion e preferências nativas.
- Substituir movimento intenso por alternativa estática ou discreta.
- Não usar movimento como único feedback.

## Matriz manual mínima

1. Percorrer fluxo principal e recuperação somente por teclado.
2. Abrir/fechar menu, modal, tabs e drawer, registrando foco antes/depois.
3. Verificar leitor de tela em carga e atualização.
4. Testar viewport estreito, intermediário e amplo.
5. Testar 320 CSS px, 200%, 400%, text spacing e strings longas.
6. Verificar contraste, forced colors, light/dark e aumento de contraste.
7. Testar touch e alvos.
8. Testar reduced motion.
9. Exercitar vazio, loading, erro, offline, permissão e dados extremos.
10. Rodar automação acessível, sem tratá-la como substituto dos passes manuais.
