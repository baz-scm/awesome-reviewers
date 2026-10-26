---
title: Identity-Aware Cache Rules
description: 'Use caches that are (1) identity-aware, (2) invalidation-correct, and
  (3) time- and failure-bounded.


  **Coding standard**

  1) **Cache keys must encode invalidation dimensions**: if a cached result is sensitive
  to plugin registry state, execution mode, account scope, etc., include those in
  the cache key (not just the “request args”).'
repository: cline/cline#v18
label: Caching
language: TypeScript
comments_count: 8
repository_stars: 70884
---

Use caches that are (1) identity-aware, (2) invalidation-correct, and (3) time- and failure-bounded.

**Coding standard**
1) **Cache keys must encode invalidation dimensions**: if a cached result is sensitive to plugin registry state, execution mode, account scope, etc., include those in the cache key (not just the “request args”).
2) **Use TTL with background refresh**: allow stale reads within TTL to avoid UX flicker, but reload behind the scenes after TTL; expose an explicit “Refresh” that forces a reload.
3) **Isolate failure from shared availability caches**: a failure in one lookup must not poison a shared cache/availability used by other independent lookups.
4) **Add bounded retry/backoff when detection may miss changes**: when “did it change?” signals (fingerprints, static analysis) can be incomplete, retry failures on a fixed backoff window rather than waiting for a detected change.
5) **Gate cached UI actions by revision+id**: any “use/send” or “apply” action that depends on cached/visible items must be refused if the currently displayed revision/item id no longer matches what the worker would accept.
6) **Snapshot user-visible inputs at commit time**: when starting a long operation, derive required inputs from the version the user selected/observed, not from “latest cache” that might update mid-flight.

**Sketch**
```ts
type CacheEntry<T> = { value: T; fetchedAt: number };
const TTL_MS = 60_000;

function getWithTtl<K, T>(
  key: K,
  cache: Map<string, CacheEntry<T>>,
  load: () => Promise<T>,
) {
  const k = JSON.stringify(key);
  const now = Date.now();
  const entry = cache.get(k);
  if (entry && now - entry.fetchedAt < TTL_MS) return entry.value; // stale ok within TTL

  // background refresh: return stale if present, otherwise block
  if (entry) void load().then(v => cache.set(k, { value: v, fetchedAt: Date.now() }));
  else throw load().then(v => (cache.set(k, { value: v, fetchedAt: Date.now() }), v));
}

function acceptUiAction(currentRevision: number, expectedRevision: number) {
  if (currentRevision !== expectedRevision) return { outcome: "refused", reason: "stale" } as const;
  return { outcome: "ok" } as const;
}
```

Apply this checklist across plugin inspection, repository/target resolution, session/status projection, and UI-driven “apply/use” flows.