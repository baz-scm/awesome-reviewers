---
title: Consistent Identifier Naming
description: 'Use consistent, standards-aligned naming for identifiers, especially
  for user-facing text/URLs and registry keys.


  - ID casing: Use `ID` (not `Id`) when it’s normal prose/descriptions; only use `Id`
  if an external API/storage contract explicitly requires it.'
repository: mermaid-js/mermaid
label: Naming Conventions
language: Markdown
comments_count: 3
repository_stars: 87952
---

Use consistent, standards-aligned naming for identifiers, especially for user-facing text/URLs and registry keys.

- ID casing: Use `ID` (not `Id`) when it’s normal prose/descriptions; only use `Id` if an external API/storage contract explicitly requires it.
- URL/path naming: Use `kebab-case` for URL segments and related identifiers that mirror URLs.
- Registry keys: Use a stable `kebab-case` canonical key for shape/component registration; if you add an alias, make it explicit and short, and keep both entries consistent with docs/config.

Example (shape registry + ID prose):
```ts
// Canonical kebab-case registry key (and optional explicit alias)
const shapes = {
  'my-new-shape': myNewShape,
  'm-nsh': myNewShape,
};

// Documentation prose should use ID
// "ID of the edge" (unless an external API contract requires "Id")
```