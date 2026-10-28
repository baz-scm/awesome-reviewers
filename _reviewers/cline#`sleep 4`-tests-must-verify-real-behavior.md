---
title: Tests must verify real behavior
description: 'A test only earns trust if it can actually fail when the behavior it
  claims to cover is broken. Audit each test for these failure modes before merging:'
repository: cline/cline#`sleep 4`
label: Testing
language: TypeScript
comments_count: 11
repository_stars: 70979
---

A test only earns trust if it can actually fail when the behavior it claims to cover is broken. Audit each test for these failure modes before merging:

1. **Non-failing assertions.** Avoid matchers that short-circuit on `undefined`/missing data (e.g. `value?.should.deepEqual(...)`). Assert on the value directly (`should(value).deepEqual(...)`) so a dropped field or regression actually fails the test.

2. **Confounded fixtures.** Make sure the fixture isolates the one variable under test. If every sample fixture happens to share an incidental signal (e.g. all "retryable" error fixtures contain the word "overloaded" in both the code and the message), the test can't tell which field the implementation is actually keying off of. Use neutral fixtures and table-driven cases that vary one dimension at a time, including the "should NOT trigger" cases, to prove the real discriminator is being checked — same for exhaustive input matrices (e.g. every finish-reason × content-shape combination) where a silently-dropped case would otherwise ship unnoticed.

3. **Mocking that diverges from reality.** Don't reach for mocks that change the semantics of what's under test (e.g. mocking `child_process` in a way that breaks a promisified `execFile`, or a shell-script stub that won't run on Windows). When a safe mock isn't practical, prefer a real/integration test against the actual runtime (spin up the real process, real SDK, real entrypoint) or validate manually and document the evidence, rather than adding brittle test-only plumbing. Conversely, don't add heavy fake-harness scaffolding just to cover a few trivial lines that are already exercised by an equivalent, covered code path — skip it and say why.

4. **Test hygiene and scope.** Use the test framework's env/mock helpers for setup and teardown (`vi.stubEnv` / `vi.unstubAllEnvs`, not manual `process.env` save-restore) so state is always cleaned up, including the case where a variable was previously unset. Stub only the call that produces the side effect (e.g. the terminal process's `run`) instead of feeding fixtures that keep listeners or streams alive past the test. Keep a test suite focused on the feature's core promises; trim cases that mostly duplicate coverage already owned by another layer (e.g. overly detailed telemetry-phase assertions for errors already handled by the run loop).

Example of the non-failing-assertion trap:
```ts
// Bad: short-circuits and passes even if annotations is dropped
server.tools?.[0].annotations?.should.deepEqual({ title: "..." })

// Good: fails loudly when annotations is missing
should(server.tools?.[0].annotations).deepEqual({ title: "..." })
```