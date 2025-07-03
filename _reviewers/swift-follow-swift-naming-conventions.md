---
title: Follow Swift naming conventions
description: 'Ensure code follows established Swift naming conventions and remains
  consistent with domain terminology:


  1. Use standard Swift parameter labels (e.g., use `named:` instead of `called:`):'
repository: tensorflow/swift
label: Naming Conventions
language: Swift
comments_count: 3
repository_stars: 6136
---

Ensure code follows established Swift naming conventions and remains consistent with domain terminology:

1. Use standard Swift parameter labels (e.g., use `named:` instead of `called:`):
```swift
// Incorrect
func expectOne<T>(called name: String, among candidates: [T]) throws -> T { ... }

// Correct
func expectOne<T>(named name: String, among candidates: [T]) throws -> T { ... }
```

2. Organize functions as methods on relevant types when appropriate:
```swift
// Less idiomatic
public func operandNames(for inst: Instruction) -> [String]? { ... }

// More idiomatic
extension Instruction {
    public var operandNames: [String]? { ... }
}
```

3. Use domain-specific terminology consistently (e.g., "operand names" not "registers" in SIL context)

4. Avoid redundancy in type names, especially in enum cases:
```swift
// Redundant
public indirect enum Type {
    case addressType(_ type: Type)
}

// Concise
public indirect enum Type {
    case address(Type)
}
```

5. Maintain consistency with existing codebase conventions (e.g., using `inst` instead of `instr` for variables if that's the established pattern)
