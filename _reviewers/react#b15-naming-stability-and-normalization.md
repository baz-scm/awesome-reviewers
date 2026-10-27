---
title: Naming stability and normalization
description: When changing or introducing identifiers that are public/semantic (props,
  exported symbols, event names, dataset keys, Flow types), treat naming as a compatibility
  contract and normalize naming at the boundaries.
repository: facebook/react#b15
label: Naming Conventions
language: JavaScript
comments_count: 4
repository_stars: 251891
---

When changing or introducing identifiers that are public/semantic (props, exported symbols, event names, dataset keys, Flow types), treat naming as a compatibility contract and normalize naming at the boundaries.

Practical rules:
1) Verify identifier renames across the repo
- If you rename a prop/field (especially one with fallback defaults), confirm the old misspelling is fully removed.
- Use a repo-wide search/grep before merge; don’t rely on tests passing.

2) Normalize naming early; avoid duplicated conversion logic
- If multiple layers repeatedly translate between two naming conventions (e.g., `topPress` ↔ `press`, `top*` ↔ event names), do the normalization once at the boundary so downstream code can use a single convention.

3) Follow established naming conventions for public types/options; preserve compatibility
- Align with existing conventions (e.g., `...Options`) for externally visible Flow types.
- If consumers may still use older exported names, provide explicit aliases rather than breaking changes (e.g., export the new name and alias the old one).

4) Choose names with minification/contract safety in mind
- For runtime-keyed properties (like dataset fields), use the established access pattern that remains safe under minification/build tooling.

Example (aliasing exported names for compatibility):
```js
export {Activity, Activity as unstable_Activity};
```

Example (repo-wide rename validation):
- After renaming `expectedEnviromentName` → `expectedEnvironmentName`, run a grep across the repo to ensure the misspelled identifier is not still referenced anywhere that would otherwise trigger a silent default.