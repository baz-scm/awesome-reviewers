---
title: Profile-Aware Semantic Checks
description: 'When optimizing compiler/IR transforms, treat both performance and semantic
  correctness as first-class:


  1) If you add whole-function (or multi-pass) traversals, profile/estimate the compile-time
  impact and leave a short cost note in the code so future changes don’t accidentally
  stack.'
repository: facebook/react#b14
label: Performance Optimization
language: TypeScript
comments_count: 3
repository_stars: 251893
---

When optimizing compiler/IR transforms, treat both performance and semantic correctness as first-class:

1) If you add whole-function (or multi-pass) traversals, profile/estimate the compile-time impact and leave a short cost note in the code so future changes don’t accidentally stack.
2) For scope/capture decisions, don’t rely on a single opcode as a proxy for “outer-scope usage.” Make the check context-sensitive (e.g., validate against the function expression’s context, since the same IR form can be used for other semantics).
3) For dependency tracking, ensure the value you “return” for each instruction matches the instruction’s semantics (e.g., destructuring should produce the dependency of the source, not just an arbitrary or last field), so downstream mapping remains correct and optimizations aren’t missed or repeated.

Example pattern (context-sensitive + semantics-aligned):

- Prefer checks that incorporate the function expression’s context rather than treating `LoadContext` as automatically “uncapture-safe”/“outline-unsafe.”
- For destructures, return/propagate the dependency of the `source` temp, since `x = {a, b} = source` semantically assigns from `source`.

This prevents both performance regressions from added passes and correctness issues that can force later passes to give up or do extra work.