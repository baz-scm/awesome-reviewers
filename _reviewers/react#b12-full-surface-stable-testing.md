---
title: Full-surface, Stable Testing
description: Write tests that (1) validate invariants across the entire produced output
  for every backend/variant, and (2) keep E2E UI targeting stable and scenario-driven.
repository: facebook/react#b12
label: Testing
language: TypeScript
comments_count: 2
repository_stars: 251896
---

Write tests that (1) validate invariants across the entire produced output for every backend/variant, and (2) keep E2E UI targeting stable and scenario-driven.

Apply this in practice:
- Prefer “global” harness assertions over narrow, path-limited checks—especially when mapping/offset/range correctness is involved. Ensure the same invariant is executed for all backends.
  - Example invariant (adapt to your AST types):
    ```ts
    // For each output node with numeric start/end and a loc.index
    if (node.start != null && node.end != null && node.loc?.index != null) {
      assert(node.start === node.loc.start.index);
      assert(node.end === node.loc.end.index);
      assert(node.start <= node.end);
    }
    // Run the same harness for every backend.
    ```
- For E2E tests, avoid brittle locators like `.nth(3)` that cause “back and forth” churn.
  - Add stable selectors (e.g., `data-testid`) to UI tabs/controls, then select by test IDs.
    ```ts
    // Prefer stable, semantic selectors
    const text = await page
      .locator('[data-testid="config-tab"] .monaco-editor')
      .first()
      .allInnerTexts();
    ```
- Add scenario coverage for meaningful toggles (e.g., “internals showing” vs “not showing”) instead of relying on incidental UI ordering.

This combination reduces both correctness regressions (by widening coverage across outputs/backends) and test flakiness/maintenance cost (by making E2E selectors deterministic and scenarios explicit).