---
title: Concurrency-Safe State Ownership
description: 'In code that runs across multiple concurrent requests/workers (OpenResty/Nginx),
  make state ownership and lifecycle explicit: use one writer/immutable shared snapshots,
  keep request/per-plugin state per-instance or per-request, and design timer/event
  flows to avoid race windows.'
repository: apache/apisix
label: Concurrency
language: Other
comments_count: 11
repository_stars: 16922
---

In code that runs across multiple concurrent requests/workers (OpenResty/Nginx), make state ownership and lifecycle explicit: use one writer/immutable shared snapshots, keep request/per-plugin state per-instance or per-request, and design timer/event flows to avoid race windows.

Apply this standard:
- **No shared mutable module state across configurations/requests**: any counter/buffer must live on the specific instance (per plugin config), not in a module-level closure shared by all `require()` users.
- **No cross-request mutation**: deep-copy config tables or other structures before mutating them inside request paths.
- **Request-bound uniqueness**: when using shared data structures (e.g., Redis ZSET members) under concurrency, include a per-request unique value (e.g., `ngx.var.request_id`) in the member.
- **Safe async/timer semantics**: when updates are asynchronous (timers, reload events), ensure correctness during the transition. Rebuild should “publish new then stop old” atomically, and tests should wait until the system is truly quiescent (not just after sending an event).
- **Avoid lock contention in hot paths**: shdict operations can lock; avoid frequent `shdict:get` in request-critical functions, or add worker-local TTL caching.
- **Avoid shared-variable execution-order races**: don’t use a process-local variable (like `all_services`) as a read/write bridge with workers; make the shared dict the source of truth and keep it immutable per update.

Example patterns:
```lua
-- 1) Per-request uniqueness in Redis ZSET members
local request_id = ngx.var.request_id
redis.call('ZADD', KEYS[1], now, request_id .. ':' .. i)

-- 2) Per-instance counter (conceptually)
local obj = {
  total_pushed_entries = 0,
  -- ... per-config buffers/state
}

-- 3) Avoid cross-request mutation
local checks = core.table.deepcopy(instance.checks)
-- mutate 'checks' safely

-- 4) Hot path: avoid locking shdict.get; use worker-local cache (conceptually)
-- local cached = cache:get(key) with TTL; only fall back to shdict on miss
```

Rule of thumb: if something can be observed/updated by more than one request concurrently, document its owner (which function/process writes), its lifecycle (when it can be reused), and its synchronization strategy (atomic publish, stop flags, immutable snapshots).