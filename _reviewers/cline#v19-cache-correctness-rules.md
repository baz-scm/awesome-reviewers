---
title: Cache Correctness Rules
description: 'When caching, optimize *only inside a correctness boundary*: the cache
  must be keyed to the exact inputs/identity that determine the value, must be invalidated
  (or refused) when the identity changes, and must use bounded TTL/backoff to recover
  from transient or “invisible” change failures.'
repository: cline/cline#v19
label: Caching
language: TypeScript
comments_count: 8
repository_stars: 70885
---

When caching, optimize *only inside a correctness boundary*: the cache must be keyed to the exact inputs/identity that determine the value, must be invalidated (or refused) when the identity changes, and must use bounded TTL/backoff to recover from transient or “invisible” change failures.

Apply these rules:
1) Cache key = canonical dependency identity
- Include all inputs that change the result (e.g., tool name + arguments; plugin path + registry state; account scope + mode; repo+branch choice). Canonicalize ordering (e.g., ignore JSON key order).

2) Refuse stale results by re-checking current identity
- Before serving cached content, verify it still matches the latest “current” pin/selection/entry. Also use a per-scope revision/sequence so you can reject or withhold late arrivals.

3) Define authoritative source of truth
- If multiple sources exist (extension toggle state vs on-disk frontmatter), model an “authoritative” phase: backfill once, then treat the authoritative source (file) as the deciding input; prune stale records.

4) Use TTL/aging for read models; reload behind when possible
- For UI/derived reads (repos, status projections), age cached values and re-fetch in the background so the UI doesn’t flicker, but subsequent state posts converge.

5) Failures need bounded retries, not permanent cache poisoning
- For cache/fingerprint cases where the change is not detectable, remember the failure and retry after a fixed backoff (and cap frequency). Don’t block unrelated features (e.g., slash commands) during failures.

Minimal pattern (identity-gated cache):
```ts
type CacheEntry<T> = { revision: number; value: T };

class IdentityCache<T> {
  private entry?: CacheEntry<T>;
  private revision = 0;

  setRevision(nextRevision: number) {
    this.revision = nextRevision;
    // optional: invalidate proactively
  }

  async getOrLoad(key: string, currentRevision: number, load: () => Promise<T>): Promise<T> {
    // key-based identity (canonicalize key)
    // revision gate (refuse stale)
    if (this.entry && this.entry.revision === currentRevision) return this.entry.value;
    const value = await load();
    this.entry = { revision: currentRevision, value };
    return value;
  }
}
```

This standard prevents the common caching bugs shown in the discussions: serving results after pins/choices changed, acting on stale projections after scope/account transitions, caching plugin discovery incorrectly after registry/mode changes, and getting stuck on failure without bounded recovery.