---
title: minimize public API surface
description: Only expose APIs that are truly necessary for external consumers and
  avoid creating public interfaces that may become maintenance burdens. Before adding
  public builders, helper utilities, or exposing internal types, critically evaluate
  whether they provide genuine value to API users.
repository: apache/spark
label: API
language: Java
comments_count: 3
repository_stars: 41554
---

Only expose APIs that are truly necessary for external consumers and avoid creating public interfaces that may become maintenance burdens. Before adding public builders, helper utilities, or exposing internal types, critically evaluate whether they provide genuine value to API users.

Key principles:
- Question the necessity of public builders when objects are unlikely to be constructed by consumers
- Avoid exposing internal implementation details (like catalyst package types) as public APIs  
- Consider whether simple helper utilities are actually needed or if they add unnecessary complexity
- Prefer internal implementations with utility methods over public builders when appropriate

Example from the codebase:
```java
// Instead of exposing a public Builder that may not be used:
public interface MergeMetrics {
  class Builder { /* public builder methods */ }
}

// Consider internal implementation:
// Keep MergeMetrics as interface, add internal case class like LogicalWriteInfo
// or make it a proper Java class with utility construction method
```

This approach reduces long-term API maintenance overhead while keeping the public interface clean and focused on genuine user needs.