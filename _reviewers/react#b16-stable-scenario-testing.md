---
title: Stable scenario testing
description: 'When a change affects behavior (compiler/codegen or UI state), lock
  it down with targeted scenario coverage and make E2E tests robust:


  - For behavior/codegen changes: add a small, realistic fixture that reproduces the
  edge case and verify it through the same pipeline developers rely on (e.g., construct
  the scenario in `shared-runtime` and verify via...'
repository: facebook/react#b16
label: Testing
language: TypeScript
comments_count: 2
repository_stars: 251891
---

When a change affects behavior (compiler/codegen or UI state), lock it down with targeted scenario coverage and make E2E tests robust:

- For behavior/codegen changes: add a small, realistic fixture that reproduces the edge case and verify it through the same pipeline developers rely on (e.g., construct the scenario in `shared-runtime` and verify via `shared-runtime-type-provider`). This prevents “it compiles” regressions when invariants are relaxed.
- For UI/E2E tests: avoid brittle selectors like DOM position (`.nth(n)`) for tabs/controls. Prefer stable selectors (e.g., `data-testid`) and explicitly test both relevant app states/feature-flag variants (e.g., internals showing vs not showing).

Example (UI selector improvement):
```ts
// Prefer stable selectors over nth-index
const texts = await page
  .locator('[data-testid="config-tab"] .monaco-editor')
  .allInnerTexts();
```

Example (scenario verification intent):
```ts
// Add a small shared-runtime example that matches the tricky pattern,
// then ensure shared-runtime-type-provider accepts/types it as expected.
```