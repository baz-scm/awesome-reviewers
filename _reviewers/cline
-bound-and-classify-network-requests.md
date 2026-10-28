---
title: Bound and classify network requests
description: Every outbound network call must be defensively bounded and any locality-based
  special-casing must be exhaustive, otherwise you get hangs or silent behavior regressions.
repository: "cline/cline\r\n"
label: Networking
language: TypeScript
comments_count: 5
repository_stars: 70946
---

Every outbound network call must be defensively bounded and any locality-based special-casing must be exhaustive, otherwise you get hangs or silent behavior regressions.

1. Timeouts/abort signals are mandatory on every fetch, including fallback paths. A primary request can be wrapped in an AbortSignal while a secondary/fallback call uses a bare `fetch` with no timeout — that fallback will hang against a host that drops packets instead of refusing, stalling the whole operation (e.g. task start). Every code path that issues a network request, including error-recovery fallbacks, needs its own timeout.

2. Never trust server-declared size headers (e.g. `Content-Length`) to enforce limits. Read responses incrementally and cancel/abort as soon as the running total crosses the limit, so a missing or wrong header can't force buffering an unbounded body into memory.

3. When request behavior is conditioned on "is this address local/loopback/proxied," the classification logic must cover all real-world address forms, not just the common case: `0.0.0.0` (what local servers print when bound to all interfaces), IPv4-mapped IPv6 (`::ffff:127.0.0.1`), and the full RFC1918/loopback/link-local ranges. Getting this wrong either defeats a timeout override meant for local servers, or — more seriously — breaks an existing proxy-bypass guarantee (e.g. a plain proxy-aware dispatcher will route loopback traffic through an HTTP proxy unless explicitly excluded, even though the platform's own resolver always connects to loopback directly). Add regression tests that set the relevant proxy/no-proxy environment variables and assert both the local and non-local paths route correctly, e.g.:

```ts
function isLocalNetworkUrl(baseUrl: string | undefined): boolean {
  if (!baseUrl) return true
  const host = new URL(baseUrl).hostname.replace(/^\[|\]$/g, "").toLowerCase()
  const family = isIP(host)
  if (family) {
    // BlockList.check handles ::ffff: mapped addresses against the IPv4 rules
    return LOCAL_NETWORK_ADDRESSES.check(host, family === 6 ? "ipv6" : "ipv4")
  }
  return !host.includes(".") || /\.(localhost|local|internal)$/.test(host)
}
```

4. Document known gaps explicitly (e.g. DNS names resolving to a LAN IP are not detected without an extra resolution step) rather than silently accepting partial coverage, so the trade-off is visible to future readers.