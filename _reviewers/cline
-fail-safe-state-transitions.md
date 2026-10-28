---
title: Fail-safe state transitions
description: When an operation can fail, don't commit or mutate shared state until
  the operation has actually succeeded, and don't infer failure/success conditions
  from fragile signals like string-matching error messages. Instead, explicitly validate
  preconditions up front and only transition state after the risky step completes
  successfully.
repository: "cline/cline\r\n"
label: Error Handling
language: TSX
comments_count: 3
repository_stars: 70946
---

When an operation can fail, don't commit or mutate shared state until the operation has actually succeeded, and don't infer failure/success conditions from fragile signals like string-matching error messages. Instead, explicitly validate preconditions up front and only transition state after the risky step completes successfully.

Guidelines:
1. Order side effects so that irreversible state changes (detaching a session, switching a runtime, clearing a reference) happen only after the dependent operation has confirmed success. For example, don't detach a cloud session before a local resume succeeds — if the resume fails, the old state should remain intact so the user isn't left in a broken, in-between state.
2. Avoid relying on error message pattern-matching to infer system state (e.g., parsing a git error string to decide whether a branch has an upstream). Instead, use an explicit, reliable check (e.g., querying `@{u}`) and branch behavior on that result.
3. Guard against operations being invoked against the wrong context/runtime (e.g., running a local-only action like `editMessageAndRegenerate` against a cloud session). Add explicit checks that reject invalid operations early with a clear error/no-op, rather than letting them silently proceed and produce corrupted state (e.g., a session with the wrong `cwd`).

Example pattern:
```ts
// Bad: mutates state before confirming success
detachCloudSession();
return await resumeLocalSession(sessionId); // if this throws, cloud session is already detached

// Good: only mutate state after success
const result = await resumeLocalSession(sessionId);
detachCloudSession();
return result;
```

Applying this consistently prevents partially-failed operations from leaving the application in an inconsistent or unrecoverable state, and makes failure scenarios predictable and testable.