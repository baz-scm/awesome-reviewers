---
title: systematic test coverage
description: When writing tests that need to cover multiple scenarios (different data
  types, backend capabilities, etc.), structure them systematically rather than duplicating
  code or hardcoding conditional logic.
repository: ggml-org/llama.cpp
label: Testing
language: C++
comments_count: 3
repository_stars: 83559
---

When writing tests that need to cover multiple scenarios (different data types, backend capabilities, etc.), structure them systematically rather than duplicating code or hardcoding conditional logic.

For multiple data types, use loops through type arrays instead of duplicating test cases:

```cpp
// Instead of duplicating test cases for each type
test_cases.emplace_back(new test_conv_2d(..., GGML_TYPE_F32, ...));
test_cases.emplace_back(new test_conv_2d(..., GGML_TYPE_F16, ...));

// Use a loop through types
for (ggml_type type : {GGML_TYPE_F32, GGML_TYPE_F16}) {
    test_cases.emplace_back(new test_conv_2d(..., type, ...));
}
```

For backend-specific capabilities, let the backend report what it supports rather than hardcoding conditional test logic. This allows tests to automatically skip unsupported operations and remain maintainable as backend capabilities evolve.

This approach ensures comprehensive test coverage while keeping the test code clean, maintainable, and adaptable to different environments and configurations.