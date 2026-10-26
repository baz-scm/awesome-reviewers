---
title: Error Handling Contracts
description: 'Establish and enforce explicit error-handling contracts: classify errors,
  recover only when safe, never let async/stream failures go unobserved, and keep
  telemetry/diagnostics side-effect-free.'
repository: cline/cline#v4
label: Error Handling
language: TypeScript
comments_count: 13
repository_stars: 70864
---

Establish and enforce explicit error-handling contracts: classify errors, recover only when safe, never let async/stream failures go unobserved, and keep telemetry/diagnostics side-effect-free.

Practical rules:
1) No unhandled async/stream errors
- Always handle both: (a) promise rejections and (b) exceptions thrown inside callbacks/attach/then-chains.
- For child-process stdin/stdout/stderr, attach an `error` listener on the stream so EPIPE/EOF doesn’t crash the host.

2) Retry/recovery must be gated by error identity
- Only treat retries as allowed for the specific error types you can prove are transient and safe to replay.
- Do NOT “make all timeouts retryable”; preserve existing retry budgets and stream-phase semantics.
- Recovery loops (e.g., MCP session re-handshake) must recognize the correct “session lost/dead id” shape and recover only then.

3) Diagnostics must match the real end state
- Record failure/success/timeout/abort reasons based on the actual outcome (including cases like empty responses or rejected-before-transcript insertion).
- Preserve structured timeout/abort attribution even if public surfaces serialize the reason.

4) Fail-open vs fail-closed must be explicit and observable
- If a protection setting can’t be read (torn/corrupt), don’t silently flip behavior. Surface a warning or include it in the tool/result.

5) Telemetry must never interrupt core logic
- If telemetry/event publishing can throw, catch it so it can’t abort inference or critical operations.

Code patterns:

A) Safe then-chain error handling
```ts
spawnSomething()
  .then(attach)              // attach may throw
  .catch((err) => fail(err));

// OR:
try {
  const s = await spawnSomething();
  attach(s); // throw handled by try/catch
} catch (err) {
  fail(err);
}
```

B) Child stdin error listener (avoid host crash)
```ts
child.stdin?.on('error', (e) => {
  // record/annotate the failure; exit handler will still report final status
  stdinFailure = String(e.message ?? e);
});
```

C) Error-type gated recovery/retry
```ts
function isSessionLost(err: unknown): boolean {
  return err instanceof StreamableHTTPError && /session not found/i.test(err.message);
}

async function withRecovery<T>(op: () => Promise<T>) {
  try {
    return await op();
  } catch (err) {
    if (!isSessionLost(err)) throw err;
    await rehandshakeOnce();
    return await op();
  }
}
```

D) Non-interrupting telemetry
```ts
try { emitTelemetry(event); } catch { /* never abort the run */ }
```

Adoption checklist for each change:
- What exact error types are we classifying?
- Which failures are retryable—and why (transient + safe replay)?
- Are we catching exceptions thrown inside callbacks (not only promise rejections)?
- Are all relevant streams/listeners handled to prevent host-level uncaught errors?
- Do diagnostics/telemetry reflect the real outcome and preserve structured reasons?
- If configuration/protection can’t be read, do we warn/propagate uncertainty rather than silently changing behavior?