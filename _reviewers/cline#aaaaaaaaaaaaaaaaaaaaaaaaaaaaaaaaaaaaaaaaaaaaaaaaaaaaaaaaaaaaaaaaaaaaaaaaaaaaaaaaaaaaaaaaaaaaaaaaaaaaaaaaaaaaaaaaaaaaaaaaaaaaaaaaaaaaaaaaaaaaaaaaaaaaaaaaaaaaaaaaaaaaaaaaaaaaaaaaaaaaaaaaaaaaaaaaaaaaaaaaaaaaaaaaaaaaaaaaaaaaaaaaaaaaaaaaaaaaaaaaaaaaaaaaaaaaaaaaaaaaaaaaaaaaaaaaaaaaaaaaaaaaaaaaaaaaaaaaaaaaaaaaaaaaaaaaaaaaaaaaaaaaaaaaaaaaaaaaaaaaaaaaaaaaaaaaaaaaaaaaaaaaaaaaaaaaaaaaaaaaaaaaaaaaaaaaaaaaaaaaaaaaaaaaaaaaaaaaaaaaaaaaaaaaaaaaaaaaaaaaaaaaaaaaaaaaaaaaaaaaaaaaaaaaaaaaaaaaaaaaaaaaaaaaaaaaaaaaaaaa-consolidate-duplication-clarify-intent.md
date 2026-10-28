---
title: Consolidate duplication, clarify intent
description: Favor code organization that makes behavior obvious from a single, shared
  source rather than scattered across near-duplicate blocks or ambiguous call sites.
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Code Style
language: TypeScript
comments_count: 7
repository_stars: 70964
---

Favor code organization that makes behavior obvious from a single, shared source rather than scattered across near-duplicate blocks or ambiguous call sites.

- Deduplicate: when two methods share the same steps (even with slightly different framing or comments), extract the common part into one helper that both call, leaving only the genuine differences in each caller. If a helper has exactly one caller, fold it into that caller instead of keeping it separate.
- Reuse existing utilities: before writing a new helper (e.g., a shell/path check), search shared packages for an equivalent and import it instead of reimplementing it locally.
- Centralize cross-cutting logic in the correct layer of the dependency graph (e.g., a logic shared by SDK and apps belongs in the package apps depend on, not duplicated in each app) so there is one place to fix bugs or add features.
- Replace repeated conditional branching on a mode/flag (e.g., `if (config.outputMode === "json") { ... } else { ... }` sprinkled through a function) with a role/strategy object constructed once and invoked with descriptive method names, e.g.:

```ts
const outputter = createRunOutputter(config); // JsonRunOutputter | ConsoleRunOutputter
outputter.runStarted();
...
outputter.runResult(result);
```

- Avoid ambiguous positional boolean parameters; use a named options object with defaults instead, so call sites are self-documenting:

```ts
// Bad: load(true, true) — unclear which boolean means what
function load(refresh = false, userInitiated = false) {}

// Good
function load({ refresh = false, userInitiated = false } = {}) {}
load({ refresh: true, userInitiated: true });
```

Applying these practices keeps related logic in one place, makes call sites self-explanatory, and prevents subtle bugs from divergent copies of "almost the same" code.