---
title: Modular, DRY code
description: Favor small, well-organized, non-duplicated code over large, scattered,
  or boolean-heavy implementations. When two functions share significant logic (e.g.,
  teardown sequences, shutdown steps), extract the common parts into a shared helper
  so only the real differences remain in each call site. Before writing a new utility,
  check if one already exists in a...
repository: cline/cline?x
label: Code Style
language: TypeScript
comments_count: 7
repository_stars: 70983
---

Favor small, well-organized, non-duplicated code over large, scattered, or boolean-heavy implementations. When two functions share significant logic (e.g., teardown sequences, shutdown steps), extract the common parts into a shared helper so only the real differences remain in each call site. Before writing a new utility, check if one already exists in a shared package (e.g., `getShellKind` in `@cline/shared`) and reuse it instead of reimplementing it locally. When a feature introduces many scattered conditionals (e.g., `if (config.outputMode === "json")` repeated throughout a flow), isolate the variation behind a small abstraction (such as a strategy/role object created once, e.g. `JsonRunOutputter` vs `ConsoleRunOutputter`) so the main logic reads as straight-line calls instead of threading the same branch everywhere. Keep files focused on a single concern — if a change adds a large, tool-specific or feature-specific block to a general-purpose module, split it into its own dedicated module rather than growing the original file. Also prefer descriptive, self-documenting call sites over ambiguous positional booleans: replace `load(true, true)` with an options object like `load({ refresh: true, userInitiated: true })`, using destructuring for defaults (`{ refresh = false, userInitiated = false } = {}`). These practices keep code readable, prevent silent misuse, and make intent clear at a glance.