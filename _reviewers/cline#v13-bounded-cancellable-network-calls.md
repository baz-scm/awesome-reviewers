---
title: Bounded, Cancellable Network Calls
description: 'When implementing networking (HTTP fetches, proxy-aware agents, or socket/Hubs),
  ensure the full request lifecycle is deterministic: routing is correct, operations
  are bounded/cancellable, and retries/resends never duplicate already-dispatched
  work.'
repository: cline/cline#v13
label: Networking
language: TypeScript
comments_count: 5
repository_stars: 70874
---

When implementing networking (HTTP fetches, proxy-aware agents, or socket/Hubs), ensure the full request lifecycle is deterministic: routing is correct, operations are bounded/cancellable, and retries/resends never duplicate already-dispatched work.

Apply this checklist:
1) Bound every network call (including fallbacks)
- Every HTTP request must have a timeout and be tied to the caller’s AbortSignal.
- Don’t forget fallback paths (e.g., alternative model discovery) and background refresh steps.

2) Preserve loopback/local routing under proxies
- If you add custom fetch/agents (e.g., to disable idle timeouts for local servers), preserve the existing “always-direct to loopback” rule when HTTP_PROXY is set.
- Your “local network” detection must cover common real-world URLs: 127.0.0.1, 0.0.0.0, IPv4-mapped loopback (::ffff:127.0.0.1), and typical RFC1918 ranges.

3) Make dispatch/retry semantics explicit
- For transport layers (Hub/client/UI), clearly distinguish:
  - pre-dispatch failure (safe to retry/resend), vs
  - post-dispatch failure (do NOT resend; user UI must offer “resend” only when safe).
- If reconnect grace is added, keep the in-flight request in the shared lifecycle and cancel only on grace expiry or explicit stop/detach—never implicitly resend or re-execute callbacks.

Example pattern (timeout + AbortSignal):
```ts
function withTimeout(signal: AbortSignal, ms: number): AbortSignal {
  const c = new AbortController();
  const onAbort = () => c.abort(signal.reason);
  if (signal.aborted) c.abort(signal.reason);
  else signal.addEventListener('abort', onAbort, { once: true });

  const t = setTimeout(() => c.abort(new Error('timeout')), ms);
  const cleanup = () => clearTimeout(t);
  c.signal.addEventListener('abort', cleanup, { once: true });
  return c.signal;
}

export async function fetchWithPolicy(url: string, init: RequestInit, signal: AbortSignal) {
  const boundedSignal = withTimeout(signal, 5000);
  return fetch(url, { ...init, signal: boundedSignal });
}
```

Result: fewer “hung” tasks, fewer proxy-related regressions for localhost, and no accidental double-send caused by incorrect retry/reconnect behavior.