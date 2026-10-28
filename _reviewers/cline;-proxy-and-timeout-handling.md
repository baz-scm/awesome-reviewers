---
title: Proxy and timeout handling
description: When writing custom fetch/dispatcher logic, never let proxy environment
  variables (HTTP_PROXY/HTTPS_PROXY) silently break direct connections to loopback
  or local-network addresses. Runtimes like VS Code and undici's EnvHttpProxyAgent
  route everything through the configured proxy unless NO_PROXY matches, so any custom
  dispatcher must explicitly replicate the...
repository: cline/cline;
label: Networking
language: TypeScript
comments_count: 4
repository_stars: 70964
---

When writing custom fetch/dispatcher logic, never let proxy environment variables (HTTP_PROXY/HTTPS_PROXY) silently break direct connections to loopback or local-network addresses. Runtimes like VS Code and undici's EnvHttpProxyAgent route everything through the configured proxy unless NO_PROXY matches, so any custom dispatcher must explicitly replicate the "always connect directly to loopback" rule before applying proxy-aware routing. Normalize and compare hosts carefully: strip brackets, handle IPv6-mapped IPv4 forms (e.g. `::ffff:127.0.0.1`), and prefer a robust matcher such as `net.BlockList` over ad-hoc string checks. Add regression tests with HTTP_PROXY set and NO_PROXY unset to catch silent proxying of local addresses.

Separately, every outbound request—including fallback code paths—must have an explicit, bounded timeout via AbortSignal. A request to a local service that may take a long time to produce its first byte (e.g. a local LLM server generating tokens) should use relaxed idle/body timeouts rather than no timeout at all, while remote/fallback requests must still abort within a reasonable window; an unbounded `fetch` in a fallback branch can hang indefinitely against a host that drops packets instead of refusing the connection, stalling the whole operation.

Example of correct routing:
```ts
function isLoopbackHost(input: string | URL | Request): boolean {
  const host = extractHostname(input)
  return LOOPBACK_BLOCKLIST.check(host) // handles 127.0.0.0/8, ::1, ::ffff:127.0.0.1, etc.
}

export const fetchForProvider: typeof fetch = (input, init) => {
  const dispatcher = isLoopbackHost(input)
    ? directDispatcher ??= new Agent(NO_IDLE_TIMEOUTS)
    : proxiedDispatcher ??= new EnvHttpProxyAgent()
  return undiciFetch(input, { ...init, dispatcher })
}
```
And ensure fallback calls are bounded:
```ts
const controller = new AbortController()
const timer = setTimeout(() => controller.abort(), 5_000)
try {
  return await fetchModelIdsFromSource(url, { signal: controller.signal })
} finally {
  clearTimeout(timer)
}
```</description>
</invoke>
