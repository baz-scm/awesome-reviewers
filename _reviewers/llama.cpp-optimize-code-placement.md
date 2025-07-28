---
title: optimize code placement
description: Ensure code is placed in its most logical and efficient location to improve
  maintainability and performance. This includes consolidating duplicate functionality
  into shared headers or utility files, and moving loop-invariant conditions outside
  of loops.
repository: ggml-org/llama.cpp
label: Code Style
language: Objective-C
comments_count: 2
repository_stars: 83559
---

Ensure code is placed in its most logical and efficient location to improve maintainability and performance. This includes consolidating duplicate functionality into shared headers or utility files, and moving loop-invariant conditions outside of loops.

When you encounter duplicate functions across multiple files, consider moving them to a shared header as inline functions. For example, instead of having `ggml_are_same_layout` duplicated in `ggml-alloc.c` and `ggml-backend.cpp`, move it to `ggml.h` as an inline function.

Similarly, extract conditions that don't change within loops to outside the loop:

```c
// Instead of:
for (size_t i = 0, n = 3; i < n; ++i) {
    if (op->src[i] != NULL && (op->src[i]->type == GGML_TYPE_BF16 || op->type == GGML_TYPE_BF16)) {
        // ...
    }
}

// Extract the loop-invariant condition:
bool op_is_bf16 = (op->type == GGML_TYPE_BF16);
for (size_t i = 0, n = 3; i < n; ++i) {
    if (op->src[i] != NULL && (op->src[i]->type == GGML_TYPE_BF16 || op_is_bf16)) {
        // ...
    }
}
```

This approach reduces code duplication, improves performance by avoiding redundant checks, and enhances code readability by making the logic structure clearer.