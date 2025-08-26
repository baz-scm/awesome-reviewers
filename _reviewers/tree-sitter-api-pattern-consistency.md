---
title: API pattern consistency
description: When designing new API functions, maintain consistent patterns across
  the codebase and avoid creating precedents that lead to function proliferation or
  inconsistent interfaces. Consider how the design will scale to similar use cases
  and whether it aligns with existing API conventions.
repository: tree-sitter/tree-sitter
label: API
language: Other
comments_count: 3
repository_stars: 21799
---

When designing new API functions, maintain consistent patterns across the codebase and avoid creating precedents that lead to function proliferation or inconsistent interfaces. Consider how the design will scale to similar use cases and whether it aligns with existing API conventions.

For example, instead of adding separate count functions for each data type:
```c
// Avoid this pattern - leads to function proliferation
uint32_t ts_language_supertype_count(const TSLanguage *self);
uint32_t ts_language_field_count(const TSLanguage *self);
uint32_t ts_language_symbol_count(const TSLanguage *self);

// Prefer this pattern - consistent with existing APIs
const TSSymbol *ts_language_supertypes(const TSLanguage *self, uint32_t *length);
```

Similarly, when deciding between separate namespaces versus unified approaches, consider the actual usage patterns and whether the separation provides meaningful benefits to API consumers. Balance API simplicity with practical usage needs, and document the reasoning behind design decisions to maintain consistency in future additions.