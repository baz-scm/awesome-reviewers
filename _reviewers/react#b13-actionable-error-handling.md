---
title: Actionable Error Handling
description: When adding or modifying compiler validations, prevent internal inconsistencies
  from turning into unhelpful invariants, and ensure diagnostics are actionable.
repository: facebook/react#b13
label: Error Handling
language: TypeScript
comments_count: 5
repository_stars: 251893
---

When adding or modifying compiler validations, prevent internal inconsistencies from turning into unhelpful invariants, and ensure diagnostics are actionable.

**Standards**
1) **Eliminate “missing definition → invariant” paths**: if code registers IDs (e.g., shape IDs) they must always have corresponding definitions. Otherwise, detect the mismatch and emit a developer-facing diagnostic (with location/identifier context) rather than relying on an invariant that may not be surfaced.
2) **Preserve source locations for suggestions**: any intermediate structure used to later build an error *or* an automated fix should retain `loc` (and enough data to point to the relevant code). If you change a validation IR/type, update it to carry `loc`.
3) **Validate against the expected IR shape**: self-reference/shape-related checks must be derived from the actual IR structure you expect (don’t assume operands/identifiers map 1:1). If a fix is subtle, add a failing fixture to lock the correct behavior.
4) **Avoid false positives with fixture-driven changes**: when behavior changes, add a minimal failing test named `error.todo-*` for cases that should error but shouldn’t (or vice versa, per your convention). This prevents regressions and makes semantics changes reviewable.

**Example pattern** (preserve loc for better errors/suggestions)
```ts
type Aggregate = {
  kind: 'Aggregate';
  dependencies: Set<InferredDependency>;
  loc: SourceLocation; // carry through so you can later build suggestions
};
```

Apply these rules to keep errors clear, correctly surfaced, and easy to fix—especially when internal compiler state could otherwise fail via invariants or incorrect IR-shape assumptions.