---
title: Document code rationale
description: 'Add clear comments that explain the "why" behind non-obvious code decisions,
  complex logic, or special-case handling. This is especially important when:'
repository: pydantic/pydantic
label: Documentation
language: Python
comments_count: 7
repository_stars: 24377
---

Add clear comments that explain the "why" behind non-obvious code decisions, complex logic, or special-case handling. This is especially important when:

- Implementing conditional logic that isn't self-explanatory
- Creating helper functions with non-obvious purposes
- Working with complex subsystems like type handling or schema generation
- Adding warnings or deprecation notices
- Overriding methods with potential side effects

Good documentation reduces cognitive load for future readers, prevents accidental breakage during refactoring, and provides context when switching between specialized domains.

For example, instead of:
```python
def _add_unique_postfix(name: str):
    """Used to prevent namespace collision."""
    # implementation
```

Write:
```python
def _add_unique_postfix(name: str):
    """Used to prevent namespace collision when resolving forward references.
    
    This is necessary because we might encounter the same named reference in 
    different modules, and without unique postfixes, references from different
    contexts could be incorrectly resolved to the same object.
    """
    # implementation
```

Similarly, when implementing complex operations like schema cleaning or discriminator handling, include explanations with basic examples that help readers understand the underlying principles and reasons behind the implementation approach.