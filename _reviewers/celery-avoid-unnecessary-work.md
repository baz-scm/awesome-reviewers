---
title: Avoid Unnecessary Work
description: 'Prefer eliminating work that can’t affect observable behavior and prevent
  resource retention in hot paths.


  Apply this as a checklist:

  1) Guard mode-dependent logic: if the subsystem doesn’t propagate updates (or the
  surrounding condition is false), skip the computation/action entirely.'
repository: celery/celery
label: Performance Optimization
language: Python
comments_count: 10
repository_stars: 28464
---

Prefer eliminating work that can’t affect observable behavior and prevent resource retention in hot paths.

Apply this as a checklist:
1) Guard mode-dependent logic: if the subsystem doesn’t propagate updates (or the surrounding condition is false), skip the computation/action entirely.
   - Example pattern (prefetch/QoS):
     ```python
     if worker_enable_prefetch_count_reduction:
         # If per-consumer QoS (apply_global=False), broker qos updates won’t reach running consumers.
         if qos_global is False:
             logger.info("Skipping prefetch reduction; per-consumer QoS in effect")
         else:
             active_count = len(active_requests)  # snapshot once
             initial_prefetch_count = max(
                 prefetch_multiplier,
                 max_prefetch_count - active_count * prefetch_multiplier,
             )
     ```
2) Run expensive checks/copies only when needed: move `detect_*` calls and `copy.copy(...)` inside the “schedule changed” condition.
3) Avoid redundant computation drift: snapshot once and reuse (e.g., `active_count = len(active_requests)`) rather than recomputing in multiple expressions/logs.
4) Use the right data structures for de-duplication: prefer sets for membership/de-dup and convert at the end, avoiding repeated O(n) `in list` checks.
5) Prevent memory retention in exception/error handling: clear traceback frame references (e.g., `traceback_clear(exc)`) and delete local traceback variables (`del tb`) when they are no longer needed.
6) Avoid “harmless” side-effect calls that allocate resources: in pub/sub flows, don’t ping when there are no subscribers or when ping triggers empty replies/extra allocations.

These changes improve throughput and memory usage without altering functional behavior.