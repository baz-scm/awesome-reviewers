---
title: Cache correctness & retries
description: 'Adopt a single standard for all caches (data, discovery, warm-ups, and
  load-result caches):


  1) Key by the real identity (include all dependencies)

  - Build cache keys from the complete set of inputs that affect the result (e.g.,
  tool name + arguments; account scope + workspace root; plugin path + execution mode
  + registry status).'
repository: CLINE/CLINE
label: Caching
language: TypeScript
comments_count: 9
repository_stars: 70837
---

Adopt a single standard for all caches (data, discovery, warm-ups, and load-result caches):

1) Key by the real identity (include all dependencies)
- Build cache keys from the complete set of inputs that affect the result (e.g., tool name + arguments; account scope + workspace root; plugin path + execution mode + registry status).
- If argument order shouldn’t matter, normalize it before keying.

2) Invalidate using an explicit version/revision boundary
- When upstream definitions change, stamp entries with a revision/version and only serve while the revision still matches.
- For async work, guard updates with “generation”/“revision” checks so late responses can’t overwrite newer state.

3) Define TTL/idle eviction + failure backoff
- Add TTL/idle limits to avoid indefinite stale data.
- For load/lookup failures, cache the failure state with a timestamp and retry only after a bounded backoff.
- If a warm-up completes but doesn’t actually populate the intended cache (e.g., still at fallback), release the handle and retry later.

4) Prevent cache poisoning
- Don’t let one failing lookup disable or poison unrelated shared caches; isolate failure impact to the specific key/scope (or roll back only the failed part).

5) Validate cache scope at read time
- Ensure reads are only possible for the correct scope (session/account/etc.), and fail fast if the URI/key doesn’t belong.

Minimal pattern (identity-keyed lookup with backoff and async safety):

```ts
class KeyedLookup<T> {
  private key?: string
  private value?: T
  private pending?: Promise<void>
  private failedAt?: number
  private generation = 0

  constructor(
    private readonly now: () => number,
    private readonly retryMs: number,
    private readonly load: (key: string) => Promise<T>,
    private readonly onSettled: () => void,
  ) {}

  async get(key: string, refresh = false): Promise<T | undefined> {
    if (this.key !== key || refresh) {
      this.generation++
      this.key = key
      this.value = undefined
      this.pending = undefined
      this.failedAt = undefined
    }

    if (this.value !== undefined) return this.value
    if (this.pending) return undefined
    if (this.failedAt !== undefined && this.now() - this.failedAt < this.retryMs) return undefined

    const gen = this.generation
    this.pending = this.load(key)
      .then((v) => {
        if (gen !== this.generation) return
        this.value = v
        this.failedAt = undefined
        this.onSettled()
      })
      .catch(() => {
        if (gen !== this.generation) return
        this.failedAt = this.now()
      })
      .finally(() => {
        if (gen === this.generation) this.pending = undefined
      })

    return undefined
  }
}
```

If you apply this checklist consistently, you’ll avoid stale/late async results, ensure caches refresh when inputs change, keep failures from freezing features, and stop one failing lookup from corrupting shared state.