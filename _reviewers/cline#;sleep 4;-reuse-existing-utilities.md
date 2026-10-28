---
title: Reuse existing utilities
description: Before adding a new helper, parser, or runner, search the codebase and
  shared/core packages for logic that already does the job, and reuse it instead of
  writing a parallel implementation. For example, `isPowerShellCommand` duplicated
  `getShellKind` from `@cline/shared`, and a new git-snapshot module duplicated remote-normalization
  and ref-reading logic that...
repository: cline/cline#;sleep 4;
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 70976
---

Before adding a new helper, parser, or runner, search the codebase and shared/core packages for logic that already does the job, and reuse it instead of writing a parallel implementation. For example, `isPowerShellCommand` duplicated `getShellKind` from `@cline/shared`, and a new git-snapshot module duplicated remote-normalization and ref-reading logic that already lived in `git-preflight.ts` and `workspace-manifest.ts`; both were removed/merged in favor of the existing code. When several internal methods perform the same operation but reshape the data differently at each call site (e.g., snapshot → list of snapshots → count), consolidate them into one method with a single, well-defined input/output shape rather than maintaining near-duplicate variants. When logic needs to be shared across apps and packages, place it in the package it logically belongs to (e.g., core/shared) and have the app import from there, respecting the dependency direction: apps may depend on core/shared, but core/shared must never depend on app code. This keeps behavior consistent, reduces maintenance surface, and avoids subtle drift between duplicate implementations.