---
title: Prefer Observable Integration Testing
description: When adding/changing tests, avoid verifying internal implementation artifacts
  (mocked operation ordering, profiler internals, or React-mechanics-specific comments).
  Instead, drive behavior through real user-like flows and assert on observable, externally
  meaningful outcomes using the most direct public seam.
repository: facebook/react#b13
label: Testing
language: JavaScript
comments_count: 7
repository_stars: 251894
---

When adding/changing tests, avoid verifying internal implementation artifacts (mocked operation ordering, profiler internals, or React-mechanics-specific comments). Instead, drive behavior through real user-like flows and assert on observable, externally meaningful outcomes using the most direct public seam.

Practical checklist:
- Drive actions from the test (not inside the component) using `act(...)`, and simulate the sequence a user would do (e.g., click twice rapidly).
- Assert via observable signals: rendered DOM, DevTools-visible events/overlays, or explicit scheduler/log hooks—rather than internal operation lists.
- Pick the right seam for the behavior: if you’re testing an overlay/highlighting output, subscribe to the overlay’s event or output path (not a related subsystem that follows a different code path).
- Use existing test utilities/helpers for warnings/errors (avoid raw `console.error` spying when a helper exists).
- Keep assertions robust (prefer containment/semantic checks over brittle exact strings/structures) and ensure mocks/spies are cleaned up reliably (e.g., prefer `jest.spyOn` so `jest.restoreAllMocks` works).

Example pattern (user-like interaction + scheduler assertions):
```js
await act(async () => {
  Scheduler.log('Render');
  submitButtonRef.current.click();
  await waitFor(['Render']);

  submitButtonRef.current.click();
  await waitFor(['Render']);
});
// Then assert on the observable result (DOM text, submitted side effects, etc.)
```

This style produces tests that are harder to break during refactors and more accurate about real user-facing behavior.