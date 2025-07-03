---
title: Maintain code consistency
description: 'Keep code clean and consistent with established project conventions.
  This includes:


  1. Follow existing formatting style in files:

  ```cpp

  // Follow Allman style if file uses it'
repository: opencv/opencv
label: Code Style
language: Other
comments_count: 5
repository_stars: 82865
---

Keep code clean and consistent with established project conventions. This includes:

1. Follow existing formatting style in files:
```cpp
// Follow Allman style if file uses it
void function()
{
    if (condition)
    {
        statement;
    }
}
```

2. Avoid `using namespace` declarations as they pollute the namespace, even if the header is not included directly.

3. Remove dead/commented-out code or guard it with macros if needed for future use:
```cpp
// Instead of leaving commented code blocks
// for (int i1 = 0; i1 < STEP_SIZE; ++i1) {
//     if (ptr + i1 < n1) {
//         matOut[ptr + i1] = matA[ptr1 + i1] + matB[ptr2 + i1];
//     }
// }

// Use feature macros if code might be needed later
#ifdef EXPERIMENTAL_FEATURE
for (int i1 = 0; i1 < STEP_SIZE; ++i1) {
    if (ptr + i1 < n1) {
        matOut[ptr + i1] = matA[ptr1 + i1] + matB[ptr2 + i1];
    }
}
#endif
```

4. Prefer C++ templates over complex multi-line macros for better debugging and type safety.

5. Use standard type names rather than shortcuts (e.g., `unsigned char` instead of `uchar`).

Consistency in code style significantly improves readability and maintainability while reducing review friction.
