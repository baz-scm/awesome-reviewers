---
title: Null-safe Input Contracts
description: 'When handling possibly-null/undefined/empty inputs, be explicit about
  nullability and keep code aligned with the promised types/semantics.


  Practical rules:'
repository: mermaid-js/mermaid
label: Null Handling
language: JavaScript
comments_count: 5
repository_stars: 87952
---

When handling possibly-null/undefined/empty inputs, be explicit about nullability and keep code aligned with the promised types/semantics.

Practical rules:
- Guard early for empty strings / missing values: return immediately instead of continuing with invalid state.
- Prefer nullish coalescing (`??`) over falsy checks (`||`) when `false` (or `0`) is a valid value that must not be treated as “missing”.
- Ensure return types and JSDoc contracts match reality (don’t return `undefined` when the function claims `string`).
- Before arithmetic/formatting, normalize union-like values (e.g., `number | string`) via a shared parser or an explicit `typeof` check.
- Don’t paper over typing issues caused by `null` defaults; add/propagate types so nullability doesn’t collapse inference.

Example pattern:
```js
function getStylesFromDbInfo(dbInfoItem) {
  return dbInfoItem?.styles ?? ''; // always a string
}

function useHtmlLabels(node, config) {
  // preserves false when it matters; only falls back on null/undefined
  return node.useHtmlLabels ?? config.flowchart.htmlLabels;
}

function getTasks(rawTasks, dateRange) {
  if (dateRange === '') return rawTasks; // early return on empty input

  // parse defensively
  const [startStr, endStr] = dateRange.split(',');
  // only use pieces if present
}
```

This reduces null/reference bugs and prevents subtle behavior changes caused by incorrect falsy-vs-nullish handling or mismatched return contracts.