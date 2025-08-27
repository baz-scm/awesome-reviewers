---
title: Ensure documentation completeness
description: All code elements should have sufficient documentation to understand
  their purpose, usage, and context. This includes adding explanatory comments for
  non-obvious constants, documenting private functions for maintainability, ensuring
  grammatical accuracy in all documentation, and providing necessary context such
  as prerequisites or limitations.
repository: bazelbuild/bazel
label: Documentation
language: Other
comments_count: 4
repository_stars: 24489
---

All code elements should have sufficient documentation to understand their purpose, usage, and context. This includes adding explanatory comments for non-obvious constants, documenting private functions for maintainability, ensuring grammatical accuracy in all documentation, and providing necessary context such as prerequisites or limitations.

Key areas to address:
- Add comments to constants or variables that aren't self-explanatory (e.g., `DWP = "dwp"  // Name of the debug package action`)
- Document private functions with dev-facing comments explaining their purpose
- Review documentation for grammatical accuracy and clarity
- Include relevant context like version requirements, prerequisites, or usage limitations

Example of complete documentation:
```cpp
// Returns the repository name for the current source file.
// Requires C++20 support for __builtin_FILE functionality.
// Use this from within `cc_test` rules.
static std::string CurrentRepository(const std::string& file = __builtin_FILE());
```

This ensures that future developers can understand and maintain the code without needing to reverse-engineer functionality or guess at requirements.