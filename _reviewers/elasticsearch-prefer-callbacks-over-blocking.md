---
title: Prefer callbacks over blocking
description: Always structure concurrent code to use asynchronous callbacks instead
  of blocking operations. Blocking calls like CountDownLatch, Thread.join(), or Future.get()
  can lead to thread starvation, reduced throughput, and complex deadlock scenarios.
repository: elastic/elasticsearch
label: Concurrency
language: Java
comments_count: 6
repository_stars: 73104
---

Always structure concurrent code to use asynchronous callbacks instead of blocking operations. Blocking calls like CountDownLatch, Thread.join(), or Future.get() can lead to thread starvation, reduced throughput, and complex deadlock scenarios.

Replace blocking patterns with callback-based approaches:

```java
// AVOID: Blocking with CountDownLatch
CountDownLatch latch = new CountDownLatch(1);
final AtomicBoolean result = new AtomicBoolean(false);
service.getResource(id, new ActionListener<>() {
    @Override
    public void onResponse(Resource resource) {
        result.set(true);
        latch.countDown();
    }
    @Override
    public void onFailure(Exception e) {
        logger.error("Failed: {}", e.getMessage());
        latch.countDown();
    }
});
latch.await(5, TimeUnit.SECONDS); // BLOCKS thread!
return result.get();

// PREFER: Fully asynchronous with listeners
void getResourceAsync(String id, ActionListener<Boolean> listener) {
    service.getResource(id, ActionListener.wrap(
        resource -> listener.onResponse(Boolean.TRUE),
        exception -> {
            if (exception instanceof ResourceNotFoundException) {
                listener.onResponse(Boolean.FALSE);
            } else {
                listener.onFailure(exception);
            }
        }
    ));
}
```

Similarly, for testing asynchronous code, avoid spawning threads and waiting with Thread.join(). Instead, use futures or test-friendly abstractions that allow controlling when callbacks are triggered.
