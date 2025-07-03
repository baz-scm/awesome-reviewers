---
title: Swift idiomatic naming
description: 'Follow Swift''s naming conventions to write more readable, maintainable
  code. The Swift language emphasizes clarity and expressiveness in naming:


  1. **Avoid `get` prefixes** in function and method names. In Swift, properties and
  zero-argument methods serve this purpose without the prefix.'
repository: tensorflow/swift
label: Naming Conventions
language: Other
comments_count: 3
repository_stars: 6136
---

Follow Swift's naming conventions to write more readable, maintainable code. The Swift language emphasizes clarity and expressiveness in naming:

1. **Avoid `get` prefixes** in function and method names. In Swift, properties and zero-argument methods serve this purpose without the prefix.

   ```swift
   // Avoid:
   func getTimeString(_ nanoseconds: Double) -> String { ... }
   
   // Prefer:
   func timeDescription(_ nanoseconds: Double) -> String { ... }
   ```

2. **Name functions according to their purpose**, not their return type. The return type is already declared in the function signature.

   ```swift
   // Avoid:
   func colorString() -> String { ... }
   
   // Prefer:
   func description() -> String { ... }
   ```

3. **Use Swift's shorthand type notation** for collections rather than the generic form.

   ```swift
   // Avoid:
   var timings: Array<Double> = [0.0]
   
   // Prefer:
   var timings: [Double] = [0.0]
   ```

4. **Leverage abbreviated dot syntax** when the type context is already known.

   ```swift
   var rank: Rank = .queen  // Instead of Rank.queen
   ```

These conventions align with the [Swift API Design Guidelines](https://swift.org/documentation/api-design-guidelines/) and help create a consistent codebase that other Swift developers can easily understand.
