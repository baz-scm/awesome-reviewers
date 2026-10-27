---
title: Robust, State-Aware Testing
description: Write tests that (1) assert correctness across the entire produced output
  (not only a narrow subset) and across all relevant variants/backends, and (2) interact
  with the UI through stable selectors while covering key UI states.
repository: facebook/react#b9
label: Testing
language: TypeScript
comments_count: 2
repository_stars: 251891
---

Write tests that (1) assert correctness across the entire produced output (not only a narrow subset) and across all relevant variants/backends, and (2) interact with the UI through stable selectors while covering key UI states.

Apply this as two rules of thumb:

1) Broaden invariant coverage in fixture/snapshot tests
- Prefer global checks over “only runs on X” logic.
- Assert structural invariants whenever fields exist (e.g., matching start/end indices and monotonicity).
- Ensure the same assertions run for both backends.

Example pattern:
```ts
for (const node of outputAstNodes) {
  const hasRanges =
    typeof node.start === 'number' &&
    typeof node.end === 'number' &&
    node.loc?.index != null &&
    node.loc.start?.index != null &&
    node.loc.end?.index != null;

  if (!hasRanges) continue;

  // Invariant: node range matches its location mapping
  expect(node.start).toBe(node.loc.start.index);
  expect(node.end).toBe(node.loc.end.index);
  expect(node.start).toBeLessThanOrEqual(node.end);
}
```

2) Make E2E tests resilient and scenario-complete
- Avoid brittle selectors like `.nth(<number>)` for meaningful UI elements.
- Add `data-testid` attributes (or similar) and select by them.
- Add/keep tests for major app states/feature toggles (e.g., internals shown vs hidden).

Example selector approach:
```ts
const text = await page
  .locator('[data-testid="config-tab"] .monaco-editor')
  .first()
  .allInnerTexts();
```

When reviewing, verify that proposed tests either (a) expand invariant/assertion scope and run across variants, and/or (b) are stable to UI changes and cover the key user-visible states toggled by the app.