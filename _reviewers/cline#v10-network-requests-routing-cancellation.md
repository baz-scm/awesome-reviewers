---
title: 'Network Requests: Routing & Cancellation'
description: 'Treat network behavior (proxy routing, local-vs-remote handling, retries,
  and cancellation) as a single policy across all request paths.


  **Standards**'
repository: cline/cline#v10
label: Networking
language: TypeScript
comments_count: 6
repository_stars: 70869
---

Treat network behavior (proxy routing, local-vs-remote handling, retries, and cancellation) as a single policy across all request paths.

**Standards**
1. **Preserve loopback direct-routing.** If your custom fetch/agent changes proxy handling, ensure loopback/localhost still bypasses HTTP_PROXY when NO_PROXY is absent, and add a regression test that sets HTTP_PROXY and unsets NO_PROXY.
2. **Classify “local” addresses robustly.** Include common local bind patterns like `127.0.0.1`, `::1`, `0.0.0.0` and IPv4-mapped IPv6 (`::ffff:127.0.0.1`) so the “local” network optimization is applied consistently.
3. **Never lose timeouts/AbortSignal in fallbacks.** Every code path that hits the network (including fallback discovery/probes) must use the same abort/timeout mechanism as the primary path.
4. **Be connection-state aware.** During expected transitions (connecting/initial hub attach), avoid immediate failure; prefer short waits/retries based on connection readiness, and cancel immediately only on explicit stop/dispose or after an intentional grace window.

**Example pattern (apply across primary + fallback):**
```ts
async function fetchWithPolicy(input: RequestInfo, init: RequestInit, abort: AbortSignal) {
  // 1) Decide routing (proxy vs direct) based on local address classification
  // 2) Always use the same AbortSignal for timeouts/cancellation
  return fetch(input, { ...init, signal: abort });
}

function withTimeout(ms: number) {
  const controller = new AbortController();
  const t = setTimeout(() => controller.abort(), ms);
  return { signal: controller.signal, cancel: () => clearTimeout(t), controller };
}

export async function modelDiscovery(primaryUrl: string, fallbackUrl: string) {
  const { signal, cancel } = withTimeout(5000);
  try {
    try {
      return await fetchWithPolicy(primaryUrl, {}, signal);
    } catch {
      // fallback must also be abortable
      return await fetchWithPolicy(fallbackUrl, {}, signal);
    }
  } finally {
    cancel();
  }
}
```

This prevents “works locally, hangs remotely” failures, maintains expected proxy behavior for localhost users, and keeps cancellation responsive for stop/disconnect flows.