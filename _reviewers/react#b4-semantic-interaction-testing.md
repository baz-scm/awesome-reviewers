---
title: Semantic Interaction Testing
description: When writing tests for React behavior, prefer **realistic interaction/behavior
  replay** and **semantic assertions** over internal sequencing, “no-throw” checks,
  or ad-hoc state.
repository: facebook/react#b4
label: Testing
language: JavaScript
comments_count: 8
repository_stars: 251885
---

When writing tests for React behavior, prefer **realistic interaction/behavior replay** and **semantic assertions** over internal sequencing, “no-throw” checks, or ad-hoc state.

**Apply this standard:**
1. **Drive from the outside (user/React root level):** Trigger the behavior via `act` and user-like events (e.g., `click`) rather than embedding the event sequence inside the component under test.
2. **Assert the invariant you actually mean:**
   - Validate externally observable output/state/visibility.
   - If the real invariant is timing/lifecycle (e.g., stays lazy until props finish), assert that directly—don’t rely solely on “the promise resolves” or “doesn’t throw”.
3. **Avoid mocking internal mechanics or ordering:** If you’re testing bridge/ops ordering or hydration internals, replace the mocked sequence with a scenario that runs through the actual React root/hydration/suspense machinery.
4. **Use existing test utilities and robust assertions:**
   - Use project helpers like `assertConsoleErrorDev`.
   - Prefer `jest.spyOn` + `jest.restoreAllMocks` for cleanup.
   - Use less brittle matchers for strings/headers (e.g., containment) and ensure matcher semantics are correct.

**Example pattern (interaction + scheduler/log assertions):**
```js
it('multiple rapid submissions do not throw and run twice', async () => {
  const submitBtn = React.createRef();

  function App() {
    return <button ref={submitBtn} onClick={() => {/* submit */}} />;
  }

  // Realistic act-driven interaction, not component-internal sequencing
  await act(async () => {
    Scheduler.log('Action');
    submitBtn.current.click();
    await waitForMicrotasks();

    Scheduler.log('Action');
    submitBtn.current.click();
  });

  assertLog(['Action', 'Action']);
});
```

This improves test resilience and correctness by verifying behavior the way React (and users) actually exercise it, and by pinning the intended contract rather than incidental outcomes.