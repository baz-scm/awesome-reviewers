---
title: Consolidate duplicated logic
description: Before adding new code, check whether equivalent logic already exists
  elsewhere (in a shared package, a sibling module, or a prior implementation) and
  reuse or extend it instead of writing a second copy. This applies to utility functions
  (e.g. shell-type detection, git remote handling), cross-cutting helpers (e.g. title
  inference, session formatting), and...
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Code Style
language: TypeScript
comments_count: 7
repository_stars: 70984
---

Before adding new code, check whether equivalent logic already exists elsewhere (in a shared package, a sibling module, or a prior implementation) and reuse or extend it instead of writing a second copy. This applies to utility functions (e.g. shell-type detection, git remote handling), cross-cutting helpers (e.g. title inference, session formatting), and near-duplicate methods that only differ in the shape of data they pass around — those should be collapsed into one canonical implementation. When placing shared logic, respect the dependency graph: put it in the lowest-level package that all consumers can depend on (e.g. core rather than an app), so every caller imports one source of truth.

The same principle applies to control flow: avoid threading the same conditional (e.g. `if (outputMode === "json")`) through many call sites, and avoid dispatching behavior via loosely-typed string keys (e.g. passing `"statusWriteQueue"` to select a field). Both patterns hide intent and let the compiler accept invalid input. Prefer small, explicitly named methods, or a role/strategy object constructed once (e.g. `JsonRunOutputter` vs `ConsoleRunOutputter`) with clearly named calls (`runStarted`, `runResult`), so the branch lives in one factory instead of scattered throughout the code, and so callers express intent directly rather than through a string:

```ts
// Avoid
private enqueueWrite(session, "statusWriteQueue", action) { ... }

// Prefer
private enqueueStatusWrite(session, action) {
  return this.chainWrite(session, s => s.statusWriteQueue, (s, q) => s.statusWriteQueue = q, action);
}
```

Removing duplication this way reduces line count, keeps a single place to fix bugs, and makes call sites self-documenting.</description>
