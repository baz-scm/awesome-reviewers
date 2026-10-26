---
title: End-to-End Error Capture
description: 'Adopt a single standard for error handling: every async failure (including
  exceptions thrown inside “success” continuations, background promises, and async
  stream/write paths) must be captured and routed into the intended success/failure/recovery
  flow—never into host-level unhandled rejections—and recovery/retry must respect
  structured error classification.'
repository: cline/cline#v9
label: Error Handling
language: TypeScript
comments_count: 9
repository_stars: 70868
---

Adopt a single standard for error handling: every async failure (including exceptions thrown inside “success” continuations, background promises, and async stream/write paths) must be captured and routed into the intended success/failure/recovery flow—never into host-level unhandled rejections—and recovery/retry must respect structured error classification.

Practical rules:
1) **No exceptions escaping inside continuations**: if you use promise chaining, ensure the chain covers both rejection *and* synchronous/async exceptions inside the continuation.
2) **No detached promises without intent**: if code creates a background promise from within a try/catch, it must have an explicit `.catch` or be awaited inside the same error boundary.
3) **Absorb “cleanup/kill/write” failures intentionally**: cleanup errors should be best-effort, but still routed into the same failure reporting mechanism so they don’t become unhandled rejections.
4) **Classify errors before changing retry behavior**: timeouts/aborts are not automatically retryable or “safe transient”; keep retry eligibility tied to structured flags/phase/type.
5) **Test the edge cases that drive correctness**: e.g., missing pairing, empty responses, stdin closed while pending, and timeout attribution across stream phases.

Example patterns:

**A. Cover exceptions thrown inside `attach` (avoid unhandled rejection):**
```ts
const handle = new SandboxedProcess();
void loadMxc()
  .then((mxc) => mxc.spawn(/* ... */))
  .then(
    (sandboxed) => {
      // If attach throws, it must be caught here
      return handle.attach(sandboxed);
    },
    (error) => handle.fail(asError(error)),
  )
  .catch((error) => handle.fail(asError(error)));
```

**B. Ensure kill failures don’t become unhandled rejections:**
```ts
async function safeKill(p: { kill(): boolean }): Promise<void> {
  try {
    p.kill();
  } catch (e) {
    // Route through normal failure path / logger, don’t let it escape
    reportFailure(e);
  }
}
```

**C. Don’t detach critical async work without a catch:**
```ts
try {
  await say("checkpoint_created");
  checkpointTracker.commit().catch((e) => {
    // preserve the prior behavior intent (log/telemetry) instead of unhandled rejection
    reportCheckpointCommitFailure(e);
  });
} catch (e) {
  // ... existing failure handling
}
```

Adhering to these rules prevents common production failures where the system appears stuck, retries incorrectly, or crashes due to unhandled promise rejections—while keeping recovery logic correct and predictable.