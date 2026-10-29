---
title: Meaningful, deterministic tests
description: Tests should verify real, intended behavior and must fail when that behavior
  is broken. Before adding a test, confirm it actually exercises the code path and
  would catch a regression — a test that passes even against the old/incorrect implementation
  provides no value. Assert on precise, meaningful values (actual header content,
  response body, instance...
repository: honojs/hono
label: Testing
language: TypeScript
comments_count: 15
repository_stars: 32741
---

Tests should verify real, intended behavior and must fail when that behavior is broken. Before adding a test, confirm it actually exercises the code path and would catch a regression — a test that passes even against the old/incorrect implementation provides no value. Assert on precise, meaningful values (actual header content, response body, instance types, redirect `Location`) rather than weak checks like array length, truthiness, or `null`/`not.toBeNull()`, which can hide bugs.

Avoid flakiness and non-determinism: never use `Math.random()` or other random data for test inputs, don't spin up real network servers/ports in tests (prefer mocks like `msw` to avoid port collisions), and resolve promises on the correct event (e.g. `close`, not `open`) to prevent races.

Keep the suite lean and focused: don't duplicate coverage that already exists elsewhere (e.g. in a lower-level module's own tests), remove tests unrelated to the feature/module under test, and don't over-test trivial variations — one happy-path and one failure-path case is often enough. Also ensure no `.only`/`.skip` is left in committed test code, since it silently disables other tests.

Example of a weak vs. strong assertion:

```ts
// Weak: passes even if value is wrong, or structure changes
expect(cookies.length).toBe(2)

// Strong: verifies actual content
expect(cookies).toContain('foo=bar; Path=/')
expect(cookies).toContain('foo2=bar2; Path=/')
```