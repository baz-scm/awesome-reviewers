---
title: Null-Safe Defaults
description: Write code assuming inputs (arrays, objects, DOM nodes) may contain `undefined`,
  `null`, or “empty slots/holes”, and normalize them early with explicit defaults.
repository: freeCodeCamp/freeCodeCamp
label: Null Handling
language: Markdown
comments_count: 5
repository_stars: 444449
---

Write code assuming inputs (arrays, objects, DOM nodes) may contain `undefined`, `null`, or “empty slots/holes”, and normalize them early with explicit defaults.

**Standards**
- **Guard reads**: when locating DOM nodes or accessing optional properties, use null-safe patterns (e.g., optional chaining) and avoid assuming existence.
- **Normalize missing fields**: if a required field might be absent (e.g., `zone`), assign a deterministic default (`"general"`).
- **Handle array holes explicitly**: if your logic iterates arrays, don’t assume all indices contain values—treat holes like missing entries and decide whether to skip/compact them.
- **Test the “empty” cases**: include tests for both `undefined` values and array holes (e.g., `[, ]`), not just one.

**Example**
```js
function groupByZone(actions) {
  return actions.reduce((acc, action) => {
    const zone = action?.item?.zone ?? 'general'; // default when missing/undefined
    (acc[zone] ??= []).push(action);
    return acc;
  }, {});
}

// Null-safe DOM access
const el = document.querySelector('.container > div');
console.assert(el?.classList.contains('output'));
console.assert(el?.classList.contains('hide'));

// Example for array-hole aware compaction
function compactFragments(arr) {
  return arr.filter(Boolean); // removes undefined/null and also skips holes
}
```