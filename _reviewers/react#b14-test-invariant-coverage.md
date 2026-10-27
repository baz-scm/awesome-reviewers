---
title: Test Invariant Coverage
description: When adding logic that promises an invariant (e.g., range/loc preservation),
  ensure tests validate the contract globally (not only for special paths), cover
  all relevant node shapes, and use robust targeting for E2E.
repository: facebook/react#b14
label: Testing
language: TypeScript
comments_count: 3
repository_stars: 251893
---

When adding logic that promises an invariant (e.g., range/loc preservation), ensure tests validate the contract globally (not only for special paths), cover all relevant node shapes, and use robust targeting for E2E.

Apply this as follows:
- Global assertions in fixtures/snapshots: if the invariant can be checked from AST node fields, assert it for every eligible node across the whole output (and run for all backends/implementations).
- Edge-case completeness or explicit follow-ups: if some syntactic forms are known to drop fields (e.g., declarations/hoisted bindings without `loc`), either extend harness coverage with fixtures for those cases or track them explicitly so the test suite documents the current boundary.
- E2E robustness: avoid brittle positional selectors (like editor `.nth(n)`); add stable `data-testid` hooks (or equivalent) and cover key UI state permutations.

Example (global range invariant check idea):
```ts
for (const node of outputAstNodes) {
  if (typeof node.start === 'number' && typeof node.end === 'number' && node.loc?.index) {
    assert(node.start === node.loc.start.index);
    assert(node.end === node.loc.end.index);
    assert(node.start <= node.end);
  }
}
```

This standard helps keep tests aligned with the true contract, prevents “green” results from only partially checking behavior, and reduces flaky E2E failures.