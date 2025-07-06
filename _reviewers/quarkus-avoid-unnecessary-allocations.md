---
title: Avoid unnecessary allocations
description: Minimize object creation and memory allocations, especially in frequently
  called methods and hot code paths, to reduce garbage collection pressure and improve
  performance.
repository: quarkusio/quarkus
label: Performance Optimization
language: Java
comments_count: 4
repository_stars: 14667
---

Minimize object creation and memory allocations, especially in frequently called methods and hot code paths, to reduce garbage collection pressure and improve performance.

Key practices:
1. Avoid varargs methods like `Objects.hash()` in `hashCode()` implementations for objects that will be used as map keys, as they allocate arrays with each call:
```java
// Instead of this:
public int hashCode() {
    return Objects.hash(name, params, returnType); // Creates array allocation
}

// Prefer this:
public int hashCode() {
    int result = name.hashCode();
    result = 31 * result + params.hashCode();
    result = 31 * result + returnType.hashCode();
    return result;
}
```

2. Cache method results that would otherwise create new collections on each call:
```java
// Instead of repeatedly calling:
method.parameterTypes().size() // Creates new collection each time

// Cache the result or use alternatives:
int paramCount = method.parametersCount(); // Doesn't create collection
```

3. Optimize collection creation for small, known sizes:
```java
// Use specialized factories for small collections:
this.params = switch (method.parametersCount()) {
    case 0 -> List.of();
    case 1 -> List.of(method.parameterTypes().get(0).name());
    case 2 -> List.of(method.parameterTypes().get(0).name(), method.parameterTypes().get(1).name());
    default -> {
        List<DotName> ret = new ArrayList<>(method.parametersCount());
        for (Type i : method.parameterTypes()) {
            ret.add(i.name());
        }
        yield ret;
    }
};
```

4. Create specialized non-collection return methods for hot paths:
```java
// Instead of always returning collections:
public List<RequestMatch<T>> mapFromPathMatcher(...) { ... }

// Provide specialized method for common cases:
public RequestMatch<T> map(String path) {
    // Direct return without collection creation
}
```

Be conscious of underlying collection implementations when choosing iteration patterns (for-loops vs iterators) as using index-based access on LinkedLists can lead to O(n²) performance.