---
title: Bound, Retry, Route Correctly
description: 'When touching networking/IPC boundaries, follow a consistent policy:


  1) Always bound *every* network path (including fallbacks/secondary requests) with
  the same timeout/AbortSignal.'
repository: cline/cline#v21
label: Networking
language: TypeScript
comments_count: 7
repository_stars: 70886
---

When touching networking/IPC boundaries, follow a consistent policy:

1) Always bound *every* network path (including fallbacks/secondary requests) with the same timeout/AbortSignal.
- Avoid “primary timed out, fallback hangs” patterns.

2) Timeouts must not leak in-flight operations.
- If you race a timeout against a connect/read, the timed-out attempt may still eventually resolve—clean it up deterministically (e.g., disconnect/close once it resolves).

3) Handle connection lifecycle explicitly.
- Don’t fail/return empty just because a hub/socket is still connecting; add a short “connected-within” grace window and retry after reconnect.
- For operations that can be retried from UI, define an explicit dispatch boundary so the UI can’t resend after you already dispatched.

4) Preserve correct routing for loopback vs proxied hosts.
- If you special-case local HTTP (e.g., disable idle timeouts for long token generation), ensure 127.0.0.1/localhost never goes through HTTP_PROXY when it previously bypassed it.
- Gate “local fetch behavior” using robust local-address detection (including 0.0.0.0 and IPv4-mapped loopback).

Example: bounded connect with deterministic cleanup
```ts
function withTimeout<T>(work: Promise<T>, ms: number, what: string, signal?: AbortSignal): Promise<T> {
  // Use the same AbortSignal for all requests that support it.
  const timeout = new Promise<never>((_, reject) => {
    const t = setTimeout(() => reject(new Error(`${what} took longer than ${ms} ms`)), ms);
    if (signal) signal.addEventListener('abort', () => {
      clearTimeout(t);
      reject(signal.reason ?? new Error('aborted'));
    }, { once: true });
  });
  return Promise.race([work, timeout]);
}

async function connectWithDeadline(client: { connect(): Promise<void>; disconnect(): Promise<void }}, timeoutMs: number) {
  let didTimeout = false;
  const connectPromise = client.connect();
  try {
    await withTimeout(connectPromise, timeoutMs, 'connect');
  } catch (e) {
    didTimeout = true;
    throw e;
  } finally {
    // If the read/deadline timed out but the connect eventually completes, close it.
    if (didTimeout) {
      try { await connectPromise; } catch {}
      await client.disconnect();
    }
  }
}
```

Example: local-vs-proxy routing rule (concept)
- When using a custom undici/agent/fetch for long-running *local* model servers, ensure loopback (localhost/127.0.0.1/::1 and IPv4-mapped) uses direct routing, while other hosts still respect the environment proxy/no-proxy behavior.

Adopt this as a checklist for any PR that introduces/changes:
- timeouts/retries
- AbortSignal propagation
- socket/hub reconnect behavior
- “send once” semantics (avoid duplicate UI resends)
- proxy/local address handling