---
title: Consistent TTL Pre-check
description: When handling TTL/expiration, decide “already expired?” (and validate
  expiry inputs) before performing DB mutations or expensive work, and then keep DB
  changes, stats/counters, and keyspace notifications consistent with the real outcome.
  For conditional variants (NX/XX, ENX/FNX/FXX), short-circuit behavior must match
  the condition.
repository: redis/redis
label: Caching
language: C
comments_count: 5
repository_stars: 74261
---

When handling TTL/expiration, decide “already expired?” (and validate expiry inputs) before performing DB mutations or expensive work, and then keep DB changes, stats/counters, and keyspace notifications consistent with the real outcome. For conditional variants (NX/XX, ENX/FNX/FXX), short-circuit behavior must match the condition.

Practical checklist:
- Parse/validate expiration arguments early.
- If TTL is already expired:
  - Do not insert/overwrite new data (unless semantics require it); delete only if an old key existed/was actually overwritten.
  - Update expired-key counters and keyspace notifications consistently with the effective DB outcome.
  - Honor conditional flags (e.g., only perform the “expired short-circuit” path when the operation would otherwise proceed per NX/XX rules).
- If you use TTL-aware fast paths/optimizations (prefetch/batching/cached pointers), ensure cache/resource lifetimes are safe across mutations that can delete/free entries; refresh per batch when necessary.
- Add tests for expire-then-insert across batch boundaries and for conditional short-circuiting.

Pattern:
```c
// Pseudocode pattern
if (expire && checkAlreadyExpired(milliseconds)) {
    if (found_existing_key) {
        // delete with correct delete semantics (e.g., overwrite deletion vs expired deletion)
        dbDeleteOrExpireSemantics(db, key);
        emit_del_ksn_and_update_stats();
    } else {
        // for “missing key” cases: short-circuit without creating state
        // but still update counters if spec requires it
        emit_required_counters_only();
    }
    return;
}
// otherwise: proceed with normal insert/update and set TTL
apply_set_or_increment_and_set_expire();
```