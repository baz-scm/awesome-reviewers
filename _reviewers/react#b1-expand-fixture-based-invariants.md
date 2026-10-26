---
title: Expand fixture-based invariants
description: 'When testing correctness properties (like source ranges/`loc` preservation),
  make your assertions broad and your fixtures targeted.


  Apply this standard:'
repository: facebook/react#b1
label: Testing
language: TypeScript
comments_count: 3
repository_stars: 251878
---

When testing correctness properties (like source ranges/`loc` preservation), make your assertions broad and your fixtures targeted.

Apply this standard:
1) Assert invariants across the full output: use a shared harness/snapshot test that checks every applicable output node (not just specific subtypes like declarations in a folder), for all backends (e.g., TS + Rust).
2) Cover edge node shapes: if some declarations/constructs legitimately lack `loc` (e.g., initializer-less hoisted `let x;`, for-in/for-of declarators), either add fixtures that capture the expected behavior or explicitly list them as tracked follow-ups so coverage doesn’t silently stop.
3) Keep E2E tests stable: avoid brittle positional selectors (`nth(...)`) when UI structure changes; add stable `data-testid`/testID hooks and include key mode coverage (e.g., internals shown vs hidden).

Example (invariant-style fixture check):
```ts
// In a shared snapshot/fixture harness
function assertRangeInvariant(node: any) {
  const hasNumeric = typeof node.start === 'number' && typeof node.end === 'number';
  const hasLocIndex = node.loc?.start?.index != null && node.loc?.end?.index != null;
  if (!hasNumeric || !hasLocIndex) return;

  expect(node.start).toBe(node.loc.start.index);
  expect(node.end).toBe(node.loc.end.index);
  expect(node.start).toBeLessThanOrEqual(node.end);
}

for (const node of allRelevantOutputNodes(ast)) {
  assertRangeInvariant(node);
}
```
