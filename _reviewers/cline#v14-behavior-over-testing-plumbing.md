---
title: Behavior over testing plumbing
description: 'When adding/changing tests, optimize for behavior/spec verification—not
  for internal implementation details or brittle harness.


  Apply this standard:

  - Prefer observable outcomes over “how it was done” metrics (e.g., process counts).
  If the only way to assert internals is heavy mocking/plumbing or cross-platform
  wrappers, rely on existing correctness/e2e...'
repository: cline/cline#v14
label: Testing
language: TypeScript
comments_count: 6
repository_stars: 70876
---

When adding/changing tests, optimize for behavior/spec verification—not for internal implementation details or brittle harness.

Apply this standard:
- Prefer observable outcomes over “how it was done” metrics (e.g., process counts). If the only way to assert internals is heavy mocking/plumbing or cross-platform wrappers, rely on existing correctness/e2e coverage instead.
- Stub at the smallest correct boundary to prevent hangs/leaked listeners. Avoid streaming fixtures that never terminate unless you also control shutdown via the right stub.
  
  ```ts
  // Bad: provide a never-ending stream and hope nothing leaks.
  // Good: stub the unit that starts execution, so the test completes deterministically.
  const runStub = sandbox
    .stub(VscodeTerminalProcess.prototype, "run")
    .resolves();
  manager.runCommand(terminalInfo, "echo hi");
  sinon.assert.calledOnce(runStub);
  ```
- Keep assertions spec-accurate. Don’t normalize/strip data in a way that can silently accept missing required groups/edge cases.
  - Example: don’t “flatten away” plural categories unless the spec explicitly allows it.
- For async/e2e tests, wait on the correct observable state transitions (UI counts, focus, button disappearance) and use timeouts only where needed (rely on defaults when appropriate).
- Don’t add tests that only lock down log payload shapes unless they’re directly tied to a behavioral contract; extra harness can make tests brittle and expensive.

Result: fewer brittle tests, less mocking complexity, and higher confidence that failures reflect real regressions.