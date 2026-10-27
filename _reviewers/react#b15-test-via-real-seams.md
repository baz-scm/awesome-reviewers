---
title: Test via Real Seams
description: Tests should validate observable behavior by driving the system like
  users/React would, using the closest stable seam, and asserting results in a way
  that doesn’t couple to internal implementation details.
repository: facebook/react#b15
label: Testing
language: JavaScript
comments_count: 7
repository_stars: 251891
---

Tests should validate observable behavior by driving the system like users/React would, using the closest stable seam, and asserting results in a way that doesn’t couple to internal implementation details.

Apply this in practice:
- Prefer end-to-end interaction over “operation ordering” or manually staged internal state.
- Use act/wait helpers to flush the real work triggered by interactions.
- Choose the closest seam that reflects the behavior you’re changing (e.g., subscribe to the feature’s event output rather than asserting on a profiler path that might not exercise the same code).
- Avoid comments (or assertions) whose purpose is to encode fragile implementation details—make the behavior scannable with direct before/after assertions.
- When asserting DOM/UI visibility changes, capture fresh instances for each visibility assertion and assert the visibility state before switching to the next mode.
- Avoid mocking internal module functions when you can assert on public/external signals.
- Use Jest spies/mocks patterns (e.g., spyOn + restore) for timing/browser APIs to avoid leaks.

Example pattern (driving a user-like action via the test harness):
```js
// Arrange: set up a stable external handle
const submitButtonRef = React.createRef();

function App() {
  return <button ref={submitButtonRef}>Submit</button>;
}

// Act: drive clicks the way a user would
await act(async () => {
  render(<App />);
  Scheduler.log('Render'); // optional: assert scheduling
  submitButtonRef.current.click();
  await waitFor(['Render']);
  submitButtonRef.current.click();
});

// Assert: verify observable result/state, not internal op order
expect(container.textContent).toContain('...');
```

Result: tests become more trustworthy (they exercise the real code paths), more maintainable (less coupling to internal mechanics), and less flaky (proper act/timing + clean mocking).