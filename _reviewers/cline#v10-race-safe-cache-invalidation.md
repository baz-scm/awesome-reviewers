---
title: Race-Safe Cache Invalidation
description: 'Adopt race-safe caching for async reads: when a cache entry is invalidated
  (refresh, close, external edits, snapshot updates), ensure any in-flight request
  can’t overwrite the newly-fresh state. Pair this with “don’t write derived state
  that should be user-controlled” and “don’t reload stable config on unrelated refresh.”'
repository: cline/cline#v10
label: Caching
language: TSX
comments_count: 4
repository_stars: 70869
---

Adopt race-safe caching for async reads: when a cache entry is invalidated (refresh, close, external edits, snapshot updates), ensure any in-flight request can’t overwrite the newly-fresh state. Pair this with “don’t write derived state that should be user-controlled” and “don’t reload stable config on unrelated refresh.”

**Rules**
1. **Version every cached entry**: keep a per-key “generation” (or request id). Increment generation whenever that key’s cache is dropped/invalidated.
2. **Discard stale responses**: when a response arrives, compare its generation/request id with the latest. If it no longer matches, drop it.
3. **Mark-but-don’t-clobber** on snapshot changes: mark cached entries as `stale` when external snapshots arrive, then re-read only when needed (avoid clearing state in a way that causes UI flicker and extra races).
4. **Minimize invalidations**: don’t clear or reload caches on events that don’t actually change the underlying configuration/data.
5. **Separate user selection from async reads**: if the user chose something (Local/Cloud, target selection), ensure late async lookups don’t flip that choice. Store source-of-truth choices, and derive dependent fields from current state.

**Reusable pattern (generation-based discard)**
```ts
const generationByKey = useRef(new Map<string, number>());

function bump(keys: Iterable<string>) {
  for (const key of keys) {
    generationByKey.current.set(key, (generationByKey.current.get(key) ?? 0) + 1);
  }
}

async function readWithCache(key: string, fetcher: () => Promise<string>) {
  const gen = generationByKey.current.get(key) ?? 0;
  const result = await fetcher();
  // Ignore late responses
  if ((generationByKey.current.get(key) ?? 0) !== gen) return;
  // Commit result to cache/UI
  // setCache(key, result)
}
```

**Application guidance**
- Call `bump([...keys])` from every operation that drops/invalidates cached contents (manual refresh, tab close, external edit, snapshot-based invalidation).
- For repo/snapshot-driven updates, prefer `stale=true` + follow-up reads over wiping caches immediately.
- For stable configuration (e.g., base URLs tied to environment/backend lifecycle), resolve once and reuse across account refreshes/reconnects unless the initial lookup failed.