---
title: Observable, User-Realistic Tests
description: When adding or updating tests, make them exercise the real behavior path
  and assert on observable outcomes—not on mocked internal ordering or implementation
  details.
repository: facebook/react#b2
label: Testing
language: JavaScript
comments_count: 9
repository_stars: 251882
---

When adding or updating tests, make them exercise the real behavior path and assert on observable outcomes—not on mocked internal ordering or implementation details.

Apply:
- Prefer integration/user-realistic flows: trigger events/updates from the test code (e.g., click buttons) rather than embedding the whole scenario inside the component.
- Choose the correct seam: if behavior changes in the overlay/highlighting logic, assert via the hook/event that represents that output instead of using a different subsystem (e.g., profiler) that doesn’t exercise the same code path.
- Avoid internal mocking as a default: intercept public/user-visible signals (like browser `error` events) instead of mocking internal modules.
- Make assertions robust: assert the relevant state before switching modes/visibility, and grab fresh instances for subsequent assertions.
- Use shared helpers/utilities for stability: prefer `assertConsoleErrorDev` over manual `console.error` spies where possible; use Jest `spyOn` and ensure mocks restore cleanly to prevent leakage.

Example pattern (user-realistic click + act):
```js
await act(async () => {
  await waitFor(['Render']);
  submitFormTwiceButtonRef.current.click();
  await waitFor(['Render']);
  submitFormTwiceButtonRef.current.click();
});
```

Example pattern (assert the behavior’s real output seam):
```js
// Instead of asserting profiler internals, subscribe to the event that drives the overlay
unsubscribe = hook.sub('traceUpdates', nodes => {
  nodes.forEach(node => highlighted.push((node.textContent || '').trim()));
});
```

This standard reduces brittleness, avoids false positives from mismatched code paths, and makes tests easier to maintain during refactors.