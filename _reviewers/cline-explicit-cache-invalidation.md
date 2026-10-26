---
title: Explicit cache invalidation
description: Don't rely on a bare TTL to keep a cache correct, and never treat "the
  connection/process is still alive" as proof a cached value is still fresh. Whenever
  the underlying source can change in a way you can detect (an edited setting, an
  edited pin definition, a new record version from the server), invalidate or re-validate
  the cache entry immediately on that...
repository: cline/cline
label: Caching
language: TypeScript
comments_count: 6
repository_stars: 70886
---

Don't rely on a bare TTL to keep a cache correct, and never treat "the connection/process is still alive" as proof a cached value is still fresh. Whenever the underlying source can change in a way you can detect (an edited setting, an edited pin definition, a new record version from the server), invalidate or re-validate the cache entry immediately on that signal rather than waiting out the TTL. When revalidating a remembered value against its source, compare it against the source's own version/timestamp (e.g. a record's `updatedAt`), not against how long a socket has been open — a retained connection is not evidence of continuous observation.

For cache keys, include exactly the inputs that determine the value's identity (e.g. tool name + arguments, ignoring key order) and exclude cosmetic fields (e.g. a display label), so edits to the identity invalidate the entry while cosmetic edits don't.

For external data with no explicit invalidation hook (e.g. a third-party repository list), use a short TTL with stale-while-revalidate: return the cached value immediately to avoid UI flicker, kick off a background refresh, and let an explicit "Refresh" action force a reload. Avoid invalidation feedback loops: only signal/notify downstream consumers when a refresh actually produced a new value, not every time a refresh attempt completes (including failed attempts that fall back to a default).

Example of version-based revalidation instead of trusting a live connection:
```ts
if (existing.agentStatus && isSettled(existing.agentStatus)) {
  // Re-check against the newest record version, not against connection uptime.
  existing.agentStatus = this.rememberedStatusOf(record)
}
```