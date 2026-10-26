---
title: Precise async error coverage
description: Ensure every async boundary fully captures *both* rejected promises and
  synchronous exceptions, and only performs recovery/retry when the error classification
  is precise and safe.
repository: Cline/Cline
label: Error Handling
language: TypeScript
comments_count: 12
repository_stars: 70840
---

Ensure every async boundary fully captures *both* rejected promises and synchronous exceptions, and only performs recovery/retry when the error classification is precise and safe.

Core rules:
1) Always cover “throw inside then”
- If you attach handlers like `.then(fnSuccess, fnFail)`, remember `fnSuccess`/`attach` may throw; you still need a `.catch(...)` that routes all failures.
- For code that returns a “ChildProcess-like” handle, ensure failure leads to a settled process/`fail()` path (not an unhandled rejection).

2) Never leave detached promises unobserved
- If you intentionally don’t await, attach `.catch(...)` to prevent unhandled rejections and to keep UI/state honest (don’t show “success” before the async work succeeds).

3) Clear timers and state on failure
- If you arm observation/timeout timers, cancel them when the underlying operation fails to avoid false telemetry/outcomes.

4) Retry only with proven semantics
- Don’t broaden retry eligibility (e.g., timeouts) without understanding whether the request/provider may have progressed or side effects occurred.
- Preserve and use the captured error attribution (timeouts/aborts) so the system reports the right phase and applies the right recovery budget.

5) Fail fast on invariant violations that risk side effects
- If invariants that prevent duplication/orphaning are not met (missing artifacts, unknown session state), prefer throwing/terminating that flow rather than falling through into a path that can duplicate work.

Example pattern (covers throw + maps to controlled failure):
```ts
// Bad: throw inside attach() can bypass the rejection handler.
void loadMxc().then((mxc) =>
  mxc.spawn(/*...*/).then((sandboxed) => handle.attach(sandboxed), fail)
);

// Good: one catch for all async failures, including throws.
void loadMxc()
  .then((mxc) => mxc.spawn(/*...*/))
  .then((sandboxed) => handle.attach(sandboxed))
  .catch((error) => {
    handle.fail(new Error(`Sandboxing failed: ${String(error)}`));
  });
```

Example pattern (detached promise must be caught):
```ts
this.say('checkpoint_created');
void this.checkpointTracker.commit()
  .then((hash) => this.messageStateHandler.updateClineMessage(/*...*/))
  .catch((error) => {
    // log + optionally update UI to reflect failure
    console.error('Failed to create checkpoint:', error);
  });
```

Checklist for PRs in this area:
- Every `.then(...)` path has a downstream `.catch(...)` (or uses `try/catch` around awaits).
- Any intentionally detached promise has a `.catch`.
- Any timer armed before/around async work is cleared on failure.
- Retry logic is driven by specific, verified error classifications (timeouts vs transient vs abort), not blanket rules.
- When invariants needed to prevent duplication/orphaning fail, code throws (or returns a clearly labeled failure) rather than continuing with a fallback path.