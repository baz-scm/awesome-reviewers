---
title: Avoid expensive allocations
description: Minimize object creation and expensive operations in performance-critical
  code paths, particularly in frequently called methods like onDraw, layout operations,
  and UI updates.
repository: facebook/react-native
label: Performance Optimization
language: Java
comments_count: 3
repository_stars: 123178
---

Minimize object creation and expensive operations in performance-critical code paths, particularly in frequently called methods like onDraw, layout operations, and UI updates.

Key strategies:
1. **Lazy allocation**: Only create objects when actually needed. For example, allocate collections like HashSet only when the feature requiring them is used, rather than eagerly during initialization.

2. **Reuse objects in hot paths**: Avoid creating new instances in frequently called methods. Instead, create reusable objects as instance variables and reset them before use:

```java
// Instead of creating new Path in onDraw:
public void onDraw(Canvas canvas) {
    Path path = new Path(); // BAD - creates object every draw
    // ...
}

// Create reusable instance variable:
private Path mReusablePath = new Path();

public void onDraw(Canvas canvas) {
    mReusablePath.reset(); // GOOD - reuse existing object
    // ...
}
```

3. **Guard expensive operations**: Before performing costly computations, check if they're actually necessary. Add conditional checks to avoid redundant expensive calls like layout calculations or complex measurements.

This approach prevents memory pressure from frequent allocations, reduces garbage collection overhead, and improves overall application performance, especially in UI rendering and animation scenarios.