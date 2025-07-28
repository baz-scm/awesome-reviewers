---
title: weak pointer callback safety
description: When capturing objects in callbacks or lambdas that may execute asynchronously,
  use weak pointers instead of raw pointers or shared pointers to prevent use-after-free
  bugs. Always validate the weak pointer before dereferencing it, and avoid redundant
  lock() calls on the same weak pointer.
repository: hyprwm/Hyprland
label: Concurrency
language: C++
comments_count: 2
repository_stars: 28863
---

When capturing objects in callbacks or lambdas that may execute asynchronously, use weak pointers instead of raw pointers or shared pointers to prevent use-after-free bugs. Always validate the weak pointer before dereferencing it, and avoid redundant lock() calls on the same weak pointer.

This pattern is essential for thread safety when objects may be destroyed while callbacks are still pending execution. The weak pointer allows the callback to safely check if the object still exists before attempting to use it.

Example of proper weak pointer usage in callbacks:
```cpp
// Good: Use weak pointer and validate before use
auto weakBuffer = WP<IHLBuffer>(PBUFFER);
PBUFFER->onBackendRelease([weakBuffer]() {
    if (auto buffer = weakBuffer.lock())
        buffer->unlock();
});

// Avoid: Redundant lock() calls in comparisons
if (weakPtr1.lock() == weakPtr2.lock()) // redundant double .lock()
// Better: Store locked pointers if comparing multiple times
auto ptr1 = weakPtr1.lock();
auto ptr2 = weakPtr2.lock();
if (ptr1 == ptr2)
```

This approach prevents crashes when the referenced object is destroyed before the callback executes, which is common in asynchronous systems with complex object lifetimes.