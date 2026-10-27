---
title: Simplify code logic
description: 'Favor the simplest, most direct implementation over added complexity
  or indirection. Before introducing a helper function, extra parameter, or separate
  conditional branch, check whether the logic can be expressed more directly:'
repository: facebook/react#b19
label: Code Style
language: TypeScript
comments_count: 3
repository_stars: 251893
---

Favor the simplest, most direct implementation over added complexity or indirection. Before introducing a helper function, extra parameter, or separate conditional branch, check whether the logic can be expressed more directly:

- Avoid extracting a helper function for logic that can be expressed inline with a simple expression. For example, prefer `key: prop.originalName !== prop.newName ? ... : ...` over introducing a dedicated `isHyphenatedJsxProp()` helper when the check is trivial.
- Don't pass data as a parameter if it's already accessible through an existing reference (e.g., don't pass `env` separately if it's reachable via `hir.env`).
- Consolidate related conditional branches instead of writing separate, overlapping `if` statements. For example:
```ts
// Instead of:
if (config.validateX && !config.validateX_exp) { ... }
if (config.validateX_exp) { ... }

// Prefer:
if (config.validateX_exp) {
  ...
} else if (config.validateX) {
  ...
}
```

Simpler code is easier to read, review, and maintain. When reviewing a PR, flag unnecessary helper functions, redundant parameters, or duplicated/overlapping conditionals, and suggest the more direct alternative.