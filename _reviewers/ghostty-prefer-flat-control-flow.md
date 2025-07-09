---
title: Prefer flat control flow
description: Minimize code nesting by using Swift features like `guard` statements
  and early returns instead of deeply nested if-else structures. When multiple code
  branches end with a return statement, avoid nesting with `else` clauses.
repository: ghostty-org/ghostty
label: Code Style
language: Swift
comments_count: 2
repository_stars: 32864
---

Minimize code nesting by using Swift features like `guard` statements and early returns instead of deeply nested if-else structures. When multiple code branches end with a return statement, avoid nesting with `else` clauses.

Instead of:
```swift
if index == count {
    return try body(accumulated)
} else {
    // More nested code here
}
```

Prefer:
```swift
if index == count {
    return try body(accumulated)
}
// Continue with the flow without nesting
```

Or consider using `guard` statements for early returns:
```swift
guard case .split(let c) = node else { return }
// Now work with the unwrapped variable
```

This approach makes code more scannable, easier to follow, and less prone to the "pyramid of doom" issue that can happen with multiple levels of nesting.