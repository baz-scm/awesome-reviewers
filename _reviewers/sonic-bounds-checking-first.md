---
title: bounds checking first
description: Always validate array and buffer bounds before accessing elements to
  prevent out-of-bounds access and potential security vulnerabilities. This is critical
  in algorithms that iterate through data structures or perform string operations.
repository: bytedance/sonic
label: Algorithms
language: C
comments_count: 2
repository_stars: 8532
---

Always validate array and buffer bounds before accessing elements to prevent out-of-bounds access and potential security vulnerabilities. This is critical in algorithms that iterate through data structures or perform string operations.

The pattern should be: check bounds first, then access content. Never assume data is within bounds without explicit validation.

Example of incorrect approach:
```c
// Dangerous - no bounds check
while(is_space(pos[i])) {
    i++;
}
```

Example of correct approach:
```c
// Safe - bounds check before content check  
while(!is_overflow(i, srclen) && is_space(pos[i])) {
    i++;
}
```

In string comparison algorithms, ensure you don't continue comparing beyond the shorter string's length. When the compared portions are equal, the longer string should be considered greater without accessing potentially invalid memory locations.

This principle applies to all array-based algorithms including parsing, sorting, searching, and string manipulation operations.