---
title: Add Fixtures For Gaps
description: When a change claims to improve behavior (e.g., compiler metadata like
  source ranges) or affects UI behavior, ensure tests don’t just “pass”—they explicitly
  cover the remaining edge cases and configuration variants.
repository: facebook/react#b13
label: Testing
language: TypeScript
comments_count: 2
repository_stars: 251893
---

When a change claims to improve behavior (e.g., compiler metadata like source ranges) or affects UI behavior, ensure tests don’t just “pass”—they explicitly cover the remaining edge cases and configuration variants.

Apply this checklist:
1) If you can’t guarantee full correctness across all declaration/paths, either:
   - add fixtures/tests for each uncovered form (even if they currently fail), or
   - list them as follow-ups with dedicated fixture coverage so regressions are measurable.
2) For E2E tests, don’t rely on fragile positional/structural selectors (like `nth(...)`) when the UI has tabs/modes/toggles. Add stable test hooks (e.g., `data-testid`) and verify both sides of configuration switches.

Example (E2E locator using test hooks):
```ts
// Prefer stable selectors over nth() or DOM structure
const tab = page.locator('[data-testid="config-tab"]');
await tab.click();

// Add coverage for both modes
await page.goto('/?internals=on');
// assert internals UI
await page.goto('/?internals=off');
// assert internals hidden UI
```

This keeps behavior claims test-backed, makes failures reproducible, and reduces flaky E2E maintenance.