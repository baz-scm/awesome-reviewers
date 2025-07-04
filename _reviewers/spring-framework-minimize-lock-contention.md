---
title: Minimize lock contention
description: When implementing thread-safe code, minimize the scope and duration of
  locks to reduce contention and improve performance. Keep critical sections small,
  avoid redundant operations under locks, and consider whether pessimistic locking
  is appropriate for your use case.
repository: spring-projects/spring-framework
label: Concurrency
language: Java
comments_count: 4
repository_stars: 58382
---

When implementing thread-safe code, minimize the scope and duration of locks to reduce contention and improve performance. Keep critical sections small, avoid redundant operations under locks, and consider whether pessimistic locking is appropriate for your use case.

**Key practices:**

1. **Keep critical sections small and focused**:
   ```java
   // Bad: Doing extra work under lock
   synchronized (lock) {
       result = computeExpensiveOperation();
       sharedState.update(result);
   }
   
   // Good: Only synchronize the state update
   result = computeExpensiveOperation();
   synchronized (lock) {
       sharedState.update(result);
   }
   ```

2. **Avoid redundant writes to shared/volatile fields**:
   ```java
   // Bad: Multiple writes to volatile field
   synchronized (this) {
       this.cachedFieldValue = desc;
       // More logic...
       this.cachedFieldValue = new ShortcutDependencyDescriptor(...);
   }
   
   // Good: Single write using local variable
   synchronized (this) {
       Object cachedFieldValue = desc;
       // More logic...
       if (condition) {
           cachedFieldValue = new ShortcutDependencyDescriptor(...);
       }
       this.cachedFieldValue = cachedFieldValue;
   }
   ```

3. **Choose appropriate concurrency primitives**:
   - Use `ReadWriteLock` for read-heavy workloads
   - Consider lock-free alternatives like `ConcurrentHashMap` and atomic variables
   - In reactive code, prefer optimistic locking with CAS operations over pessimistic locks

4. **Be aware of hidden performance costs**:
   - Collection operations like `size()` on linked structures may require traversal
   - Improper lock granularity can cause contention hotspots
   - Consider thread scheduling and context switching overhead