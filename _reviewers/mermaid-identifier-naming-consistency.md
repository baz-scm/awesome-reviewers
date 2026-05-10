---
title: Identifier Naming Consistency
description: 'Use naming that is explicit, consistent, and self-describing.


  Rules:

  - Avoid magic strings for statement/type/keyword values: create named constants
  (and reuse them).'
repository: mermaid-js/mermaid
label: Naming Conventions
language: JavaScript
comments_count: 5
repository_stars: 87952
---

Use naming that is explicit, consistent, and self-describing.

Rules:
- Avoid magic strings for statement/type/keyword values: create named constants (and reuse them).
- Avoid abbreviations; prefer meaningful, intention-revealing names (e.g., `today`, `midnightDate`).
- Enforce a single identifier style for externally referenced keys/names (e.g., choose kebab-case everywhere; don’t support both camelCase and kebab-case).
- Standardize patterned generated IDs via a shared helper/function, and use template literals for readability.
- Prefer named constructs over index-based ones (e.g., named capture groups instead of `untilStatement[1]`).

Example:
```js
// Named constants (avoid magic strings)
export const STMT_STATE = 'state';
export const STMT_DIR = 'dir';

function getDirection(rootDoc) {
  const doc = rootDoc.find((d) => d.stmt === STMT_DIR);
  return doc;
}

// Shared ID generator (consistent IDs)
export const getEdgeId = (from, to, { counter = 0 } = {}) =>
  `edge_${from}_${to}_${counter}`;

// Named capture groups (clarity)
const match = /^until\s+(?<ids>[\d\w- ]+)/.exec(str);
if (match) {
  for (const id of match.groups.ids.split(' ')) {
    // ...
  }
}
```

Apply these consistently across the codebase to reduce confusion, prevent subtle mismatches (like casing), and make identifiers easier to search, understand, and maintain.