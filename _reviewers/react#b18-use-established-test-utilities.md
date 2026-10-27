---
title: Use established test utilities
description: 'Prefer the project''s existing test helpers and public, observable behavior
  over ad-hoc mocking or hand-rolled patterns. Concretely:


  - For dev warnings, use `assertConsoleErrorDev` instead of manually spying on `console.error`
  (`spyOnDev(console, ''error'').mockImplementation(...)`). Only fall back to a custom
  patch when you need to synchronize on a specific...'
repository: facebook/react#b18
label: Testing
language: JavaScript
comments_count: 10
repository_stars: 251889
---

Prefer the project's existing test helpers and public, observable behavior over ad-hoc mocking or hand-rolled patterns. Concretely:

- For dev warnings, use `assertConsoleErrorDev` instead of manually spying on `console.error` (`spyOnDev(console, 'error').mockImplementation(...)`). Only fall back to a custom patch when you need to synchronize on a specific call (e.g., to avoid an infinite loop), and even then still run the assertion through the shared helper where possible.
- For async interactions, use `act`/`actAsync`/`waitFor`-style helpers instead of raw `setTimeout`/`Promise` polling loops. If a real user action spans two renders, drive it from outside the component (e.g., `button.click(); await waitFor([...]); button.click();`) so the test exercises timing the way a user would, rather than hardcoding the race inside the component under test.
- Avoid mocking internal/private modules (`jest.mock('shared/reportGlobalError', ...)`) just to intercept how a feature is implemented. Instead, listen for the same public signal the feature produces (e.g., a browser `error` event) so the test still passes after an internal refactor.
- When stubbing globals (e.g., `requestAnimationFrame`, `IntersectionObserver`), use `jest.spyOn` rather than directly reassigning the global so `jest.restoreAllMocks()` reliably cleans it up and you don't leak state across tests/environments.
- Keep environment/mock setup centralized where the codebase already does it (e.g., `setupHostConfigs.js`) rather than splitting related mocks across multiple setup files, which can cause ordering conflicts and silently override each other.
- Match the testing style already used in the surrounding suite (e.g., exercise real end-to-end behavior rather than mocking how the code under test calls into a dependency), so new tests stay consistent and resilient to internal refactors.

Example — prefer this:
```js
it('warns for an uncached use() promise', async () => {
  // ...
  await assertConsoleErrorDev([
    'A component was suspended by an uncached promise...',
  ]);
});
```
over manually wiring a spy:
```js
it('warns for an uncached use() promise', async () => {
  spyOnDev(console, 'error').mockImplementation(() => {});
  // ...assert console.error.mock.calls manually...
});
```