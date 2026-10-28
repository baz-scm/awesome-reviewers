---
title: Eliminate duplicated logic
description: Before adding new logic, check whether it already exists elsewhere in
  the codebase (a shared utility, a sibling module, or another method on the same
  class) and reuse or extend it instead of reimplementing it. When review reveals
  that two or more code paths contain near-identical blocks — the same sequence of
  statements, the same conditional check, the same...
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Code Style
language: TypeScript
comments_count: 7
repository_stars: 70986
---

Before adding new logic, check whether it already exists elsewhere in the codebase (a shared utility, a sibling module, or another method on the same class) and reuse or extend it instead of reimplementing it. When review reveals that two or more code paths contain near-identical blocks — the same sequence of statements, the same conditional check, the same cleanup steps — refactor them into a single shared function or method, leaving each call site with only its true differences.

This applies at several levels:
- Utility functions: don't hand-roll a check that already lives in a shared package (e.g. writing a bespoke `isPowerShellCommand` when `getShellKind` from `@cline/shared` already does it, or re-implementing git remote/branch normalization that already exists in `git-preflight.ts`).
- Conditional branches: when a condition needs an exception, extend the existing condition rather than duplicating it with slightly different logic (`if (isAzure && !isDeepseek)` instead of a parallel `if (isDeepseek)` branch).
- Methods/classes: when multiple methods repeat the same setup/teardown sequence with the same comments explaining "why", extract the common steps into one method (e.g. a shared `beginTeardown`/`shutDownSessionRuntime` helper) and keep only the distinct remainder in each caller.
- Cross-module placement: if logic is being duplicated because a lower layer doesn't expose it, move the logic to the appropriate shared layer (respecting the dependency direction, e.g. apps depend on core, never the reverse) so all consumers share one implementation.

Doing this consistently keeps behavior from drifting between "copies" of the same logic, reduces the surface area reviewers and future maintainers must reason about, and typically shrinks the diff (e.g. a refactor that collapses duplicated teardown logic can net negative lines while clarifying intent).