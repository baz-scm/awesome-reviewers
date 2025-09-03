---
title: Thread safety synchronization
description: 'Ensure proper synchronization when accessing shared data structures
  and coordinate operations across multiple threads to prevent race conditions.


  **Key practices:**'
repository: flutter/flutter
label: Concurrency
language: Other
comments_count: 3
repository_stars: 172252
---

Ensure proper synchronization when accessing shared data structures and coordinate operations across multiple threads to prevent race conditions.

**Key practices:**

1. **Protect shared data with mutexes**: When modifying shared data structures, use appropriate locking mechanisms:
```cpp
// Before: Unprotected access
expected_frame_constraints_.erase(view_id);

// After: Protected with mutex
std::scoped_lock<std::mutex> lock(resize_mutex_);
expected_frame_constraints_.erase(view_id);
```

2. **Clean up before destruction**: Unregister handlers and cleanup resources before destroying objects to avoid receiving callbacks during destruction:
```cpp
@override
void destroy() {
  if (_destroyed) return;
  
  // Unregister BEFORE destroying to avoid race conditions
  _owner.removeMessageHandler(this);
  _Win32PlatformInterface.destroyWindow(getWindowHandle());
  _destroyed = true;
  _delegate.onWindowDestroyed();
}
```

3. **Consolidate multi-threaded operations**: When operations span multiple threads, consider consolidating critical sections to a single thread or use proper coordination. As noted in platform view embedding: "We still do it in 2 different threads... Those 2 threads would be in a race condition." Consider posting all related operations to the same thread:
```cpp
// Consolidate to platform thread
task_runners_.GetPlatformTaskRunner()->PostTask([&, jni_facade = jni_facade_]() {
  HideOverlayLayerIfNeeded();
  jni_facade->applyTransaction();
});
```

Race conditions between threads processing different frame states can lead to inconsistent UI state and are difficult to debug. Always consider the threading model when designing APIs that modify shared state.