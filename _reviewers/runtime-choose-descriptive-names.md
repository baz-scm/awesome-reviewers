---
title: Choose descriptive names
description: Names should clearly convey purpose and meaning. Parameter, variable,
  and method names should be self-explanatory and accurately reflect their behavior
  and intent. Rename elements when their original name no longer captures their purpose
  or could lead to confusion.
repository: dotnet/runtime
label: Naming Conventions
language: C++
comments_count: 3
repository_stars: 16578
---

Names should clearly convey purpose and meaning. Parameter, variable, and method names should be self-explanatory and accurately reflect their behavior and intent. Rename elements when their original name no longer captures their purpose or could lead to confusion.

For example, if a parameter indicates whether side effects can be ignored:
```cpp
// Less clear
bool IsRedundantMov(instruction ins, format fmt, size_t size, operand dst, operand src, bool canSkip)

// More clear
bool IsRedundantMov(instruction ins, format fmt, size_t size, operand dst, operand src, bool canIgnoreSideEffects)
```

Similarly, ensure that error messages and user-facing text use precise, accurate terminology that reflects current platform realities (like changing "not a managed .dll or .exe" to "not a managed .dll" when managed .exe files aren't relevant in modern .NET).

When variables are used across different scopes (like in lambdas), be especially attentive to naming clarity to avoid ambiguity about which variables are being referenced.
