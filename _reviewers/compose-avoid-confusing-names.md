---
title: Avoid confusing names
description: Choose clear, unambiguous names that don't shadow existing identifiers
  or create confusion about their purpose. Avoid variable names that shadow method
  names, class names, or built-in functions, as this makes code harder to understand
  and can suggest incorrect behavior like recursive calls.
repository: docker/compose
label: Naming Conventions
language: Python
comments_count: 2
repository_stars: 35858
---

Choose clear, unambiguous names that don't shadow existing identifiers or create confusion about their purpose. Avoid variable names that shadow method names, class names, or built-in functions, as this makes code harder to understand and can suggest incorrect behavior like recursive calls.

When naming variables, methods, or writing documentation text, prioritize clarity over brevity. If a name could be interpreted multiple ways or conflicts with existing identifiers, choose a more descriptive alternative.

Example of problematic naming:
```python
# Bad: 'build' shadows the method name, suggesting recursion
build = self.client.build if not _exec else exec_build
build_output = build(...)
```

Example of clear naming:
```python
# Good: Clear intent, no shadowing
build_func = self.client.build if not _exec else exec_build
build_output = build_func(...)
```

This principle also applies to documentation and help text - avoid ambiguous product names or terminology that could confuse users about what they're actually using.