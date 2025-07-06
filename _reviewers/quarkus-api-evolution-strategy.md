---
title: API evolution strategy
description: 'Design APIs with future extensibility in mind by using parameter objects
  instead of direct method parameters. When an API might need additional parameters
  in the future, encapsulate them in an interface or class:'
repository: quarkusio/quarkus
label: API
language: Java
comments_count: 7
repository_stars: 14667
---

Design APIs with future extensibility in mind by using parameter objects instead of direct method parameters. When an API might need additional parameters in the future, encapsulate them in an interface or class:

```java
// Instead of adding parameters directly:
<K, V> Uni<V> get(K key, Function<K, V> valueLoader, Duration expiresIn);

// Prefer an encapsulating approach:
<K, V> Uni<V> get(K key, Function<K, V> valueLoader, CacheOptions options);
```

For parameter objects, prefer interfaces over concrete classes to allow for extension without breaking changes. When naming parameters or methods, align with established industry standards (e.g., use "expiresAfter" instead of "expiresIn" to match Caffeine's terminology). 

Choose clear, descriptive method names over abbreviations (e.g., `authenticationContextInterceptorCreator()` rather than `authCtxInterceptorCreator()`). For methods with similar functionality, maintain a consistent pattern - if you have `send()` and `sendAndAwait()`, consider also adding `sendAndForget()` for completeness.

When providing builder-style APIs, ensure utility methods that don't contribute to object construction are placed in appropriate utility classes rather than in the builder itself.