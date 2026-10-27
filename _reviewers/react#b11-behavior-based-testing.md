---
title: Behavior-Based Testing
description: Tests should validate user-/consumer-observable behavior using the most
  appropriate public seam, avoiding mocked internal mechanics and brittle implementation
  details.
repository: facebook/react#b11
label: Testing
language: JavaScript
comments_count: 8
repository_stars: 251894
---

Tests should validate user-/consumer-observable behavior using the most appropriate public seam, avoiding mocked internal mechanics and brittle implementation details.

Apply this standard by following these rules:
- Prefer realistic interaction flows over internal operation ordering. Drive behavior the same way users do (e.g., button clicks, state updates, rerenders) and synchronize with `act`/flush helpers.
- Use the best verification seam for the actual feature output. If you’re testing an overlay/highlight, assert the overlay’s observable effect (e.g., event payloads) rather than an unrelated internal/profiler signal that can’t distinguish the regression.
- Don’t encode React/implementation details in comments or “walk boundaries”; instead assert the DOM/visibility outcome directly and in a way that’s easy to scan.
- Avoid stale references: capture fresh DOM instances per assertion phase, and assert pre- and post-conditions around mode changes.
- Mock internals only as a last resort. If possible, assert public effects (e.g., browser-level `error` event) instead of mocking internal reporting modules.
- Use existing test helpers/assertion utilities (e.g., `assertConsoleErrorDev`) and reliable mocking patterns (`jest.spyOn` + automatic restore) to prevent leaks and brittleness.

Example pattern (end-to-end user flow + observable assertions):
```js
await act(async () => {
  // Drive the same way a user would
  submitBtn.click();
  await waitFor(['Render']);
  submitBtn.click();
});

// Assert on observable UI output, not internal op ordering
expect(rootEl.textContent).toContain('...');
```

Checklist:
- Does the test fail if React internals change but observable behavior stays correct?
- Is the verification tied to the feature’s real observable output?
- Are assertions stable and based on public behavior/DOM state?
- Are mocks spies minimal and cleaned up via `restoreAllMocks`?