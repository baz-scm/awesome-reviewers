---
title: Behavior-Driven Test Standards
description: When writing tests, drive React/code under test in a way that matches
  real-world usage, assert via externally observable outcomes, and avoid coupling
  to internal implementation details or brittle intermediate structures.
repository: facebook/react#b8
label: Testing
language: JavaScript
comments_count: 7
repository_stars: 251889
---

When writing tests, drive React/code under test in a way that matches real-world usage, assert via externally observable outcomes, and avoid coupling to internal implementation details or brittle intermediate structures.

Apply these rules:
- Exercise the real integration path: prefer behavior in an actual root/render/hydration scenario over “mocked operations order” or internal sequence simulation.
- Drive user-like actions from the test (not from hidden component internals), inside proper `act(...)` scopes, and wait for observable completion.
- Assert using public/observable signals (logs, events, UI state) rather than internal counters or assumptions about internal steps.
- Avoid encoding React implementation details in comments/logic; assert state transitions that matter to users (e.g., visibility) instead.
- Prefer the best seam to observe what the feature actually produces (e.g., subscribe to the trace/highlight output event rather than profiler internals when the goal is the overlay).
- Keep assertions resilient to formatting/ordering where exact structure isn’t semantically important (use containment/looser matchers when appropriate).
- Use safe mocking patterns (`jest.spyOn` + `jest.restoreAllMocks`) to prevent leaks.

Example pattern (user-like interaction + observable assertion):
```js
await act(async () => {
  // Trigger like a real user
  Scheduler.log('Render');
  submitButtonRef.current.click();
  await waitFor(['Render']);
  submitButtonRef.current.click();
});

// Or, if asserting counts/order:
Scheduler.log('Action');
expectLog(['Action', 'Action']);
```

This improves test stability, correctness, and maintainability by aligning tests with the contract users (or the next integration layer) actually observe.