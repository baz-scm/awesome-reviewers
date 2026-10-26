---
title: Cache with provenance keys
description: 'Use caching only when you can prove the cached value is still valid
  for the *exact dependency set* that produced it. Concretely:


  - **Key by provenance, not by identity alone:** include the inputs that determine
  the output (e.g., tool name + normalized arguments; plugin path + execution mode;
  pin revision).'
repository: cline/cline#v9
label: Caching
language: TypeScript
comments_count: 7
repository_stars: 70868
---

Use caching only when you can prove the cached value is still valid for the *exact dependency set* that produced it. Concretely:

- **Key by provenance, not by identity alone:** include the inputs that determine the output (e.g., tool name + normalized arguments; plugin path + execution mode; pin revision).
- **Bind cached values to a validity condition:** serve cached data only while the producing definition still matches; when a definition changes, invalidate or return “no data” rather than serving stale output.
- **Guard async superseding:** if a newer request/scope/definition arrives while an older async load is in-flight, discard the older result (e.g., compare generation/revision before writing).
- **Bound lifetime and memory:** enforce TTL and/or size/idle eviction (byte budgets, LRU, idle iteration limits) so caches can’t grow stale or unbounded.
- **When invalidation is incomplete, add retry/backoff:** if you can’t reliably detect changes (e.g., dynamic imports, fingerprint blind spots), retry after a delay but with limits, and avoid retrying side-effecting operations.

Example pattern (pinned-read style):
```ts
type CacheEntry = { revision: number; fetchedAt: number; value: string };

class ExamplePinnedCache {
  private cache = new Map<string, CacheEntry>();

  refresh(scopeId: string, currentRevision: number, compute: () => Promise<string>) {
    // Only overwrite when the caller's revision is still current.
    return compute().then((value) => {
      const prev = this.cache.get(scopeId);
      // If revision changed mid-flight, do not serve old data.
      if (prev && prev.revision !== currentRevision) return;
      this.cache.set(scopeId, { revision: currentRevision, fetchedAt: Date.now(), value });
    });
  }

  read(scopeId: string, currentRevision: number) {
    const entry = this.cache.get(scopeId);
    if (!entry) return undefined;
    if (entry.revision !== currentRevision) return undefined; // invalidated by mutation
    return entry.value;
  }
}
```
Apply the same ideas to plugin inspection, tool/result caches, cloud-scope projections, and lookup caches: define what makes the cached value “true,” encode it in the key/revision, invalidate on mutation, and keep eviction/retry bounded and safe.