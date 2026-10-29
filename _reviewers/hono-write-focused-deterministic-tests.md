---
title: Write focused, deterministic tests
description: 'Keep the test suite lean and trustworthy by following these rules:


  1. **Avoid redundancy.** Before adding a test, check whether the behavior is already
  covered elsewhere (e.g. in another test file or an existing case). Don''t add near-duplicate
  tests (e.g. many permutations of header-based auth) when one success and one failure
  case already prove the logic...'
repository: HONOJS/HONO
label: Testing
language: TypeScript
comments_count: 13
repository_stars: 32741
---

Keep the test suite lean and trustworthy by following these rules:

1. **Avoid redundancy.** Before adding a test, check whether the behavior is already covered elsewhere (e.g. in another test file or an existing case). Don't add near-duplicate tests (e.g. many permutations of header-based auth) when one success and one failure case already prove the logic works. Remove assertions that don't add new information (e.g. asserting a type is `NotEqual<any>` when a stronger follow-up assertion already proves the exact type).

2. **Make assertions meaningful.** A test must actually fail against the old/buggy implementation — don't write a test that passes regardless of the fix. Assert on concrete values, not just counts or truthiness:
   ```ts
   // Bad
   expect(cookies.length).toBe(2)

   // Good
   expect(cookies.includes('foo=bar; Path=/')).toBe(true)
   expect(cookies.includes('foo2=bar2; Path=/')).toBe(true)
   ```

3. **Keep tests deterministic and isolated.** Never rely on `Math.random()`, real timers, or other non-deterministic input, since this can cause tests to fail intermittently. Avoid spinning up real network servers/ports in tests (which can collide with other processes); instead mock HTTP calls with a library like `msw`:
   ```ts
   const server = setupServer(
     http.get('http://localhost/.well-known/jwks.json', () => HttpResponse.json({ keys }))
   )
   beforeAll(() => server.listen())
   afterEach(() => server.resetHandlers())
   afterAll(() => server.close())
   ```

4. **Never commit focused/skipped tests.** Remove `it.only`, `describe.only`, or `.skip` before merging — these silently disable the rest of the suite in CI.

Applying these rules keeps the suite fast, reliable, and genuinely protective against regressions.