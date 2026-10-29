---
title: Focused, precise tests
description: 'Write small, single-purpose tests that are easy to read and trust:


  - One behavior per test. Don''t combine multiple features (e.g. mixed `.arguments()`,
  `.argument()`, `.addArgument()`, or multiple options) in a single test case, since
  a failure won''t tell you which part actually broke. If you need to cover several
  similar variations, use a data-driven...'
repository: tj/commander.js#CANARY-1ebfbbf4
label: Testing
language: JavaScript
comments_count: 6
repository_stars: 28444
---

Write small, single-purpose tests that are easy to read and trust:

- One behavior per test. Don't combine multiple features (e.g. mixed `.arguments()`, `.argument()`, `.addArgument()`, or multiple options) in a single test case, since a failure won't tell you which part actually broke. If you need to cover several similar variations, use a data-driven approach (e.g. `test.each`) instead of cramming them into one test or copy-pasting many near-duplicate tests.
- Keep test setup minimal and put tests in the file/describe block that matches the behavior under test. Don't add incidental complexity (like an unnecessary subcommand) just because a nearby test happened to use it — only add what's needed to exercise the behavior being verified.
- Suppress expected error/warning output using the library's own configuration hooks rather than hand-rolled mocks of `stdout`/`stderr`. For example:

```js
const program = new commander.Command()
  .exitOverride()
  .configureOutput({ writeErr: () => {} });
```

Prefer a shared test helper (e.g. `createTestCommand()`) over repeating this suppression boilerplate in every test file.

- Assert the most precise value that matches the documented contract. Use `toBe(true)` rather than `toBeTruthy()` when the API is specifically documented/expected to return `true`, so a regression that changes the value to some other truthy result is caught.
- In async or callback-based tests, add `expect.hasAssertions()` at the start to guarantee the test actually performed its assertions before resolving/completing, protecting against silently-passing tests where the assertion callback was never invoked.

Following these practices keeps failures diagnosable, avoids brittle or misleading tests, and keeps test output clean and meaningful.</description>
