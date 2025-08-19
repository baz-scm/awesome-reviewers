---
title: Documentation precision standards
description: 'Ensure API documentation uses precise type specifications, proper formatting,
  and clear language to improve developer understanding and usability.


  Key requirements:'
repository: ClickHouse/ClickHouse
label: Documentation
language: C++
comments_count: 4
repository_stars: 42425
---

Ensure API documentation uses precise type specifications, proper formatting, and clear language to improve developer understanding and usability.

Key requirements:
- Use specific generic types instead of generic placeholders (e.g., `Array(T)` instead of `Array`)
- Apply backticks around technical terms, numbers, and variable names for proper formatting (e.g., "`1` to `N`, where `N` is number of capturing groups")
- Remove confusing notation like square brackets in parameter names (use `max_substrings` not `[max_substrings]`)
- Simplify overly complex or confusing descriptions with clear, direct language

Example of improved documentation:
```cpp
FunctionDocumentation::Arguments arguments = {
    {"arr", "The array to concatenate.", {"Array(T)"}},  // Specific type
    {"max_substrings", "Optional. When `max_substrings > 0`...", {"Int64"}}  // Clear naming, backticks for technical terms
};
```

This ensures documentation serves as an effective reference for developers and reduces confusion about parameter types and usage.