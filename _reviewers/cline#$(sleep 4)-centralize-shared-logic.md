---
title: Centralize shared logic
description: 'Before adding new logic, check whether equivalent functionality already
  exists in a shared layer (e.g. `@cline/core`, `@cline/shared`) and reuse or extend
  it instead of re-implementing it locally in an app or sidecar. Respect the dependency
  graph: shared/core packages should hold the canonical implementation, and apps may
  depend on core but never the...'
repository: cline/cline#$(sleep 4)
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 70978
---

Before adding new logic, check whether equivalent functionality already exists in a shared layer (e.g. `@cline/core`, `@cline/shared`) and reuse or extend it instead of re-implementing it locally in an app or sidecar. Respect the dependency graph: shared/core packages should hold the canonical implementation, and apps may depend on core but never the reverse. If logic is duplicated across layers with slightly different rules (e.g. two git runners with different remote-validation logic, two shell-detection helpers), consolidate it into one place so there is a single source of truth and behavior stays consistent.

This also applies within a single file: when a module accumulates a large block of logic specific to one concern (e.g. command-tool history tracking inside a generic tool-definitions file), extract it into its own well-named module rather than letting unrelated concerns pile up together. Good organization makes it obvious where functionality lives, prevents divergent re-implementations, and keeps individual files focused and readable.

Example: instead of writing a new `isPowerShellCommand` helper in `subprocess-runner.ts`, reuse the existing `getShellKind` from `@cline/shared`. Instead of building a second git snapshot/preflight runner in an app's sidecar, move the extra logic into core next to `git-preflight.ts` and import the shared implementation.