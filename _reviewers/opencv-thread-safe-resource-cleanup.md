---
title: Thread-safe resource cleanup
description: When implementing resource cleanup in concurrent applications, avoid
  using deprecated finalizers and instead use PhantomReference-based cleanup mechanisms
  that ensure thread safety.
repository: opencv/opencv
label: Concurrency
language: Java
comments_count: 2
repository_stars: 82865
---

When implementing resource cleanup in concurrent applications, avoid using deprecated finalizers and instead use PhantomReference-based cleanup mechanisms that ensure thread safety.

Key considerations:
1. Use PhantomReference with a ReferenceQueue to detect when objects are ready for cleanup
2. Maintain appropriate data structures (e.g., doubly-linked lists) to track references and support efficient removal
3. Implement a dedicated daemon thread to process the cleanup queue
4. Ensure the cleaner object outlives the resources it manages

Example implementation:
```java
public final class SafeResourceCleaner {
    private final ReferenceQueue<Object> queue = new ReferenceQueue<>();
    private final PhantomCleanable phantomCleanableList = new PhantomCleanable();
    
    // Create a single cleaner per application/library component
    public static SafeResourceCleaner create() {
        SafeResourceCleaner cleaner = new SafeResourceCleaner();
        cleaner.startCleanerThread();
        return cleaner;
    }
    
    public Cleanable register(Object resource, Runnable cleanupAction) {
        return new PhantomCleanable(
            Objects.requireNonNull(resource), 
            Objects.requireNonNull(cleanupAction)
        );
    }
    
    private void startCleanerThread() {
        Thread thread = new Thread(() -> {
            while (!isShutdown()) {
                try {
                    // Use reasonable timeout to allow thread termination if needed
                    Cleanable ref = (Cleanable) queue.remove(60 * 1000L);
                    if (ref != null) {
                        ref.clean();
                    }
                } catch (Throwable e) {
                    // Handle exceptions gracefully, never let them terminate the cleaner thread
                }
            }
        }, "ResourceCleaner-Thread");
        thread.setDaemon(true);  // Don't prevent JVM shutdown
        thread.start();
    }
}
```

This approach is particularly important for concurrent applications where thread safety must be maintained during resource cleanup, and it provides a more reliable alternative to the deprecated finalize() method.
