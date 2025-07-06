---
title: Prevent test resource leaks
description: Always ensure proper cleanup of resources in tests to prevent memory
  leaks. When using EmbeddedChannel, call readOutbound() to process all expected buffers
  and finish() at the end of your test to verify no resources remain and release any
  remaining buffers. This is particularly important for tests involving data buffers,
  channels, and I/O operations.
repository: netty/netty
label: Testing
language: Java
comments_count: 3
repository_stars: 34227
---

Always ensure proper cleanup of resources in tests to prevent memory leaks. When using EmbeddedChannel, call readOutbound() to process all expected buffers and finish() at the end of your test to verify no resources remain and release any remaining buffers. This is particularly important for tests involving data buffers, channels, and I/O operations.

Example:
```java
@Test
public void testBufferHandling() {
    EmbeddedChannel channel = new EmbeddedChannel(new YourHandler());
    
    // Write test data
    channel.writeInbound(Unpooled.wrappedBuffer(testData));
    
    // Read and verify all expected results
    ByteBuf result1 = channel.readInbound();
    assertEquals(expectedData1, result1);
    result1.release();
    
    ByteBuf result2 = channel.readInbound();
    assertEquals(expectedData2, result2);
    result2.release();
    
    // Ensure channel is properly closed and no resources are leaked
    assertFalse(channel.finish());
}
```

This pattern prevents resource leaks that can accumulate during test runs and ensures that your tests properly validate the complete processing of data.