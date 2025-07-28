---
title: Use descriptive names
description: Choose names that clearly describe the purpose, behavior, and content
  of functions, variables, and constants. Names should be self-documenting and unambiguous
  to other developers.
repository: llvm/llvm-project
label: Naming Conventions
language: C++
comments_count: 8
repository_stars: 33702
---

Choose names that clearly describe the purpose, behavior, and content of functions, variables, and constants. Names should be self-documenting and unambiguous to other developers.

**Function Names:** Use verbs that accurately describe what the function does. For example, prefer `getOrGenImplicitDefaultDeclareMapper` over `genImplicitDefaultDeclareMapper` when the function both retrieves existing items and generates new ones. Similarly, use `canPassByValue` instead of `isLiteralType` when checking if a variable can be passed by value rather than just checking for literal types.

**Variable Names:** Choose names that clearly indicate the variable's purpose and avoid ambiguity. For example, use `hasMapHdr` and `hasStringHdr` instead of `hasMap` and `hasString` when referring to header files, since the latter are common names that usually don't refer to headers.

**Constants:** Define named constants instead of using magic strings or literals directly in code. Replace inline strings like `"aligned_alloc"` or `"localabstract"` with properly declared constants:

```cpp
// Instead of magic strings
if (callOp.getCallee() != "aligned_alloc")

// Use named constants  
static constexpr char kAlignedAllocFunc[] = "aligned_alloc";
if (callOp.getCallee() != kAlignedAllocFunc)
```

**Misleading Names:** Avoid names that suggest different functionality than what is actually implemented. For instance, don't use `asan_dispatch_apply_f_block` for a function that handles regular function callbacks rather than blocks - prefer `asan_dispatch_apply_f_callback` instead.

This approach makes code more maintainable, reduces the likelihood of errors, and improves code readability for all team members.