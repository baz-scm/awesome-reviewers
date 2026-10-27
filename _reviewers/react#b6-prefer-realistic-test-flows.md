---
title: Prefer Realistic Test Flows
description: When writing tests, prefer driving the system through real observable
  behavior (React roots, hydration flows, and user-like interactions) instead of manually
  constructing internal operation sequences or asserting on implementation-specific
  mechanics.
repository: facebook/react#b6
label: Testing
language: JavaScript
comments_count: 6
repository_stars: 251888
---

When writing tests, prefer driving the system through real observable behavior (React roots, hydration flows, and user-like interactions) instead of manually constructing internal operation sequences or asserting on implementation-specific mechanics.

Rules:
- Drive through real flows: trigger updates from the rendered root or via user-like events, and wrap those triggers in `act` so React work is flushed.
- Assert on observable outcomes: verify user-visible/state-visible results (e.g., DOM visibility/text, store highlight sets via the hook event) rather than internal ordering/flags.
- Avoid implementation-detail encoding: don’t rely on explanatory comments that mirror React’s internal walk/markers; add straightforward assertions that a reader can scan.
- Keep assertions robust: use resilient matchers (`toContain` over brittle equality when appropriate) and capture fresh DOM instances for each assertion stage.
- Mock safely and transparently: prefer `jest.fn`/`jest.spyOn` so `jest.restoreAllMocks` works and avoid intercepting module internals unless there’s no public seam.

Example pattern (user-like interaction with `act`):
```js
await act(async () => {
  submitButtonRef.current.click();
  await waitFor(['Render']); // or waitForMicrotasks(), per test utility
  submitButtonRef.current.click();
});
```
