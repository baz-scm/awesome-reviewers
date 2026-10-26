---
title: Bound and cleanup network calls
description: When adding/modifying networking, you must make timeout/cancellation
  behavior consistent across *all* paths, ensure late-arriving connects are cleaned
  up, and preserve correct routing semantics (especially loopback vs proxy) when you
  change fetch/dispatchers.
repository: cline/cline#v25
label: Networking
language: TypeScript
comments_count: 4
repository_stars: 70891
---

When adding/modifying networking, you must make timeout/cancellation behavior consistent across *all* paths, ensure late-arriving connects are cleaned up, and preserve correct routing semantics (especially loopback vs proxy) when you change fetch/dispatchers.

Apply this standard:
1) Bound every network operation
- Every primary request and every fallback must share the same timeout/AbortSignal policy.
- If a fallback uses “bare fetch” (or otherwise unbounded I/O), it can hang startup even if the primary path is bounded.

2) Handle “timeout fired, connection still completes”
- If you race/timeout an operation, don’t abandon the underlying socket/connection lifecycle.
- Keep the connect promise; when it eventually resolves, immediately disconnect if the caller already timed out.

3) For dependent services that can be “connecting”, don’t fail immediately
- If a read depends on a hub/transport that may still be handshaking, wait briefly for readiness and retry once after a drop instead of returning empty/unknown results.

4) If you customize fetch/dispatchers (e.g., disable idle timeouts), preserve proxy semantics
- Disabling idle timeouts is not enough: preserve loopback behavior (connect directly to 127.0.0.1/::1 even when HTTP_PROXY is set and NO_PROXY is absent).
- Add regression tests that run with HTTP_PROXY set and NO_PROXY unset.

Example pattern (timeout + late connect cleanup + abort):
```ts
function withTimeout<T>(work: Promise<T>, ms: number, what: string): Promise<T> {
  const ac = new AbortController()
  const t = setTimeout(() => ac.abort(new Error(`${what} exceeded ${ms} ms`)), ms)
  return work.finally(() => clearTimeout(t))
}

async function connectThenUse({ connect, disconnect, call }, timeoutMs: number) {
  let timedOut = false
  const connectPromise = connect().catch((e) => { throw e })

  try {
    // Bound waiting for connect
    await withTimeout(connectPromise, timeoutMs, "connect")
    return await call()
  } catch (e) {
    timedOut = true
    throw e
  } finally {
    // If connect resolved after the caller timed out, ensure cleanup.
    if (timedOut) {
      await connectPromise.catch(() => undefined)
      await disconnect()
    }
  }
}
```

Checklist for PRs in this area:
- [ ] All code paths (including fallbacks) use the same timeout/AbortSignal.
- [ ] Any “race with timeout” doesn’t leak sockets: late connects are cleaned up.
- [ ] Connection-dependent reads wait briefly/retry when the transport is still connecting.
- [ ] Any dispatcher changes preserve loopback/direct routing and are tested with HTTP_PROXY/NO_PROXY env settings.