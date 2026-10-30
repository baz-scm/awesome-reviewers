---
title: Cache keys and invalidation
description: 'Caches must never serve data that silently diverges from the current
  source of truth. When adding a cache, explicitly design its invalidation and lifecycle
  rather than defaulting to "cache forever" or "cache per handle":'
repository: cline/cline#zzz-unlikely-123abc
label: Caching
language: TypeScript
comments_count: 7
repository_stars: 71035
---

Caches must never serve data that silently diverges from the current source of truth. When adding a cache, explicitly design its invalidation and lifecycle rather than defaulting to "cache forever" or "cache per handle":

1. **Key on everything that affects the result.** A cache key must include every input that changes the output — not just an id. A pinned-tool cache keyed only by scope id served stale results after the pin's tool/arguments changed; it was fixed by keying on tool+arguments (order-independent) plus a revision. A plugin-inspection cache missed turned-off/reloaded plugins because the key omitted registry `state`/`updatedAt` and execution mode. A warm-up cache for a per-workspace service must be keyed by the exact resolved path later used to look it up, not by a value (e.g. process cwd) that can differ from it in production.

2. **Prefer change detection over indefinite caching.** Where feasible, invalidate via a cheap, real signal — file mtime, content fingerprint, or an explicit revision/version — rather than caching per-process for the session lifetime. A conventions cache that never re-read `package.json` kept suggesting a removed script; switching to an mtime-checked reader per call fixed it. A plugin-source fingerprint should follow every file actually reachable (including side-effect imports), with a backoff-retry fallback for changes a fingerprint can't see (dynamic imports, `node_modules`).

3. **For externally-owned or distributed data, use a bounded TTL with background refresh (stale-while-revalidate)** instead of either no expiry or a blocking refetch on every read: return the cached value immediately, kick off a refresh after it ages past the TTL, and keep an explicit manual-refresh path for the user-triggered case. Accept that perfect consistency with an external system (e.g., access granted/revoked elsewhere) is not achievable — bound the staleness window instead of trying to eliminate it.

4. **Give every cache a lifecycle, not just a fill path.** On-disk or otherwise resource-backed caches need a clear write-once/read-many contract and, where applicable, disposal. Don't recompute or rewrite a cached artifact on every read (e.g., re-truncating a large tool result on each request); write it once at completion and reuse the pointer. If a cache directory accumulates files across runs, give it a disposal path tied to the owning lifetime (session/runtime shutdown) instead of leaving it to grow unbounded.

5. **Add a regression test for the invalidation condition itself** (e.g., "does not answer from a cached inspection after the plugin is turned off", "re-reads repositories once they age"), not just for the happy-path cache hit.</description>
</invoke>
