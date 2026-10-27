---
title: Prefer fixture-backed regression
description: When changing compiler/codegen behavior, add (or extend) fixture/snapshot
  coverage to lock in the full intended invariant across all supported paths/backends,
  including known edge cases; if coverage can’t be added immediately, create follow-up
  fixtures so gaps are explicitly tracked.
repository: facebook/react#b4
label: Testing
language: TypeScript
comments_count: 4
repository_stars: 251885
---

When changing compiler/codegen behavior, add (or extend) fixture/snapshot coverage to lock in the full intended invariant across all supported paths/backends, including known edge cases; if coverage can’t be added immediately, create follow-up fixtures so gaps are explicitly tracked.

Apply this as:
- **Assert the complete invariant in the shared harness** (not just a subset). Example pattern:
  ```ts
  for (const node of outputAstNodesWithNumericRanges) {
    assert(node.start === node.loc.start.index);
    assert(node.end === node.loc.end.index);
    assert(node.start <= node.end);
  }
  ```
- **Add fixtures for spec mismatches / missing metadata** (e.g., cases where `loc` is absent and the output shrinks to an identifier). Either cover them or list them as tracked follow-ups with fixtures.
- **For correctness changes that removed/altered invariants, add a minimal end-to-end repro** through the existing runtime/type integration (construct the smallest example in the shared-runtime and verify compilation/typing).
- **Keep E2E tests deterministic**: don’t rely on DOM positional indices; use stable selectors (e.g., `data-testid`) and cover key UI states (feature toggles/visibility on vs off).