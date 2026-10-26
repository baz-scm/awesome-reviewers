---
title: Deterministic Error Handling
description: 'Treat error handling as a first-class control-flow contract: explicitly
  classify failures, contain async exceptions, and only recover/retry when the error
  is proven safe.'
repository: cline/cline#v11
label: Error Handling
language: TypeScript
comments_count: 20
repository_stars: 70871
---

Treat error handling as a first-class control-flow contract: explicitly classify failures, contain async exceptions, and only recover/retry when the error is proven safe.

Apply these rules:
1) **Classify before you recover**
- Recovery must be driven by specific, semantic predicates (e.g., “session lost”, “detached capability owner”, “missing git path/object”), not by generic catch-all retries.
- Anything outside the allow-list must propagate the real error (avoid mapping unknown failures to “missing/absent”).

2) **Bound waits and retries; fail early on “can’t succeed” states**
- If a system can’t answer (or can’t be repaired safely), fail immediately rather than waiting.
- Probe/health/polling should not treat semantically invalid states as “retryable”.

3) **Contain async failures—no unhandled rejections / uncaught exceptions**
- Any detached promise, background task, or stdin/socket error path must be either awaited or `.catch(...)`-handled, or converted into the same controlled error-reporting channel as the main operation.
- When you spawn timers/observers, cancel/clear them on spawn failure so later events don’t report false samples.

4) **Preserve evidence and attribution**
- User-facing messages and diagnostics should reflect the real terminal reason (timeout vs empty-response vs abort), and retries should not erase the original attribution.
- If you trim logs or budget/compaction outputs, keep failed/incomplete evidence so failures remain debuggable.

Example pattern (controlled recovery by classification + contained async):
```ts
async function withRecovery<T>(op: () => Promise<T>): Promise<T> {
  try {
    return await op();
  } catch (err) {
    if (!isRecoverableError(err)) throw err; // allow-list only

    // Never retry indefinitely; retry once.
    // Preserve original error for diagnostics if retry also fails.
    const retryErrMarker = err;
    try {
      await reconnectOrRehandshake();
      return await op();
    } catch (e2) {
      throw annotateWithOriginal(e2, retryErrMarker);
    }
  }
}

// Ensure async side effects never leak unhandled.
function fireAndRecord(p: Promise<unknown>, onError: (e: unknown) => void) {
  p.catch(onError);
}
```

Net effect: fewer “mystery hangs”, fewer silent degradations, safer retries, and diagnostics that always tell the truth about what actually happened.