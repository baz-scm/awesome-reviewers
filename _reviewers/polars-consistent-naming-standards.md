---
title: Consistent naming standards
description: 'Maintain consistent and standardized naming throughout the codebase:


  1. **Use snake_case for multi-word identifiers**: Separate words in variable names,
  function names, and parameters with underscores.'
repository: pola-rs/polars
label: Naming Conventions
language: Python
comments_count: 3
repository_stars: 34296
---

Maintain consistent and standardized naming throughout the codebase:

1. **Use snake_case for multi-word identifiers**: Separate words in variable names, function names, and parameters with underscores.

2. **Be consistent with identifier names**: Use the same name for a concept throughout function signatures, implementations, and documentation.

3. **Choose descriptive, semantic names**: Select names that clearly reflect the purpose and context of the identifier. More specific names improve code clarity and maintainability.

Example:
```python
# Incorrect
def filter(self, predicate: Expr, *, use_abspath: bool = False) -> Series:
    """
    Filter elements by expr
    """
    # implementation using expr

# Correct
def filter(self, predicate: Expr, *, use_abs_path: bool = False) -> Series:
    """
    Filter elements by predicate
    """
    # implementation using predicate
    
# More descriptive naming
MaintainOrderJoin: TypeAlias = Literal["none", "left", "right", "left_right", "right_left"]
```

Consistent naming reduces cognitive load, improves code readability, and helps prevent bugs that could arise from naming confusion.