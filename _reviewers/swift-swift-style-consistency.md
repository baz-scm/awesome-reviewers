---
title: Swift style consistency
description: 'Maintain consistent Swift style conventions throughout all code, including
  examples in documentation and comments. Follow these specific guidelines:


  1. Use 4-space indentation for all Swift code'
repository: tensorflow/swift
label: Code Style
language: Markdown
comments_count: 2
repository_stars: 6136
---

Maintain consistent Swift style conventions throughout all code, including examples in documentation and comments. Follow these specific guidelines:

1. Use 4-space indentation for all Swift code
2. Do not use spaces before colons in type declarations

For example:

```swift
// Correct
struct Model: Differentiable {
    var parameter: Float
    
    var allDifferentiableVariables: AllDifferentiableVariables {
        get { return AllDifferentiableVariables(parameter: parameter) }
        set { parameter = newValue.parameter }
    }
}

// Incorrect
struct Model : Differentiable { // space before colon
  var parameter: Float  // 2-space indentation
  
  var allDifferentiableVariables: AllDifferentiableVariables {
      get { return AllDifferentiableVariables(parameter: parameter) }
      set { parameter = newValue.parameter }
  }
}
```

When showing code patterns that may be truncated (like in documentation examples), use "..." to maintain symmetry and clarity of the pattern structure.

```swift
// Complete pattern with "..." for consistency
var allDifferentiableVariables: AllDifferentiableVariables {
    get { return AllDifferentiableVariables(x: x, y: y, ...) }
    set { x = newValue.x; y = newValue.y; ... }
}
```
