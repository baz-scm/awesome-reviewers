---
title: Test via public behavior
description: Tests should exercise and assert on public, observable behavior rather
  than reaching into internal implementation details, and should use the project's
  established test utilities instead of hand-rolled equivalents.
repository: facebook/react#b19
label: Testing
language: JavaScript
comments_count: 6
repository_stars: 251893
---

Tests should exercise and assert on public, observable behavior rather than reaching into internal implementation details, and should use the project's established test utilities instead of hand-rolled equivalents.

Concretely:
- Never mock internal module implementations as a way to observe behavior (e.g. `jest.mock('shared/reportGlobalError', ...)`). Instead, listen for the actual public signal the code produces (a DOM `error` event, a callback, a public API), so the test still passes if the internal implementation changes but breaks if the real external contract breaks.
- When asserting dev warnings, use the shared helper (`assertConsoleErrorDev`) instead of manually spying on `console.error`:
  ```js
  // Avoid
  spyOnDev(console, 'error').mockImplementation(() => {});

  // Prefer
  assertConsoleErrorDev([
    'Expected warning message',
  ]);
  ```
  Only fall back to manual console patching when you genuinely need to synchronize on a specific call (e.g. to avoid an infinite loop while waiting for a particular message), and even then still validate the message content.
- When spying on globals/browsers APIs (e.g. `requestAnimationFrame`, `IntersectionObserver`), use `jest.spyOn` rather than directly reassigning the global. This ensures `jest.restoreAllMocks()` in `afterEach` properly tears down the mock and prevents leaking it into other tests/environments.
- Never silence errors from the code under test (e.g. passing a no-op `onError`). Collect errors/rejections and assert on them explicitly so regressions that introduce new errors are caught rather than hidden.

Applying this consistently keeps tests resilient to refactors, prevents false negatives from swallowed errors, and keeps assertions aligned with how the code is actually used in production.