---
title: maintain naming consistency
description: Follow established naming patterns and conventions consistently throughout
  the codebase. This includes using consistent formatting (dashes vs underscores),
  proper capitalization, descriptive parameter names, and uniform data type representations.
repository: ggml-org/llama.cpp
label: Naming Conventions
language: C++
comments_count: 8
repository_stars: 83559
---

Follow established naming patterns and conventions consistently throughout the codebase. This includes using consistent formatting (dashes vs underscores), proper capitalization, descriptive parameter names, and uniform data type representations.

Key principles:
- Use consistent separators: prefer dashes over underscores in identifiers like `"falcon-h1"` instead of `"falcon_h1"`
- Follow established capitalization patterns: `"kFLOP"` not `"KFLOP"`
- Use descriptive parameter names: `type` instead of single letters like `T`
- Maintain consistency in data representation: use either byte offsets or element offsets throughout, not both
- Choose clear, semantic names that convey purpose: `send_progress` instead of `include_prompt_progress`

Example of inconsistent naming:
```cpp
// Inconsistent - mixing byte and element offsets
params[1] = src_misalignment;           // byte offset
params[3] = src->nb[0]/ggml_type_size(src->type);  // element offset

// Consistent - all element offsets
params[1] = src_misalignment_elements;
params[3] = src_stride_elements;
```

Before introducing new names, check existing codebase patterns and follow the established conventions. This reduces cognitive load and makes the code more maintainable.