---
title: Preserve Network Semantics
description: When changing networking behavior (HTTP agents, timeouts, sandbox network
  policy, or disconnect handling), encode the intended semantics explicitly and validate
  them with environment-specific tests.
repository: cline/cline#v29
label: Networking
language: TypeScript
comments_count: 6
repository_stars: 70893
---

When changing networking behavior (HTTP agents, timeouts, sandbox network policy, or disconnect handling), encode the intended semantics explicitly and validate them with environment-specific tests.

Apply these rules:
1) Local vs proxied routing must stay correct
- If you disable/alter HTTP behavior for local servers (e.g., to avoid idle-timeout aborts), only do it when the target is truly local (cover `localhost`, `127.0.0.0/8`, `10/8`, `192.168/16`, link-local, `::1`, `0.0.0.0`, and IPv4-mapped loopback).
- Always preserve “direct connect” for loopback even when `HTTP_PROXY` is set. If `NO_PROXY` is absent, env-var proxy agents may incorrectly send `127.0.0.1/::1` through the proxy.

2) Platform sandbox policy must match enforcement tier
- Don’t request network rules that a platform’s sandbox fallback rejects. If one platform tier errors on a policy (e.g., loopback ingress in an AppContainer fallback), gate that rule by platform (and ideally by enforcement path).

3) Connection lifecycle (retry/cancel/grace) must be consistent with actual reachable states
- If you cancel pending work on disconnect, decide whether you want reconnect grace for already-pending requests. If so, keep the pending operation in the lifecycle, cancel only after grace expiry, and don’t transfer/re-execute callbacks.

Minimal implementation sketch (loopback/direct + local-only relaxed fetch):
```ts
const loopbackDirectAgent = new EnvHttpProxyAgent({ headersTimeout: 0, bodyTimeout: 0, /* but DO NOT proxy localhost */ });
// In practice: pick an agent that matches your existing resolver’s “always direct to loopback” rule.

function isProbablyLocalBaseUrl(url: URL) {
  // Ensure your local detection covers 0.0.0.0 and IPv4-mapped loopback.
  // e.g., treat 0.0.0.0 and ::ffff:127.0.0.1 as local.
  return /* blocklist/subnet check + mapped-loopback handling */;
}

export async function fetchLocalAware(input: RequestInfo | URL, init?: RequestInit) {
  const url = typeof input === 'string' ? new URL(input) : input instanceof URL ? input : new URL(input.url);
  const isLoopback = url.hostname === 'localhost' || url.hostname === '127.0.0.1' || url.hostname === '::1';

  if (isLoopback) {
    // Always connect directly to loopback, even if HTTP_PROXY is set.
    return fetch(input, { ...init, /* dispatcher/agent: plain direct */ });
  }

  if (isProbablyLocalBaseUrl(url)) {
    // Use idle-timeout-free fetch for local model servers.
    return fetchWithoutIdleTimeouts(input, init);
  }

  // Otherwise keep proxy-aware behavior.
  return fetch(input, init);
}
```

Tests to require:
- With `HTTP_PROXY` set and `NO_PROXY` unset, verify loopback requests still reach the local server.
- Verify local-provider detection includes `0.0.0.0` / IPv4-mapped loopback so the relaxed timeout path is actually used.
- For sandbox changes, add a platform-gated test (or at least a static assertion) ensuring disallowed policy fields (like loopback ingress on rejected tiers) aren’t requested on that platform.
- For reconnect/disconnect, cover reconnect grace (if intended) and ensure callbacks aren’t re-run after reconnection.