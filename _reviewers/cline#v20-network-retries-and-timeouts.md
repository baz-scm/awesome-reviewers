---
title: Network retries and timeouts
description: 'When adding or modifying networking code, treat retries/recovers, timeouts,
  and proxy/routing as first-class correctness concerns:


  1) Make retry decisions based on an explicit *dispatch boundary*'
repository: cline/cline#v20
label: Networking
language: TypeScript
comments_count: 5
repository_stars: 70886
---

When adding or modifying networking code, treat retries/recovers, timeouts, and proxy/routing as first-class correctness concerns:

1) Make retry decisions based on an explicit *dispatch boundary*
- Record whether the server/controller actually dispatched the side effect.
- Only offer “resend” for requests that failed strictly *before* dispatch; never for failures after dispatch/commit.
- On reconnection, replays must respect current lifecycle state (detached/forgotten/disposed) and must not acquire leases again.

2) Ensure every network path is *bounded* (including fallbacks)
- Use AbortSignal for all fetch/TCP/handshake operations.
- Do not leave fallback paths unbounded (e.g., secondary model discovery) because they can hang the task pipeline.

3) Preserve correct routing for local/loopback under proxies
- If the runtime may honor env proxies (HTTP_PROXY/NO_PROXY), ensure loopback (and known local model servers) still route directly when required.
- Implement local-network detection/gating robustly (include 0.0.0.0 and IPv4-mapped loopback).

Example pattern (bound request + safe retry decision):
```ts
type DispatchStatus = { dispatched: true } | { dispatched: false };

async function sendWithDispatchBoundary(args: {
  attempt: () => Promise<{ ok: boolean; error?: unknown; payload?: unknown; status: DispatchStatus }>;
  beforeRetry?: () => void;
  abortSignal: AbortSignal;
}): Promise<any> {
  const res = await args.attempt();
  if (res.ok) return res.payload;

  // Retry only when we know nothing was dispatched.
  if (!res.status.dispatched) {
    args.beforeRetry?.();
    return (await args.attempt()).payload;
  }

  // Post-dispatch failure: do not auto-resend.
  throw res.error ?? new Error("dispatched failure");
}

// Always pass abortSignal into fetch/streaming reads.
```
Adopting these rules prevents duplicate side effects on reconnect, avoids hangs from unbounded fallbacks, and keeps local services working even when proxy environment variables are present.