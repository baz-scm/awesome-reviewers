---
title: Optimize allocation hotspots
description: Identify and optimize object allocation in performance-critical paths
  by applying appropriate allocation strategies based on usage patterns. For frequently
  accessed objects, consider reusing instances rather than creating new ones. For
  short-lived objects in hot code paths, evaluate whether the JIT can optimize allocations
  away or if explicit object...
repository: netty/netty
label: Performance Optimization
language: Java
comments_count: 17
repository_stars: 34227
---

Identify and optimize object allocation in performance-critical paths by applying appropriate allocation strategies based on usage patterns. For frequently accessed objects, consider reusing instances rather than creating new ones. For short-lived objects in hot code paths, evaluate whether the JIT can optimize allocations away or if explicit object pooling/caching is needed.

For example, instead of creating new handler instances for each channel:
```java
// Inefficient - creates new instance per channel
channel.pipeline().addLast(new MyHandler());

// Efficient - reuses single instance across channels
private static final MyHandler SHARED_HANDLER = new MyHandler();
// Add @Sharable annotation to handler class
channel.pipeline().addLast(SHARED_HANDLER);
```

For frequent operations, consider thread-local caching when appropriate:
```java
// Cache event objects per thread for high-frequency operations
private static final ThreadLocal<MyEvent> EVENT_CACHE = 
    ThreadLocal.withInitial(MyEvent::new);

public void onHighFrequencyOperation() {
    MyEvent event = EVENT_CACHE.get();
    event.reset(); // Prepare for reuse
    // Use event...
}
```

When dealing with buffer management, ensure proper release and consider zero-copy approaches:
```java
ByteBuf buffer = null;
try {
    buffer = allocator.directBuffer(size);
    // Use buffer...
} finally {
    if (buffer != null) {
        buffer.release(); // Ensure proper release
    }
}
```

For frequently used resource handles like file descriptors, consider caching and reuse:
```java
// Instead of creating new pipes for each operation
if (pipe == null) {
    pipe = FileDescriptor.pipe();
}
```

Measure performance impact of allocation strategies with benchmarks before committing to complex optimization patterns, as JIT may already optimize simple allocation patterns in some cases.