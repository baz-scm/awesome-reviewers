---
title: Identity-Guarded Cache
description: 'When caching, correctness comes before speed:


  1) Key by *all inputs that affect the cached value* (tool + arguments; plugin set
  state; dependency scope; etc.). If any dependency can change, it must be reflected
  in the cache key.'
repository: cline/cline#v17
label: Caching
language: TypeScript
comments_count: 7
repository_stars: 70883
---

When caching, correctness comes before speed:

1) Key by *all inputs that affect the cached value* (tool + arguments; plugin set state; dependency scope; etc.). If any dependency can change, it must be reflected in the cache key.
2) Serve only if the cached value’s *identity still matches* the current request/session. Add a revision/version (or compute an identity hash) and validate it right before returning/publishing.
3) Separate “warm/cache fetch” from “publish”: only publish UI/state updates when the cache was actually populated with the expected (non-fallback) result.
4) For failures, cache the failure with a bounded retry window; don’t re-run expensive work on every request forever, but also don’t permanently poison the cache.
5) Bind or alias cache entries when the same logical session can have multiple runtime/UI identifiers; otherwise cached drafts/results can become stranded or stale.

Example pattern (TypeScript):

```ts
type CacheEntry<T> = {
  identity: string; // e.g., tool+args hash, plugin-set+mode fingerprint, etc.
  revision: number;
  value: T;
  filledAt: number;
};

class IdentityCache<T> {
  private entry?: CacheEntry<T>;
  private revision = 0;

  get(identity: string, loader: () => Promise<T>, now = Date.now()): Promise<T> {
    // Serve only when identity matches
    if (this.entry?.identity === identity) return Promise.resolve(this.entry.value);
    const rev = ++this.revision;
    return loader().then((value) => {
      // Publish only if we’re still the latest identity
      if (rev !== this.revision) throw new Error('stale');
      this.entry = { identity, revision: rev, value, filledAt: now() };
      return value;
    });
  }
}
```

Use this checklist during reviews: if a cached value can be served after pins/plugins/session identifiers change, or after reconnection/refresh changes the underlying snapshot, require identity-guarding, correct keying, and explicit publish/invalidation rules.