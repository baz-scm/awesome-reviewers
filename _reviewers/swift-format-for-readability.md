---
title: Format for readability
description: 'Code should be formatted to optimize readability. Apply these key practices:


  1. **Maintain reasonable line length** (typically 100 columns) by breaking long
  lines of code. For function declarations with multiple parameters or long statements,
  wrap them across lines with proper indentation:'
repository: tensorflow/swift
label: Code Style
language: Other
comments_count: 3
repository_stars: 6136
---

Code should be formatted to optimize readability. Apply these key practices:

1. **Maintain reasonable line length** (typically 100 columns) by breaking long lines of code. For function declarations with multiple parameters or long statements, wrap them across lines with proper indentation:

```swift
// Instead of:
func getMedianExecutionTime(iterationCount: UInt = 10, _ verbose:Bool = false, _ function: () -> ()) -> Double {

// Use:
func getMedianExecutionTime(
  iterationCount: UInt = 10, _ verbose:Bool = false, _ function: () -> ()
) -> Double {
```

2. **Leverage language syntax conventions** for cleaner code. In Swift, when a closure is the last argument, you can omit the parentheses:

```swift
// Instead of:
array.sorted(by: { s1, s2 in return s1 > s2 })

// You can write:
array.sorted { s1, s2 in return s1 > s2 }
```

3. **Use appropriate formatting for multiline strings**. In Swift, the indentation of multiline strings is aligned with the closing triple quotes, not the indentation in the source code:

```swift
let quotation = """
    This text will have leading whitespace aligned
    with the closing triple quotes.
    """
```

These formatting practices improve code readability, reduce cognitive load, and make the codebase more maintainable.
