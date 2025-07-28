---
title: Provide contextual code documentation
description: Code should include documentation that explains the purpose, rationale,
  and context behind implementation decisions, not just what the code does. This helps
  future maintainers understand the reasoning and makes the codebase more maintainable.
repository: llvm/llvm-project
label: Documentation
language: C++
comments_count: 6
repository_stars: 33702
---

Code should include documentation that explains the purpose, rationale, and context behind implementation decisions, not just what the code does. This helps future maintainers understand the reasoning and makes the codebase more maintainable.

Key areas requiring contextual documentation:

1. **Top-level entities**: Document the purpose and role of classes, structs, and major functions
2. **File-level context**: New files should include comments explaining why they were created or split from other files
3. **Complex logic blocks**: When code implements intricate algorithms or generates complex structures, include comments explaining the overall approach
4. **Data structure semantics**: Document the meaning and constraints of data structure elements, especially non-obvious ones
5. **Specification compliance**: When implementing standards or specifications, quote the relevant text verbatim to preserve intent and context
6. **Conditional logic**: Explain the reasoning behind complex conditions, especially when they handle edge cases or specific requirements

Example of good contextual documentation:
```cpp
// SYCL 2020 section 5.10.1, "SYCL functions and member functions linkage":
//   When a function is declared with SYCL_EXTERNAL, that macro must be
//   used on the first declaration of that function in the translation unit.
//   Redeclarations of the function in the same translation unit may
//   optionally use SYCL_EXTERNAL, but this is not required.
if (hasFirstDeclSYCLExternal && !hasSYCLExternal) {
  // Implementation logic...
}
```

Avoid redundant comments that merely restate what the code obviously does. Focus on the "why" rather than the "what".