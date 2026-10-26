---
title: Intentional network semantics
description: When changing networking/connection logic, make the behavior explicitly
  intentional for (a) local vs remote routing, (b) proxy environment effects, (c)
  sandbox/network policy validity, and (d) transport lifecycle (timeouts/cancellation).
  Add regression tests that simulate real network conditions.
repository: cline/cline#v26
label: Networking
language: TypeScript
comments_count: 6
repository_stars: 70893
---

When changing networking/connection logic, make the behavior explicitly intentional for (a) local vs remote routing, (b) proxy environment effects, (c) sandbox/network policy validity, and (d) transport lifecycle (timeouts/cancellation). Add regression tests that simulate real network conditions.

Practical rules:
1) Preserve localhost/direct-routing invariants: if you introduce a proxy-aware dispatcher/client, ensure loopback (127.0.0.0/8, ::1, and IPv4-mapped loopback) still connects directly when HTTP_PROXY is set but NO_PROXY is not.
2) Apply special HTTP behavior only after you positively identify local destinations: e.g., disable idle timeouts for local model servers that may be silent for >300s, but keep proxy-aware behavior and dead-connection caps for remote gateways.
3) Validate sandbox/network policy per enforcement tier: request the minimal ingress/egress your platform can enforce. Don’t grant loopback ingress if the fallback tier rejects such a policy.
4) Define reconnect/disconnect cancellation semantics: for pending network requests, document whether they are cancelled immediately or preserved for a reconnect grace window; ensure cleanup/pending-work logic can’t deadlock on stale connection settings.
5) Regression-test environment-dependent behavior: include tests with HTTP_PROXY set and NO_PROXY unset, and cover wildcard local bindings like 0.0.0.0 and IPv4-mapped addresses.

Sketch:
```ts
// Route loopback direct even when HTTP_PROXY is set, and only disable idle timeouts
// when the provider base URL is known-local.
function isLoopback(hostname: string): boolean {
  return hostname === "localhost" || /^127\./.test(hostname) || hostname === "::1";
}

export async function fetchWithoutIdleTimeouts(input: string | URL | Request, init?: RequestInit) {
  const url = typeof input === "string" ? new URL(input) : input instanceof URL ? input : new URL(input.url);
  if (isLoopback(url.hostname)) {
    // Use no-timeout direct agent (no proxy for loopback)
    return undiciFetchWithNoIdleTimeoutsDirect(input, init);
  }

  // For non-loopback: if HTTP_PROXY is set, use proxy-aware agent
  // but only enable the no-idle-timeout behavior for verified local model servers.
  if (isVerifiedLocalProviderBase(url)) {
    return undiciFetchWithNoIdleTimeoutsProxyAware(input, init);
  }
  return undiciFetchProxyAware(input, init); // keep default timeouts/caps
}
```

Apply the same “intentional semantics + minimal policy + targeted tests” mindset to TCP/WebSocket disconnect/reconnect logic and to sandbox network policy generation.