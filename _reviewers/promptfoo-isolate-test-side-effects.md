---
title: Isolate test side effects
description: Tests must not leak global or shared state across runs, and must not
  depend on execution order. Before mutating anything shared with the rest of the
  process — signal listeners (`SIGTERM`/`SIGINT`/`beforeExit`), module-level caches,
  environment variables, or mocks — snapshot the prior state in `beforeEach`/setup
  and restore it in `afterEach`/`finally`, even...
repository: promptfoo/promptfoo
label: Testing
language: TypeScript
comments_count: 5
repository_stars: 26565
---

Tests must not leak global or shared state across runs, and must not depend on execution order. Before mutating anything shared with the rest of the process — signal listeners (`SIGTERM`/`SIGINT`/`beforeExit`), module-level caches, environment variables, or mocks — snapshot the prior state in `beforeEach`/setup and restore it in `afterEach`/`finally`, even when the test throws. When adding listeners for a test (e.g. `process.once('SIGTERM', ...)`), remove any pre-existing listeners first so only the test's own handlers observe the emitted event, then restore the originals afterward.

Mocks must be reset between tests rather than relying on call order: use `vi.resetAllMocks()`/explicit re-implementation in `beforeEach` so a suite is correct under randomized test ordering, not just the order it happens to run in locally.

Avoid writing files or other artifacts to the repository checkout during a test run; commit required fixtures instead (e.g. config/test data files under `fixtures/`) so a test run leaves the working tree clean.

Before relying on an existing shared test harness for isolation (e.g. an in-memory DB reset between files), verify the harness actually provides the isolation needed rather than adding redundant setup/teardown, but err toward explicit local isolation when a test touches global, process-wide state.

Example:
```ts
it('cleans up on SIGTERM without ending the process', async () => {
  const saved = process.rawListeners('SIGTERM');
  process.removeAllListeners('SIGTERM');
  try {
    // ...test body registering and emitting SIGTERM...
  } finally {
    process.removeAllListeners('SIGTERM');
    saved.forEach((listener) => process.on('SIGTERM', listener));
  }
});
```