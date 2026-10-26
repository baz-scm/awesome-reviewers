---
title: Loopback proxy bypass
description: When building custom network dispatchers, fetch wrappers, or NO_PROXY
  merging logic, never let proxy environment variables (HTTP_PROXY/HTTPS_PROXY/ALL_PROXY,
  any casing) route traffic to loopback/local addresses through a proxy. Libraries
  like undici's EnvHttpProxyAgent proxy everything, including localhost, whenever
  NO_PROXY is unset — this silently breaks...
repository: cline/cline
label: Networking
language: TypeScript
comments_count: 3
repository_stars: 70886
---

When building custom network dispatchers, fetch wrappers, or NO_PROXY merging logic, never let proxy environment variables (HTTP_PROXY/HTTPS_PROXY/ALL_PROXY, any casing) route traffic to loopback/local addresses through a proxy. Libraries like undici's EnvHttpProxyAgent proxy everything, including localhost, whenever NO_PROXY is unset — this silently breaks local tooling (e.g. LM Studio/Ollama model servers) for any user who launches the app with proxy env vars set but no NO_PROXY.

Always special-case loopback explicitly rather than relying on the proxy library's own matching:
- Enumerate every loopback spelling the user might hit: `localhost`, `127.0.0.1`/`127.x.x.x`, `::1`, `[::1]`, `0.0.0.0`, and IPv4-mapped IPv6 forms such as `::ffff:127.0.0.1` (which URL parsing can rewrite to `[::ffff:7f00:1]`). Match these with a real IP-aware matcher (e.g. Node's `BlockList`) rather than string equality, since mapped/compressed forms won't match literal lists.
- Route loopback hosts through a plain, non-proxying dispatcher/agent and send everything else through the proxy-aware one, mirroring the platform's own proxy resolver (VS Code's resolver always connects to loopback directly).
- When merging NO_PROXY values from multiple sources/casings, union the entries and always inject the loopback hosts, but preserve a `*` wildcard (opt-out of all proxying) on either side instead of overwriting it.
- Add regression tests that set a proxy env var (pointing at a rejecting/recording proxy) with NO_PROXY deliberately absent, and assert loopback requests connect directly while non-loopback requests hit the proxy. Don't only test with both proxy vars unset — that misses the exact corporate-proxy configuration that breaks this.

Example pattern:
```ts
const LOOPBACK_HOSTS = new Set(["localhost", "0.0.0.0", "::1", "::ffff:127.0.0.1"]);
function isLoopbackHost(input: string | URL | Request): boolean {
  const host = new URL(toUrlString(input)).hostname.replace(/^\[|\]$/g, "").toLowerCase();
  return LOOPBACK_HOSTS.has(host) || host.startsWith("127.") || blockList.check(host, "ipv6");
}
// direct, no-timeout Agent for loopback; EnvHttpProxyAgent for everything else
```
</description>
