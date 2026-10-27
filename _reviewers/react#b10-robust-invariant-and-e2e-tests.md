---
title: Robust Invariant and E2E Tests
description: 'Ensure tests validate the full surface area of correctness and remain
  stable over UI/implementation changes.


  - For correctness/integration tests: define the core invariant(s) and assert them
  globally (not only for special directories or partial cases) and across all relevant
  backends. Add regression tests for known offset/shift/missing-data failure modes.'
repository: facebook/react#b10
label: Testing
language: TypeScript
comments_count: 2
repository_stars: 251894
---

Ensure tests validate the full surface area of correctness and remain stable over UI/implementation changes.

- For correctness/integration tests: define the core invariant(s) and assert them globally (not only for special directories or partial cases) and across all relevant backends. Add regression tests for known offset/shift/missing-data failure modes.
- For E2E/UI tests: avoid brittle selectors like DOM index (`nth(x)`). Prefer stable selectors via `data-testid`, and cover key UI state combinations (e.g., feature toggles shown/hidden).

Example patterns:

```ts
// Global invariant check (range/offset consistency) in snapshot/AST validation
for (const node of outputAst.nodesWithRanges()) {
  if (typeof node.start === 'number' && typeof node.end === 'number' && node.loc?.index != null) {
    assert(node.start === node.loc.start.index);
    assert(node.end === node.loc.end.index);
    assert(node.start <= node.end);
  }
}

// E2E stable selection (avoid nth(x))
const editorTexts = await page
  .locator('[data-testid="config-tab"] .monaco-editor')
  .allInnerTexts();
```

Practical checklist:
1) What is the invariant the product guarantees? Assert it across the entire structure.
2) Do tests cover each backend/state combination that can diverge?
3) Are E2E selectors resilient (test IDs), and are important UI toggles exercised?
4) When a regression is found, add a targeted test that would have failed previously.