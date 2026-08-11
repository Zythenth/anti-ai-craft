(function () {
  "use strict";

  const fixture = {
    meta: {
      surfaceName: "Oficina de Tradução",
      projectName: "Projeto Aurora",
      batchName: "Lote de 28 de julho",
      fixtureLabel: "Dados de demonstração",
      referenceDate: "28 de julho de 2026",
      referenceTime: "09:14",
      viewport: { width: 1280, height: 800, zoom: 1 },
      pipeline: "traduzir.sh · perfil padrão",
      executionModel: "Cada chamada é isolada e recebe contexto somente do workspace.",
      simulationNotice: "As ações desta tela são simuladas e não alteram arquivos."
    },
    summary: {
      chapters: 4,
      words: 15743,
      ready: 1,
      blocked: 1,
      reviewing: 1,
      queued: 1
    },
    filters: [
      { id: "all", label: "Todos", count: 4 },
      { id: "attention", label: "Precisa de atenção", count: 1 },
      { id: "progress", label: "Em andamento", count: 1 },
      { id: "ready", label: "Prontos", count: 1 }
    ],
    chapters: [
      {
        id: "ch114",
        title: "O preço do juramento",
        words: 3842,
        stage: "V3 pronta",
        state: "ready",
        filter: "ready",
        glossary: {
          label: "Atualizado",
          detail: "Nenhuma divergência encontrada."
        },
        summary: "V1 e V3 concluídas; o diff está pronto para aplicação.",
        expectedAt: "09:40",
        selectable: true,
        nextAction: { id: "apply-diff", label: "Aplicar diff" },
        inspectAction: { id: "compare", label: "Ver comparação" }
      },
      {
        id: "ch115",
        title: "A lâmina sob a neve",
        words: 4106,
        stage: "Diff bloqueado",
        state: "blocked",
        filter: "attention",
        glossary: {
          label: "2 decisões pendentes",
          detail: "Definir “véu de cinzas” e “marca do vigia”."
        },
        summary: "apply_diffs.py foi interrompido antes de alterar o capítulo.",
        expectedAt: "Aguardando decisão",
        selectable: false,
        incident: {
          title: "Dois termos ainda não têm decisão",
          effect: "Nenhum arquivo foi alterado.",
          terms: ["véu de cinzas", "marca do vigia"],
          recoveryAction: { id: "resolve-glossary", label: "Resolver glossário" },
          retryAction: { id: "retry", label: "Tentar novamente" },
          reportAction: { id: "view-report", label: "Ver relatório" }
        },
        nextAction: { id: "resolve-glossary", label: "Resolver glossário" },
        inspectAction: { id: "view-report", label: "Ver relatório" }
      },
      {
        id: "ch116",
        title: "O nome no portão",
        words: 3574,
        stage: "Revisão V1",
        state: "reviewing",
        filter: "progress",
        glossary: {
          label: "Atualizado",
          detail: "Nenhuma divergência encontrada."
        },
        summary: "O relatório está disponível; a V1 aguarda revisão humana.",
        expectedAt: "10:20",
        selectable: false,
        nextAction: { id: "open-review", label: "Abrir revisão" },
        inspectAction: { id: "view-report", label: "Ver relatório" }
      },
      {
        id: "ch117",
        title: "Cinzas no mapa",
        words: 4221,
        stage: "Na fila",
        state: "queued",
        filter: "queued",
        glossary: {
          label: "Atualizado",
          detail: "Contexto e glossário estão prontos."
        },
        summary: "O contexto foi montado; a geração da V1 ainda não começou.",
        expectedAt: "10:55",
        selectable: false,
        nextAction: { id: "generate-v1", label: "Gerar V1" },
        inspectAction: { id: "view-context", label: "Ver contexto" }
      }
    ]
  };

  function deepFreeze(value) {
    Object.freeze(value);
    Object.values(value).forEach(function (item) {
      if (item && typeof item === "object" && !Object.isFrozen(item)) {
        deepFreeze(item);
      }
    });
    return value;
  }

  Object.defineProperty(window, "DEMO_TRADUCAO", {
    value: deepFreeze(fixture),
    writable: false,
    configurable: false,
    enumerable: true
  });
})();
