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

  // Directory: filter and sort the rows that the page already renders.
  var list = document.getElementById("entries");
  if (!list) return;

  var rows = Array.prototype.slice.call(list.querySelectorAll(".row"));
  var search = document.getElementById("q");
  var category = document.getElementById("category");
  var language = document.getElementById("language");
  var sort = document.getElementById("sort");
  var tabs = Array.prototype.slice.call(document.querySelectorAll(".tabs [role=tab]"));
  var status = document.getElementById("status");
  var empty = document.getElementById("empty");
  var reset = document.getElementById("reset");

  var state = { q: "", kind: "", category: "", language: "", sort: "featured" };

  rows.forEach(function (row, index) {
    row.dataset.index = String(index);
    row.dataset.hay = row.textContent.replace(/\s+/g, " ").toLowerCase();
  });

  function unique(attribute) {
    var seen = {};
    rows.forEach(function (row) {
      var value = row.dataset[attribute];
      if (value) seen[value] = true;
    });
    return Object.keys(seen).sort(function (a, b) { return a.localeCompare(b); });
  }

  function fill(select, values) {
    values.forEach(function (value) {
      var option = document.createElement("option");
      option.value = value;
      option.textContent = value;
      select.appendChild(option);
    });
  }

  fill(category, unique("category"));
  fill(language, unique("language"));

  // Totals per type for the tab labels.
  tabs.forEach(function (tab) {
    var kind = tab.dataset.kind;
    var total = rows.filter(function (row) { return !kind || row.dataset.kind === kind; }).length;
    var count = tab.querySelector(".count");
    if (count) count.textContent = total.toLocaleString("en-US");
  });

  function readUrl() {
    var params = new URLSearchParams(window.location.search);
    state.q = params.get("q") || "";
    state.kind = params.get("kind") || "";
    state.category = params.get("category") || "";
    state.language = params.get("language") || "";
    state.sort = params.get("sort") || "featured";
  }

  function writeUrl() {
    var params = new URLSearchParams();
    Object.keys(state).forEach(function (key) {
      if (state[key] && !(key === "sort" && state[key] === "featured")) params.set(key, state[key]);
    });
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

  function compare(a, b) {
    var byIndex = Number(a.dataset.index) - Number(b.dataset.index);
    if (state.sort === "discussed") {
      var diff = Number(b.dataset.count) - Number(a.dataset.count);
      return diff || byIndex;
    }
    if (state.sort === "name") {
      var names = a.querySelector(".row__title").textContent.localeCompare(b.querySelector(".row__title").textContent);
      return names || byIndex;
    }
    return byIndex;
  }

  function render() {
    rows.sort(compare).forEach(function (row) { list.appendChild(row); });
    var shown = 0;
    rows.forEach(function (row) {
      var visible = matches(row);
      row.hidden = !visible;
      if (visible) {
        shown += 1;
        row.querySelector(".row__rank").textContent = String(shown);
      }
    });
    tabs.forEach(function (tab) {
      tab.setAttribute("aria-selected", String(tab.dataset.kind === state.kind));
    });
    search.value = state.q;
    category.value = state.category;
    language.value = state.language;
    sort.value = state.sort;
    status.textContent = shown === rows.length
      ? rows.length.toLocaleString("en-US") + " entries"
      : shown.toLocaleString("en-US") + " of " + rows.length.toLocaleString("en-US") + " entries";
    empty.hidden = shown > 0;
    writeUrl();
  }

  function update(changes) {
    Object.keys(changes).forEach(function (key) { state[key] = changes[key]; });
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
    update({ q: "", kind: "", category: "", language: "", sort: "featured" });
  });

  document.addEventListener("keydown", function (event) {
    if (event.key !== "/" || event.metaKey || event.ctrlKey || event.altKey) return;
    var target = event.target;
    if (target && /^(INPUT|TEXTAREA|SELECT)$/.test(target.tagName)) return;
    event.preventDefault();
    search.focus();
  });

  readUrl();
  render();
})();
