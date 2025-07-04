---
title: Design for API extension
description: When designing APIs, prioritize extensibility by providing clear extension
  points and avoiding direct exposure of implementation details. This allows for future
  enhancements without breaking compatibility.
repository: spring-projects/spring-framework
label: API
language: Java
comments_count: 5
repository_stars: 58382
---

When designing APIs, prioritize extensibility by providing clear extension points and avoiding direct exposure of implementation details. This allows for future enhancements without breaking compatibility.

Key practices:
1. Use interface-based designs over concrete classes
2. Provide extension hooks through protected methods or customization functions
3. Consider future use cases in method signatures
4. Favor composition over inheritance for flexibility

Example of good API design with extension points:

```java
// Instead of directly exposing implementation:
public class HttpConnector {
    private HttpContext createContext() {
        return new HttpContext();
    }
}

// Provide extension hooks:
public class HttpConnector {
    // Allow customization through function
    public HttpConnector(BiFunction<HttpMethod, URI, HttpContext> contextProvider) {
        this.contextProvider = contextProvider;
    }
    
    // Protected methods for subclass customization
    protected HttpContext createContext(HttpMethod method, URI uri) {
        return contextProvider.apply(method, uri);
    }
}
```

This approach:
- Enables customization without breaking changes
- Keeps implementation details private
- Provides clear extension points
- Maintains backward compatibility