---
title: Cache Correctness Rules
description: 'Caches must be designed so they are correct for the full input space,
  bounded in time, and recover from “invisible” fixes/failures.


  Apply these rules:'
repository: cline/cline#v5
label: Caching
language: TypeScript
comments_count: 6
repository_stars: 70864
---

Caches must be designed so they are correct for the full input space, bounded in time, and recover from “invisible” fixes/failures.

Apply these rules:
1) **Key caches on the true inputs**
   - If results depend on scope/mode/state, include them in the cache key.
   - If results depend on object identity, cache-by-reference is valid—but then tests must ensure that mutating payloads doesn’t incorrectly change the cached output.

2) **Invalidate on explicit state/scope boundaries**
   - When account/workspace/task scope changes, reset caches and pinned resources before re-reading.
   - Ensure state projection layers (history/status/usage) re-enumerate only after invalidation.

3) **Use TTL/age-out to prevent staleness**
   - For distributed or control-plane-driven data, expire cached reads and reload behind the scenes to avoid UI flicker.

4) **Avoid cache-driven infinite loops**
   - When “warm-up” attempts may only populate a fallback, don’t keep the handle pinned or keep posting identical state.
   - Only treat the warm-up as successful if it actually populated the intended cache.

5) **Add bounded retry/backoff for failures where change detection may not change keys**
   - If a failure can be fixed without changing fingerprints/keys (e.g., dependency installed in node_modules or dynamic/computed imports), retry on a timer (e.g., every 30s) up to the point where a successful re-import/refresh provides new evidence.

Minimal pattern (age-out + reload-without-flicker):
```ts
const TTL_MS = 60_000;

class Lookup<T> {
  private value?: T;
  private pending?: Promise<void>;
  private failedAt?: number;

  constructor(private readonly load: () => Promise<T>, private readonly now: () => number) {}

  async get(refresh = false): Promise<T | undefined> {
    if (!refresh && this.value !== undefined && (this.failedAt === undefined || this.now() - this.failedAt > TTL_MS)) {
      return this.value;
    }
    if (this.pending) return undefined;

    this.pending = this.load()
      .then((v) => { this.value = v; this.failedAt = undefined; })
      .catch(() => { this.failedAt = this.now(); })
      .finally(() => { this.pending = undefined; });

    await this.pending;
    return this.value;
  }
}
```

Adhering to these rules prevents stale/cross-scope data leaks, eliminates “stuck fallback” behavior, and ensures caches remain both performant and reliably correct.