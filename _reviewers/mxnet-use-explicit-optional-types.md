---
title: Use explicit optional types
description: When dealing with values that may be absent or null, always use explicit
  optional type wrappers instead of implicit null checks or nullable types without
  clear type constraints. This makes the code's intent clearer, prevents null reference
  errors, and improves type safety.
repository: apache/mxnet
label: Null Handling
language: Other
comments_count: 3
repository_stars: 20801
---

When dealing with values that may be absent or null, always use explicit optional type wrappers instead of implicit null checks or nullable types without clear type constraints. This makes the code's intent clearer, prevents null reference errors, and improves type safety.

In Perl, use `Maybe[Type]` to clearly indicate a value could be absent:
```perl
has 'sum_metric' => (is => 'rw', isa => 'Maybe[Num|ArrayRef[Num]|PDL]');
```

In C++, use appropriate optional containers like `dmlc::optional<T>` (or `std::optional<T>` in C++17) when a parameter might not have a value:
```cpp
dmlc::optional<bool> shifted_output;  // Clearly indicates this boolean might not be set
```

Be explicit about which values can be null and provide appropriate methods to safely access or transform these values. When working with optional types, ensure consistent handling across the codebase rather than using ad-hoc null checks. This pattern helps catch null-related errors at compile time rather than runtime.
