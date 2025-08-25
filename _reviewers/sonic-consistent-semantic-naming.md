---
title: Consistent semantic naming
description: Maintain consistent naming conventions throughout the codebase and use
  semantically clear identifiers that clearly indicate their purpose and behavior.
  All functions, variables, and other identifiers should follow the same naming style
  (preferably snake_case for C code) and have descriptive names that make their functionality
  obvious.
repository: bytedance/sonic
label: Naming Conventions
language: C
comments_count: 3
repository_stars: 8532
---

Maintain consistent naming conventions throughout the codebase and use semantically clear identifiers that clearly indicate their purpose and behavior. All functions, variables, and other identifiers should follow the same naming style (preferably snake_case for C code) and have descriptive names that make their functionality obvious.

Key principles:
1. **Consistency**: Use the same naming convention across all code. Don't mix camelCase and snake_case within the same project.
2. **Semantic clarity**: Choose names that clearly indicate what the function does and what it returns, avoiding generic terms.
3. **Global application**: Apply naming standards consistently across the entire codebase.

Example improvements:
```c
// Before: Mixed styles and unclear names
bool isSpace(char a);
bool isInteger(char a); 
int charToNum(char c);
bool compare(MapPair lhs, MapPair rhs);

// After: Consistent snake_case and clear semantics
bool is_space(char a);
bool is_integer(char a);
int char_to_num(char c);
bool less_than(MapPair lhs, MapPair rhs);
```

This ensures code readability and maintainability by eliminating confusion about naming patterns and making function purposes immediately clear to other developers.