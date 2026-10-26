---
title: Revisioned Cache Invalidation
description: 'When caching derived/remote results, make staleness impossible to ignore:
  include every dependency’s identity (and revision/state) in the cache key, gate
  serving by that same revision, add TTL aging for distributed state, and use bounded
  retries when changes can’t be reliably detected.'
repository: cline/cline#v20
label: Caching
language: TypeScript
comments_count: 12
repository_stars: 70886
---

When caching derived/remote results, make staleness impossible to ignore: include every dependency’s identity (and revision/state) in the cache key, gate serving by that same revision, add TTL aging for distributed state, and use bounded retries when changes can’t be reliably detected.

Apply this checklist:
- **Key the cache on inputs that affect output** (not just “what you queried”). Example: pin results cached by **tool + arguments**, not only tool name; plugin inspection cache key includes **plugin state/updatedAt + execution mode**.
- **Invalidate or refuse to serve when the dependency definition changed**. Store a **revision** alongside the cached entry and require it to match (pinned scopes / UI set revision / authoritative frontmatter).
- **Use TTL/aging for distributed or permissioned data** (e.g., refresh repo lists after a short TTL to pick up access changes without flicker).
- **Bound retries when detection is imperfect** (e.g., retry failed plugin imports on a backoff even if fingerprints don’t change).
- **Validate ownership/format before serving cached artifacts** (e.g., tool-result cache URIs must match the current session).
- **Isolate failures** so one failing lookup doesn’t poison unrelated shared caches.

Minimal pattern (revision-gated cache):
```ts
type Entry<T> = { value: T; revision: string; fetchedAt: number };

class RevisionedCache<T> {
  private map = new Map<string, Entry<T>>();
  constructor(private readonly ttlMs: number) {}

  get(key: string, requiredRevision: string): T | undefined {
    const e = this.map.get(key);
    if (!e) return;
    if (e.revision !== requiredRevision) return; // definition changed
    if (Date.now() - e.fetchedAt > this.ttlMs) return; // distributed aging
    return e.value;
  }

  set(key: string, revision: string, value: T) {
    this.map.set(key, { value, revision, fetchedAt: Date.now() });
  }
}
```
Use this rule of thumb for cache keys: **if you wouldn’t be comfortable serving the wrong answer after a definition edit, that definition edit must change the cache key or the revision gate.**