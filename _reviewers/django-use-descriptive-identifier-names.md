---
title: Use descriptive identifier names
description: Choose clear, descriptive names for variables, functions, and classes
  that accurately convey their purpose and follow framework conventions. Avoid abbreviations,
  single-letter names, or generic placeholders that might confuse readers.
repository: django/django
label: Naming Conventions
language: Python
comments_count: 7
repository_stars: 84182
---

Choose clear, descriptive names for variables, functions, and classes that accurately convey their purpose and follow framework conventions. Avoid abbreviations, single-letter names, or generic placeholders that might confuse readers.

Key guidelines:
- Replace abbreviated names with their full form (e.g., 'pagination' instead of 'p')
- Avoid meaningless placeholder names (e.g., 'Foo', 'Bar') in favor of domain-specific terms
- Use semantic naming that reflects the actual behavior
- For class-returning methods, include 'class' suffix in the name

Example:
```python
# Poor naming
def get_pagination(self, request, **kwargs):
    p = self.pagination_cls()
    return p

# Better naming
def get_pagination_class(self, request, **kwargs):
    pagination_instance = self.pagination_class()
    return pagination_instance
```

This approach improves code readability, maintains consistency with framework patterns, and makes the codebase more maintainable.