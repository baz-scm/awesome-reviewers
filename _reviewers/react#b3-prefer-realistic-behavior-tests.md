---
title: Prefer Realistic Behavior Tests
description: When adding/modifying tests, prefer driving and asserting real, observable
  behavior through public or stable seams—rather than mocking internal sequencing
  or encoding implementation details. Keep assertions readable and robust, and use
  the project’s existing test utilities for reliability.
repository: facebook/react#b3
label: Testing
language: JavaScript
comments_count: 14
repository_stars: 251883
---

When adding/modifying tests, prefer driving and asserting real, observable behavior through public or stable seams—rather than mocking internal sequencing or encoding implementation details. Keep assertions readable and robust, and use the project’s existing test utilities for reliability.

Practical rules:
- Drive tests like users/roots: use `act` and trigger the same external interactions (clicks, rerenders, re-mounts) a real app would.
- Assert via observable seams: listen to public events or externally reported outputs (e.g., backend trace overlay events, DOM, browser `error`), not private/internal call order.
- Avoid implementation-detail “breadcrumbs”: don’t encode React/Fiber traversal rules in comments; instead make assertions explicit and locally readable.
- Re-fetch/compare correctly: when you’re asserting state transitions (like visibility), ensure you’re asserting against the current instances after each action.
- Follow harness conventions: use `spyOn`/provided assertion helpers (e.g., `assertConsoleErrorDev`) and the repo’s gating approach (`@gate`) so failures are meaningful and don’t produce pathological runs (like infinite loops).

Example patterns:

1) Drive interactions outside the component (closer to real user flow)
```js
await act(async () => {
  submitBtnRef.current.click();
  await waitFor(['Render']);
  submitBtnRef.current.click();
});
Scheduler.log('Render');
```

2) Assert via a real seam/event instead of mocking internal behavior
```js
const highlighted = [];
unsubscribe = hook.sub('traceUpdates', (nodes) => {
  nodes.forEach(n => highlighted.push((n.textContent || '').trim()));
});
// ...perform the actual state update/interaction... 
expect(highlighted).toEqual(['expected text']);
```

3) Avoid brittle assertions that only depend on exact internal details; assert the intended semantic/output
```js
expect(headers.Link).toContain('referrerpolicy="no-referrer"');
```