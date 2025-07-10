---
title: Prefer safe null handling
description: 'Use explicit, safe practices when dealing with potentially null resources
  to prevent memory leaks and undefined behavior.


  Key guidelines:

  1. **Use `nullptr` instead of `NULL`** in all C++ code, even when calling C functions:'
repository: maplibre/maplibre-native
label: Null Handling
language: C++
comments_count: 5
repository_stars: 1411
---

Use explicit, safe practices when dealing with potentially null resources to prevent memory leaks and undefined behavior.

Key guidelines:
1. **Use `nullptr` instead of `NULL`** in all C++ code, even when calling C functions:
```cpp
// Poor: Uses outdated NULL macro
sqlite3_vfs* os_fs = sqlite3_vfs_find(NULL);

// Better: Uses modern nullptr keyword
sqlite3_vfs* os_fs = sqlite3_vfs_find(nullptr);
```

2. **With `unique_ptr`, prefer `.reset()` over `.release()`** when clearing resources:
```cpp
// Poor: Memory is leaked after release()
response.error.release();

// Better: Properly destroys the managed object
response.error.reset();
```

3. **Explicitly handle ownership after move operations** to prevent accessing invalid objects:
```cpp
// Poor: Using pendingReleases after moving it
threadPool.schedule(
    [this, wrap_{CaptureWrapper{std::move(pendingReleases)}}]() {
        // pendingReleases is now in an invalid state
        pendingReleases.push_back(...); // Undefined behavior!
    });

// Better: Clear or reinitialize after move
threadPool.schedule(
    [this, wrap_{CaptureWrapper{std::move(pendingReleases)}}]() {
        // Code that uses wrap_ instead of pendingReleases
    });
// Reset pendingReleases to known state here if needed
pendingReleases.clear();
```

4. **Avoid raw pointers** when ownership semantics are needed; use appropriate smart pointers instead:
```cpp
// Poor: Raw pointer ownership is unclear
gpuExpression = other.gpuExpression ? new gfx::GPUExpression(*(other.gpuExpression)) : nullptr;

// Better: Ownership is explicit with smart pointers
gpuExpression = other.gpuExpression ? std::make_unique<gfx::GPUExpression>(*(other.gpuExpression)) : nullptr;
```

These practices make code more robust by eliminating common sources of null-related bugs and memory leaks.