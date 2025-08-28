---
title: isolate lock safety
description: Always ensure proper isolate lock management and thread-safe access patterns
  when working with JavaScript contexts and cross-thread operations. Accessing JSG
  objects, IoContext, or V8 handles without holding the isolate lock leads to undefined
  behavior and crashes.
repository: cloudflare/workerd
label: Concurrency
language: Other
comments_count: 8
repository_stars: 6989
---

Always ensure proper isolate lock management and thread-safe access patterns when working with JavaScript contexts and cross-thread operations. Accessing JSG objects, IoContext, or V8 handles without holding the isolate lock leads to undefined behavior and crashes.

Key requirements:
1. **Use explicit capture lists** in async lambdas instead of `[&]` - reference capture is only safe for synchronous execution
2. **Use `ctx.run()` for isolate entry** - manually acquiring locks misses critical setup like setting current IoContext and honoring input locks  
3. **Capture weak references for cross-thread access** - use `IoContext::current().getWeakRef()` and check validity before accessing
4. **Avoid blocking I/O in sync functions** - use proper async patterns instead of `.wait()` or threads
5. **Mark thread-sensitive resources clearly** - use concrete names like `ownContentIsRpcResponse` to indicate thread affinity requirements

Example of unsafe vs safe patterns:

```cpp
// UNSAFE: Reference capture in async lambda
return context.awaitIo(js, kj::mv(promise), [&](jsg::Lock& js, kj::String text) mutable {
  // [&] is unsafe when lambda executes asynchronously
});

// SAFE: Explicit capture list
return context.awaitIo(js, kj::mv(promise), [context = &context](jsg::Lock& js, kj::String text) mutable {
  // Explicit capture is safe
});

// UNSAFE: Manual isolate lock without proper context
auto lock = co_await ctx.getWorker()->takeAsyncLockWithoutRequest(nullptr);

// SAFE: Use ctx.run() for proper isolate entry
co_await ctx.run([](Worker::Lock& lock) {
  // Proper context setup with IoContext, input locks, etc.
});
```

This prevents data races, use-after-free bugs, and ensures proper resource lifecycle management across thread boundaries.