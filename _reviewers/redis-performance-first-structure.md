---
title: Performance-first Structure
description: 'When optimizing, treat performance as a design constraint: prevent contention/cache
  inefficiency, ensure server-side work is bounded per call, and keep tests from becoming
  slow bottlenecks.'
repository: redis/redis
label: Performance Optimization
language: Other
comments_count: 5
repository_stars: 74261
---

When optimizing, treat performance as a design constraint: prevent contention/cache inefficiency, ensure server-side work is bounded per call, and keep tests from becoming slow bottlenecks.

1) Cache-line & contention hygiene (C structs)
- Align/pad frequently-updated counters to avoid false sharing.
- Avoid mixing rarely-used “cold” fields into the same cache footprint as hot ones; move them deeper in the struct.
- Prefer per-thread stats to share less with other threads; if needed, split “hot counters” into their own cache-line-aligned struct.

Example pattern:
```c
typedef struct __attribute__((aligned(CACHE_LINE_SIZE))) {
    redisAtomic long long io_reads_processed;
    redisAtomic long long io_writes_processed;
    /* other hot, per-IO-thread counters */
} IOThreadStats;

typedef struct {
    /* hot per-IO-thread fields */
    IOThreadStats stats; /* each thread updates its own cache line */
    /* cold / infrequently read fields after */
    int unused_cold_field;
} IOThread;
```

2) Bound work for collection-style commands
- For commands that iterate over IDs supplied by the client, ensure per-ID processing is O(1) with a small constant, and rely on the existing batching convention (client chooses how many IDs to send).
- Only introduce server-side COUNT/batching knobs if they meaningfully prevent a real bottleneck or reduce complexity (not just to mimic client-side batching).

3) Keep tests fast and deterministic
- Avoid long fixed sleeps for timing/cron behavior.
- Use polling/`wait_for_condition`-style loops and reduce durations/timeouts so CI runtime stays low.
