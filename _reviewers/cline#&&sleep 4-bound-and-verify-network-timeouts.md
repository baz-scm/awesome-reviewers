---
title: Bound and verify network timeouts
description: Every outbound network call, including fallback and secondary code paths,
  must have an explicit timeout or AbortSignal; an unbounded `fetch` that only "previously
  stalled webview surfaces" can now hang a critical path (e.g. task start) when a
  host drops packets instead of refusing. When a request times out or a connection
  drops, treat it as "unknown...
repository: cline/cline#&&sleep 4
label: Networking
language: TypeScript
comments_count: 5
repository_stars: 70980
---

Every outbound network call, including fallback and secondary code paths, must have an explicit timeout or AbortSignal; an unbounded `fetch` that only "previously stalled webview surfaces" can now hang a critical path (e.g. task start) when a host drops packets instead of refusing. When a request times out or a connection drops, treat it as "unknown outcome," not "failed": prefer a bounded health probe or reconnect-with-resume over immediately retiring the transport, and never blindly replay a command that may not be idempotent (writes especially).

Any logic that classifies an address as local/loopback/proxy-bypassable must be exhaustive and tested against real-world variants, not just the common case: `0.0.0.0`, IPv4-mapped IPv6 (`::ffff:127.0.0.1`), private ranges (RFC1918, link-local, ULA), and the interaction with environment-driven proxy agents (`HTTP_PROXY`/`NO_PROXY`) which otherwise silently route loopback traffic through a proxy and break local model servers. Add regression tests that set the relevant environment variables (`HTTP_PROXY` set, `NO_PROXY` unset) and assert direct routing for loopback/local hosts, and unroutable-through-proxy behavior for everything else.

Example of what to guard against:
```ts
// BAD: no timeout on the fallback path
async function fetchModelIdsFromSource(url: string) {
  const res = await fetch(url) // can hang forever on a host that drops packets
  ...
}

// GOOD
async function fetchModelIdsFromSource(url: string, timeoutMs = 5000) {
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), timeoutMs)
  try {
    const res = await fetch(url, { signal: controller.signal })
    ...
  } finally {
    clearTimeout(timer)
  }
}
```
Document the chosen timeout/retry policy (including why non-idempotent operations are not replayed) directly next to the implementation, and cover the documented edge cases with tests rather than relying on manual verification.