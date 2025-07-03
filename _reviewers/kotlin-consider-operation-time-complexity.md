---
title: Consider operation time complexity
description: 'When implementing operations that manipulate collections or perform
  repeated actions, carefully consider the time complexity implications. Avoid operations
  that could result in unexpected quadratic or worse complexity. Pay special attention
  to:'
repository: JetBrains/kotlin
label: Algorithms
language: Kotlin
comments_count: 5
repository_stars: 50857
---

When implementing operations that manipulate collections or perform repeated actions, carefully consider the time complexity implications. Avoid operations that could result in unexpected quadratic or worse complexity. Pay special attention to:

1. Collection modifications that shift elements
2. Nested loops or repeated operations on growing datasets
3. Data structure choice based on access patterns

Example of problematic implementation:
```kotlin
// BAD: O(n²) complexity
fun <E> ArrayList<E>.addAll(index: Int, elements: Collection<E>) {
    var i = index
    elements.forEach { element ->
        array.asDynamic().splice(i, 0, element) // Shifts array on each insert
        i++
    }
}

// BETTER: O(n) complexity
fun <E> ArrayList<E>.addAll(index: Int, elements: Collection<E>) {
    // Single array modification with all elements
    array.asDynamic().splice(index, 0, *elements.toTypedArray())
}
```

Choose data structures based on your specific use case:
- Use ArrayList when you need indexed access and mostly append operations
- Use LinkedList when you frequently insert/remove from middle
- Use HashSet for fast lookups and uniqueness checks
- Consider LinkedHashMap only when ordering is critical and worth the overhead
