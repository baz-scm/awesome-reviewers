---
title: Prefer observable behavior tests
description: When adding or updating tests, assert the behavior a real user/devtools/consumer
  would observe—avoid tests that only verify internal sequencing, profiler bookkeeping,
  or mocked module internals.
repository: facebook/react#b17
label: Testing
language: JavaScript
comments_count: 12
repository_stars: 251891
---

When adding or updating tests, assert the behavior a real user/devtools/consumer would observe—avoid tests that only verify internal sequencing, profiler bookkeeping, or mocked module internals.

Apply this by:
- Drive behavior through the actual public API/renderer/root (e.g., render in a real React root) rather than constructing expected internal operation orders.
- Trigger actions from the test harness (wrap in `act`) to simulate user interaction timing, then assert the observable result (DOM changes, store snapshots, scheduler logs, or emitted events).
- Prefer assertions based on externally reported outputs/events over “seams” that might not exercise the changed code path.
- Avoid brittle coupling to implementation details (including comments that effectively document internal mechanics); assert pre/post state transitions instead.
- Use existing project test utilities for logs/warnings/console assertions rather than ad-hoc spies.

Example (move interaction + assert via Scheduler log):
```js
await act(async () => {
  Scheduler.log('Render');
  submitFormTwiceButtonRef.current.click();
  await waitFor(['Render']);
  Scheduler.log('Render');
  submitFormTwiceButtonRef.current.click();
});
assertLog(['Render', 'Render']);
```

If you must inspect internals, treat it as a last resort and confirm the test still proves the externally observable behavior changed (not just that an internal data structure looks right).