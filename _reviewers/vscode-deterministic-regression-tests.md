---
title: Deterministic Regression Tests
description: When fixing or adding behavior, update tests so they deterministically
  exercise the exact event/guard path and assert observable outcomes—never rely on
  “happy-path only” coverage.
repository: microsoft/VSCode
label: Testing
language: TypeScript
comments_count: 8
repository_stars: 194303
---

When fixing or adding behavior, update tests so they deterministically exercise the exact event/guard path and assert observable outcomes—never rely on “happy-path only” coverage.

Apply this checklist:
- Ensure tests are actually registered (e.g., in Mocha, nested `test(...)` blocks won’t run; keep them as siblings under the `suite`).
- Target the real problematic event sequence (e.g., maximization, compositionend/IME, restore gating, keyboard activation from descendants) and assert the corrected invariant (counts, focus/tab order, menu opening vs toggling).
- Add failing-closed / negative cases that must remain invalid (so future changes can’t silently loosen parsing/permission logic).
- Prefer realistic surfaces over narrow hand-rolled fakes when API surface may grow (use the same real service/provider plumbing with in-memory backing rather than a minimal custom interface).

Example patterns:
- Mocha registration:
```ts
suite('MyFeature', () => {
  test('case A', () => { /* ... */ });

  // Correct: sibling test
  test('case B', () => { /* ... */ });
});
```
- Deterministic UI assertions (focus/tab order):
```ts
// After re-render, verify which element is tabbable
assert.strictEqual(focusedActionEl.getAttribute('tabindex'), '0');
assert.strictEqual(otherActionEl.getAttribute('tabindex'), null);
```

Following this standard will prevent the common failure modes shown here: guards/event paths not covered, tests not executing, interaction regressions slipping through, and fake services drifting away from real APIs.