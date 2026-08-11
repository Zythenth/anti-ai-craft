(function () {
  "use strict";

  const fixture = window.DEMO_TRADUCAO;

  if (!fixture) {
    document.body.innerHTML = "<main><h1>Não foi possível carregar os dados de demonstração.</h1></main>";
    throw new Error("window.DEMO_TRADUCAO não foi carregado");
  }

  const ui = {
    filter: "all",
    query: "",
    selected: new Set(),
    glossaryConfirmed: false,
    pendingConfirmation: null,
  };

  const elements = {
    rows: document.querySelector("#chapter-rows"),
    search: document.querySelector("#chapter-search"),
    clearSearch: document.querySelector("#clear-search"),
    recoverResults: document.querySelector("#recover-results"),
    filters: document.querySelector("#filters"),
    resultSummary: document.querySelector("#result-summary"),
    emptyState: document.querySelector("#empty-state"),
    applySelection: document.querySelector("#apply-selection"),
    actionLog: document.querySelector("#action-log"),
    incident: document.querySelector("#incident-spotlight"),
    chapterDialog: document.querySelector("#chapter-dialog"),
    chapterDialogTitle: document.querySelector("#chapter-dialog-title"),
    chapterDialogBody: document.querySelector("#chapter-dialog-body"),
    chapterDialogActions: document.querySelector("#chapter-dialog-actions"),
    confirmDialog: document.querySelector("#confirm-dialog"),
    confirmDialogTitle: document.querySelector("#confirm-dialog-title"),
    confirmDialogCopy: document.querySelector("#confirm-dialog-copy"),
    confirmAction: document.querySelector("#confirm-action"),
    toast: document.querySelector("#toast"),
    toastMessage: document.querySelector("#toast-message"),
  };

  let toastTimer;

  function setText(selector, value) {
    document.querySelector(selector).textContent = value;
  }

  function normalize(value) {
    return value
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLocaleLowerCase("pt-BR")
      .trim();
  }

  function formatWords(value) {
    return new Intl.NumberFormat("pt-BR").format(value);
  }

  function button(label, className, attributes) {
    const control = document.createElement("button");
    control.type = "button";
    control.className = className;
    control.textContent = label;
    Object.entries(attributes || {}).forEach(([name, value]) => {
      if (value !== undefined) control.setAttribute(name, value);
    });
    return control;
  }

  function cell(label, primary, secondary, className) {
    const tableCell = document.createElement("td");
    tableCell.dataset.label = label;
    if (className) tableCell.className = className;

    const primaryText = document.createElement("span");
    primaryText.className = "cell-primary";
    primaryText.textContent = primary;
    tableCell.append(primaryText);

    if (secondary) {
      const secondaryText = document.createElement("span");
      secondaryText.className = "cell-secondary";
      secondaryText.textContent = secondary;
      tableCell.append(secondaryText);
    }

    return tableCell;
  }

  function initializeMeta() {
    const { meta, summary } = fixture;
    setText("#surface-name", meta.surfaceName);
    setText("#project-name", meta.projectName);
    setText("#batch-name", meta.batchName);
    setText("#fixture-label", meta.fixtureLabel);
    setText("#reference-time", `${meta.referenceDate} · ${meta.referenceTime}`);
    setText("#summary-date", `Referência: ${meta.referenceTime}`);
    setText("#pipeline-name", meta.pipeline);
    setText("#execution-model", meta.executionModel);
    setText("#simulation-notice", meta.simulationNotice);

    const metrics = [
      { label: "Capítulos", value: summary.chapters, tone: "" },
      { label: "Palavras", value: formatWords(summary.words), tone: "" },
      { label: "Pronto", value: summary.ready, tone: "ready" },
      { label: "Bloqueado", value: summary.blocked, tone: "blocked" },
      { label: "Em revisão", value: summary.reviewing, tone: "reviewing" },
      { label: "Na fila", value: summary.queued, tone: "queued" },
    ];

    elements.summaryMetrics = document.querySelector("#summary-metrics");
    elements.summaryMetrics.replaceChildren(
      ...metrics.map((metric) => {
        const item = document.createElement("div");
        item.className = `metric${metric.tone ? ` metric--${metric.tone}` : ""}`;
        const term = document.createElement("dt");
        term.textContent = metric.label;
        const description = document.createElement("dd");
        description.textContent = metric.value;
        item.append(term, description);
        return item;
      }),
    );
  }

  function initializeFilters() {
    elements.filters.replaceChildren(
      ...fixture.filters.map((filter) => {
        const control = button(filter.label, "filter-button", {
          "data-filter": filter.id,
          "aria-pressed": String(filter.id === "all"),
          "aria-label": `${filter.label}, ${filter.count} capítulo${filter.count === 1 ? "" : "s"}`,
        });
        if (filter.id === "all") control.classList.add("is-active");
        const count = document.createElement("span");
        count.setAttribute("aria-hidden", "true");
        count.textContent = filter.count;
        control.append(count);
        return control;
      }),
    );
  }

  function initializeIncident() {
    const chapter = fixture.chapters.find((item) => item.incident);
    if (!chapter) {
      elements.incident.hidden = true;
      return;
    }

    const headingGroup = document.createElement("div");
    const heading = document.createElement("h2");
    heading.id = "incident-title";
    heading.textContent = `${chapter.id} · ${chapter.incident.title}`;
    const effect = document.createElement("p");
    effect.textContent = `${chapter.summary} ${chapter.incident.effect}`;
    headingGroup.append(heading, effect);

    const paths = document.createElement("div");
    paths.className = "incident__paths";
    paths.textContent = `${chapter.glossary.detail} Caminhos: ${chapter.incident.recoveryAction.label}, ${chapter.incident.retryAction.label} e ${chapter.incident.reportAction.label}.`;

    const actions = document.createElement("div");
    actions.className = "incident__actions";
    actions.append(
      button(chapter.incident.recoveryAction.label, "button button--secondary", {
        "data-next-id": chapter.id,
        "aria-label": `${chapter.incident.recoveryAction.label}: ${chapter.id} ${chapter.title}`,
      }),
      button(chapter.incident.reportAction.label, "button button--quiet", {
        "data-inspect-id": chapter.id,
        "aria-label": `${chapter.incident.reportAction.label}: ${chapter.id} ${chapter.title}`,
      }),
    );

    elements.incident.replaceChildren(headingGroup, paths, actions);
  }

  function filteredChapters() {
    const query = normalize(ui.query);
    return fixture.chapters.filter((chapter) => {
      const matchesFilter = ui.filter === "all" || chapter.filter === ui.filter;
      const matchesQuery = !query || normalize(`${chapter.id} ${chapter.title}`).includes(query);
      return matchesFilter && matchesQuery;
    });
  }

  function createRow(chapter) {
    const row = document.createElement("tr");
    row.dataset.chapterId = chapter.id;
    row.classList.toggle("is-selected", ui.selected.has(chapter.id));

    const selectionCell = document.createElement("td");
    selectionCell.className = "selection-cell";
    const selection = document.createElement("input");
    selection.type = "checkbox";
    selection.dataset.selectId = chapter.id;
    selection.checked = ui.selected.has(chapter.id);
    selection.disabled = !chapter.selectable;
    selection.setAttribute("aria-label", chapter.selectable
      ? `Selecionar ${chapter.id} ${chapter.title} para aplicação em lote`
      : `${chapter.id} ${chapter.title} indisponível para aplicação em lote`);
    if (!chapter.selectable) selection.title = "Indisponível: o diff ainda não está pronto";
    selectionCell.append(selection);

    const chapterCell = document.createElement("td");
    chapterCell.className = "chapter-cell";
    const id = document.createElement("strong");
    id.textContent = chapter.id;
    const title = document.createElement("span");
    title.textContent = chapter.title;
    const words = document.createElement("small");
    words.textContent = `${formatWords(chapter.words)} palavras`;
    chapterCell.append(id, title, words);

    const stageCell = document.createElement("td");
    const stage = document.createElement("span");
    stage.className = `stage stage--${chapter.state}`;
    stage.textContent = chapter.stage;
    stageCell.append(stage);

    const glossaryCell = cell("Glossário", chapter.glossary.label, chapter.glossary.detail);
    const summaryCell = cell("Situação", chapter.summary, null, "summary-cell");
    const expectedCell = cell("Previsão", chapter.expectedAt, null, "expected-cell");

    const actionsCell = document.createElement("td");
    actionsCell.className = "actions-cell";
    const actions = document.createElement("div");
    actions.className = "row-actions";
    const next = button(chapter.nextAction.label, "button button--secondary", {
      "data-next-id": chapter.id,
      "aria-label": `${chapter.nextAction.label}: ${chapter.id} ${chapter.title}`,
    });
    const inspect = button(chapter.inspectAction.label, "button button--quiet", {
      "data-inspect-id": chapter.id,
      "aria-label": `${chapter.inspectAction.label}: ${chapter.id} ${chapter.title}`,
    });
    actions.append(next, inspect);
    actionsCell.append(actions);

    row.append(selectionCell, chapterCell, stageCell, glossaryCell, summaryCell, expectedCell, actionsCell);
    return row;
  }

  function renderRows() {
    const visible = filteredChapters();
    elements.rows.replaceChildren(...visible.map(createRow));
    elements.emptyState.hidden = visible.length !== 0;
    elements.rows.closest("table").hidden = visible.length === 0;
    elements.clearSearch.hidden = !ui.query;
    elements.applySelection.disabled = ui.selected.size === 0;
    elements.applySelection.textContent = ui.selected.size
      ? `Aplicar seleção (${ui.selected.size})`
      : "Aplicar seleção";
    elements.resultSummary.textContent = `Exibindo ${visible.length} de ${fixture.summary.chapters} capítulos`;
  }

  function updateFilter(filterId) {
    ui.filter = filterId;
    elements.filters.querySelectorAll("[data-filter]").forEach((control) => {
      const isActive = control.dataset.filter === filterId;
      control.classList.toggle("is-active", isActive);
      control.setAttribute("aria-pressed", String(isActive));
    });
    renderRows();
  }

  function resetResults() {
    ui.query = "";
    elements.search.value = "";
    updateFilter("all");
    elements.search.focus();
  }

  function addDetailItem(list, label, value) {
    const item = document.createElement("div");
    const term = document.createElement("dt");
    term.textContent = label;
    const description = document.createElement("dd");
    description.textContent = value;
    item.append(term, description);
    list.append(item);
  }

  function openChapterDialog(chapter) {
    elements.chapterDialog.dataset.chapterId = chapter.id;
    elements.chapterDialogTitle.textContent = `${chapter.id} · ${chapter.title}`;

    const details = document.createElement("dl");
    details.className = "detail-grid";
    addDetailItem(details, "Quantidade", `${formatWords(chapter.words)} palavras`);
    addDetailItem(details, "Etapa", chapter.stage);
    addDetailItem(details, "Glossário", chapter.glossary.label);
    addDetailItem(details, "Horário previsto", chapter.expectedAt);

    const glossary = document.createElement("p");
    glossary.className = "detail-summary";
    glossary.textContent = chapter.glossary.detail;
    const summary = document.createElement("p");
    summary.className = "detail-summary";
    summary.textContent = chapter.summary;
    elements.chapterDialogBody.replaceChildren(details, glossary, summary);

    if (chapter.incident) {
      const incident = document.createElement("section");
      incident.className = "incident-detail";
      const heading = document.createElement("strong");
      heading.textContent = chapter.incident.title;
      const effect = document.createElement("p");
      effect.textContent = chapter.incident.effect;
      const terms = document.createElement("ul");
      chapter.incident.terms.forEach((term) => {
        const item = document.createElement("li");
        item.textContent = term;
        terms.append(item);
      });
      incident.append(heading, effect, terms);
      elements.chapterDialogBody.append(incident);
    }

    const close = button("Fechar", "button button--secondary", { "data-close-dialog": "chapter-dialog" });
    const inspect = button(chapter.inspectAction.label, "button button--quiet", {
      "data-simulate-id": chapter.id,
      "data-simulate-action": chapter.inspectAction.id,
    });

    if (chapter.incident) {
      const retry = button(chapter.incident.retryAction.label, "button button--secondary", {
        "data-retry-id": chapter.id,
      });
      retry.disabled = !ui.glossaryConfirmed;
      retry.title = retry.disabled ? "Confirme as decisões de glossário antes de tentar novamente" : "Confirmação de glossário registrada";
      const resolve = button(chapter.incident.recoveryAction.label, "button button--primary", {
        "data-resolve-id": chapter.id,
      });
      elements.chapterDialogActions.replaceChildren(close, inspect, retry, resolve);
    } else {
      const next = button(chapter.nextAction.label, "button button--primary", {
        "data-dialog-next-id": chapter.id,
      });
      elements.chapterDialogActions.replaceChildren(close, inspect, next);
    }

    elements.chapterDialog.showModal();
  }

  function closeDialog(dialog) {
    if (dialog.open) dialog.close();
  }

  function openConfirmation(title, copy, confirmLabel, callback) {
    ui.pendingConfirmation = callback;
    elements.confirmDialogTitle.textContent = title;
    elements.confirmDialogCopy.textContent = copy;
    elements.confirmAction.textContent = confirmLabel;
    elements.confirmDialog.showModal();
  }

  function showFeedback(message) {
    window.clearTimeout(toastTimer);
    elements.actionLog.textContent = message;
    elements.toastMessage.textContent = message;
    elements.toast.hidden = false;
    toastTimer = window.setTimeout(() => {
      elements.toast.hidden = true;
    }, 3800);
  }

  function simulatedMessage(chapter, action) {
    return `${action.label} · ${chapter.id}: ação simulada com sucesso; nenhum arquivo foi alterado.`;
  }

  function requestChapterAction(chapter, action) {
    if (chapter.incident && action.id === chapter.incident.recoveryAction.id) {
      openChapterDialog(chapter);
      return;
    }

    openConfirmation(
      action.label,
      `${chapter.id} · ${chapter.title}. Esta ação não executará scripts nem alterará arquivos.`,
      `Confirmar ${action.label}`,
      () => showFeedback(simulatedMessage(chapter, action)),
    );
  }

  function requestGlossaryResolution(chapter) {
    closeDialog(elements.chapterDialog);
    openConfirmation(
      chapter.incident.recoveryAction.label,
      `${chapter.id}: confirmar decisões simuladas para “${chapter.incident.terms[0]}” e “${chapter.incident.terms[1]}”?`,
      "Confirmar decisões",
      () => {
        ui.glossaryConfirmed = true;
        showFeedback(`${chapter.id}: decisões de glossário confirmadas somente nesta interface. Tentar novamente está disponível.`);
        openChapterDialog(chapter);
      },
    );
  }

  function requestRetry(chapter) {
    openConfirmation(
      chapter.incident.retryAction.label,
      `${chapter.id}: a confirmação simulada do glossário foi registrada. Nenhum script real será chamado.`,
      chapter.incident.retryAction.label,
      () => {
        showFeedback(`${chapter.id}: nova tentativa simulada; nenhum arquivo foi alterado.`);
        openChapterDialog(chapter);
      },
    );
  }

  elements.search.addEventListener("input", (event) => {
    ui.query = event.target.value;
    renderRows();
  });

  elements.clearSearch.addEventListener("click", () => {
    ui.query = "";
    elements.search.value = "";
    renderRows();
    elements.search.focus();
  });

  elements.recoverResults.addEventListener("click", resetResults);

  elements.filters.addEventListener("click", (event) => {
    const control = event.target.closest("[data-filter]");
    if (control) updateFilter(control.dataset.filter);
  });

  elements.rows.addEventListener("change", (event) => {
    const selection = event.target.closest("[data-select-id]");
    if (!selection) return;
    if (selection.checked) ui.selected.add(selection.dataset.selectId);
    else ui.selected.delete(selection.dataset.selectId);
    renderRows();
  });

  document.addEventListener("click", (event) => {
    const close = event.target.closest("[data-close-dialog]");
    if (close) {
      closeDialog(document.querySelector(`#${close.dataset.closeDialog}`));
      return;
    }

    const inspect = event.target.closest("[data-inspect-id]");
    if (inspect) {
      const chapter = fixture.chapters.find((item) => item.id === inspect.dataset.inspectId);
      if (chapter) openChapterDialog(chapter);
      return;
    }

    const next = event.target.closest("[data-next-id]");
    if (next) {
      const chapter = fixture.chapters.find((item) => item.id === next.dataset.nextId);
      if (chapter) requestChapterAction(chapter, chapter.nextAction);
      return;
    }

    const dialogNext = event.target.closest("[data-dialog-next-id]");
    if (dialogNext) {
      const chapter = fixture.chapters.find((item) => item.id === dialogNext.dataset.dialogNextId);
      if (chapter) {
        closeDialog(elements.chapterDialog);
        requestChapterAction(chapter, chapter.nextAction);
      }
      return;
    }

    const simulate = event.target.closest("[data-simulate-id]");
    if (simulate) {
      const chapter = fixture.chapters.find((item) => item.id === simulate.dataset.simulateId);
      const action = chapter && chapter.inspectAction.id === simulate.dataset.simulateAction
        ? chapter.inspectAction
        : null;
      if (chapter && action) {
        closeDialog(elements.chapterDialog);
        requestChapterAction(chapter, action);
      }
      return;
    }

    const resolve = event.target.closest("[data-resolve-id]");
    if (resolve) {
      const chapter = fixture.chapters.find((item) => item.id === resolve.dataset.resolveId);
      if (chapter && chapter.incident) requestGlossaryResolution(chapter);
      return;
    }

    const retry = event.target.closest("[data-retry-id]");
    if (retry) {
      const chapter = fixture.chapters.find((item) => item.id === retry.dataset.retryId);
      if (chapter && chapter.incident && ui.glossaryConfirmed) {
        closeDialog(elements.chapterDialog);
        requestRetry(chapter);
      }
    }
  });

  elements.applySelection.addEventListener("click", () => {
    const selectedChapters = fixture.chapters.filter((chapter) => ui.selected.has(chapter.id));
    if (!selectedChapters.length) return;
    const selectionLabel = selectedChapters.map((chapter) => chapter.id).join(", ");
    openConfirmation(
      "Aplicar diff em lote",
      `${selectionLabel}: a aplicação será somente simulada e não alterará arquivos.`,
      "Confirmar aplicação",
      () => showFeedback(`${selectionLabel}: aplicação do diff em lote simulada com sucesso; nenhum arquivo foi alterado.`),
    );
  });

  elements.confirmAction.addEventListener("click", () => {
    const callback = ui.pendingConfirmation;
    ui.pendingConfirmation = null;
    closeDialog(elements.confirmDialog);
    if (callback) callback();
  });

  document.addEventListener("keydown", (event) => {
    const typing = event.target.matches("input, textarea, [contenteditable='true']");
    if (event.key === "/" && !typing && !elements.chapterDialog.open && !elements.confirmDialog.open) {
      event.preventDefault();
      elements.search.focus();
    }
    if (event.key === "Escape" && document.activeElement === elements.search && elements.search.value) {
      ui.query = "";
      elements.search.value = "";
      renderRows();
    }
  });

  initializeMeta();
  initializeFilters();
  initializeIncident();
  renderRows();
})();
