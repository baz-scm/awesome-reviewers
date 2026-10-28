---
title: Defensive network request handling
description: 'Treat every network call—including fallback paths, proxies, sandboxed
  subprocess traffic, and persistent connections—as inherently unreliable, and code
  defensively against hangs, unbounded data, and misrouting:'
repository: cline/cline#|sleep 4
label: Networking
language: TypeScript
comments_count: 7
repository_stars: 70979
---

Treat every network call—including fallback paths, proxies, sandboxed subprocess traffic, and persistent connections—as inherently unreliable, and code defensively against hangs, unbounded data, and misrouting:

1. **Timeouts/abort signals on every path, not just the primary one.** If a primary request has an AbortSignal/timeout, any fallback or secondary request triggered on its failure must have one too; otherwise a server that drops packets instead of refusing can hang the whole operation even though the primary path looked safe (e.g. a bounded `/api/v1/models` call failing over to an unbounded `fetch`).

2. **Bound data transfer by actual bytes received, not declared headers.** Don't trust `Content-Length` to cap downloads—a missing or incorrect header lets a response buffer without limit. Read the body incrementally and abort the stream as soon as the running total exceeds the configured max.

3. **Get proxy/local-network routing right for every destination class.** When bypassing or special-casing routing (loopback, LAN model servers, sandbox network policies per OS), verify the actual bypass conditions of the library/platform in use (e.g. `EnvHttpProxyAgent` proxies loopback too unless `NO_PROXY` is set) and mirror the platform's existing routing rules rather than assuming env-var proxy conventions apply uniformly. Only request the network capabilities (e.g. ingress/loopback) actually needed, since over-requesting can cause stricter enforcement tiers to reject the whole policy on some platforms.

4. **Invalidate and recreate connection state when identity or target changes.** Control sockets, SSH masters, and cached transports keyed by credentials or target must be torn down and rebuilt when the underlying identity/profile changes, not reused with stale credentials. Health-probe or coalesce checks before declaring a connection dead, and make sure writes/prompts are never silently replayed.

Example of the fallback-timeout gap to avoid:
```ts
// BAD: fallback has no bound, so a packet-dropping host hangs the task
try {
  return await fetchWithTimeout(primaryUrl, { timeoutMs: 5000 });
} catch {
  return await fetch(fallbackUrl); // no AbortSignal — can hang forever
}
```
```ts
// GOOD: every path is bounded
try {
  return await fetchWithTimeout(primaryUrl, { timeoutMs: 5000 });
} catch {
  return await fetchWithTimeout(fallbackUrl, { timeoutMs: 5000 });
}
```

Apply this checklist whenever adding or reviewing code that opens sockets, issues HTTP requests, downloads data, or manages long-lived connections.