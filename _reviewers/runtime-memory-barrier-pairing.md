---
title: Memory barrier pairing
description: When implementing low-level synchronization mechanisms in multi-threaded
  code, ensure that memory barriers are correctly paired between reader and writer
  operations. For each read barrier, implement a corresponding write barrier to maintain
  memory consistency and prevent race conditions.
repository: dotnet/runtime
label: Concurrency
language: Other
comments_count: 2
repository_stars: 16578
---

When implementing low-level synchronization mechanisms in multi-threaded code, ensure that memory barriers are correctly paired between reader and writer operations. For each read barrier, implement a corresponding write barrier to maintain memory consistency and prevent race conditions.

For example, in ARM64 assembly:
```asm
// Read side
dmb ishld   // Data memory barrier for load operations

// Write side (corresponding barrier needed)
dmb ishst   // Data memory barrier for store operations
```

Consider whether specialized atomic instructions (like `ldar` for loads or `stlr` for stores) might provide the same memory ordering guarantees with potentially better performance in specific scenarios. However, ensure these are implemented at the correct locations in the code to properly maintain the synchronization semantics.
