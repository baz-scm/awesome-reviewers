---
title: Copy external string inputs
description: When storing string pointers from external sources (like command-line
  arguments), always validate the input and create managed copies to prevent null
  references and lifetime issues. This practice ensures that your stored references
  remain valid throughout your program's execution and prevents potential crashes
  from null or invalid pointers.
repository: JetBrains/kotlin
label: Null Handling
language: C++
comments_count: 2
repository_stars: 50857
---

When storing string pointers from external sources (like command-line arguments), always validate the input and create managed copies to prevent null references and lifetime issues. This practice ensures that your stored references remain valid throughout your program's execution and prevents potential crashes from null or invalid pointers.

Follow these steps when handling external string inputs:
1. Verify the pointer is valid (check boundary conditions)
2. Ensure the string isn't empty when needed
3. Create a copy with reasonable size limits for persistent storage

```cpp
// Unsafe approach:
kotlin::programName = argv[0]; // May cause crashes if argc=0 or lifetime issues later

// Safe approach:
if (argc > 0 && argv[0][0] != '\0') {
  kotlin::programName = strndup(argv[0], 4096); // Creates bounded copy with independent lifetime
}
```

This approach prevents crashes from invalid pointers, protects against potential buffer issues by limiting string length, and eliminates lifetime concerns by managing your own copy of the data.
