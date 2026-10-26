---
title: Cache Key Correctness
description: 'Use caching only when you can guarantee result correctness under change,
  and always prevent serving stale async results.


  **Coding standard**

  1. **Key by full inputs (no hidden dependencies):**'
repository: cline/cline#v12
label: Caching
language: TypeScript
comments_count: 7
repository_stars: 70872
---

Use caching only when you can guarantee result correctness under change, and always prevent serving stale async results.

**Coding standard**
1. **Key by full inputs (no hidden dependencies):**
   - Include every value that affects the computed output: identifiers + all user/config choices + resolved args/branch + execution mode.
   - For structured inputs, normalize key order (e.g., serialize maps with stable ordering) so logically identical args hit the same entry.
2. **Include revisions/fingerprints for upstream changes:**
   - When data can change without a simple identifier change, add a revision counter or compute a content fingerprint (e.g., based on the entry file and all transitively statically imported sources; include side-effect imports).
3. **Guard against stale in-flight work:**
   - Track a **generation/identity** and only apply results if the request is still current.
   - Prefer patterns like: “serve only while pin still matches” and “revalidate remembered status against the latest record”.
4. **Use TTL/age-out for freshness without flicker:**
   - If you must refresh, do it behind the scenes and keep returning the cached value until the new load is ready (avoid UI jitter).
5. **Cache failures with bounded retry:**
   - Remember load failures under the same cache key plus a timestamp; retry after a fixed/backoff delay to avoid repeated expensive attempts.
   - Ensure warm-up retries are bounded and do not stack when already pending.
6. **Invalidate/prune dependent caches:**
   - When upstream state changes (scope/account, pin set, plugin state, repository checkout), invalidate affected caches.
   - Prune entries that are no longer reachable/valid (e.g., session IDs no longer present).

**Example (identity-guarded lookup with TTL + failure backoff)**
```ts
class Lookup<T> {
  private key?: string;
  private value?: T;
  private pending?: Promise<void>;
  private failedAt?: number;

  constructor(
    private readonly now: () => number,
    private readonly TTL_MS: number,
    private readonly retryMs: number,
    private readonly load: (key: string) => Promise<T>,
  ) {}

  async get(key: string, refresh = false): Promise<T | undefined> {
    if (this.key !== key || refresh) {
      this.key = key;
      this.value = undefined;
      this.pending = undefined;
      this.failedAt = undefined;
    }

    // Serve cached value until it ages out.
    if (this.value !== undefined && this.now() - (this.failedAt ?? 0) <= this.TTL_MS) {
      return this.value;
    }

    // If a failure is recent, don’t hammer.
    if (this.failedAt !== undefined && this.now() - this.failedAt < this.retryMs) {
      return this.value;
    }

    if (!this.pending) {
      const pending = this.load(key).then(
        (v) => {
          // Identity guard: only commit if still on the same key.
          if (this.key === key) this.value = v;
          this.failedAt = undefined;
        },
        () => {
          if (this.key === key) this.failedAt = this.now();
        },
      );
      this.pending = pending.finally(() => {
        if (this.pending === pending) this.pending = undefined;
      }) as Promise<void>;
    }

    await this.pending;
    return this.value;
  }
}
```

Apply this standard whenever you add/modify a cache: explicitly list the cache key inputs, add a revision/fingerprint when upstream changes aren’t captured by identifiers, include TTL/backoff for freshness and resilience, and guard commits of async results with identity/generation checks.