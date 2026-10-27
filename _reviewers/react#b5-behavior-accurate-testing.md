---
title: Behavior-Accurate Testing
description: 'When adding or modifying tests, prefer behavior-accurate, end-to-end-style
  assertions over mocking internal mechanisms. Concretely:


  - Drive the code like a real user/React root: simulate the interaction from the
  outside (wrap in `act`/`actAsync`) and assert on resulting UI/state/scheduler behavior,
  not on the order of internal operation constants.'
repository: facebook/react#b5
label: Testing
language: JavaScript
comments_count: 7
repository_stars: 251886
---

When adding or modifying tests, prefer behavior-accurate, end-to-end-style assertions over mocking internal mechanisms. Concretely:

- Drive the code like a real user/React root: simulate the interaction from the outside (wrap in `act`/`actAsync`) and assert on resulting UI/state/scheduler behavior, not on the order of internal operation constants.
- Don’t silence errors in tests. Collect error callbacks and assert the observable failure reason.
- Prefer asserting the public surface instead of mocking module internals (e.g., assert the browser-level `error` event payload rather than intercepting an internal reporter).
- Use existing test utilities/helpers for assertions and dev warnings (e.g., `assertConsoleErrorDev`) rather than manual `console.error` spying.
- Use `jest.spyOn` (so `jest.restoreAllMocks()` works) and avoid brittle/time-sensitive assertions; add fake timers only when a specific timer-dependent behavior requires them.

Example (drive interaction + assert render outcome, not operation ordering):
```js
await act(async () => {
  // click-driven from the outside, like a real user
  submitFormTwiceButtonRef.current.click();
  await waitFor(['Render']);
  submitFormTwiceButtonRef.current.click();
});

// Also ensure dev-time failures/errors would be caught, not silenced.
```

This standard improves test trustworthiness (tests fail for real regressions), reduces brittleness, and keeps cleanup/maintenance predictable.