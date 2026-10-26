---
title: Bound and route network
description: 'Network code must be reliable under disconnects, proxies, and partial
  connectivity.


  Apply this checklist:

  1) **Bound + cancel every path**: Any HTTP/TCP fetch (including fallbacks) must
  honor an `AbortSignal` (and/or a timeout) so “packet drop” scenarios don’t hang
  beyond the UI/task lifecycle.'
repository: cline/cline#v5
label: Networking
language: TypeScript
comments_count: 7
repository_stars: 70864
---

Network code must be reliable under disconnects, proxies, and partial connectivity.

Apply this checklist:
1) **Bound + cancel every path**: Any HTTP/TCP fetch (including fallbacks) must honor an `AbortSignal` (and/or a timeout) so “packet drop” scenarios don’t hang beyond the UI/task lifecycle.
2) **Make retry side-effect safe**: For “send” flows, clearly distinguish **pre-dispatch vs post-dispatch** (or “confirmed vs lost reply”) so retry/resend only occurs when no side effects were sent. Preserve pending operations across brief reconnects only if your lifecycle explicitly supports it.
3) **Preserve intended routing (proxy vs direct)**: Local/loopback requests must not be silently routed through environment proxies. When using custom fetch/dispatchers, ensure loopback bypass is preserved even when `HTTP_PROXY` is set.
4) **Classify local addresses correctly**: When choosing special local-network behavior, include common real-world forms like `0.0.0.0/32` and IPv4-mapped IPv6 (`::ffff:127.0.0.1`).
5) **Least-necessary network policy**: In sandboxes/isolators, don’t add permissive ingress/loopback rules unless required; some enforcement tiers reject those policies and break execution.

Example (bounded fallback + abort):
```ts
async function fetchModelIdsWithAbort(url: string, signal: AbortSignal) {
  // Ensure fallback fetches also use the same signal.
  return fetch(url, { signal });
}
```

Example (loopback direct routing when proxy exists):
- If you override fetch/dispatchers, add a “loopback uses direct agent, others use EnvHttpProxyAgent” rule, and cover tests with `HTTP_PROXY` set and `NO_PROXY` unset.