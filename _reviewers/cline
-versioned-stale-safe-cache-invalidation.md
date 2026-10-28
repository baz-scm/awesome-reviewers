---
title: Versioned, stale-safe cache invalidation
description: Async caches (file reads, diffs, generated artifacts, remote catalogs)
  must guard against race conditions between in-flight fetches and invalidation events,
  and must invalidate on every trigger that can make the data stale.
repository: 'cline/cline

  '
label: Caching
language: TSX
comments_count: 6
repository_stars: 70942
---

Async caches (file reads, diffs, generated artifacts, remote catalogs) must guard against race conditions between in-flight fetches and invalidation events, and must invalidate on every trigger that can make the data stale.

- Tag each cache entry with a per-key generation/version counter. Bump it on every invalidation trigger (manual refresh, closing a tab, an agent/external edit, switching context such as org→personal). When an async response resolves, compare its captured generation to the current one and discard the response if it's stale instead of overwriting fresher data.
- Prefer marking entries `stale` and keeping the previously cached value visible while a refetch runs, rather than deleting the cache outright — this avoids spinner/flash regressions on polling or background refresh. Only replace the displayed content once the fresh response lands.
- If a read is already in flight when a new invalidation/snapshot arrives, don't cancel or duplicate it — let it land, then trigger at most one follow-up read if the entry is still marked stale.
- Don't invalidate based on shallow signatures (e.g., comparing counts) — a single changed byte can be missed. When in doubt, invalidate broadly (mark the whole cache stale) rather than relying on a fragile equality check.
- For cached derived/generated resources (e.g., materialized files from base64 payloads), key the cache by a content hash rather than by call order, so repeated generation of identical data reuses the existing artifact instead of leaking duplicates.
- Audit every place a cache is populated from a stale source (e.g., fetching a remote catalog once and reusing it across contexts) and force a refetch when the context that produced the cached value changes.

Example pattern for generation-guarded invalidation:
```ts
const readGenerationRef = useRef(new Map<string, number>());

function invalidate(keys: Iterable<string>) {
  for (const key of keys) {
    readGenerationRef.current.set(key, (readGenerationRef.current.get(key) ?? 0) + 1);
  }
}

async function read(key: string) {
  const generation = readGenerationRef.current.get(key) ?? 0;
  const result = await fetchData(key);
  if ((readGenerationRef.current.get(key) ?? 0) !== generation) return; // stale, discard
  applyResult(key, result);
}
```