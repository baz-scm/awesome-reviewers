---
title: Prefer Behavioral Tests
description: When adding/adjusting tests, prefer behavior-level assertions driven
  by realistic interactions/root rendering and public seams (DOM, user events, public
  hooks/events). Avoid tests that validate internal implementation details (mocked
  operation ordering, module internals) or that rely on fragile assumptions.
repository: facebook/react#b1
label: Testing
language: JavaScript
comments_count: 6
repository_stars: 251878
---

When adding/adjusting tests, prefer behavior-level assertions driven by realistic interactions/root rendering and public seams (DOM, user events, public hooks/events). Avoid tests that validate internal implementation details (mocked operation ordering, module internals) or that rely on fragile assumptions.

**Rules**
- **Drive like a user/root:** Use `act` to perform real interactions (e.g., dispatch clicks, re-render, resolve data) rather than asserting on mocked internal sequences.
- **Assert what users/devtools can observe:** Verify DOM state, visibility, thrown/warn behavior, or emitted hook/event data that represents the externally visible outcome.
- **Use public seams, not internals:** Prefer subscribing to an exposed hook/event/overlay signal over mocking internal modules or relying on profiler/internals unless it truly reflects the behavior under test.
- **Keep stepwise assertions maintainable:** For each transition (e.g., visible→hidden), assert the intended state *before* and *after* the action. Don’t rely on stale node instances; capture fresh references per assertion.
- **Avoid “implementation-detail comments”:** If a reader needs the React internals to understand the assertion, rewrite the test to include clearer assertions instead.

**Example pattern (interaction + public observation)**
```js
await act(async () => {
  // realistic user interaction under act
  submitButton.click();
  await waitFor(['Render']);
  submitButton.click();
});

// assert observable outcome (DOM/state/event)
expect(screen.getByText(/Current username:/)).toBeTruthy();
```

Use this checklist: **(1) Is the test driven by a real interaction/root update? (2) Does it assert an observable outcome via a public seam? (3) Are assertions stepwise with fresh references and no reliance on internal ordering?**