---
title: Be deliberate naming
description: Use consistent, contract-aware naming for any identifier that can leak
  outside its local scope (props, exported APIs/types, event names, public labels).
repository: facebook/react#b8
label: Naming Conventions
language: JavaScript
comments_count: 5
repository_stars: 251889
---

Use consistent, contract-aware naming for any identifier that can leak outside its local scope (props, exported APIs/types, event names, public labels).

**Rules**
1. **Eliminate naming typos/legacy spellings everywhere**: if you rename an identifier, ensure there are no remaining references to the old spelling, and avoid relying on silent fallbacks.
2. **Standardize names at the boundary**: if you have repeated “adapter” logic (e.g., converting naming conventions), prefer normalizing the naming at the source so downstream code doesn’t need special-case checks.
3. **Treat exported/semi-public names as stable contracts**: follow established conventions for type/option naming, and preserve compatibility with aliases when renaming public exports.
4. **Follow established semantic suffix/patterns for constants/flags**: if you deviate, explain why the semantics differ.
5. **Keep user-visible labels consistent with existing naming logic** (don’t introduce ad-hoc terms without a rationale).

**Examples**
- Verify rename propagation:
```js
// If you rename expectedEnviromentName -> expectedEnvironmentName,
// do a repo-wide check before merging.
// e.g. `git grep -n expectedEnviromentName`
```
- Preserve public API compatibility via alias:
```js
export { Activity, Activity as unstable_Activity };
```
- Avoid duplicated event naming translation by normalizing at the source (conceptually):
```js
// Prefer generating/dispatching event names without a legacy prefix
// so downstream code can consume one canonical form.
```