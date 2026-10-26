---
title: Correctness-Driven Caching
description: 'Caching rules for correctness: the cache key must fully represent the
  semantic inputs, and the cache must only be served while a matching revision/generation
  still applies.'
repository: cline/cline#v3
label: Caching
language: TypeScript
comments_count: 7
repository_stars: 70863
---

Caching rules for correctness: the cache key must fully represent the semantic inputs, and the cache must only be served while a matching revision/generation still applies.

**Standard**
1. **Key by all inputs that change output**
   - Include identities (e.g., tool name / plugin path / session id) *and* parameters (e.g., arguments, repo+branch, account scope).
   - For object arguments, use a stable serialization where key order doesn’t affect the result.
2. **Gate cache usage with a revision/generation**
   - If the producer can change (pin edited, feature flag toggled, account scope switched, plugin state changes), attach a `revision`/`generation` to the cache entry and only serve when it still matches.
   - Never let late async results overwrite newer semantics.
3. **Invalidate dependent caches on upstream changes**
   - When you change a toggle/setting that affects what should be listed or computed, invalidate all downstream caches *before* emitting updated state.
4. **Use TTL only as a performance optimization**
   - TTL must not be the mechanism that ensures correctness. If correctness depends on a snapshot (e.g., “model the user submitted”), take the snapshot once and ignore later cache refreshes for that operation.
5. **Retry failures with bounded backoff when keys/fingerprints may not change**
   - If a failure might be “invisible” to change detection (e.g., not covered by fingerprint), cache the failure briefly and retry on a schedule with an upper bound.

**Example pattern (revision-gated cache)**
```ts
type CacheEntry = { revision: number; value: string };

function stableArgsKey(args: Record<string, unknown>): string {
  // stable stringify (key-order independent)
  return JSON.stringify(Object.keys(args).sort().map(k => [k, args[k]]));
}

function makeCacheKey(tool: string, args: Record<string, unknown>) {
  return `${tool}:${stableArgsKey(args)}`;
}

class Cache {
  private map = new Map<string, CacheEntry>();

  get(key: string, currentRevision: number): string | undefined {
    const entry = this.map.get(key);
    return entry && entry.revision === currentRevision ? entry.value : undefined;
  }

  set(key: string, revision: number, value: string) {
    this.map.set(key, { revision, value });
  }
}
```

Apply this across your codebase for pinned/task results, plugin discovery caches, cloud list/status snapshots, and any “derived” cache that can be invalidated by config, scope, or edits.