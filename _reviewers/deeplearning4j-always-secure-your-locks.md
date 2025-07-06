---
title: Always secure your locks
description: When using locks or other synchronization mechanisms in concurrent code,
  always release locks in a finally block to ensure they are released even when exceptions
  occur. Failure to do so can lead to deadlocks if other threads need the same lock.
repository: deeplearning4j/deeplearning4j
label: Concurrency
language: Java
comments_count: 3
repository_stars: 14036
---

When using locks or other synchronization mechanisms in concurrent code, always release locks in a finally block to ensure they are released even when exceptions occur. Failure to do so can lead to deadlocks if other threads need the same lock.

Additionally, choose the appropriate concurrency primitive for your specific use case. Using the wrong tool (like a Semaphore when a CountDownLatch is more appropriate) can lead to subtle bugs that are difficult to diagnose.

Bad example:
```java
public void updateModel(@NonNull Model model) {
    modelLock.writeLock().lock();
    // If an exception occurs here, lock is never released!
    // Do work with the model...
    modelLock.writeLock().unlock();
}
```

Good example:
```java
public void updateModel(@NonNull Model model) {
    modelLock.writeLock().lock();
    try {
        // Do work with the model...
    } finally {
        modelLock.writeLock().unlock();
    }
}
```

For wait/notify patterns, consider whether a CountDownLatch or other higher-level concurrency primitive would be more appropriate than using raw locks or semaphores:

```java
// Instead of this:
private Semaphore semaphore = new Semaphore(0);
public void update(Observable o, Object arg) {
    semaphore.release(Integer.MAX_VALUE); // Potential overflow!
}

// Consider this:
private CountDownLatch latch = new CountDownLatch(1);
public void update(Observable o, Object arg) {
    latch.countDown(); // Safe, can only transition once
}

public void waitTillDone() throws InterruptedException {
    latch.await(); // Properly propagate interruption
}
```