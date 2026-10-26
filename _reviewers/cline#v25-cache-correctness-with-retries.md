---
title: Cache Correctness With Retries
description: 'When caching anything that depends on external state (pins, remote sessions,
  plugins, lookups), prioritize correctness over hit-rate: ensure the cache key fully
  represents the inputs/version required to serve the right answer, invalidate on
  observable changes, and add bounded retry for cases where fixes aren’t detectable
  by the invalidation signal.'
repository: cline/cline#v25
label: Caching
language: TypeScript
comments_count: 8
repository_stars: 70891
---

When caching anything that depends on external state (pins, remote sessions, plugins, lookups), prioritize correctness over hit-rate: ensure the cache key fully represents the inputs/version required to serve the right answer, invalidate on observable changes, and add bounded retry for cases where fixes aren’t detectable by the invalidation signal.

Apply these rules:
1) **Key by full identity + revision**
- Include tool+arguments, pin id, record id, and any *revision/generation* that changes on edits or scope transitions.
- If argument order must not matter, normalize it when forming the key.

2) **Gate reads by “still matches” checks**
- Serve cached results only while the thing they were derived from is still the same (e.g., the pin still matches the cached definition; the entry still belongs to the current generation).
- Never let late async responses populate a cache that is already obsolete.

3) **Use TTL/age-based refresh for “eventually consistent” inputs**
- For distributed/auth/availability changes, refresh based on an age limit but avoid flicker by keeping the current cached value until the background refresh replaces it.

4) **Add bounded backoff retries for invisible fixes**
- If invalidation can’t see the change (e.g., a failed plugin import becomes fixed without fingerprint-changing inputs), retry the operation on a timer/backoff.
- Keep the retry bounded (e.g., at most once per N seconds) and preserve degraded behavior until recovery.

5) **Test cache semantics explicitly**
- Add tests for: (a) stale data not served after edits, (b) TTL refresh without flicker, (c) order-insensitive argument caching where required, and (d) retry behavior when invalidation signals don’t change.

Example pattern (deterministic key + “still matches” gate + bounded retry):
```ts
type CacheEntry<T> = { value: T; fetchedAt: number; revision: number };

function makeKey(tool: string, args: Record<string, unknown>) {
  // normalize argument order if needed
  const stableArgs = JSON.stringify(Object.entries(args).sort());
  return `${tool}:${stableArgs}`;
}

class PinnedLikeCache<T> {
  private cache = new Map<string, CacheEntry<T>>();
  private failedAt = new Map<string, number>();
  private revisionCounter = 0;

  // revision increments when the definition changes
  bumpRevision() { this.revisionCounter++; }

  async getOrLoad(key: string, load: () => Promise<T>, pinRevision: number, retryMs: number) {
    const entry = this.cache.get(key);
    if (entry && entry.revision === pinRevision) return entry.value;

    const now = Date.now();
    const lastFail = this.failedAt.get(key);
    if (lastFail !== undefined && now - lastFail < retryMs) {
      return undefined; // degrade gracefully
    }

    try {
      const value = await load();
      this.cache.set(key, { value, fetchedAt: now, revision: pinRevision });
      this.failedAt.delete(key);
      return value;
    } catch {
      this.failedAt.set(key, now);
      return undefined;
    }
  }
}
```
This approach prevents stale/cross-scope/cross-definition serving, keeps UX stable with TTL-backed refresh, and ensures recovery when fixes are not directly observable by the cache invalidation signal.