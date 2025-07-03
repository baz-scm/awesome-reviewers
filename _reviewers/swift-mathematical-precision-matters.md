---
title: Mathematical precision matters
description: When implementing mathematical algorithms, ensure precise terminology
  and correct implementation of mathematical concepts. This is especially important
  for complex domains like differentiation, optimization, or numerical methods.
repository: tensorflow/swift
label: Algorithms
language: Markdown
comments_count: 4
repository_stars: 6136
---

When implementing mathematical algorithms, ensure precise terminology and correct implementation of mathematical concepts. This is especially important for complex domains like differentiation, optimization, or numerical methods.

Three key practices to follow:

1. **Use mathematically accurate terminology in documentation**
   Descriptions should precisely match mathematical definitions. For example, when documenting differentiation:

   ```swift
   // INCORRECT:
   // Speaking in terms of elementary calculus, only functions that have derivatives can be differentiated.
   
   // CORRECT:
   // Speaking in terms of elementary calculus, only functions are "differentiable": only functions can *have derivatives* and can *be differentiated*.
   ```

2. **Be explicit about algorithm limitations and edge cases**
   Clearly state when algorithms might fail or have special requirements:

   ```swift
   // GOOD EXPLANATION:
   // Differentiation can fail for several reasons:
   // * The function contains computation that cannot be differentiated
   // * The function is opaque (a function parameter with a non-@differentiable type)
   ```

3. **Ensure mathematical correctness in example code**
   Example implementations must correctly implement the mathematical operations they demonstrate:

   ```swift
   // INCORRECT pullback implementation (missing parameter):
   @differentiating(sillyExp)
   func sillyDerivative(_ x: Float) -> (value: Float, pullback: (Float) -> Float) {
     let y = sillyExp(x)
     return (value: y, pullback: { _ in y }) // Incorrect: ignores parameter
   }
   
   // CORRECT implementation:
   @differentiating(sillyExp)
   func sillyDerivative(_ x: Float) -> (value: Float, pullback: (Float) -> Float) {
     let y = sillyExp(x)
     return (value: y, pullback: { v in v * y }) // Correct: uses parameter
   }
   ```

Following these practices ensures that algorithms are implemented correctly and are properly documented, making them more maintainable and less prone to subtle errors that can emerge when mathematical concepts are imprecisely translated to code.
