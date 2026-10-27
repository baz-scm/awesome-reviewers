---
title: Test observable behavior
description: When writing tests, prefer exercising the real system behavior through
  user-facing or public seams (DOM, emitted events, overlay data, Scheduler logs),
  and assert on semantic outcomes—not on mocked internal ordering or implementation
  details.
repository: facebook/react#b10
label: Testing
language: JavaScript
comments_count: 15
repository_stars: 251894
---

When writing tests, prefer exercising the real system behavior through user-facing or public seams (DOM, emitted events, overlay data, Scheduler logs), and assert on semantic outcomes—not on mocked internal ordering or implementation details.

Practical rules:
- Use real interactions/flows: trigger the same actions a user would (clicks, rerenders, state updates) and assert externally observed effects.
- Subscribe to/inspect the actual observable output for the feature under test (e.g., an emitted `traceUpdates` event or DOM changes), rather than a related internal store that doesn’t distinguish the buggy path.
- Keep assertions robust:
  - Assert against stable, deterministic identifiers (add `key` where snapshot identity matters).
  - Avoid coupling to internal mechanics (comments/instance reuse tied to implementation). If visibility/state changes are expected, re-query elements for each assertion.
  - Prefer standard test helpers/matchers (e.g., `Scheduler.log` + `assertLog`, `assertConsoleErrorDev`, `jest.fn`/`jest.spyOn`) over ad-hoc instrumentation.
- Don’t reduce scenario coverage when updating tests; ensure you still cover the “no option / option provided” variants, etc.

Example (Scheduler-based assertions for timing/order):
```js
it('handles repeated actions', async () => {
  const {clickTwice} = setupRealUI();
  Scheduler.unstable_mockImplementation(() => {});

  // In app code, log observable milestones
  // Scheduler.log('Action'); then trigger Action twice

  await act(async () => {
    clickTwice();
    await waitForMicrotasks();
  });

  assertLog(['Action', 'Action']);
});
```