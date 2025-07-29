---
title: Use descriptive names
description: Choose variable, function, and parameter names that clearly communicate
  their purpose and avoid confusion. Names should be descriptive enough that their
  intent is obvious without requiring additional context or comments.
repository: vlang/v
label: Naming Conventions
language: Other
comments_count: 15
repository_stars: 36582
---

Choose variable, function, and parameter names that clearly communicate their purpose and avoid confusion. Names should be descriptive enough that their intent is obvious without requiring additional context or comments.

Key principles:
- Use specific, meaningful names over generic ones (e.g., `file_content` instead of `file` when it contains file contents)
- Avoid confusing parameter pairs like `file` and `path` that could mean the same thing
- Function names should accurately reflect their behavior and return types
- Prefer longer, descriptive names over abbreviated ones that save only a few characters
- Use semantic English names in code, avoiding local language terms

Examples of improvements:
```v
// Poor: confusing parameter names
fn string_reproduces(file string, pattern string, command string, path string) bool

// Better: clear, distinct parameter names  
fn string_reproduces(file_content string, pattern string, command string, file_path string) bool

// Poor: abbreviated, unclear method name
fn (mut c DiffContext[T]) gen_str() string

// Better: descriptive method name
fn (mut c DiffContext[T]) generate_patch() string

// Poor: misleading function name vs return type
fn (mut g Gen) get_enum_type_idx_from_fn_name(fn_name string) (string, ast.Type)

// Better: name matches return type
fn (mut g Gen) get_enum_type_from_fn_name(fn_name string) (string, ast.Type)
```

This approach reduces cognitive load for code readers and makes the codebase more maintainable by eliminating ambiguity about what variables and functions represent.