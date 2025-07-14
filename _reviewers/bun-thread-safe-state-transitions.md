---
title: Thread-safe state transitions
description: When modifying shared state in multithreaded code, implement proper checks
  and state transitions to prevent race conditions. This applies to flags, counters,
  and resource management.
repository: oven-sh/bun
label: Concurrency
language: C++
comments_count: 2
repository_stars: 79093
---

When modifying shared state in multithreaded code, implement proper checks and state transitions to prevent race conditions. This applies to flags, counters, and resource management.

1. Use atomic operations when checking and modifying shared state
2. Check state values after atomic operations rather than before 
3. For multi-step processes, track in-flight operations and only perform final state transitions when all operations are complete

Bad:
```cpp
// Don't check flags without thread safety
if (m_terminationFlags & TerminatedFlag) {
    // Already terminated, skip work
    return;
}
// Race condition: Another thread might have set the flag between check and action
```

Good:
```cpp
// Use atomic operations and check the return value
if (atomic_fetch_or(&m_terminationFlags, TerminatedFlag) & TerminatedFlag) {
    // Already terminated, skip work
    return;
}

// For multi-step processes, track completion:
protectedThis->m_messagesInFlight -= 1;
if (protectedThis->m_messagesInFlight == 0)
    protectedThis->close(); // Only close when all messages are processed
```