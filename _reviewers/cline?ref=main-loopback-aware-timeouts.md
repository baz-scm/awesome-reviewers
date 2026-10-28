---
title: Loopback-aware timeouts
description: When overriding default HTTP timeout or proxy behavior for network calls
  (e.g. disabling undici's idle timeouts for slow local model servers), be exhaustive
  about what counts as "local" and never leave a network call without an explicit,
  bounded timeout.
repository: cline/cline?ref=main
label: Networking
language: TypeScript
comments_count: 5
repository_stars: 70980
---

When overriding default HTTP timeout or proxy behavior for network calls (e.g. disabling undici's idle timeouts for slow local model servers), be exhaustive about what counts as "local" and never leave a network call without an explicit, bounded timeout.

1. Match every representation of a loopback/local address, not just the obvious one. `127.0.0.1`, `localhost`, `::1`, `0.0.0.0`, and IPv4-mapped IPv6 forms like `::ffff:127.0.0.1` (which `new URL()` normalizes to `[::ffff:7f00:1]`) must all resolve to the same bucket. Prefer a structured matcher (e.g. Node's `BlockList` with IPv4 subnets, which also matches `::ffff:` addresses against those same rules) over ad-hoc string prefix checks.

2. Preserve existing proxy-bypass semantics when introducing a custom dispatcher/agent. Libraries like undici's `EnvHttpProxyAgent` will route *everything*, including loopback, through `HTTP_PROXY`/`http_proxy` whenever `NO_PROXY` is unset — which is exactly the shape of a typical corporate environment. If the platform you're integrating with (VS Code, JetBrains, etc.) always connects to loopback directly, your override must replicate that: route loopback/local-network hosts through a plain no-timeout dispatcher, and only use the proxy-aware dispatcher for everything else.

3. Apply timeout/cancellation handling consistently across *all* code paths for a feature, not just the primary one. A bounded request with an `AbortSignal` is worthless if its fallback path uses a bare `fetch` with no timeout — against a host that drops packets instead of refusing, that fallback hangs indefinitely and the user-facing operation never completes.

4. Write regression tests that set the proxy environment variables rather than just deleting them. A test suite that clears `HTTP_PROXY`/`NO_PROXY` before asserting direct behavior doesn't exercise the scenario that actually breaks in production: `HTTP_PROXY` set, `NO_PROXY` absent.

Example pattern for routing local vs. remote hosts:

```ts
const LOCAL_NETWORK_ADDRESSES = new BlockList()
for (const [address, prefix] of [
  ["127.0.0.0", 8], ["0.0.0.0", 32], ["10.0.0.0", 8],
  ["172.16.0.0", 12], ["192.168.0.0", 16],
] as const) {
  LOCAL_NETWORK_ADDRESSES.addSubnet(address, prefix, "ipv4")
}
LOCAL_NETWORK_ADDRESSES.addAddress("::1", "ipv6")

function dispatcherFor(host: string) {
  return isLocal(host, LOCAL_NETWORK_ADDRESSES)
    ? new Agent({ headersTimeout: 0, bodyTimeout: 0 }) // no proxy, no idle timeout
    : new EnvHttpProxyAgent() // honors HTTP_PROXY/NO_PROXY, keeps default timeouts
}
```

And ensure fallback requests carry the same timeout discipline as the primary request (e.g. `fetch(url, { signal: AbortSignal.timeout(5000) })`) so an unreachable fallback host fails fast instead of hanging the caller.