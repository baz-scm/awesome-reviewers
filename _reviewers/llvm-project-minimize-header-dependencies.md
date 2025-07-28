---
title: minimize header dependencies
description: Organize code to minimize header dependencies and improve compilation
  times. Use forward declarations instead of includes when possible, avoid unnecessary
  dependencies, and follow proper header organization patterns.
repository: llvm/llvm-project
label: Code Style
language: Other
comments_count: 5
repository_stars: 33702
---

Organize code to minimize header dependencies and improve compilation times. Use forward declarations instead of includes when possible, avoid unnecessary dependencies, and follow proper header organization patterns.

Key practices:
- Use forward declarations in headers when you only need to declare pointers or references to a type
- Implementation files (.cpp) should contain the actual includes, while headers (.h) should minimize dependencies
- Avoid including heavy headers when lighter alternatives exist
- Never use `static` declarations in header files as they create separate instances in each translation unit
- Organize includes to separate interface declarations from implementation dependencies

Example:
```cpp
// Good: Use forward declaration in header
// MyClass.h
class WarnUnusedResultAttr; // Forward declaration
class MyClass {
  WarnUnusedResultAttr* attr;
};

// MyClass.cpp - actual include in implementation
#include "clang/AST/Attr.h"

// Bad: Heavy include in header
// MyClass.h  
#include "clang/AST/Attr.h" // Unnecessary dependency
```

This approach reduces compilation times, minimizes rebuild cascades when headers change, and creates cleaner module boundaries.