---
title: Merge-Aware Transformation Guards
description: 'When adding or refactoring compiler analyses/optimizations, enforce
  correctness with two practices:


  1) **Merge derived facts, don’t overwrite.** If an instruction/phi operand can contribute
  multiple sources/types/facts across passes, update the cache by *joining/merging*
  with any existing entry (e.g., join lattice values, union sources). Avoid “last
  write...'
repository: facebook/react#b5
label: Algorithms
language: TypeScript
comments_count: 7
repository_stars: 251886
---

When adding or refactoring compiler analyses/optimizations, enforce correctness with two practices:

1) **Merge derived facts, don’t overwrite.** If an instruction/phi operand can contribute multiple sources/types/facts across passes, update the cache by *joining/merging* with any existing entry (e.g., join lattice values, union sources). Avoid “last write wins” behavior that drops information.

2) **Guard structural assumptions with invariants.** Any transformation that changes control flow, value-block structure, or scoping must either (a) prove its preconditions via stronger structural checks, or (b) enforce invariants with global assertions/tests (and ensure coverage across backends).

**Application examples (pattern level):**
- Derivation-cache validations: when new derivation info is computed for an operand/value, **merge with the existing derivation** instead of replacing it.
- Control-flow rewrites (e.g., ternary constant propagation): before redirecting gotos, add a structural guard that the target block shape matches what the rewrite assumes (e.g., no incompatible nested value-block structure).
- Scoping/context checks for outlining/validation: use the correct IR semantics for “outer scope” vs “function context,” and extend the check to other instruction kinds (e.g., both LoadContext and StoreContext where relevant).
- Dependency extraction: for destructuring, ensure the dependency returned corresponds to the **correct semantic source** (e.g., destructure assigns from the `source`, so dependency should be based on `source`, not just the last extracted field).

**Concrete standard rule to adopt:**
- If you touch data-flow caches: require a merge/join function and add/keep tests that would previously fail under overwrite (multi-operand joins, loops/phis).
- If you touch rewrites: require either a structural invariant check (assertions) or a fixture that exercises the previously-assumed IR shape, and run it for both backends.
