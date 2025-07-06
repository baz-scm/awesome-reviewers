---
title: Document public APIs
description: 'All public APIs, interfaces, and methods should include comprehensive
  JavaDoc that clearly explains their purpose, parameters, return values, and any
  non-obvious behaviors. This is especially important for:'
repository: quarkusio/quarkus
label: Documentation
language: Java
comments_count: 5
repository_stars: 14667
---

All public APIs, interfaces, and methods should include comprehensive JavaDoc that clearly explains their purpose, parameters, return values, and any non-obvious behaviors. This is especially important for:

1. Public interfaces and SPIs that will be used by external developers
2. Methods with complex parameters (like priority values)
3. Methods with non-obvious execution order or side effects
4. Build items and integration points

JavaDoc should be added at the time the code is written, not as an afterthought. For deprecations, ensure to include `forRemoval=true` to clearly document the API lifecycle.

Example:
```java
/**
 * Context for handling application shutdown.
 * Tasks can be registered with different priorities to control execution order.
 */
public interface ShutdownContext {

    int DEFAULT_PRIORITY = Interceptor.Priority.LIBRARY_AFTER;
    int SHUTDOWN_EVENT_PRIORITY = DEFAULT_PRIORITY + 100_000;

    /**
     * Adds a shutdown task with the default priority.
     * 
     * @param runnable The task to execute during shutdown
     */
    default void addShutdownTask(Runnable runnable) {
        addShutdownTask(DEFAULT_PRIORITY, runnable);
    }

    /**
     * Adds a shutdown task with the specified priority.
     * Higher priority tasks are executed first during shutdown.
     * 
     * @param priority Task execution priority - higher values run before lower values
     * @param runnable The task to execute during shutdown
     */
    void addShutdownTask(int priority, Runnable runnable);
}
```