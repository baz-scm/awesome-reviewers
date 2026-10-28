---
title: Eliminate duplicate logic
description: Before writing new code, search for an existing implementation of the
  same behavior in the repo (shared packages, sibling modules, or nearby methods)
  and reuse or extend it instead of re-implementing it. When you find near-identical
  blocks across functions or files — the same sequence of steps, the same git/shell/env
  check, the same "snapshot and record"...
repository: 'cline/cline

  '
label: Code Style
language: TypeScript
comments_count: 8
repository_stars: 70942
---

Before writing new code, search for an existing implementation of the same behavior in the repo (shared packages, sibling modules, or nearby methods) and reuse or extend it instead of re-implementing it. When you find near-identical blocks across functions or files — the same sequence of steps, the same git/shell/env check, the same "snapshot and record" pattern — extract the common part into a single helper or base method and let each caller supply only what differs. This keeps the codebase DRY, makes the real differences between code paths visible, and prevents drift when one copy is fixed but others are forgotten.

This also applies to the shape of the APIs you introduce while consolidating: prefer a small, named-options object over multiple positional booleans, and prefer a role/strategy object (e.g. `JsonRunOutputter` vs `ConsoleRunOutputter`) over threading `if (mode === "x")` branches through business logic. Both make call sites self-documenting and let you add a new mode/outputter without touching the core logic.

Example:
```ts
// Before: ambiguous booleans, duplicated across call sites
load(true, true)

// After: self-documenting, with sane defaults
function load({ refresh = false, userInitiated = false } = {}) { ... }
load({ refresh: true, userInitiated: true })
```

```ts
// Before: three near-identical methods reshaping the same data
discardQueue(...); recordDiscardedPrompts(...); emitDiscarded(...);

// After: one method, one shape
reportDiscardedPrompts(session, entries, reason);
```

When reviewing a PR, flag any new function, check, or git/shell/env utility that duplicates logic already present elsewhere (e.g. `getShellKind`, `normalizeGitHubRemoteUrl`, `git-preflight`), and ask the author to import/extend the existing one or move shared logic to a common location that respects the dependency graph (e.g. apps depend on core, never the reverse).</description>
</invoke>
