---
title: Align With Naming Conventions
description: Use established naming conventions to make identifiers semantically accurate,
  consistent across layers, and stable for public/externally consumed APIs.
repository: facebook/react#b14
label: Naming Conventions
language: JavaScript
comments_count: 7
repository_stars: 251893
---

Use established naming conventions to make identifiers semantically accurate, consistent across layers, and stable for public/externally consumed APIs.

Guidelines:
- Match existing public naming contracts: if a name is effectively public (exported Flow types, external API exports), follow the established convention and avoid “random” renames.
- Prefer semantic/observable names: when runtime data behaves like a common type, use that common name (e.g., show “Promise” for thenables that represent promises), and only use more specific/less common labels when truly appropriate.
- Enforce pattern consistency (suffix/prefix): follow existing identifier patterns (e.g., “${ucfirst(methodName)}Options” for option types; static-flag suffix conventions). Document and justify exceptions.
- Centralize naming-convention conversions at boundaries: don’t duplicate “top vs non-top” mapping logic across the codebase—apply the canonical form at the source, then let downstream code assume it.
- Make abstractions imply behavior: if a helper’s name/role guarantees a condition, callers shouldn’t re-check the same condition.
- For renames, preserve compatibility explicitly: export both the new stable name and the old unstable name via aliasing.

Example (compatibility aliasing):
```js
export {
  Activity,
  Activity as unstable_Activity,
};
```

Example (option type naming convention):
```js
export type RenderToReadableStreamOptions = {/* ... */};
export type RenderIntoContainerOptions = {/* ... */};
```