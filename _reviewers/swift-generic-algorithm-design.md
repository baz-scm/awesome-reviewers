---
title: Generic algorithm design
description: 'When implementing generic algorithms in Swift, follow these best practices
  to improve code clarity and performance:


  1. Place type constraints directly on associated types rather than at the protocol
  level:'
repository: tensorflow/swift
label: Algorithms
language: Other
comments_count: 3
repository_stars: 6136
---

When implementing generic algorithms in Swift, follow these best practices to improve code clarity and performance:

1. Place type constraints directly on associated types rather than at the protocol level:

```swift
// Not recommended
protocol SortingAlgorithm where Element: Comparable {
    associatedtype Element
    mutating func sort(_ array: inout [Element])
}

// Recommended
protocol SortingAlgorithm {
    associatedtype Element: Comparable
    mutating func sort(_ array: inout [Element])
}
```

2. For filtering operations and predicates, evaluate whether a function type would be more appropriate than a custom protocol:

```swift
// Using a protocol - more flexible but verbose
protocol FilterPredicate {
    associatedtype Element
    func shouldKeep(_ item: Element) -> Bool
}

// Using a function type - often simpler for basic cases
func filter<T>(_ items: [T], predicate: (T) -> Bool) -> [T] {
    return items.filter(predicate)
}
```

3. Start with concrete implementations first, then extract protocols once patterns emerge. This helps you identify the minimal set of requirements needed for your generic algorithm to work effectively.
