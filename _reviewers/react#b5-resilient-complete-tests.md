---
title: Resilient, Complete Tests
description: When a change has a clear behavioral guarantee, don’t stop at the “happy
  path.” Add targeted fixtures/coverage for known special cases, and for e2e UI flows,
  avoid brittle selectors and cover important state permutations.
repository: facebook/react#b5
label: Testing
language: TypeScript
comments_count: 2
repository_stars: 251886
---

When a change has a clear behavioral guarantee, don’t stop at the “happy path.” Add targeted fixtures/coverage for known special cases, and for e2e UI flows, avoid brittle selectors and cover important state permutations.

Apply as:
1) Coverage for guarantees + edge cases
- If the promise is “declarator ranges/`loc` are preserved,” ensure tests assert it for special forms (e.g., hoisted `let x;`, `for-in`/`for-of` declarators, context/scope-related declarations). 
- If you can’t fully cover them immediately, explicitly create follow-up items and include fixtures that isolate each uncovered case.

2) E2E selector resilience + state-mode tests
- Prefer stable selectors over index-based DOM queries (e.g., avoid `nth(3)` when the UI can reorder).
- Add `data-testid` to interactive tabs/containers so the test targets the correct editor reliably.
- Add coverage for key modes/toggles (e.g., start the app with “internals” shown and hidden).

Example (e2e selector + state mode):
```ts
// Prefer data-testid over nth()
const editorTexts = await page
  .locator('[data-testid="config-tab"] .monaco-editor')
  .allInnerTexts();

// Test both UI modes
await app.start({ showInternals: true });
await expect(editorTexts).toContain(/* ... */);

await app.start({ showInternals: false });
await expect(/* ... */).not.toContain(/* ... */);
```

Example (fixture follow-up for range/loc):
- Create a fixture that includes each declaration form where `loc` is currently missing, and assert `declarator`/identifier ranges for each variant; if incomplete, track remaining variants as follow-ups with those fixtures.