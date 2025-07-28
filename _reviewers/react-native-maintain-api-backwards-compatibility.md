---
title: maintain API backwards compatibility
description: When modifying existing public APIs, prioritize backwards compatibility
  to avoid breaking external consumers. Before making changes that alter method signatures,
  property access patterns, or introduce new abstract methods, first investigate whether
  existing functionality can be preserved or extended.
repository: facebook/react-native
label: API
language: Java
comments_count: 2
repository_stars: 123178
---

When modifying existing public APIs, prioritize backwards compatibility to avoid breaking external consumers. Before making changes that alter method signatures, property access patterns, or introduce new abstract methods, first investigate whether existing functionality can be preserved or extended.

For property access changes, provide alternative access methods while maintaining the original interface:
```java
// Instead of only changing:
// mEventEmitterCallback.invoke("onPress"); 
// to:
// getEventEmitterCallback().invoke("onPress");

// Provide both approaches - keep the property accessible AND add the getter
protected EventEmitterCallback mEventEmitterCallback; // Keep original
protected final EventEmitterCallback getEventEmitterCallback() { // Add new getter
    return mEventEmitterCallback;
}
```

For new functionality, leverage existing methods rather than creating new abstract methods:
```java
// Instead of adding:
// public abstract void invalidate();

// Use existing method:
public void clear() {
    // Add invalidation logic here
    // existing clear logic...
}
```

This approach protects downstream consumers, reduces migration burden, and maintains API stability. Always check if your changes affect external packages before finalizing API modifications.