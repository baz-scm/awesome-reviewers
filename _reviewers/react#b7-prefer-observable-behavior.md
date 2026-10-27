---
title: Prefer observable behavior
description: When adding or updating tests, assert the externally observable behavior
  the change is meant to affect. Avoid brittle coupling to internal implementation
  details, assumed operation ordering, or mocking deep internals when there’s a public/observable
  seam.
repository: facebook/react#b7
label: Testing
language: JavaScript
comments_count: 9
repository_stars: 251888
---

When adding or updating tests, assert the externally observable behavior the change is meant to affect. Avoid brittle coupling to internal implementation details, assumed operation ordering, or mocking deep internals when there’s a public/observable seam.

Practical rules:
- Use real interaction flows (e.g., DOM click + Scheduler/act/log assertions) rather than embedding sequencing logic inside components.
- Validate through the actual behavior seam (events/UI state as users/devtools observe it), not indirect signals that may exercise different code paths.
- Don’t rely on React/internal implementation comments or specific internal ordering; instead assert the state transitions you expect.
- Keep assertions robust: capture fresh instances for “before/after” checks, and use existing assertion utilities (e.g., console error helpers) plus Jest spyOn for clean restoration.

Example pattern (user-like interaction + observable logging):
```js
import {act} from 'internal-test-utils';
import {waitFor} from 'internal-test-utils';
import {Scheduler} from 'scheduler';

it('handles rapid repeated submits without throwing', async () => {
  const buttonRef = React.createRef();

  await act(async () => {
    buttonRef.current.click();
    Scheduler.unstable_flushAllWithoutAsserting?.();
    await waitFor(['Render']);
    buttonRef.current.click();
  });

  // Prefer asserting what actually happened (renders/logs), not internal ordering.
  expect(Scheduler.log).toEqual(['Render', 'Render']);
});
```

Result: fewer flaky tests, better regression coverage, and tests that explain the intended behavior rather than React internals.