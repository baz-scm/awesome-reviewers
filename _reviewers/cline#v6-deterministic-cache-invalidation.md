---
title: Deterministic Cache Invalidation
description: 'When caching derived/distributed state, make cache correctness explicit:
  include all dependencies in the cache key, invalidate on authoritative changes (flags,
  scope/account transitions, definition/version changes), and prevent stale async
  work from overwriting newer live state. If you can’t detect a change via the key,
  add bounded retry/backoff and only...'
repository: cline/cline#v6
label: Caching
language: TypeScript
comments_count: 9
repository_stars: 70864
---

When caching derived/distributed state, make cache correctness explicit: include all dependencies in the cache key, invalidate on authoritative changes (flags, scope/account transitions, definition/version changes), and prevent stale async work from overwriting newer live state. If you can’t detect a change via the key, add bounded retry/backoff and only update published state once consistency is verified.

Practical rules:
1) Key by the full dependency tuple
- Example: pinned reads should cache by (tool identity + arguments), not just tool name.
- Example: plugin inspection cache keys must include enough state (plugin path + registry status/state + mode) to avoid stale enable/disable outcomes.

2) Invalidate at the boundaries that change meaning
- Feature toggles that affect what gets listed must invalidate dependent caches before posting state.
- Account/scope transitions must invalidate/clear entries and detach hosts so different account data can’t mix.

3) Snapshot baselines when producing cached data
- If you later compare “before vs after” for changes, take the baseline at the moment you build the surface/value used by the operation.

4) Guard against async races with identity/generation checks
- Use a generation/identity token captured when starting an async refresh; only publish results if the token still matches.
- This also applies to teardown/reconnect flows: stale background work must not mutate the current live view.

5) Use bounded retry/backoff when invalidation signals are incomplete
- If the cache key can’t observe some changes (e.g., dynamic imports, computed paths), schedule a retry at most every N ms and cap the number of repeated attempts.

Example pattern (keyed cached lookup with stale-drop + bounded retry):
```ts
const LOOKUP_RETRY_MS = 30_000;

class KeyedLookup<T> {
  private key?: string;
  private value?: T;
  private pending?: Promise<T>;
  private failedAt?: number;
  private generation = 0;

  constructor(
    private readonly now: () => number,
    private readonly onLoaded: () => void,
  ) {}

  async get(key: string, load: () => Promise<T>, refresh = false): Promise<T | undefined> {
    if (refresh || this.key !== key) {
      this.generation++;
      this.key = key;
      this.value = undefined;
      this.failedAt = undefined;
      this.pending = undefined;
    }
    if (this.value !== undefined) return this.value;

    if (this.pending) return this.pending;

    if (this.failedAt !== undefined && this.now() - this.failedAt < LOOKUP_RETRY_MS) return undefined;

    const myGen = this.generation;
    this.pending = load()
      .then(v => {
        if (this.generation !== myGen) return v; // stale; value is ignored by caller
        this.value = v;
        this.failedAt = undefined;
        this.pending = undefined;
        this.onLoaded();
        return v;
      })
      .catch(() => {
        if (this.generation !== myGen) return undefined;
        this.pending = undefined;
        this.failedAt = this.now();
        return undefined;
      });

    return this.pending;
  }
}
```

Apply this standard consistently to caching layers (session/tool results, connector outputs, history lists, plugin discovery, and feature-flagged views): deterministic keys + explicit invalidation + stale-write suppression + bounded retries.