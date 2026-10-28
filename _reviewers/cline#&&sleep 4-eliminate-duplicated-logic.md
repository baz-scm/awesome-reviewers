---
title: Eliminate duplicated logic
description: When two or more code paths repeat the same steps, comments, or conditional
  branches, factor the shared behavior into a single helper, module, or role object
  instead of letting copies drift. Before writing new logic, check whether an equivalent
  utility already exists in a shared package (e.g. `@cline/shared`) and import it
  rather than reimplementing it...
repository: cline/cline#&&sleep 4
label: Code Style
language: TypeScript
comments_count: 7
repository_stars: 70980
---

When two or more code paths repeat the same steps, comments, or conditional branches, factor the shared behavior into a single helper, module, or role object instead of letting copies drift. Before writing new logic, check whether an equivalent utility already exists in a shared package (e.g. `@cline/shared`) and import it rather than reimplementing it locally.

Concretely:
- If two functions begin or end with the same sequence of statements (e.g. `beginTeardown` setting flags and emitting fallback events in both `shutdownSession` and `releaseSessionRuntime`), move that sequence into one function both callers invoke, leaving each caller with only its real differences.
- Replace repeated `if (config.someMode === "x") { ... } else { ... }` branches scattered through a code path with a single factory that constructs the right strategy/role object (e.g. a `RunOutputter` built once as `JsonRunOutputter`/`ConsoleRunOutputter`), so the rest of the code makes straight-line calls instead of threading conditionals.
- Don't hand-roll logic that a shared package already exports (e.g. a bespoke `isPowerShellCommand` when `getShellKind` in `@cline/shared` already does the check) — import and reuse it, and drop now-unneeded imports.
- When a file grows into several unrelated concerns (naming, color parsing, theming, zoom, PNG export, etc.), split it into focused submodules grouped by domain, and keep the original entry point as a thin re-export façade so existing imports keep working.
- When logic needs to be shared across packages/apps, place it at the correct layer of the dependency graph (e.g. in a lower-level package like `@cline/core`) so every consumer imports one canonical implementation instead of each maintaining its own copy.

Applying this consistently keeps behavior in one place, shrinks diffs, and makes the real differences between similar code paths easy to spot.