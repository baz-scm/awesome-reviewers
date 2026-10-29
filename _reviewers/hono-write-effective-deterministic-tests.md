---
title: Write effective, deterministic tests
description: 'Every test must genuinely validate the behavior it claims to cover,
  run deterministically, and avoid noise from redundant or stale cases.


  - **Verify the test actually fails without the fix.** Before adding a regression
  test, temporarily revert the fix and confirm the test fails. A test that passes
  on both old and new code gives false confidence (e.g....'
repository: honojs/Hono
label: Testing
language: TypeScript
comments_count: 10
repository_stars: 32741
---

Every test must genuinely validate the behavior it claims to cover, run deterministically, and avoid noise from redundant or stale cases.

- **Verify the test actually fails without the fix.** Before adding a regression test, temporarily revert the fix and confirm the test fails. A test that passes on both old and new code gives false confidence (e.g. asserting `cookies.length` instead of the actual cookie values, or asserting generic type inequality instead of the concrete expected type).
- **Assert concrete expected values, not just shape or count.** Prefer `expect(cookies).toContain('foo=bar; Path=/')` over `expect(cookies.length).toBe(2)`, and prefer `toBeInstanceOf(ALBProcessor)` over a loose truthy check.
- **Keep tests deterministic and isolated.** Never use `Math.random()`, real network ports, or timing-dependent assumptions in tests — use fixed/mocked values (e.g. mock HTTP servers with `msw` instead of spinning up a real server on a fixed port, which can collide with other processes), and make sure async event listeners resolve on the correct event (e.g. resolve on `close`, not `open`, when testing a close handshake).
- **Avoid redundant or misplaced tests.** Don't add a test that duplicates existing coverage (e.g. a `::` case already covered by a trailing-`::` test), and don't add tests to a module's suite that belong elsewhere (e.g. generic request-cloning tests inside `validator.test.ts`). Do not remove existing tests without a replacement unless the behavior they cover is actually gone.
- **Cover meaningful edge cases, including negatives and defaults.** When adding a feature, also test the "off"/default case (e.g. verify no `report-uri` is emitted when unspecified) and boundary inputs (empty input, single-element arrays, trailing slashes, etc.).
- **Clean up test artifacts before merging.** Remove stray `.only()`/`.skip()` calls, debug `console.log`/`console.debug` statements, and unused scaffolding. If `any` is intentionally used in a test, suppress the lint warning explicitly (`// eslint-disable-next-line @typescript-eslint/no-explicit-any`) rather than leaving a warning.

Example of a weak vs. strong test:
```ts
// Weak: passes even with the bug, and only checks length
it('keeps previous cookies', () => {
  const res = c.json({ message: 'Hello' })
  expect(res.headers.getSetCookie().length).toBe(2)
})

// Strong: verifies actual values, would fail without the fix
it('keeps previous cookies', () => {
  const res = c.json({ message: 'Hello' })
  const cookies = res.headers.getSetCookie()
  expect(cookies).toContain('foo=bar; Path=/')
  expect(cookies).toContain('foo2=bar2; Path=/')
})
```