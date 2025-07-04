---
title: Minimize allocation hotspots
description: Reduce object creation in performance-critical paths by carefully evaluating
  allocation patterns. For frequently instantiated objects, consider caching instances
  or using static helpers, but always validate improvements with proper benchmarks.
repository: spring-projects/spring-framework
label: Performance Optimization
language: Java
comments_count: 11
repository_stars: 58382
---

Reduce object creation in performance-critical paths by carefully evaluating allocation patterns. For frequently instantiated objects, consider caching instances or using static helpers, but always validate improvements with proper benchmarks.

Key practices:
1. Identify allocation hotspots with profiling tools before optimizing
2. Size collections appropriately to avoid resizing: `new HashMap<>(expectedSize * 4/3 + 1)`
3. Reuse objects in loops rather than creating new ones each iteration
4. Cache frequently used utility objects as static variables
5. Use pooled resources (buffers, connections) with proper release mechanisms

Example of object creation optimization with benchmark validation:

```java
// Before: Creates new factory for every request
public URI getUrl() {
    final DefaultUriBuilderFactory factory = new DefaultUriBuilderFactory();
    factory.setEncodingMode(DefaultUriBuilderFactory.EncodingMode.URI_COMPONENT);
    return factory.expand(uriTemplate.toString(), uriVariables);
}

// After: Uses static factory instance
private static final DefaultUriBuilderFactory URI_BUILDER_FACTORY;

static {
    URI_BUILDER_FACTORY = new DefaultUriBuilderFactory();
    URI_BUILDER_FACTORY.setEncodingMode(DefaultUriBuilderFactory.EncodingMode.URI_COMPONENT);
}

public URI getUrl() {
    return URI_BUILDER_FACTORY.expand(uriTemplate.toString(), uriVariables);
}
```

Always verify optimizations with JMH benchmarks that prevent dead-code elimination:

```java
@Benchmark
public Object measureOptimizedCode(Blackhole blackhole) {
    Object result = optimizedOperation();
    blackhole.consume(result); // Prevent JVM optimization from removing code
    return result;
}
```