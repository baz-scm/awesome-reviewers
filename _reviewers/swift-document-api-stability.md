---
title: Document API stability
description: 'When working with AI frameworks and machine learning libraries, clearly
  document the stability state of APIs being used. For experimental or evolving features:'
repository: tensorflow/swift
label: AI
language: Other
comments_count: 3
repository_stars: 6136
---

When working with AI frameworks and machine learning libraries, clearly document the stability state of APIs being used. For experimental or evolving features:

1. Add explicit warnings about API stability in documentation
2. Provide workarounds for unstable features while indicating when they might be resolved
3. Link to official documentation rather than source code when possible

For example, when documenting a feature with known limitations:

```swift
// EXPERIMENTAL: Boolean operators (&&, ||) are not differentiable in v0.11
// Use these alternative functions until the next release:
extension Bool {
    public static func and(_ a: Bool, _ b: Bool) -> Bool {
        if a {
            if b {
                return true
            }
        }
        return false
    }
    
    // Usage: if Bool.and(condition1, condition2) instead of if condition1 && condition2
}

// TODO: Remove when upgrading to Swift release with apple/swift/pull/33511
```

This approach helps users understand current limitations, provides immediate solutions, and establishes clear upgrade paths when the framework evolves.
