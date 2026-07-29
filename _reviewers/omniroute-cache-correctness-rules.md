---
title: Cache correctness rules
description: 'Adopt a “cache correctness” checklist for all in-memory/DB caches:


  1) Explicit bypass must be honored

  - If the caller passes a disable value (commonly `ttlMs === 0`), bypass both lookup
  and inflight coalescing. Don’t treat `0` as “use default TTL”.'
repository: diegosouzapw/OmniRoute
label: Caching
language: TypeScript
comments_count: 7
repository_stars: 33162
---

Adopt a “cache correctness” checklist for all in-memory/DB caches:

1) Explicit bypass must be honored
- If the caller passes a disable value (commonly `ttlMs === 0`), bypass both lookup and inflight coalescing. Don’t treat `0` as “use default TTL”.

2) Never poison future caching on failure
- When the cached mechanism becomes invalid (e.g., a limiter instance after repeated 429), evict/disconnect so future calls lazily create a fresh instance.
- Avoid permanently stopping/poisoning objects that remain referenced by in-flight work.

3) Guard correctness against changing upstream state
- Use generation/epoch guards and clear/bump generations on relevant writes.
- Keep caches bounded (max size) and add TTL/staleness policies aligned to refresh cadence.
- Provide test reset hooks for any module-level cache that depends on mutable external state.

Example patterns:

// (1) Honor ttlMs=0 bypass (also ensure defaulting doesn’t override 0)
async function getOrCoalesce<T>(ttlMs: number, fetchFn: () => Promise<T>) {
  if (ttlMs <= 0) {
    const data = await fetchFn();
    return { data, cached: false };
  }
  // ... normal cache lookup + inflight coalescing
}

// (2) Evict rather than stop/poison
function onRateLimited429(/* ... */) {
  // evict so future getLimiter() creates a new instance
  // DO NOT call stop() if it would permanently reject future scheduling
}

// (3) Generation-guarded, bounded cache
const MAX = 100;
let gen = 0;
const cache = new Map<string, { generation: number; value: string }>();

function onWriteThatAffectsCache() {
  gen++;
  cache.clear();
}

function get(key: string): string | null {
  const entry = cache.get(key);
  if (!entry || entry.generation !== gen) return null;
  return entry.value;
}

function set(key: string, value: string) {
  if (cache.size >= MAX) cache.delete(cache.keys().next().value);
  cache.set(key, { generation: gen, value });
}

Rule of thumb: every cache needs (a) explicit bypass semantics, (b) safe invalidation/eviction, and (c) a correctness strategy for when upstream data changes (generation/TTL + bounded size + test reset).