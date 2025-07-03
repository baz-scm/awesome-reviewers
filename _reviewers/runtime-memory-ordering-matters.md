---
title: Memory ordering matters
description: 'When working with shared data in multithreaded environments, memory
  ordering is critical to prevent race conditions and ensure thread safety:


  1. **Avoid transient incorrect states** - Don''t write an incorrect value before
  replacing it with the correct one, as other threads may see the intermediate state:'
repository: dotnet/runtime
label: Concurrency
language: C++
comments_count: 3
repository_stars: 16578
---

When working with shared data in multithreaded environments, memory ordering is critical to prevent race conditions and ensure thread safety:

1. **Avoid transient incorrect states** - Don't write an incorrect value before replacing it with the correct one, as other threads may see the intermediate state:

```cpp
// INCORRECT: Creates a race window where incorrect value is visible
*ppvRetAddrLocation = (void*)pfnHijackFunction;
#if defined(TARGET_ARM64)
*ppvRetAddrLocation = PacSignPtr(*ppvRetAddrLocation);
#endif

// CORRECT: Prepare final value before publishing
void* pvHijackAddr = (void*)pfnHijackFunction;
#if defined(TARGET_ARM64)
pvHijackAddr = PacSignPtr(pvHijackAddr);
#endif
*ppvRetAddrLocation = pvHijackAddr;
```

2. **Use atomic operations correctly** - Pay careful attention to argument order in functions like `InterlockedCompareExchange(destination, exchange, comparand)`:

```cpp
// INCORRECT: Arguments in wrong order
if (versionStart != InterlockedCompareExchange(&s_stackWalkNativeToILCacheVersion, versionStart, versionStart | 1))

// CORRECT: Proper argument order
if (versionStart != InterlockedCompareExchange(&s_stackWalkNativeToILCacheVersion, versionStart | 1, versionStart))
```

3. **Use memory barriers when publishing shared data** - Ensure supporting data is visible before publishing pointers:

```cpp
// INCORRECT: May be reordered
s_stackWalkCacheSize = cacheSize;
s_stackWalkCache = newCache; // Other threads might see the pointer before size is set

// CORRECT: Memory barrier ensures proper ordering
VolatileStore(&s_stackWalkCacheSize, cacheSize);
s_stackWalkCache = newCache;
```

Proper memory ordering is essential for preventing subtle multithreading bugs that may only appear under high load or on specific hardware architectures.
