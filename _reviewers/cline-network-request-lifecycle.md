---
title: Network request lifecycle
description: Any code that performs network I/O must define (1) routing correctness
  (proxy vs loopback/local), and (2) a bounded request lifecycle (AbortSignal/timeout)
  for *every* path, including fallbacks; and (3) consistent in-flight cancellation/grace
  semantics on disconnect.
repository: cline/CLINE
label: Networking
language: TypeScript
comments_count: 5
repository_stars: 70839
---

Any code that performs network I/O must define (1) routing correctness (proxy vs loopback/local), and (2) a bounded request lifecycle (AbortSignal/timeout) for *every* path, including fallbacks; and (3) consistent in-flight cancellation/grace semantics on disconnect.

Apply this standard:
- Route correctly
  - If you override HTTP dispatchers/agents (e.g., undici/EnvHttpProxyAgent), preserve the project’s intended “loopback is direct” behavior under HTTP_PROXY/NO_PROXY.
  - Add regression tests that run with HTTP_PROXY set and NO_PROXY unset, verifying loopback reaches directly while non-loopback uses the proxy.
  - When selecting “local server” behavior, ensure classification covers real bind/address variants (e.g., 0.0.0.0 and IPv4-mapped loopback).
- Bound lifecycle everywhere
  - Every fetch (including fallback functions) must be wired to a shared AbortSignal or an explicit timeout; never allow a bare/unbounded fetch that can hang indefinitely on packet drops.
- Be consistent on disconnect
  - Define whether pending requests survive brief reconnects via a grace period; cancel only on grace expiry/explicit Stop, and don’t transfer/re-execute callbacks implicitly.

Example pattern (bounded + correct dispatcher selection):
```ts
const idleTimeoutFreeDispatcher = new EnvHttpProxyAgent({ headersTimeout: 0, bodyTimeout: 0 })

function createRequest(signal: AbortSignal, url: string) {
  const isLocal = isLocalModelUrl(url) // must cover 0.0.0.0 + mapped loopback, etc.

  // Preserve loopback direct routing when HTTP_PROXY is set.
  const dispatcher = isLocal && !isLoopback(url)
    ? idleTimeoutFreeDispatcher
    : /* your normal direct-vs-proxy dispatcher */ undefined

  return { dispatcher, signal }
}

async function fetchWithAllPathsBound(url: string, signal: AbortSignal): Promise<Response> {
  const { dispatcher } = createRequest(signal, url)
  return fetch(url, { dispatcher, signal })
}

async function fetchModelIdsWithFallback(url: string, signal: AbortSignal) {
  try {
    return await fetchWithAllPathsBound(url, signal)
  } catch {
    // IMPORTANT: fallback must reuse the same AbortSignal.
    return await fetchWithAllPathsBound(url, signal)
  }
}
```

If you do this consistently, you avoid hangs from unbounded fallbacks, prevent proxy/env-var regressions for loopback/local servers, and maintain predictable behavior for in-flight network operations during disconnects/reconnects.