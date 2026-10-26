---
title: Safe Input Lookup
description: When you map potentially attacker-influenced strings (file paths, extensions,
  names, command/menu paths) to behavior via plain objects, harden both the lookup
  and the normalization.
repository: cline/cline#v14
label: Security
language: TSX
comments_count: 4
repository_stars: 70876
---

When you map potentially attacker-influenced strings (file paths, extensions, names, command/menu paths) to behavior via plain objects, harden both the lookup and the normalization.

**1) Only accept own keys in lookup tables**
Use `Object.hasOwn` (or an equivalent own-key check) so values like `__proto__`, `constructor`, `toString`, etc. can’t be resolved through inherited properties.

```ts
type IconSpec = { icon: unknown; className: string };
const BY_EXTENSION: Record<string, IconSpec> = { ts: { icon: {}, className: "..." } };
const NEUTRAL: IconSpec = { icon: {}, className: "text-muted-foreground" };

export function iconForPath(path: string): IconSpec {
  const name = path.split(/[\\/]/).pop() ?? path;
  const ext = name.includes(".") ? (name.split(".").pop() ?? "").toLowerCase() : "";

  // Own-property guard against prototype/inherited-member abuse
  if (Object.hasOwn(BY_EXTENSION, ext)) return BY_EXTENSION[ext];
  return NEUTRAL;
}
```

**2) Normalize cross-component strings before lookup/dispatch**
If different parts of the system normalize differently (menu path vs runner path), you can get mismatches that undermine security intent. Normalize the same way everywhere (e.g., `trim()`, basename extraction, consistent case) *before* building lookup keys and before inspection/execution.

```ts
const normalizedMenuPath = menuPath.trim();
// use normalizedMenuPath for both inspection and execution
```

**3) Keep security settings text precise**
If there is a sandbox/authorization boundary (read vs command-write, toolchain access vs project-only mutation), ensure the UI copy matches what’s actually enforced, including execution context (e.g., background executor vs terminal).