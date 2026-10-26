---
title: Connection semantics and timeouts
description: Network code should have explicit, consistent semantics for (a) request
  lifetime across disconnect/reconnect, (b) retry side effects, (c) routing under
  proxies (especially loopback), and (d) timeouts/AbortSignal propagation—validated
  by regression tests that simulate real network conditions.
repository: cline/cline#v6
label: Networking
language: TypeScript
comments_count: 7
repository_stars: 70864
---

Network code should have explicit, consistent semantics for (a) request lifetime across disconnect/reconnect, (b) retry side effects, (c) routing under proxies (especially loopback), and (d) timeouts/AbortSignal propagation—validated by regression tests that simulate real network conditions.

Apply these rules:
- Reconnect grace: If a transport disconnects, either (1) preserve pending requests for a short grace window and cancel on grace expiry, or (2) cancel immediately—pick one policy and apply it consistently. Avoid immediately cancelling “already-pending” work when recovery is expected.
- Retry safety: When you resend work after reconnection/registration, ensure it flows through the same dispatch/lifecycle hooks and does not produce duplicate side effects. If the user detached/forgot/disposed during the disconnect, withdrawn work should resolve as unavailable and must not reattach.
- Proxy + loopback correctness: For “local server” networking (e.g., model servers), ensure loopback (127.0.0.1/::1) connects directly even when HTTP(S)_PROXY env vars are set, unless NO_PROXY explicitly matches. Add a regression test with HTTP_PROXY set and NO_PROXY unset.
- Timeout/abort consistency: Every request path—including fallbacks—must honor AbortSignal/timeout policies. Don’t accidentally introduce an unbounded fetch in a fallback branch.

Example pattern (proxy-safe localhost + abort/timeout discipline):
```ts
// Pseudocode illustrating the standard
const idleTimeoutFreeDispatcher = new Agent({ headersTimeout: 0, bodyTimeout: 0 });

export async function fetchLocalStreaming(url: string, init: RequestInit & { signal?: AbortSignal }) {
  // Ensure loopback bypasses env proxies, while non-loopback may use env proxy agent.
  const isLoopback = url.includes('127.0.0.1') || url.includes('localhost') || url.includes('::1');
  const dispatcher = isLoopback ? new Agent({}) : idleTimeoutFreeDispatcher;

  // Ensure init.signal is honored; never use a fallback fetch without it.
  return undiciFetch(url, { ...init, dispatcher });
}
```

Minimum regression coverage:
- Proxy test: HTTP_PROXY set, NO_PROXY unset → loopback succeeds.
- Reconnect test: “endpoint not ready” race → pending command is held and sent once the endpoint is up.
- Lifecycle test: after detach/forget during reconnect, resend must not double-attach.
- Streaming test: silent-body period doesn’t trigger idle-body abort, while cancellation still follows AbortSignal.