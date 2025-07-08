---
title: Purpose-revealing identifier names
description: 'Choose identifier names that clearly reveal their purpose and behavior.
  Names should be specific, descriptive, and self-explanatory:


  - **Function names** should include verbs that indicate the action being performed
  or a question being answered (e.g., use `is_consistent()` rather than `consistency()`)'
repository: pytorch/pytorch
label: Naming Conventions
language: Python
comments_count: 3
repository_stars: 91345
---

Choose identifier names that clearly reveal their purpose and behavior. Names should be specific, descriptive, and self-explanatory:

- **Function names** should include verbs that indicate the action being performed or a question being answered (e.g., use `is_consistent()` rather than `consistency()`)
- **Class names** should reflect the nature and purpose of the class (e.g., `VersionString` is better than generic `VersionParser`)
- **Method and variable names** should be descriptive enough that comments aren't needed to explain their purpose

Avoid vague or overly generic names that don't communicate their specific role. When reviewing code, ask "Does this name clearly explain what it does or represents?"

Example:
```python
# Less clear:
def contains_ungroupable(node):
    # Implementation...

# More clear:
def contains_gemm_like(node):
    # Implementation...
```

This naming approach reduces cognitive load for readers and makes code more maintainable over time by making its purpose immediately evident.