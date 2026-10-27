---
title: Prefer existing test utilities
description: Favor the project's established test helpers and idioms over hand-rolled
  equivalents, and verify behavior through observable/public surfaces rather than
  reaching into implementation internals.
repository: facebook/react#b20
label: Testing
language: JavaScript
comments_count: 12
repository_stars: 251895
---

Favor the project's established test helpers and idioms over hand-rolled equivalents, and verify behavior through observable/public surfaces rather than reaching into implementation internals.

Concretely:
- Use `assertConsoleErrorDev` for dev-only console.error assertions instead of manually spying on `console.error` with `jest.fn`/custom patching, unless you need to block/wait on a specific message to avoid an infinite loop — in that narrow case, document why the manual approach is necessary.
- Use `jest.fn()` + call assertions to observe behavior (e.g., event firing, handler calls) instead of pushing to ad-hoc arrays like `eventLog`.
- Use `jest.spyOn` (and `jest.restoreAllMocks` in `afterEach`) instead of manually overwriting globals (e.g., `global.requestAnimationFrame = ...`), so mocks are reliably cleaned up and don't leak across tests/environments.
- Wrap async flows and events in `act`/`actAsync` rather than raw `setTimeout`/`Promise` polling, and avoid introducing real timers or extra Promises when the existing act utilities already flush the needed work.
- Avoid mocking internal implementation modules (e.g., `jest.mock('shared/reportGlobalError', ...)`) as a shortcut; instead, assert against the actual public/observable effect (e.g., listen for the real browser `error` event). Mocking internals should be a last resort, since it couples tests to implementation details and can mask regressions in the real code path.
- When adding coverage for a bug, confirm the test exercises the actual code path the fix changes (not an adjacent one, like a different store/profiler path) — an assertion that passes "by accident" through an unrelated path isn't a valid regression test.
- Never silence errors in tests (e.g., empty `onError` handlers); capture and assert on them.

Example — preferred pattern for event assertions:
```js
const handler = jest.fn();
customElement.dispatchEvent(new CustomEvent('my-event'));
expect(handler).toHaveBeenCalledTimes(1);
```
instead of:
```js
const eventLog = [];
// ... push to eventLog manually and assert on its contents
```

Applying this consistently keeps tests resilient to refactors, reduces flakiness from leaked mocks or timers, and ensures assertions reflect genuine, user-observable behavior rather than internal plumbing.