---
title: Loopback bypass and timeouts
description: 'When writing custom fetch/proxy logic, treat local and remote destinations
  correctly and never let a network call hang indefinitely.


  1. Loopback/local-network bypass must match the platform''s own proxy resolver.
  Agents like undici''s `EnvHttpProxyAgent` will proxy `localhost`/`127.0.0.1`/`::1`
  whenever `HTTP_PROXY`/`HTTPS_PROXY` is set and `NO_PROXY`...'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Networking
language: TypeScript
comments_count: 4
repository_stars: 70964
---

When writing custom fetch/proxy logic, treat local and remote destinations correctly and never let a network call hang indefinitely.

1. Loopback/local-network bypass must match the platform's own proxy resolver. Agents like undici's `EnvHttpProxyAgent` will proxy `localhost`/`127.0.0.1`/`::1` whenever `HTTP_PROXY`/`HTTPS_PROXY` is set and `NO_PROXY` doesn't explicitly exempt them. If the existing fetch stack always connects to loopback directly, a custom dispatcher must preserve that behavior (e.g. route loopback hosts through a plain `Agent`, everything else through the env-proxy agent). Add regression tests with the proxy env var set and `NO_PROXY` *unset* — deleting both vars in tests hides this bug.

2. `NO_PROXY` matching in many HTTP stacks (undici, Bun, curl) is literal per-host and per-casing, not fuzzy. When programmatically injecting a loopback bypass, enumerate every spelling (`localhost`, `127.0.0.1`, `::1`, `[::1]`) and merge into both the upper- and lower-case env var variants, while still honoring an existing `*` wildcard opt-out on either casing.

3. When classifying an endpoint as "local" to decide on proxy/timeout behavior, use the same IP-range/hostname heuristics consistently (e.g. RFC1918 ranges, `::1`, `.local`/`.internal` suffixes) and document known gaps (e.g. DNS names resolving to local IPs are not detected without an extra resolution step) rather than silently guessing.

4. Every network call — including fallback paths — must be bounded by an explicit timeout or `AbortSignal`. A primary request guarded by a 5s abort but a fallback using a bare `fetch` with no timeout will hang forever against a host that drops packets instead of refusing the connection (e.g. VPN down, remote server unreachable). Audit all fetch call sites reachable from the same code path and ensure each one propagates or sets its own abort/timeout so a single unresponsive host can't block a user-facing operation (e.g. task start).

Example pattern for local-host-aware dispatch:
```ts
function dispatcherFor(host: string): Dispatcher {
  return isLoopback(host) ? noTimeoutAgent : envProxyAgent;
}
```
Example for bounding a fallback call:
```ts
async function fetchModelIdsFromSource(url: string) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 5000);
  try {
    return await fetch(url, { signal: controller.signal });
  } finally {
    clearTimeout(timer);
  }
}
```</description>
</invoke>
