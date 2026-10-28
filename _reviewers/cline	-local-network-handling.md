---
title: Local network handling
description: 'When code makes decisions based on whether an endpoint is "local" (e.g.
  skipping a proxy, extending idle timeouts for local model servers), enumerate all
  valid address representations rather than a convenient subset: IPv4 loopback/private/link-local
  ranges, `0.0.0.0`, IPv6 loopback/unique-local/link-local, and IPv4-mapped IPv6 addresses...'
repository: "cline/cline\t"
label: Networking
language: TypeScript
comments_count: 5
repository_stars: 70947
---

When code makes decisions based on whether an endpoint is "local" (e.g. skipping a proxy, extending idle timeouts for local model servers), enumerate all valid address representations rather than a convenient subset: IPv4 loopback/private/link-local ranges, `0.0.0.0`, IPv6 loopback/unique-local/link-local, and IPv4-mapped IPv6 addresses (`::ffff:127.0.0.1`). Prefer library utilities (e.g. Node's `BlockList`, which normalizes mapped addresses) over hand-rolled regexes, and mirror the platform's existing resolution behavior (e.g. a VS Code proxy resolver that always connects to loopback directly) instead of trusting a dependency's default, which may proxy everything unless `NO_PROXY` happens to match. Add regression tests that exercise the proxy/timeout decision with realistic env-var combinations (e.g. `HTTP_PROXY` set, `NO_PROXY` unset) against both a loopback and a non-local target.

Separately, every network call on a critical path — including fallback/secondary requests, not just the primary one — must carry an explicit timeout or `AbortSignal`. An unbounded fallback fetch against a host that drops packets (closed VPN, unreachable LAN server) will hang indefinitely and stall the whole operation, even if the primary call is already bounded. When a timeout does fire, distinguish "this specific request stalled" from "the connection is dead": prefer a lightweight health probe or waiting for any reply on the same connection before tearing it down, so one slow operation doesn't kill other in-flight traffic.

Example gap to avoid:
```ts
// Primary call is bounded, fallback is not — silently reintroduces a hang.
try {
  return await fetchWithTimeout(primaryUrl, { signal: AbortSignal.timeout(5000) })
} catch {
  return await fetch(fallbackUrl) // no timeout: hangs on a dead host
}
```
</description>
