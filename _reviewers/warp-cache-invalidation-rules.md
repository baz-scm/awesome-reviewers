---
title: Cache invalidation rules
description: 'Any cached value must have an explicit, testable “when does it become
  stale?” policy, plus a fallback path when updates may be missed.


  Apply this as a checklist:'
repository: warpdotdev/warp
label: Caching
language: Markdown
comments_count: 3
repository_stars: 56893
---

Any cached value must have an explicit, testable “when does it become stale?” policy, plus a fallback path when updates may be missed.

Apply this as a checklist:
1) **State the cache scope & dependencies**: What inputs does this cached data depend on? (e.g., harness selection + auth secrets, repo path + embedding config, shared snapshot version, identity key/authorization)
2) **Enumerate invalidation triggers** (at minimum):
   - **Schema/data integrity**: version mismatch, corrupt/missing snapshot files → invalidate and rebuild/refetch.
   - **Upstream configuration changes**: backend config / embedding config changes → mark stale and rerun necessary work.
   - **Source-of-truth changes**: filesystem watcher events, repo path disappearing/not a repo → mark stale and fail over appropriately.
   - **Authorization/root-hash validity**: if the backend rejects or can’t authorize a previously “ready” root hash for a specific identity/user → mark failed and require re-association/rebuild.
   - **Identity changes**: clear identity-scoped client caches; shared machine caches can remain if they contain no user-specific/credential data.
3) **Refresh strategy**: don’t rely solely on “refetch on login”. Use either:
   - **TTL/periodic revalidation**, aligned with existing refresh cadence, or
   - **event-driven invalidation** when you have reliable signals.
4) **Pull-based fallback when pushes may be missed**: when navigating to a new repo/state or reconnecting, issue a **status/read query** if your model might be incomplete or outdated.

Example pattern (Rust-style pseudocode):
```rust
enum CacheState<T> { Fresh(T), Stale { reason: String } }

fn should_invalidate(reason_from_inputs: Option<&str>, integrity_ok: bool) -> bool {
    !integrity_ok || reason_from_inputs.is_some()
}

async fn get_with_invalidation(cache_key: Key) -> Result<Value> {
    let entry = load_cache(cache_key)?;
    if should_invalidate(entry.integrity_ok == false, entry.dep_version_changed) {
        invalidate(cache_key);
        return fetch_from_source(cache_key).await;
    }

    // If push might have been missed or we’re not confident it’s current:
    if entry.age > TTL || entry.last_update_suspicious {
        return fetch_and_replace(cache_key).await;
    }

    Ok(entry.value)
}
```

Result: fewer “mysteriously stale” UIs, safer authorization handling, and consistent behavior across both local and remote/daemon-backed caches.