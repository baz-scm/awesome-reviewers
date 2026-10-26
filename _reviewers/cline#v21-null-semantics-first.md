---
title: Null Semantics First
description: 'Treat `null`/`undefined` as intentional states, not incidental absence.


  Apply these rules:

  1) Align types with runtime: if your code normalizes `null` to omission (or vice
  versa), make the function signature and downstream checks match that reality.'
repository: cline/cline#v21
label: Null Handling
language: TypeScript
comments_count: 4
repository_stars: 70886
---

Treat `null`/`undefined` as intentional states, not incidental absence.

Apply these rules:
1) Align types with runtime: if your code normalizes `null` to omission (or vice versa), make the function signature and downstream checks match that reality.
2) Normalize early: convert incoming `null | undefined` into a single internal representation (e.g., `undefined` or a dedicated state) before branching.
3) Avoid silent fallbacks when semantics differ: if missing inputs change behavior (credentials resolution, config disable precedence, option application), do not let defaults kick in invisibly—either preserve the intended legacy behavior or model an explicit “unknown/absent” outcome.
4) Be exact with external systems: some runtimes bind “missing” differently (e.g., DB named params). Pass the exact required tokens and add targeted tests for that runtime.

Example (aligning signature + normalization):
```ts
type Input = { reasoning?: { enabled?: boolean } | null };

function resolveReasoning(req: Input): 'none' | undefined {
  // Normalize before applying defaults
  const enabled = req.reasoning?.enabled;
  if (enabled === false) return 'none';
  if (enabled === undefined) return undefined;
  // ...
  return undefined;
}
```