---
title: Respect proxy env vars correctly
description: When building custom fetch dispatchers or HTTP clients that honor `HTTP_PROXY`/`HTTPS_PROXY`/`NO_PROXY`,
  never let a configured proxy silently swallow loopback or local-network traffic.
  Libraries like undici's `EnvHttpProxyAgent` will route `127.0.0.1`/`localhost`/local-server
  requests through the proxy whenever `HTTP_PROXY` is set and `NO_PROXY` doesn't...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Networking
language: TypeScript
comments_count: 4
repository_stars: 70965
---

When building custom fetch dispatchers or HTTP clients that honor `HTTP_PROXY`/`HTTPS_PROXY`/`NO_PROXY`, never let a configured proxy silently swallow loopback or local-network traffic. Libraries like undici's `EnvHttpProxyAgent` will route `127.0.0.1`/`localhost`/local-server requests through the proxy whenever `HTTP_PROXY` is set and `NO_PROXY` doesn't explicitly exempt them — this breaks local model servers (LM Studio, Ollama) that previously worked with the platform's default resolver, which always connects to loopback directly.

To apply this standard:
- Explicitly special-case loopback/local-network hosts to use a direct, non-proxied dispatcher, and only send everything else through the proxy-aware agent — mirroring the "always direct to loopback" convention of the platform's built-in resolver.
- When merging proxy configuration from multiple sources (e.g. both `HTTP_PROXY` and `http_proxy` casings), union all variants robustly rather than picking one, and short-circuit correctly when either side opts out entirely with `*`.
- Write regression tests that set the proxy env vars (e.g. `HTTP_PROXY` pointed at a dead/recording proxy) with `NO_PROXY` left unset, and assert that loopback requests still succeed directly while non-local requests are correctly proxied. Don't test only with proxy vars cleared — that masks the exact bug these agents introduce.
- Document any known gaps (e.g. DNS names resolving to LAN addresses not being detected as "local") as an accepted trade-off rather than silently leaving it unhandled.

Example shape of the fix:
```ts
function dispatcherFor(host: string): Agent {
  return isLoopbackOrLocal(host)
    ? directAgent // no proxy, no idle timeout
    : envProxyAgent // honors HTTP_PROXY/HTTPS_PROXY/NO_PROXY
}
```