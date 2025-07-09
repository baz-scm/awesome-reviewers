---
title: Optimize comparison patterns efficiently
description: 'Choose efficient comparison patterns and algorithms based on the data
  type and use case. Key guidelines:


  1. For string pattern matching, prefer glob patterns over regex for simple cases:'
repository: ghostty-org/ghostty
label: Algorithms
language: Other
comments_count: 4
repository_stars: 32864
---

Choose efficient comparison patterns and algorithms based on the data type and use case. Key guidelines:

1. For string pattern matching, prefer glob patterns over regex for simple cases:
```zig
// Inefficient
if [[ "$FEATURES" =~ ssh-env ]]

// Efficient
if [[ "$FEATURES" == *ssh-env* ]]
```

2. For floating-point comparisons, use epsilon-based or range checks:
```zig
// Incorrect
if (opacity == 1.0)

// Correct
const epsilon = 1e-6;
if (@fabs(opacity - 1.0) < epsilon)
```

3. For version/order comparisons, use built-in comparison utilities:
```zig
// Verbose and error-prone
if (version.major > required.major ||
    (version.major == required.major && version.minor > required.minor))

// Cleaner and more efficient
return version.order(required) != .lt;
```

These patterns improve both code reliability and performance by using more appropriate comparison techniques for each data type.