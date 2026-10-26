---
title: Deterministic Cache Invalidation
description: 'When caching, make staleness impossible by design: key by the *real
  inputs identity*, gate reads with a *revision/generation match*, and use *bounded
  TTL/backoff* (including negative caching).'
repository: cline/cline#v4
label: Caching
language: TypeScript
comments_count: 7
repository_stars: 70864
---

When caching, make staleness impossible by design: key by the *real inputs identity*, gate reads with a *revision/generation match*, and use *bounded TTL/backoff* (including negative caching).

**Standards**
1. **Include input identity in the cache key**
   - Cache entries must be uniquely determined by the inputs that affect the result (e.g., pinned reads use `tool + arguments` with stable key-order normalization).
   - Plugin inspection caches must include execution mode and registry state (not just path).
   - Lookup caches must include all dependency keys (account scope + workspace root + repository/branch).

2. **Gate cache reads with a revision/generation**
   - If context can change (scope/account, config reload, pin edits), store a revision/generation alongside cached data and only serve while the revision matches.
   - Cloud-style pattern: increment a `scopeGeneration` on scope transitions and ignore/refresh results when generations differ.

3. **Use short, explicit TTL for “list/projection” caches**
   - Cache derived collections only briefly and invalidate eagerly on boundaries (scope transition, visibility changes, authority changes).

4. **Time-bound negative caching (failures) with backoff**
   - Failures should not permanently suppress functionality.
   - If a fix could be “invisible” to change detection (e.g., fingerprint unchanged), retry failed loads/imports after a cooldown; otherwise keep the last failure short-lived.

5. **Avoid repeated cache mutation**
   - If results are stored and shortened once at completion, later requests/resumes must read—not rewrite/re-truncate.

**Reusable pattern (sketch)**
```ts
type Entry<T> = { value: T; expiresAt: number; contextRev: number; failedAt?: number };

class Cache<T> {
  private store = new Map<string, Entry<T>>();
  constructor(private now: () => number, private ttlMs: number, private ctxRev: () => number) {}

  get(key: string): T | undefined {
    const e = this.store.get(key);
    if (!e) return;
    if (e.contextRev !== this.ctxRev()) return; // revision/generation gate
    if (e.expiresAt <= this.now()) return;
    return e.value;
  }

  set(key: string, value: T) {
    this.store.set(key, { value, expiresAt: this.now() + this.ttlMs, contextRev: this.ctxRev() });
  }

  // Negative caching with bounded retry
  shouldRetryFailure(key: string, retryAfterMs: number): boolean {
    const e = this.store.get(key);
    return !e?.failedAt || this.now() - e.failedAt >= retryAfterMs;
  }
}
```
Apply these rules so stale data can’t “win”: the cache key captures identity, the revision/generation captures context, and TTL/backoff captures recovery behavior.