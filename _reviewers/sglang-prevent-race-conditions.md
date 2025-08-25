---
title: Prevent race conditions
description: Ensure atomic operations and proper synchronization when multiple threads
  or processes access shared state. Race conditions occur when the timing of operations
  affects correctness, leading to data corruption, memory leaks, or inconsistent behavior.
repository: sgl-project/sglang
label: Concurrency
language: Python
comments_count: 4
repository_stars: 17245
---

Ensure atomic operations and proper synchronization when multiple threads or processes access shared state. Race conditions occur when the timing of operations affects correctness, leading to data corruption, memory leaks, or inconsistent behavior.

Common patterns to watch for:
- **Check-then-act sequences**: When checking a condition and acting on it are separate operations, the state can change between them
- **Shared counter updates**: Multiple threads modifying counters without proper locking
- **Cross-process state management**: Replacing managed objects instead of updating them in-place

Example of a race condition:
```python
# Thread A checks condition
if operation.is_done():  # Returns False
    # Thread B calls operation.mark_done() here
    # Thread A continues with stale information
    operation.completed_tokens += self.page_size
    self.mem_pool_host.free(operation.host_indices[operation.completed_tokens:])
```

Solutions:
- Use locks or atomic operations for shared state modifications
- Combine check-and-update operations into single atomic transactions
- For multiprocessing, update managed objects in-place rather than replacing them
- Consider if synchronization is necessary on critical paths and document the reasoning

When implementing distributed operations, ensure all ranks maintain consistent state to prevent divergent behavior across the system.