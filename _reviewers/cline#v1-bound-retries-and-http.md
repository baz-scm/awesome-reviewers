---
title: Bound retries and HTTP
description: 'For any networked operation (Hub transport, WebSocket/TCP recovery,
  and HTTP fetches), make reliability explicit:


  1) Retry/replay must be dispatch-aware (no double effects)'
repository: cline/cline#v1
label: Networking
language: TypeScript
comments_count: 6
repository_stars: 70862
---

For any networked operation (Hub transport, WebSocket/TCP recovery, and HTTP fetches), make reliability explicit:

1) Retry/replay must be dispatch-aware (no double effects)
- Define a clear “dispatch boundary” (before/after the point where the remote has accepted the message).
- When reconnecting or retrying, only replay requests that were not dispatched, and gate replays using current state (e.g., attached vs detached; still relevant session; still following).
- If you add reconnect grace, preserve pending requests within the shared lifecycle and cancel only after grace expiry or explicit stop.

2) Always bound HTTP networking (including fallbacks)
- Every code path that calls `fetch` must honor an `AbortSignal`/timeout, not just the primary request.
- When using alternative dispatchers/agents for long-generation local servers, preserve loopback direct routing even when `HTTP_PROXY` is set and `NO_PROXY` is not.
- Ensure your “local server” detection is correct for common variants (e.g., `0.0.0.0` and IPv4-mapped loopback), so you don’t accidentally apply the wrong timeout/proxy behavior.

Example pattern (bounded fallback):
```ts
async function withTimeout<T>(p: Promise<T>, signal: AbortSignal, ms: number): Promise<T> {
  const t = setTimeout(() => controller.abort(), ms);
  try { return await p; } finally { clearTimeout(t); }
}

async function fetchWithBoundedFallback(primaryUrl: string, fallbackUrl: string): Promise<any> {
  const controller = new AbortController();
  const signal = controller.signal;
  const primary = fetch(primaryUrl, { signal });
  try {
    const res = await withTimeout(primary, signal, 5000);
    if (!res.ok) throw new Error("primary failed");
    return await res.json();
  } catch {
    // fallback must also be bounded/abortable
    const res = await withTimeout(fetch(fallbackUrl, { signal }), signal, 5000);
    return await res.json();
  }
}
```

Checklist for reviews
- Does disconnect/retry logic specify whether the remote received the action?
- Are replay actions gated by state and lifecycle (not just “we’re reconnecting”)?
- Are *all* HTTP paths—especially fallbacks—abortable and bounded?
- If using special fetch/agents for local servers, are proxy/loopback rules preserved and local detection correct (including `0.0.0.0` and IPv4-mapped loopback)?
