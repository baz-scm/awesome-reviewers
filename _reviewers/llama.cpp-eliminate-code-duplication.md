---
title: eliminate code duplication
description: Avoid duplicating code blocks by extracting common functionality into
  reusable functions, using templates for type-generic operations, and moving shared
  utilities to common modules. Code duplication makes maintenance difficult, increases
  the likelihood of bugs, and violates the DRY (Don't Repeat Yourself) principle.
repository: ggml-org/llama.cpp
label: Code Style
language: C++
comments_count: 7
repository_stars: 83559
---

Avoid duplicating code blocks by extracting common functionality into reusable functions, using templates for type-generic operations, and moving shared utilities to common modules. Code duplication makes maintenance difficult, increases the likelihood of bugs, and violates the DRY (Don't Repeat Yourself) principle.

When you find similar code patterns:
1. Extract common logic into helper functions
2. Use templates for type-generic operations instead of copying code for different types
3. Move shared utilities to common modules (like `common.cpp`) for reuse across files
4. Refactor similar functions to share implementation details

Example of extracting a common string utility:
```cpp
// Instead of duplicating string suffix logic:
static bool str_has_suffix(const std::string & str, const std::string & suffix) {
    return str.size() >= suffix.size() && str.compare(str.size() - suffix.size(), str.size(), suffix) == 0;
}

// Move to common.cpp as string_ends_with() for reuse
```

Example of using templates instead of duplication:
```cpp
// Instead of separate functions for different types:
template<typename T>
static void ggml_compute_forward_repeat(const ggml_compute_params * params, ggml_tensor * dst) {
    // Generic implementation
}
```

This approach improves maintainability, reduces bugs, and makes the codebase more consistent and easier to understand.