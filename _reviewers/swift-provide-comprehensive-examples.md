---
title: Provide comprehensive examples
description: API documentation should include complete examples that demonstrate all
  key usage patterns. When documenting related functions (like differentiation APIs),
  provide examples for each variant to show their relationships and differences. Include
  examples that showcase both basic usage and advanced patterns.
repository: tensorflow/swift
label: Documentation
language: Markdown
comments_count: 3
repository_stars: 6136
---

API documentation should include complete examples that demonstrate all key usage patterns. When documenting related functions (like differentiation APIs), provide examples for each variant to show their relationships and differences. Include examples that showcase both basic usage and advanced patterns.

For example, when documenting differentiation APIs:

```swift
// Basic usage example
let x: Float = 3.0
print(gradient(at: x, in: square)) // 6.0

// More comprehensive examples showing related functions
// Show value with gradient
print(valueWithGradient(at: x, in: square)) // (value: 9.0, gradient: 6.0)

// Show pullback functionality
let (result, pullback) = valueWithPullback(at: x, in: square)
print(pullback(1.0)) // 6.0

// Show higher-arity function example
let multiArgFunc: @differentiable (Float, Float) -> Float = { x, y in x * y }
print(gradient(at: 2.0, 3.0, in: multiArgFunc)) // (3.0, 2.0)
```

Comprehensive examples help users understand the full capabilities of your API and how different functions relate to each other, which is essential for complex systems like automatic differentiation. When documenting complex APIs or concepts, ensure your examples cover different use cases that readers might encounter in real-world scenarios.
