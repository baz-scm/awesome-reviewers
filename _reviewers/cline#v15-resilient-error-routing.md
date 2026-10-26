---
title: Resilient Error Routing
description: 'Adopt a single error-handling pattern: route *all* failures (including
  exceptions thrown inside async continuations and async stream/process errors) into
  the same classified failure path, and only retry/fallback when the error evidence
  matches the contract.'
repository: cline/cline#v15
label: Error Handling
language: TypeScript
comments_count: 11
repository_stars: 70877
---

Adopt a single error-handling pattern: route *all* failures (including exceptions thrown inside async continuations and async stream/process errors) into the same classified failure path, and only retry/fallback when the error evidence matches the contract.

Practical rules:
1) Never leave async continuations unguarded
- Prefer `await` + `try/catch`.
- If you use promises, ensure both rejection *and thrown exceptions* inside the next callback are handled.

```ts
// Good: attach errors from attach-phase too
const handle = new SandboxedProcess();
loadMxc()
  .then((mxc) => mxc.spawn(/* ... */))
  .then((sandboxed) => handle.attach(sandboxed))
  .catch((error) => {
    handle.fail(new Error(`Sandbox failed: ${error instanceof Error ? error.message : String(error)}`));
  });
```

2) Avoid fire-and-forget when correctness depends on it
- If UI/state depends on an async operation (e.g., checkpoint commit), either `await` it or attach a `.catch()` that logs/telemeters and prevents misleading “success” messages.

3) Classify retries/fallbacks by evidence, not by type alone
- Don’t blanket-mark timeouts/retries as whole-turn retryable; timeouts can mean “client stopped waiting,” not “provider is transient.”
- Don’t synthesize “missing” when the real error is “too large/limit exceeded.”

4) Handle “in-progress” intermediate states explicitly
- For health/probe/startup loops, treat expected transitional responses (e.g., `503 Starting`) as “keep waiting” instead of “invalid/fatal.”

5) Correlate asynchronous process/stream errors
- For stdin write failures (EPIPE/EOF) or similar stream errors, add listeners so they’re absorbed and correlated with the same lifecycle that fails pending work.
- If killing a child can throw, catch that and route it through the same `fail()`/error channel to avoid unhandled rejections.

6) Preserve user intent and data contracts on failure
- If settings read fails or persistence fails, don’t silently flip behavior off or claim success; keep last known intent or retry safely later.

Result: fewer unhandled rejections/hangs, more accurate user-facing errors, and safer retry/fallback behavior that doesn’t repeat side effects or hide real faults.