---
title: Bound every network call
description: Every network request, including fallback and retry paths, must have
  an explicit, bounded timeout or deadline so a dropped connection, a silent/slow
  server, or a reconnect-in-progress can never hang a task indefinitely. When one
  code path adds an AbortSignal/timeout but a fallback does not (e.g. a primary request
  times out at 5s while...
repository: cline/cline#zzz-unlikely-123abc
label: Networking
language: TypeScript
comments_count: 4
repository_stars: 71035
---

Every network request, including fallback and retry paths, must have an explicit, bounded timeout or deadline so a dropped connection, a silent/slow server, or a reconnect-in-progress can never hang a task indefinitely. When one code path adds an AbortSignal/timeout but a fallback does not (e.g. a primary request times out at 5s while `fetchModelIdsFromSource` falls back to a bare `fetch` with no timeout), the fallback can hang forever against a host that drops packets instead of refusing — defeating the original timeout. Apply timeouts consistently to every branch, and make deadlines survive reconnects (e.g. a pending run should reject within a fixed window if no replay/live evidence arrives, rather than waiting forever).

When special-casing network behavior by address (e.g. disabling idle timeouts or bypassing a proxy for local/loopback servers), the address-matching logic must be exhaustive, not just the common cases. Ollama/LM Studio often bind to `0.0.0.0`, and IPv4 loopback can appear as an IPv4-mapped IPv6 address (`::ffff:127.0.0.1`); missing these causes requests to silently fall back to the wrong timeout/proxy behavior. Prefer a single well-tested address-matching utility (e.g. `BlockList`, which normalizes `::ffff:` mappings against IPv4 rules) over hand-rolled range checks, and add `0.0.0.0/32` explicitly if it's meant to be treated as local. Cover both spellings in tests.

Example of the kind of gap to avoid:
```ts
// BAD: primary path has a timeout, fallback does not
const res = await fetchWithTimeout(url, { signal: AbortSignal.timeout(5000) })
  .catch(() => fetchModelIdsFromSource(fallbackUrl)); // no timeout — can hang forever

// GOOD: every path is bounded
const res = await fetchWithTimeout(url, { signal: AbortSignal.timeout(5000) })
  .catch(() => fetchModelIdsFromSource(fallbackUrl, { signal: AbortSignal.timeout(5000) }));
```