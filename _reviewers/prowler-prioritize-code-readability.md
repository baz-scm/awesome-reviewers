---
title: Prioritize code readability
description: Write code that optimizes for human readability and understanding. Complex
  expressions, while technically correct, can become difficult to understand and maintain
  over time.
repository: prowler-cloud/prowler
label: Code Style
language: Python
comments_count: 5
repository_stars: 11834
---

Write code that optimizes for human readability and understanding. Complex expressions, while technically correct, can become difficult to understand and maintain over time.

When facing complex logic, prefer explicit, step-by-step approaches over condensed one-liners. This applies particularly to nested expressions, complex conditionals, and list comprehensions.

For example, instead of:

```python
klass = next(
    (c for cond, c in COMPLIANCE_CLASS_MAP.get(provider_type, []) if cond(name)),
    GenericCompliance,
)
```

Consider a more readable approach:

```python
klass = GenericCompliance  # Default value
for condition, cls in COMPLIANCE_CLASS_MAP.get(provider_type, []):
    if condition(name):
        klass = cls
        break
```

Other readability practices to follow:
- Maintain consistent indentation patterns in conditional blocks
- Ensure function names clearly represent their behavior (e.g., `get_` functions should return values, not modify state)
- Use descriptive variable names, even if slightly longer
- Break long statements into multiple lines with clear structure
- Add explanatory comments for non-obvious logic

Remember that code is read many more times than it's written. Optimizing for readability leads to fewer bugs and easier maintenance.