---
title: Assert via Real Behavior
description: When adding or updating tests, validate externally observable behavior
  through user-like flows or public seams. Avoid coupling to internal implementation
  details (operation order, hidden intermediate data structures, or comments that
  encode React internals). Prefer standard test utilities/mocks that make assertions
  robust and restore correctly.
repository: facebook/react#b14
label: Testing
language: JavaScript
comments_count: 6
repository_stars: 251893
---

When adding or updating tests, validate externally observable behavior through user-like flows or public seams. Avoid coupling to internal implementation details (operation order, hidden intermediate data structures, or comments that encode React internals). Prefer standard test utilities/mocks that make assertions robust and restore correctly.

Practical rules:
- Drive interactions from the outside (DOM events, root renders/updates) inside `act`, and assert on scheduler logs/visible DOM/state—not on mocked internal sequences.
- Observe the behavior that actually changes: if the bug affects an overlay, console output, or event emission, subscribe/assert that output rather than using a different internal subsystem as a proxy.
- Keep assertions implementation-agnostic: capture fresh node instances when needed and assert observable state (e.g., visibility/DOM content) directly.
- Use Jest/test utilities (`jest.fn`, `jest.spyOn`, `assertConsoleErrorDev`, etc.) instead of custom event logs or manual `console` spying.

Example pattern (user-like interaction + scheduler assertion):
```js
await act(async () => {
  Scheduler.log('Render');
  submitButtonRef.current.click();
  await waitFor(['Render']);
  submitButtonRef.current.click();
});
expect(Scheduler.unstable_clearLog()).toEqual(['Render', 'Render']);
```

If you need to validate a DevTools overlay/trace output, ensure you assert the overlay’s actual event stream (or other public interface) rather than relying on profiler/internal store data that may exercise a different code path.