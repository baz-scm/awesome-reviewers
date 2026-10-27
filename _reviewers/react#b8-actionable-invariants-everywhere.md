---
title: Actionable Invariants Everywhere
description: 'When compiler/validation logic relies on assumptions (e.g., IR shape
  correctness, scope correctness, dependency structure), handle failures explicitly
  and make diagnostics *actionable*:'
repository: facebook/react#b8
label: Error Handling
language: TypeScript
comments_count: 4
repository_stars: 251889
---

When compiler/validation logic relies on assumptions (e.g., IR shape correctness, scope correctness, dependency structure), handle failures explicitly and make diagnostics *actionable*:

- **Avoid silent invariant crashes:** If missing metadata (like an HIR “shape” entry) would cause an invariant, ensure it results in a surfaced compiler diagnostic (with a clear reason). Don’t assume external tooling (like eslint) will report it.
- **Prefer invariants for impossible states:** For conditions that “should never happen,” use `CompilerError.invariant` (or equivalent) with a **stable `reason`** and **`loc`**.
- **Preserve source locations for later fixes:** If you change internal validation structures (e.g., to add aggregates of dependencies), carry `loc` through so you can build precise automated `suggestion`s later.
- **Guard correctness-critical assumptions:** If transforming/rewriting IR to avoid invalid constructs, optionally add a targeted in-scope assertion to prevent future regressions.

Example pattern:
```ts
import {CompilerError, SourceLocation} from '..';

function require(condition: boolean, reason: string, loc: SourceLocation) {
  CompilerError.invariant(condition, {
    reason,
    loc,
  });
}

// “should never happen” state
require(startMemo == null, 'Unexpected nested memo calls', value.loc);

// When adding metadata for later suggestions
type Aggregate = { kind: 'Aggregate'; dependencies: Set<InferredDependency>; loc: SourceLocation };
```

Applying this standard typically prevents confusing runtime/invariant failures and improves users’ ability to understand and fix issues via accurate, location-aware compiler feedback.