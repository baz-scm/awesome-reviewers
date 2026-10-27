---
title: Fail Loudly With Context
description: When introducing or relying on invariants/assumptions, ensure failures
  are (1) reachable as real diagnostics (not silent/in eslint-invisible crashes) and
  (2) actionable by preserving precise source locations.
repository: facebook/react#b7
label: Error Handling
language: TypeScript
comments_count: 5
repository_stars: 251888
---

When introducing or relying on invariants/assumptions, ensure failures are (1) reachable as real diagnostics (not silent/in eslint-invisible crashes) and (2) actionable by preserving precise source locations.

Apply this standard:
- Avoid “declared-but-undefined” references (e.g., shape ids). If something is referenced by id, it must have a corresponding definition; otherwise replace/augment with an explicit diagnostic/invariant.
- When refactoring control/data flow (new IR variants like aggregates), preserve `loc` through the transformation so later stages can create precise error messages and automated suggestions.
- When relaxing or tightening validation conditions, ensure the diagnostic condition matches semantics (e.g., primitive vs reactive behavior) to avoid false positives that push users toward incorrect fixes.
- If you remove defensive checks after proving they are unnecessary, replace them with explicit `CompilerError.invariant(...)` (including `reason` and `loc`) rather than silently continuing.

Example pattern (carry location + explicit invariant):
```ts
type Aggregate = { kind: 'Aggregate'; dependencies: Set<InferredDependency>; loc: SourceLocation };

function onStartMemoize(value: StartMemoize, deps: Set<InferredDependency>) {
  CompilerError.simpleInvariant(startMemo == null, {
    reason: 'Unexpected nested memo calls',
    loc: value.loc,
  });

  // If a derived assumption is made, fail loudly with context
  CompilerError.invariant(haveAllRequiredMetadata(), {
    reason: 'Missing derivation metadata',
    loc: value.loc,
  });
}
```

Net effect: errors become visible, specific, and fixable for users instead of surfacing as hard-to-debug invariants or silent compiler behavior.