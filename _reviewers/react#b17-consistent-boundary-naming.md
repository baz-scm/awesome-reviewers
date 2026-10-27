---
title: Consistent Boundary Naming
description: 'When a name is part of a boundary (public exports, semi-public types,
  encoded/wire fields, or cross-system event names), treat it like an API: keep naming
  consistent, remove legacy/typo identifiers everywhere, and avoid scattering ad-hoc
  translation logic.'
repository: facebook/react#b17
label: Naming Conventions
language: JavaScript
comments_count: 5
repository_stars: 251891
---

When a name is part of a boundary (public exports, semi-public types, encoded/wire fields, or cross-system event names), treat it like an API: keep naming consistent, remove legacy/typo identifiers everywhere, and avoid scattering ad-hoc translation logic.

Practical rules:
1) No partial renames: after changing an identifier, verify the old spelling/name has no remaining uses.
- Example risk: a misspelled prop can fall back to a default and make tests pass.
- Action: run a repo-wide search/grep for the old name and fix all call sites/fixtures.

2) Normalize at the source, not downstream.
- If you currently have repeated “remove prefix / convert naming” helpers across layers, prefer changing the upstream naming so downstream code can use the direct canonical form (reducing special cases).

3) Preserve compatibility for public/semi-public naming.
- If you must rename something that others depend on (e.g., exported API surface or option/type names), follow existing conventions and provide an explicit alias during the transition instead of removing the old name outright.

Example (alias during rename):
```js
export {Activity};
export {Activity as unstable_Activity}; // keep old name as alias
```

Example (rename typo safely):
- Rename `expectedEnviromentName` → `expectedEnvironmentName`.
- Then confirm `expectedEnviromentName` no longer exists anywhere via grep to prevent silent fallback behavior from masking missed updates.