(function () {
  "use strict";

  // Copy buttons on entry pages: copy the text of the element named by data-copy.
  document.querySelectorAll("button[data-copy]").forEach(function (button) {
    button.addEventListener("click", function () {
      var source = document.getElementById(button.getAttribute("data-copy"));
      if (!source || !navigator.clipboard) return;
      navigator.clipboard.writeText(source.innerText.trim()).then(function () {
        var label = button.textContent;
        button.textContent = "Copied";
        setTimeout(function () { button.textContent = label; }, 1500);
      }, function () { /* clipboard refused: leave the button unchanged */ });
    });
  });

  // Directory: filter, sort and page the rows that the page already renders.
  var list = document.getElementById("entries");
  if (!list) return;

  var PAGE = 100;
  var rows = Array.prototype.slice.call(list.querySelectorAll(".row"));
  var search = document.getElementById("q");
  var category = document.getElementById("category");
  var language = document.getElementById("language");
  var sort = document.getElementById("sort");
  var tabs = Array.prototype.slice.call(document.querySelectorAll(".tabs [role=tab]"));
  var status = document.getElementById("status");
  var empty = document.getElementById("empty");
  var reset = document.getElementById("reset");
  var more = document.getElementById("more");

  var state = { q: "", kind: "", category: "", language: "", sort: "usage", limit: PAGE };

  rows.forEach(function (row, index) {
    row.dataset.index = String(index);
    row.dataset.hay = row.textContent.replace(/\s+/g, " ").toLowerCase();
  });

  function count(n) { return n.toLocaleString("en-US"); }

  // Tab labels show totals per type.
  tabs.forEach(function (tab) {
    var kind = tab.dataset.kind;
    var total = rows.filter(function (row) { return !kind || row.dataset.kind === kind; }).length;
    var label = tab.querySelector(".count");
    if (label) label.textContent = count(total);
  });

  // Categories and languages offered depend on the type selected: a reviewer label
  // never matches a verification entry, and verification entries have no language.
  function fillSelect(select, values, emptyLabel) {
    select.innerHTML = "";
    var first = document.createElement("option");
    first.value = "";
    first.textContent = emptyLabel;
    select.appendChild(first);
    values.forEach(function (value) {
      var option = document.createElement("option");
      option.value = value;
      option.textContent = value;
      select.appendChild(option);
    });
  }

  function valuesFor(attribute, kind) {
    var seen = {};
    rows.forEach(function (row) {
      if (kind && row.dataset.kind !== kind) return;
      var value = row.dataset[attribute];
      if (value) seen[value] = true;
    });
    return Object.keys(seen).sort(function (a, b) { return a.localeCompare(b); });
  }

  function refreshOptions() {
    fillSelect(category, valuesFor("category", state.kind), "All categories");
    fillSelect(language, valuesFor("language", state.kind === "verification" ? "reviewer" : state.kind), "All languages");
    language.disabled = state.kind === "verification";
    if (language.disabled) state.language = "";
    if (state.category && !category.querySelector('option[value="' + CSS.escape(state.category) + '"]')) state.category = "";
  }

  function readUrl() {
    var params = new URLSearchParams(window.location.search);
    state.q = params.get("q") || "";
    state.kind = params.get("kind") || "";
    state.category = params.get("category") || "";
    state.language = params.get("language") || "";
    var sortValue = params.get("sort") || "usage";
    state.sort = sortValue === "name" ? "name" : "usage";
  }

  function writeUrl() {
    var params = new URLSearchParams();
    if (state.q) params.set("q", state.q);
    if (state.kind) params.set("kind", state.kind);
    if (state.category) params.set("category", state.category);
    if (state.language) params.set("language", state.language);
    if (state.sort !== "usage") params.set("sort", state.sort);
    var query = params.toString();
    history.replaceState(null, "", window.location.pathname + (query ? "?" + query : "") + window.location.hash);
  }

  function matches(row) {
    if (state.kind && row.dataset.kind !== state.kind) return false;
    if (state.category && row.dataset.category !== state.category) return false;
    if (state.language && row.dataset.language !== state.language) return false;
    if (state.q) {
      var words = state.q.toLowerCase().split(/\s+/).filter(Boolean);
      return words.every(function (word) { return row.dataset.hay.indexOf(word) !== -1; });
    }
    return true;
  }

  // Usage: discussions for reviewers, repos for verification. Ties fall back to name.
  function compare(a, b) {
    var names = a.querySelector(".row__title").textContent.localeCompare(b.querySelector(".row__title").textContent);
    if (state.sort === "name") return names || Number(a.dataset.index) - Number(b.dataset.index);
    var usage = Number(b.dataset.count) - Number(a.dataset.count);
    return usage || names || Number(a.dataset.index) - Number(b.dataset.index);
  }

  function render() {
    rows.sort(compare).forEach(function (row) { list.appendChild(row); });
    var matched = rows.filter(matches);
    var shown = matched.slice(0, state.limit);
    rows.forEach(function (row) { row.hidden = true; });
    shown.forEach(function (row, index) {
      row.hidden = false;
      row.querySelector(".row__rank").textContent = String(index + 1);
    });
    tabs.forEach(function (tab) {
      tab.setAttribute("aria-selected", String(tab.dataset.kind === state.kind));
    });
    search.value = state.q;
    category.value = state.category;
    language.value = state.language;
    sort.value = state.sort;
    status.textContent = matched.length === rows.length
      ? count(rows.length) + " entries, " + Math.min(state.limit, matched.length) + " shown"
      : count(matched.length) + " matching of " + count(rows.length) + ", " + shown.length + " shown";
    var remaining = matched.length - shown.length;
    more.hidden = remaining <= 0;
    more.textContent = "Show " + Math.min(PAGE, remaining) + " more";
    empty.hidden = matched.length > 0;
    writeUrl();
  }

  // Changing a filter or sort starts again from the first page.
  function update(changes) {
    Object.keys(changes).forEach(function (key) { state[key] = changes[key]; });
    state.limit = PAGE;
    if ("kind" in changes) refreshOptions();
    render();
  }

  var timer = null;
  search.addEventListener("input", function () {
    clearTimeout(timer);
    timer = setTimeout(function () { update({ q: search.value.trim() }); }, 80);
  });
  category.addEventListener("change", function () { update({ category: category.value }); });
  language.addEventListener("change", function () { update({ language: language.value }); });
  sort.addEventListener("change", function () { update({ sort: sort.value }); });
  tabs.forEach(function (tab) {
    tab.addEventListener("click", function () { update({ kind: tab.dataset.kind }); });
  });
  reset.addEventListener("click", function () {
    update({ q: "", kind: "", category: "", language: "", sort: "usage" });
  });
  more.addEventListener("click", function () {
    state.limit += PAGE;
    render();
  });

  document.addEventListener("keydown", function (event) {
    if (event.key !== "/" || event.metaKey || event.ctrlKey || event.altKey) return;
    var target = event.target;
    if (target && /^(INPUT|TEXTAREA|SELECT)$/.test(target.tagName)) return;
    event.preventDefault();
    search.focus();
  });

  readUrl();
  refreshOptions();
  render();
})();
