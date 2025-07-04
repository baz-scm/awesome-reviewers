---
title: Release resources consistently
description: Always ensure resources are properly released, especially in exception
  paths. Use try-finally blocks to guarantee cleanup of buffers, streams, and other
  resources even when errors occur.
repository: netty/netty
label: Error Handling
language: Java
comments_count: 5
repository_stars: 34227
---

Always ensure resources are properly released, especially in exception paths. Use try-finally blocks to guarantee cleanup of buffers, streams, and other resources even when errors occur.

Common mistakes include:
1. Forgetting to release resources in error paths
2. Not handling promises in cleanup methods
3. Failing to close resources before throwing exceptions

Example of problematic code:
```java
public void write(ChannelHandlerContext ctx, Object msg, ChannelPromise promise) throws Exception {
    ByteBuf content = ctx.alloc().buffer();
    dohQueryEncoder.encode(ctx, (DnsQuery) msg, content);
    
    HttpRequest request = createRequest(content);
    // If an exception occurs here, both content and msg will leak
    super.write(ctx, request, promise);
}
```

Better implementation:
```java
public void write(ChannelHandlerContext ctx, Object msg, ChannelPromise promise) throws Exception {
    DnsQuery query = (DnsQuery) msg;
    ByteBuf content = ctx.alloc().buffer();
    try {
        dohQueryEncoder.encode(ctx, query, content);
        HttpRequest request = createRequest(content);
        ctx.write(request, promise);
    } finally {
        content.release();
        query.release();
    }
}
```

Also ensure proper cleanup in lifecycle methods like `handlerRemoved()` and `doClose()` to prevent leaks, and when throwing exceptions, release any allocated resources first:

```java
if (!IoUring.isRegisterBufferRingSupported()) {
    // Close ringBuffer before throwing to ensure we release all memory on failure
    ringBuffer.close();
    throw new UnsupportedOperationException("io_uring_register_buffer_ring is not supported");
}
```

When handling error conditions, prefer specific exceptions with clear messages:
```java
// Bad
if (encoderFactory == null) {
    throw new Error();
}

// Good
if (encoderFactory == null) {
    throw new IllegalStateException("Couldn't find CompressionEncoderFactory: " + targetContentEncoding);
}
```