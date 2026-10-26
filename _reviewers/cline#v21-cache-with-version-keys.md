---
title: Cache With Version Keys
description: 'When caching, treat correctness as part of the key: every cache entry
  must include (or be guarded by) the version/revision/generation of the underlying
  data, and you must invalidate/refresh when that identity changes. Use TTL/backoff
  only for performance—never as a substitute for identity-based invalidation.'
repository: cline/cline#v21
label: Caching
language: TypeScript
comments_count: 6
repository_stars: 70886
---

When caching, treat correctness as part of the key: every cache entry must include (or be guarded by) the version/revision/generation of the underlying data, and you must invalidate/refresh when that identity changes. Use TTL/backoff only for performance—never as a substitute for identity-based invalidation.

Apply this standard:
1) Key by *complete dependency identity*
- Include all parameters that affect the result (e.g., tool + arguments; ignore argument key order by canonicalization).
- Include scope identifiers (account/workspace) so caches can’t mix across transitions.
- Include producer state when it changes behavior (e.g., plugin registry `state` and `updatedAt`).

2) Guard against stale producers
- When an operation can finish late (previous pin definition, previous scope, superseded fetch), serve results only if the current revision/generation still matches.

3) Invalidate on observed state changes
- If you can detect that inputs changed (revision increments, scopeGeneration increments, status transitions), proactively call cache invalidation and re-projection rather than waiting for TTL.

4) Use TTL/backoff + retries only for transient/undetectable changes
- If a failure might be fixed without changing your primary cache key (e.g., “invisible” change), retry with bounded backoff even when the fingerprint/key didn’t change.

5) Never repeatedly re-derive/persist-alter on cache hits
- If you persist derived/truncated artifacts, write/shorten once per completion and keep later reads from re-truncating.

Example pattern (identity-keyed cache + guarded refresh):
```ts
type Entry<T> = { value: T; loadedAt: number; revision: number };
const cache = new Map<string, Entry<string>>();

async function getWithVersion<T>({
  key,
  revision,
  ttlMs,
  load,
}: {
  key: string;
  revision: number;
  ttlMs: number;
  load: () => Promise<T>;
}): Promise<T> {
  const existing = cache.get(key);
  if (existing && existing.revision === revision && Date.now() - existing.loadedAt < ttlMs) {
    return existing.value;
  }

  const value = await load();
  cache.set(key, { value: String(value) as unknown as T, loadedAt: Date.now(), revision });
  return value;
}
```

Checklist for code review:
- Does the cache key (or entry guard) change whenever the effective inputs change?
- Are late/stale async results prevented from overwriting current state?
- Is there an explicit invalidation path when detected changes occur?
- Are retries bounded (rate-limited/backoff) for undetectable fixes?
- Are derived persisted artifacts written once per completion (not re-truncated on every request/resume)?