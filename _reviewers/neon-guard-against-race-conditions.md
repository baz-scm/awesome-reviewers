---
title: Guard against race conditions
description: 'When working with concurrent operations, always implement proper guards
  to prevent race conditions between processes. This includes:


  1. Adding explicit checks before operations that might be affected by concurrent
  processes:'
repository: neondatabase/neon
label: Concurrency
language: C
comments_count: 3
repository_stars: 19015
---

When working with concurrent operations, always implement proper guards to prevent race conditions between processes. This includes:

1. Adding explicit checks before operations that might be affected by concurrent processes:

```c
// Before performing an operation that assumes file existence
if (mdnblocks(reln, forknum) >= blocknum)
{
    // Operation is safe to proceed
    // Comment explaining the race condition being prevented
}
```

2. Using precise mechanisms to detect resource availability in multi-process environments. For shared memory access, prefer `UsedShmemSegAddr` over `IsUnderPostmaster` since some processes may have detached shared memory:

```c
// Correct check for shared memory availability
if (newval && *newval != '\0' && UsedShmemSegAddr && shared_resource_available)
```

3. Implementing robust interrupt handling for operations that may be suspended. Always recalculate timing after potential interruptions:

```c
// Loop to handle interrupted sleeps
while (elapsed_time < required_delay)
{
    pg_usleep(required_delay - elapsed_time);
    
    // Handle potential interrupts
    CHECK_FOR_INTERRUPTS();
    
    // Recalculate elapsed time with fresh timestamp
    current_time = GetCurrentTimestamp();
    elapsed_time = current_time - start_time;
}
```

Always add clear comments explaining the race condition being prevented to help future developers understand the reasoning behind these guards.