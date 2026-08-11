(function () {
  "use strict";

  const fixture = window.DEMO_TRADUCAO;

  if (!fixture) {
    document.body.textContent = "The demonstration data could not be loaded.";
    throw new Error("window.DEMO_TRADUCAO is unavailable.");
  }

  const stateLabels = {
    ready: "Ready",
    blocked: "Blocked",
    reviewing: "Under review",
    queued: "Queued"
  };

  const view = {
    filter: "all",
    query: "",
    selected: new Set(),
    expanded: new Set(),
    glossaryConfirmed: false
  };

  const elements = {
    fixtureLabel: document.querySelector("#fixture-label"),
    surfaceName: document.querySelector("#surface-name"),
    projectName: document.querySelector("#project-name"),
    batchName: document.querySelector("#batch-name"),
    referenceTime: document.querySelector("#reference-time"),
    batchSummary: document.querySelector("#batch-summary"),
    pipelineName: document.querySelector("#pipeline-name"),
    executionModel: document.querySelector("#execution-model"),
    search: document.querySelector("#chapter-search"),
    clearSearch: document.querySelector("#clear-search"),
    filterGroup: document.querySelector("#filter-group"),
    bulkAction: document.querySelector("#bulk-action"),
    bulkCount: document.querySelector("#bulk-count"),
    resultCount: document.querySelector("#result-count"),
    queueBody: document.querySelector("#queue-body"),
    tableScroll: document.querySelector(".table-scroll"),
    emptyState: document.querySelector("#empty-state"),
    resetView: document.querySelector("#reset-view"),
    actionStatus: document.querySelector("#action-status"),
    actionMessage: document.querySelector("#action-message")
  };

  function formatNumber(value) {
    return new Intl.NumberFormat("en-US").format(value);
  }

  function normalize(value) {
    return value
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLocaleLowerCase("en-US");
  }

  function appendText(element, text) {
    element.appendChild(document.createTextNode(text));
  }

  function makeButton(label, className, action, chapter) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = className;
    button.dataset.action = action.id;
    button.dataset.chapterId = chapter.id;
    button.textContent = label;
    button.setAttribute("aria-label", label + " — " + chapter.id + " " + chapter.title);
    return button;
  }

  function setStaticContent() {
    const meta = fixture.meta;
    const summary = fixture.summary;

    elements.fixtureLabel.textContent = meta.fixtureLabel;
    elements.surfaceName.textContent = meta.surfaceName;
    elements.projectName.textContent = meta.projectName;
    elements.batchName.textContent = meta.batchName;
    elements.referenceTime.textContent = meta.referenceDate + ", " + meta.referenceTime;
    elements.batchSummary.textContent =
      summary.chapters + " chapters · " +
      formatNumber(summary.words) + " words · " +
      summary.ready + " ready · " +
      summary.blocked + " blocked · " +
      summary.reviewing + " under review · " +
      summary.queued + " queued";
    elements.pipelineName.textContent = meta.pipeline;
    elements.executionModel.textContent = meta.executionModel;
    elements.actionMessage.textContent = meta.simulationNotice;
  }

  function renderFilters() {
    const fragment = document.createDocumentFragment();

    fixture.filters.forEach(function (filter) {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "filter-button";
      button.dataset.filter = filter.id;
      button.setAttribute("aria-pressed", String(view.filter === filter.id));
      appendText(button, filter.label);

      const count = document.createElement("span");
      count.className = "filter-button__count";
      count.setAttribute("aria-hidden", "true");
      count.textContent = filter.count;
      button.appendChild(count);
      fragment.appendChild(button);
    });

    elements.filterGroup.replaceChildren(fragment);
  }

  function createSelectionCell(chapter) {
    const cell = document.createElement("td");
    cell.className = "select-column";
    const label = document.createElement("label");
    label.className = "selection-control";
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.dataset.selectChapter = chapter.id;
    checkbox.checked = view.selected.has(chapter.id);
    checkbox.disabled = !chapter.selectable;
    checkbox.setAttribute(
      "aria-label",
      chapter.selectable
        ? "Select " + chapter.id + " " + chapter.title + " for batch application"
        : chapter.id + " " + chapter.title + " unavailable for batch application"
    );
    label.appendChild(checkbox);
    cell.appendChild(label);
    return cell;
  }

  function createChapterCell(chapter) {
    const cell = document.createElement("td");
    cell.dataset.label = "Chapter";

    const id = document.createElement("span");
    id.className = "chapter-id";
    id.textContent = chapter.id;
    const title = document.createElement("span");
    title.className = "chapter-title";
    title.textContent = chapter.title;
    const words = document.createElement("span");
    words.className = "chapter-words";
    words.textContent = formatNumber(chapter.words) + " words";
    cell.append(id, title, words);
    return cell;
  }

  function createStageCell(chapter) {
    const cell = document.createElement("td");
    cell.dataset.label = "Stage";
    const state = document.createElement("span");
    state.className = "state-label";
    state.dataset.state = chapter.state;
    state.textContent = stateLabels[chapter.state];
    const stage = document.createElement("span");
    stage.className = "stage-name";
    stage.textContent = chapter.stage;
    cell.append(state, stage);
    return cell;
  }

  function createOperationCell(chapter) {
    const cell = document.createElement("td");
    cell.dataset.label = "Operational status";
    const glossary = document.createElement("span");
    glossary.className = "glossary-label";
    glossary.textContent = "Glossary: " + chapter.glossary.label;
    const summary = document.createElement("p");
    summary.className = "summary-text";
    summary.textContent = chapter.summary;
    cell.append(glossary, summary);
    return cell;
  }

  function createExpectedCell(chapter) {
    const cell = document.createElement("td");
    cell.dataset.label = "Estimated";
    const expected = document.createElement("span");
    expected.className = "expected-at";
    expected.textContent = chapter.expectedAt;
    cell.appendChild(expected);
    return cell;
  }

  function createActionsCell(chapter) {
    const cell = document.createElement("td");
    cell.dataset.label = "Actions";
    const actions = document.createElement("div");
    actions.className = "row-actions";

    const next = makeButton(chapter.nextAction.label, "primary-button", chapter.nextAction, chapter);
    if (chapter.nextAction.id === "apply-diff") {
      next.disabled = !view.selected.has(chapter.id);
      next.setAttribute("aria-describedby", "apply-help-" + chapter.id);
    }

    if (chapter.nextAction.id === "resolve-glossary") {
      next.setAttribute("aria-expanded", String(view.expanded.has(chapter.id)));
      next.setAttribute("aria-controls", "details-" + chapter.id);
    }

    const inspect = makeButton(chapter.inspectAction.label, "secondary-button", chapter.inspectAction, chapter);
    inspect.dataset.inspect = "true";
    inspect.setAttribute("aria-expanded", String(view.expanded.has(chapter.id)));
    inspect.setAttribute("aria-controls", "details-" + chapter.id);
    actions.append(next, inspect);
    cell.appendChild(actions);

    if (chapter.nextAction.id === "apply-diff") {
      const help = document.createElement("span");
      help.className = "visually-hidden";
      help.id = "apply-help-" + chapter.id;
      help.textContent = "Select the chapter to enable simulated application.";
      cell.appendChild(help);
    }

    return cell;
  }

  function createDetailsRow(chapter) {
    const row = document.createElement("tr");
    row.className = "details-row";
    row.dataset.detailsFor = chapter.id;
    row.hidden = !view.expanded.has(chapter.id);
    const cell = document.createElement("td");
    cell.colSpan = 6;
    const details = document.createElement("div");
    details.className = "chapter-details";
    details.id = "details-" + chapter.id;

    const grid = document.createElement("div");
    grid.className = "chapter-details__grid";
    const detailBlock = document.createElement("section");
    detailBlock.className = "detail-block";
    const detailTitle = document.createElement("h3");
    detailTitle.textContent = "Details for " + chapter.id;
    const glossaryDetail = document.createElement("p");
    glossaryDetail.textContent = chapter.glossary.detail;
    const operationalSummary = document.createElement("p");
    operationalSummary.textContent = chapter.summary;
    detailBlock.append(detailTitle, glossaryDetail, operationalSummary);
    grid.appendChild(detailBlock);

    if (chapter.incident) {
      const incident = document.createElement("section");
      incident.className = "incident";
      incident.setAttribute("aria-labelledby", "incident-title-" + chapter.id);
      const incidentTitle = document.createElement("h3");
      incidentTitle.id = "incident-title-" + chapter.id;
      incidentTitle.textContent = chapter.incident.title;
      const effect = document.createElement("p");
      effect.textContent = chapter.incident.effect;
      const list = document.createElement("ul");
      chapter.incident.terms.forEach(function (term) {
        const item = document.createElement("li");
        item.textContent = term;
        list.appendChild(item);
      });

      const help = document.createElement("p");
      help.className = "incident__help";
      help.id = "retry-help-" + chapter.id;
      help.textContent = view.glossaryConfirmed
        ? "Decisions confirmed in this simulation; retry is available."
        : "Confirm the simulated decisions before trying again.";

      const incidentActions = document.createElement("div");
      incidentActions.className = "incident__actions";
      const confirm = document.createElement("button");
      confirm.type = "button";
      confirm.className = "incident-action";
      confirm.dataset.action = "confirm-glossary";
      confirm.dataset.chapterId = chapter.id;
      confirm.textContent = view.glossaryConfirmed ? "Decisions confirmed" : "Confirm decisions";
      confirm.disabled = view.glossaryConfirmed;

      const retry = makeButton(chapter.incident.retryAction.label, "incident-action", chapter.incident.retryAction, chapter);
      retry.disabled = !view.glossaryConfirmed;
      retry.setAttribute("aria-describedby", help.id);
      const report = makeButton(chapter.incident.reportAction.label, "incident-action", chapter.incident.reportAction, chapter);
      report.dataset.inspect = "true";
      incidentActions.append(confirm, retry, report);
      incident.append(incidentTitle, effect, list, help, incidentActions);
      grid.appendChild(incident);
    }

    details.appendChild(grid);
    cell.appendChild(details);
    row.appendChild(cell);
    return row;
  }

  function matchesView(chapter) {
    const matchesFilter = view.filter === "all" || chapter.filter === view.filter;
    const searchable = normalize(chapter.id + " " + chapter.title);
    const matchesSearch = searchable.includes(normalize(view.query.trim()));
    return matchesFilter && matchesSearch;
  }

  function renderQueue() {
    const matchingChapters = fixture.chapters.filter(matchesView);
    const fragment = document.createDocumentFragment();

    matchingChapters.forEach(function (chapter) {
      const row = document.createElement("tr");
      row.className = "chapter-row";
      row.dataset.chapterId = chapter.id;
      row.dataset.state = chapter.state;
      row.classList.toggle("is-selected", view.selected.has(chapter.id));
      row.append(
        createSelectionCell(chapter),
        createChapterCell(chapter),
        createStageCell(chapter),
        createOperationCell(chapter),
        createExpectedCell(chapter),
        createActionsCell(chapter)
      );
      fragment.append(row, createDetailsRow(chapter));
    });

    elements.queueBody.replaceChildren(fragment);
    elements.tableScroll.hidden = matchingChapters.length === 0;
    elements.emptyState.hidden = matchingChapters.length !== 0;
    elements.resultCount.textContent = matchingChapters.length === 1
      ? "1 visible chapter"
      : matchingChapters.length + " visible chapters";
    elements.clearSearch.hidden = view.query.length === 0;
    updateBulkAction();
  }

  function updateBulkAction() {
    const selectedReady = fixture.chapters.filter(function (chapter) {
      return chapter.selectable && view.selected.has(chapter.id);
    });
    elements.bulkCount.textContent = selectedReady.length;
    elements.bulkAction.disabled = selectedReady.length === 0;
    elements.bulkAction.setAttribute(
      "aria-label",
      "Apply diff as a batch; " + selectedReady.length + " selected chapter"
    );
  }

  function announce(message) {
    elements.actionMessage.textContent = message;
    elements.actionStatus.classList.add("has-message");
  }

  function chapterById(id) {
    return fixture.chapters.find(function (chapter) {
      return chapter.id === id;
    });
  }

  function toggleDetails(chapterId, forceOpen) {
    const shouldOpen = forceOpen === undefined ? !view.expanded.has(chapterId) : forceOpen;
    if (shouldOpen) {
      view.expanded.add(chapterId);
    } else {
      view.expanded.delete(chapterId);
    }
    const detailsRow = elements.queueBody.querySelector('[data-details-for="' + chapterId + '"]');
    if (detailsRow) detailsRow.hidden = !shouldOpen;
    elements.queueBody
      .querySelectorAll('[aria-controls="details-' + chapterId + '"]')
      .forEach(function (control) {
        control.setAttribute("aria-expanded", String(shouldOpen));
      });
    return shouldOpen;
  }

  function simulateAction(chapter, actionId, label) {
    if (actionId === "resolve-glossary") {
      toggleDetails(chapter.id, true);
      announce("Glossary decisions opened for " + chapter.id + ". No files were changed.");
      return;
    }

    if (actionId === "confirm-glossary") {
      view.glossaryConfirmed = true;
      view.expanded.add(chapter.id);
      renderQueue();
      const retry = elements.queueBody.querySelector(
        '[data-chapter-id="' + chapter.id + '"][data-action="retry"]'
      );
      if (retry) retry.focus();
      announce("Decisions for " + chapter.id + " were confirmed only in this simulation. Retry is now enabled.");
      return;
    }

    if (actionId === "retry") {
      announce("A new attempt for " + chapter.id + " was simulated. The chapter and fixture remain unchanged.");
      return;
    }

    announce(label + " for " + chapter.id + " was simulated. No files were changed.");
  }

  elements.search.addEventListener("input", function (event) {
    view.query = event.target.value;
    renderQueue();
  });

  elements.clearSearch.addEventListener("click", function () {
    view.query = "";
    elements.search.value = "";
    renderQueue();
    elements.search.focus();
  });

  elements.resetView.addEventListener("click", function () {
    view.query = "";
    view.filter = "all";
    elements.search.value = "";
    renderFilters();
    renderQueue();
    elements.search.focus();
  });

  elements.filterGroup.addEventListener("click", function (event) {
    const button = event.target.closest("[data-filter]");
    if (!button) return;
    view.filter = button.dataset.filter;
    elements.filterGroup.querySelectorAll("[data-filter]").forEach(function (filterButton) {
      filterButton.setAttribute("aria-pressed", String(filterButton.dataset.filter === view.filter));
    });
    renderQueue();
  });

  elements.queueBody.addEventListener("change", function (event) {
    const checkbox = event.target.closest("[data-select-chapter]");
    if (!checkbox) return;
    if (checkbox.checked) {
      view.selected.add(checkbox.dataset.selectChapter);
    } else {
      view.selected.delete(checkbox.dataset.selectChapter);
    }
    const chapterRow = checkbox.closest(".chapter-row");
    if (chapterRow) {
      chapterRow.classList.toggle("is-selected", checkbox.checked);
      const applyButton = chapterRow.querySelector('[data-action="apply-diff"]');
      if (applyButton) applyButton.disabled = !checkbox.checked;
    }
    updateBulkAction();
    announce(
      checkbox.dataset.selectChapter +
      (checkbox.checked ? " selected for simulated batch application." : " removed from simulated batch application.")
    );
  });

  elements.queueBody.addEventListener("click", function (event) {
    const button = event.target.closest("button[data-action]");
    if (!button) return;
    const chapter = chapterById(button.dataset.chapterId);
    if (!chapter) return;

    if (button.dataset.inspect === "true") {
      const opened = toggleDetails(chapter.id);
      announce(
        opened
          ? button.textContent + " opened for " + chapter.id + "."
          : button.textContent + " closed for " + chapter.id + "."
      );
      return;
    }

    simulateAction(chapter, button.dataset.action, button.textContent);
  });

  elements.bulkAction.addEventListener("click", function () {
    const selectedIds = Array.from(view.selected);
    announce(
      "Batch diff application simulated for " + selectedIds.join(", ") + ". No files were changed."
    );
  });

  setStaticContent();
  renderFilters();
  renderQueue();
})();
