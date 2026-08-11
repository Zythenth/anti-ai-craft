(function () {
  "use strict";

  const fixture = {
    meta: {
      surfaceName: "Translation Workshop",
      projectName: "Project Aurora",
      batchName: "July 28 Batch",
      fixtureLabel: "Demonstration data",
      referenceDate: "July 28, 2026",
      referenceTime: "09:14",
      viewport: { width: 1280, height: 800, zoom: 1 },
      pipeline: "traduzir.sh · default profile",
      executionModel: "Each call is isolated and receives context only from the workspace.",
      simulationNotice: "Actions on this screen are simulated and do not change files."
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
      { id: "all", label: "All", count: 4 },
      { id: "attention", label: "Needs attention", count: 1 },
      { id: "progress", label: "In progress", count: 1 },
      { id: "ready", label: "Ready", count: 1 }
    ],
    chapters: [
      {
        id: "ch114",
        title: "The Price of the Oath",
        words: 3842,
        stage: "V3 ready",
        state: "ready",
        filter: "ready",
        glossary: {
          label: "Updated",
          detail: "No divergence found."
        },
        summary: "V1 and V3 are complete; the diff is ready to apply.",
        expectedAt: "09:40",
        selectable: true,
        nextAction: { id: "apply-diff", label: "Apply diff" },
        inspectAction: { id: "compare", label: "View comparison" }
      },
      {
        id: "ch115",
        title: "The Blade Beneath the Snow",
        words: 4106,
        stage: "Diff blocked",
        state: "blocked",
        filter: "attention",
        glossary: {
          label: "2 pending decisions",
          detail: "Define “veil of ashes” and “watcher's mark”."
        },
        summary: "apply_diffs.py stopped before changing the chapter.",
        expectedAt: "Awaiting decision",
        selectable: false,
        incident: {
          title: "Two terms still need a decision",
          effect: "No files were changed.",
          terms: ["veil of ashes", "watcher's mark"],
          recoveryAction: { id: "resolve-glossary", label: "Resolve glossary" },
          retryAction: { id: "retry", label: "Try again" },
          reportAction: { id: "view-report", label: "View report" }
        },
        nextAction: { id: "resolve-glossary", label: "Resolve glossary" },
        inspectAction: { id: "view-report", label: "View report" }
      },
      {
        id: "ch116",
        title: "The Name at the Gate",
        words: 3574,
        stage: "V1 review",
        state: "reviewing",
        filter: "progress",
        glossary: {
          label: "Updated",
          detail: "No divergence found."
        },
        summary: "The report is available; V1 is awaiting human review.",
        expectedAt: "10:20",
        selectable: false,
        nextAction: { id: "open-review", label: "Open review" },
        inspectAction: { id: "view-report", label: "View report" }
      },
      {
        id: "ch117",
        title: "Ashes on the Map",
        words: 4221,
        stage: "Queued",
        state: "queued",
        filter: "queued",
        glossary: {
          label: "Updated",
          detail: "Context and glossary are ready."
        },
        summary: "The context has been assembled; V1 generation has not started.",
        expectedAt: "10:55",
        selectable: false,
        nextAction: { id: "generate-v1", label: "Generate V1" },
        inspectAction: { id: "view-context", label: "View context" }
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
