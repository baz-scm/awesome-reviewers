---
title: surface failures early
description: 'Make rendering/runtime failures observable instead of silently tolerated.


  Apply two concrete rules:

  1) **Cover failure-prone inputs in tests**: when your code parses special syntaxes
  (e.g., `@{ ... }` blocks), add variations that stress spacing/quoting/formatting
  so broken input is exercised.'
repository: mermaid-js/mermaid
label: Error Handling
language: JavaScript
comments_count: 2
repository_stars: 87952
---

Make rendering/runtime failures observable instead of silently tolerated.

Apply two concrete rules:
1) **Cover failure-prone inputs in tests**: when your code parses special syntaxes (e.g., `@{ ... }` blocks), add variations that stress spacing/quoting/formatting so broken input is exercised.

2) **Don’t swallow async dependency errors**: if loading external assets/fonts fails, avoid `try/catch` that only logs. Either let the promise reject (so Cypress/test fails) or rethrow after adding context.

Example (preferred: errors surface and tests fail):
```js
async function contentLoaded() {
  await loadFontAwesomeCSS();
  await Promise.all(Array.from(document.fonts, (font) => font.load()));
}
```

Example (log *and* propagate):
```js
const contentLoaded = async () => {
  try {
    await loadFontAwesomeCSS();
    await Promise.all(Array.from(document.fonts, (font) => font.load()));
  } catch (err) {
    console.error('Error loading fonts', err);
    throw err;
  }
};
```

Outcome: developers get a clear stack/error when something breaks, and tests/CI catch edge-case syntax issues instead of only validating the happy path.