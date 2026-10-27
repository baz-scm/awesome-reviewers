---
title: Follow Canonical Names
description: 'Use established, canonical identifier names and conventions as part
  of the API/semantics contract.


  Guidelines:

  1) Treat naming/exports as compatibility surface.'
repository: facebook/react#b6
label: Naming Conventions
language: JavaScript
comments_count: 7
repository_stars: 251888
---

Use established, canonical identifier names and conventions as part of the API/semantics contract.

Guidelines:
1) Treat naming/exports as compatibility surface.
- Follow existing patterns for option/type names (e.g., `*Options`) and flag naming schemes; don’t rename public-ish types/exports without explicit compatibility intent.
- If stabilizing an identifier, keep the expected aliases (e.g., `Activity` and `unstable_Activity`) rather than removing/renaming piecemeal.

2) Prevent partial renames and silent fallbacks.
- When correcting typos or renaming props/fields, update all call sites and fixtures, and run a repo-wide search to ensure the old name no longer appears.

Example:
```js
// Bad: misspelled prop with silent fallback
const env = props.expectedEnviromentName || 'Server';

// Do: rename and ensure the old spelling is fully gone
const env = props.expectedEnvironmentName || 'Server';
// Then: git grep expectedEnviromentName (and fix any remaining uses)
```

3) Avoid duplicated ad-hoc naming normalization.
- If the same naming translation exists in many places (e.g., converting `topPress` ⇄ `press`), centralize it or remove the unnecessary prefix at the source so downstream checks become simpler.

4) Don’t bake incorrect semantics into identifiers/examples.
- If `name` values are not actually paths, don’t label them as paths in code/examples—document the real meaning (indent/structure may matter more than URL-like semantics).