---
title: Stable, Contract-Driven Tests
description: 'When changing behavior, write tests that are (a) stable, (b) contract-complete,
  and (c) isolated—using the right test level.


  - Avoid brittle “test plumbing” that tightly couples to OS/process details. If the
  only way to assert something is to mock core environment primitives (e.g., child_process)
  or rely on shell PATH hacks (breaking on Windows), prefer...'
repository: cline/cline#v6
label: Testing
language: TypeScript
comments_count: 7
repository_stars: 70864
---

When changing behavior, write tests that are (a) stable, (b) contract-complete, and (c) isolated—using the right test level.

- Avoid brittle “test plumbing” that tightly couples to OS/process details. If the only way to assert something is to mock core environment primitives (e.g., child_process) or rely on shell PATH hacks (breaking on Windows), prefer validating user-visible correctness instead.
- Use wire/adapter-level tests when the bug is in request wiring or real integration (e.g., real adapter + stubbed fetch) rather than over-mocking internal types.
- Keep tests deterministic and leak-free: stub the minimal surface so background work (never-ending streams, event listeners, process hooks) can’t outlive the test.
- Assert the true contract precisely (exact exported versions/values; required locale plural categories; required telemetry field updates). Don’t “paper over” missing cases with overly-permissive normalization.
- Apply regression-test-first: write a failing test that reproduces the exact incorrect state/field propagation, then fix, ensuring the state is reset/isolated between turns.
- Don’t add brittle tests for incidental formatting/shape (e.g., exact log JSON payload fields) when the behavioral path is already covered by existing integration/server tests—focus assertions on behavior that would regress.

Example (leak-free stub + reveal-only behavior):
```ts
it("reveals without taking focus", () => {
  const showStub = sandbox.stub();
  const terminalInfo = {
    id: 1,
    busy: false,
    lastCommand: "",
    lastActive: Date.now(),
    terminal: {
      shellIntegration: {
        executeCommand: () => ({
          read: () => createNeverEndingStream(),
        }),
      },
      show: showStub,
    },
  } as unknown as vscode.Terminal;

  manager.runCommand(
    terminalInfo as unknown as Parameters<typeof manager.runCommand>[0],
    "echo hi"
  );

  sinon.assert.calledOnceWithExactly(terminalInfo.terminal.show as sinon.SinonStub, true);
});
```