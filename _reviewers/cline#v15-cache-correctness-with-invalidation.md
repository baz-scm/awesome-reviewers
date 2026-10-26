---
title: Cache Correctness with Invalidation
description: 'When caching data that depends on external state (pins, session identity,
  filesystem content, account/workspace scope, plugin registry status, tool inputs),
  make cache correctness the primary rule:'
repository: cline/cline#v15
label: Caching
language: TypeScript
comments_count: 9
repository_stars: 70877
---

When caching data that depends on external state (pins, session identity, filesystem content, account/workspace scope, plugin registry status, tool inputs), make cache correctness the primary rule:

- **Key caches by all inputs** that influence output. If you can observe a **revision/version** (e.g., pin revision, plugin registry state, session/tool surface generation), include it in the key.
- **Suppress stale async updates**: if a promise resolves after the key/revision changed, the result must not overwrite the cache.
- **Use TTL + background refresh carefully**:
  - Keep serving the last good value until the refreshed value is ready (**no flicker**).
  - Deduplicate concurrent loads (one in-flight per key).
- **Handle failures safely**:
  - On load failure, prefer keeping the previous value (if it’s safe) and **retry with bounded backoff**.
  - If change detection may be incomplete (e.g., fixes invisible to fingerprints), add **time-based retries** even when the fingerprint/key is unchanged.
- **Detect “invisible” changes** with stronger invalidation where possible (fingerprints that include relevant import patterns, or explicit revision signals).

Example pattern (TypeScript):
```ts
type CacheEntry<T> = { value?: T; fetchedAt?: number; pending?: Promise<void>; failedAt?: number };

function makeKey(params: { pinTool: string; args: Record<string, unknown>; revision: string }) {
  // Include revision and normalize args deterministically (e.g., stable key order)
  const argsKey = JSON.stringify(params.args, Object.keys(params.args).sort());
  return `${params.pinTool}|${argsKey}|${params.revision}`;
}

class KeyedCache<T> {
  private entry = new Map<string, CacheEntry<T>>();
  constructor(private readonly fetcher: (key: string) => Promise<T>, private readonly now = () => Date.now(),
              private readonly ttlMs = 10_000, private readonly retryMs = 30_000) {}

  async get(key: string): Promise<T | undefined> {
    const e = this.entry.get(key) ?? {};
    this.entry.set(key, e);

    const fresh = e.value !== undefined && e.fetchedAt !== undefined && this.now() - e.fetchedAt < this.ttlMs;
    if (fresh) return e.value;

    const cooldown = e.failedAt !== undefined && this.now() - e.failedAt < this.retryMs;
    if (e.value !== undefined && cooldown) return e.value;

    if (!e.pending) {
      const pendingKey = key;
      e.pending = this.fetcher(key).then(
        (value) => {
          // stale-result suppression
          if (pendingKey !== key) return;
          e.value = value;
          e.fetchedAt = this.now();
          e.failedAt = undefined;
        },
        () => {
          e.failedAt = this.now();
        },
      ).finally(() => { e.pending = undefined; });
    }

    await e.pending;
    return e.value;
  }
}
```
Adopt this checklist in any caching layer that can be invalidated by user edits, remote updates, scope changes, plugin enable/disable/reload, filesystem changes, or session reconnects.