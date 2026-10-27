---
title: Integration-Realistic Testing
description: When adding or modifying tests, prefer integration-realistic flows that
  validate observable behavior through stable public seams, rather than mocking internal
  implementation details or asserting brittle intermediate states.
repository: facebook/react#b12
label: Testing
language: JavaScript
comments_count: 11
repository_stars: 251896
---

When adding or modifying tests, prefer integration-realistic flows that validate observable behavior through stable public seams, rather than mocking internal implementation details or asserting brittle intermediate states.

Do:
- Drive behavior from the test using real user/React-root interactions (e.g., click/updates) under `act`, not by manually constructing internal operation sequences.
- Assert via observable outputs (DOM state, public events, frontend-visible logs, hook/public callbacks). If you need a seam, pick one that corresponds to the behavior you changed.
- Use scheduler/event logging for deterministic assertions when timing matters (e.g., `Scheduler.log('Render')` + `assertLog(['Render', ...])`).
- Refresh DOM node references before each visibility/state assertion when the UI may replace nodes.
- Write assertions that capture semantics, not just structure (e.g., mutability/propagation), and avoid overly brittle string equality when looser checks would suffice.
- Use Jest’s standard helpers (`jest.fn`, `jest.spyOn`) so cleanup/restoration works reliably.

Don’t:
- Don’t validate behavior by expecting a mocked/internal ordering of operations unless the public behavior itself depends on that ordering.
- Don’t rely on React/renderer implementation details as part of the test narrative (long “how React does it” comments), when you can assert the same invariant from the outside.

Example pattern (real user action + deterministic observable assertion):
```js
await act(async () => {
  Scheduler.log('Action');
  submitBtnRef.current.click();
  await waitFor(['Render']); // or waitForMicrotasks() per suite conventions
  Scheduler.log('Action');
  submitBtnRef.current.click();
});

assertLog(['Action', 'Render', 'Action', 'Render']);
// and assert on the DOM/result that the user would observe
expect(output.textContent).toContain('...');
```

This approach yields tests that are more resilient to refactors while still pinning the behavior users actually see.