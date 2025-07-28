---
title: Avoid synchronous main dispatch
description: Avoid using `RCTUnsafeExecuteOnMainQueueSync` and similar synchronous
  main queue dispatch methods as they can cause deadlocks, especially in initialization
  code, dispatch_once blocks, or when called from background threads that may already
  hold main queue dependencies.
repository: facebook/react-native
label: Concurrency
language: Other
comments_count: 4
repository_stars: 123178
---

Avoid using `RCTUnsafeExecuteOnMainQueueSync` and similar synchronous main queue dispatch methods as they can cause deadlocks, especially in initialization code, dispatch_once blocks, or when called from background threads that may already hold main queue dependencies.

Deadlocks occur when the main queue is waiting for a background queue, and that background queue then tries to synchronously dispatch back to the main queue. This creates a circular dependency where both queues are blocked waiting for each other.

Instead, use asynchronous alternatives like `RCTExecuteOnMainQueue` which avoids the jump if already on the main queue, or standard `dispatch_async(dispatch_get_main_queue(), ...)` when you need to ensure execution at the end of the main queue.

Example of problematic code:
```objc
// BAD - Can cause deadlock
- (void)invalidate {
  RCTUnsafeExecuteOnMainQueueSync(^{
    if (_didInvalidate) {
      return;
    }
    // ... invalidation logic
  });
}
```

Example of safer alternative:
```objc
// GOOD - Uses async dispatch to avoid deadlock
- (void)invalidate {
  RCTExecuteOnMainQueue(^{
    if (_didInvalidate) {
      return;
    }
    // ... invalidation logic
  });
}
```

This pattern is particularly important in React Native's multi-threaded environment where JavaScript, UI, and background threads frequently interact.