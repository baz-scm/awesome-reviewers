---
title: Minimize unnecessary work
description: 'Optimize performance by reducing the amount of computation performed,
  especially on data that won''t appear in the final result. Apply these strategies:'
repository: JetBrains/kotlin
label: Performance Optimization
language: Kotlin
comments_count: 7
repository_stars: 50857
---

Optimize performance by reducing the amount of computation performed, especially on data that won't appear in the final result. Apply these strategies:

1) **Filter early**: Filter collections before performing expensive transformations like sorting
```kotlin
// Suboptimal: Sorts all elements, then removes private ones
functions.sortBy(KmFunction::name)
functions.removeIf { it.visibility.isPrivate }

// Optimized: Removes private elements first, then sorts only what's needed
functions.removeIf { it.visibility.isPrivate }
functions.sortBy(KmFunction::name)
```

2) **Short-circuit common cases**: Add early returns for special cases like empty collections or single elements
```kotlin
public fun <T> Array<out Array<out T>>.flatten(): List<T> {
    if (isEmpty()) return emptyList() // Early return for common case
    // Regular processing...
}
```

3) **Cache expensive results**: Use memoization for operations that may be called repeatedly with the same input
```kotlin
private val containsCache = mutableMapOf<IrDeclaration, Boolean>()

override fun containsDeclaration(declaration: IrDeclaration): Boolean = 
    containsCache.getOrPut(declaration) {
        // Expensive computation here
    }
```

4) **Optimize for expected usage patterns**: Special-case handle common scenarios based on benchmarks
```kotlin
// Optimization for common no-argument functions
if (parameters.isEmpty()) {
    return reflectionCall {
        caller.call(if (isSuspend) arrayOf(continuationArgument) else emptyArray()) as R
    }
}
```

Always verify your optimizations with benchmarks to ensure they provide measurable benefits in real-world scenarios.
