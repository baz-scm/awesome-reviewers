---
title: Error Handling Contracts
description: Error handling must be complete (no missed sync/async throws), contract-aligned
  (retries/recovery only for the right error classes), and transparent (no silent
  unsafe fallbacks).
repository: cline/cline#v13
label: Error Handling
language: TypeScript
comments_count: 9
repository_stars: 70874
---

Error handling must be complete (no missed sync/async throws), contract-aligned (retries/recovery only for the right error classes), and transparent (no silent unsafe fallbacks).

Apply these rules:
1) Wrap both synchronous exceptions and rejected promises
- If you do work in an attach/continuation callback, don’t rely on “.then(onFulfilled, onRejected) catches only rejections”. Ensure exceptions thrown inside the fulfillment path are caught too.

```ts
// Prefer: attach inside try/catch, or use .then(...).catch(...)
void loadMxc()
  .then(mxc => mxc.spawn(/*...*/))
  .then(sandboxed => {
    // attach() may throw synchronously
    attach(handle, sandboxed);
  })
  .catch(err => fail(handle, err));
```

2) Never ignore termination/cancel failures
- If kill/shutdown returns a promise or can throw, wire it into your existing error funnel (fail/telemetry/log), not into an ignored finally.

3) Don’t detach fallible work from user-visible success
- Avoid changing from `await` inside the try/catch to `promise.then(...)` without attaching a `.catch`. Otherwise failures become unhandled rejections and UI state can be wrong (e.g., “checkpoint_created” shown without a hash).

4) Retry/recovery must be gated by precise error classification
- Don’t blanket-mark timeouts/retriable; preserve existing retry-budget semantics.
- Don’t treat all “errors” as “missing”; distinguish “not found / absent / expired” from “rate limit / buffer limit / malformed / other” so you don’t fabricate results.

5) Be explicit when config/protection cannot be read
- If a safety-critical setting read fails (corrupt/torn file), avoid silently falling back to an unsafe default. Distinguish “file absent” vs “unreadable” and surface a warning/telemetry so behavior matches user expectation.

6) Fix asynchronous stream/timer edge cases
- Handle async stream errors (EPIPE, stdin/socket failures) so they don’t escape as uncaught host exceptions.
- If you use an observation/timeout timer, cancel it on early failure so you don’t report false “ran for N ms” samples.

Adopt a checklist for each change in this category: (a) any callback passed to .then/handlers cannot throw unhandled; (b) every cancellation/kill path routes errors; (c) user-visible “success” only occurs after the corresponding fallible work is confirmed; (d) retry/recovery uses the most specific error predicate available; (e) config read failures are logged/warned, not silently downgraded.