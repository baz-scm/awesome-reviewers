---
title: Cache key and invalidation correctness
description: 'Caches and memoized state cause subtle bugs when the key or invalidation
  logic doesn''t account for every dimension that affects the cached value''s validity.
  When building a cache (in-memory, on-disk, or a "remembered" state keyed by id),
  verify:'
repository: cline/cline;
label: Caching
language: TypeScript
comments_count: 6
repository_stars: 70964
---

Caches and memoized state cause subtle bugs when the key or invalidation logic doesn't account for every dimension that affects the cached value's validity. When building a cache (in-memory, on-disk, or a "remembered" state keyed by id), verify:

1. The cache key must encode every input that changes the correct output. If any factor can flip the result (a new turn even without tool calls, a plugin's enabled/disabled state, an execution mode, a workspace path), fold it into the key so a change is never silently masked by a stale hit. Example: a refresh key based only on tool-call count missed turns with no tool calls; it had to become `${status}:${userCount}:${toolCount}` so every turn invalidates it. Likewise, a plugin-inspection cache key had to include the plugin's registry `state`/`updatedAt` so toggling a plugin off/on busts the cache.

2. Never assume a retained resource (an open connection, a warmed service, a held host) is still valid just because it was valid when created — revalidate it against the authoritative source on each read instead of trusting continuous observation. A connection kept alive across record updates must be re-checked against the latest record, not treated as proof the remembered status still holds.

3. Use the same key that lookups will actually use. A cache warmed under one key (e.g., process launch cwd) is useless if real reads use a different key (e.g., the resolved/adopted workspace path); warm or populate the cache from the single source that produces the key consumers will query.

4. Prefer a stale-while-revalidate pattern with an explicit TTL: return the cached value immediately to avoid flicker/latency, kick off a background refresh past the TTL, and expose an explicit "force refresh" path for user-triggered updates. Avoid caches with no TTL/invalidation path at all, and avoid caching failed/partial results — only cache clean, complete outcomes so a transient failure doesn't poison later reads.

When adding or reviewing a cache, explicitly state in code comments: what the key represents, what triggers invalidation, and why a retained resource doesn't exempt a read from revalidation.