---
title: Ensure comprehensive documentation
description: 'Documentation should be complete, properly formatted, and clearly explain
  purpose with adequate examples. When writing documentation, ensure that:


  1. **Code examples are properly formatted** - Match indentation requirements and
  follow established formatting conventions'
repository: llvm/llvm-project
label: Documentation
language: Other
comments_count: 2
repository_stars: 33702
---

Documentation should be complete, properly formatted, and clearly explain purpose with adequate examples. When writing documentation, ensure that:

1. **Code examples are properly formatted** - Match indentation requirements and follow established formatting conventions
2. **Examples are comprehensive** - Include examples that illustrate all requirements, constraints, and edge cases, not just the happy path
3. **Functions and concepts are clearly explained** - Provide explanatory comments for functions with unclear or ambiguous names, especially when terminology has specific technical meanings

For example, when documenting an attribute with requirements:

```cpp
// Good: Comprehensive examples showing both valid and invalid usage
[[clang::sycl_external]] void Foo(); // Ok.

[[clang::sycl_external]] void Bar() { /* ... */ } // Ok.

[[clang::sycl_external]] extern void Baz(); // Ok.

[[clang::sycl_external]] static void Quux() { /* ... */ } // error: Quux() has internal linkage.
```

Similarly, when adding functions with potentially ambiguous names, include comments explaining their purpose:

```cpp
// Generates a concise string representation of a NamedDecl for diagnostic purposes
SmallString<128> toTerseString(const NamedDecl &D) const;
```

This approach prevents confusion and ensures documentation serves as an effective reference for both current and future developers.