---
title: Comments versus docstrings usage
description: Choose between comments and docstrings based on the documentation's purpose
  and scope. Use docstrings for API-level documentation of functions, classes, and
  methods, writing verbs as commands (e.g., "Return" not "Returns"). Use inline comments
  sparingly for implementation details that aren't appropriate for the public API
  documentation.
repository: django/django
label: Documentation
language: Python
comments_count: 5
repository_stars: 84182
---

Choose between comments and docstrings based on the documentation's purpose and scope. Use docstrings for API-level documentation of functions, classes, and methods, writing verbs as commands (e.g., "Return" not "Returns"). Use inline comments sparingly for implementation details that aren't appropriate for the public API documentation.

Avoid redundant documentation:
- Don't duplicate test names in docstrings when the name is sufficiently descriptive
- Avoid "what" comments that merely restate the code
- Don't use comments for information that belongs in docstrings

Example:
```python
# Bad - redundant docstring duplicating test name
def test_user_authentication_success(self):
    """Test that user authentication succeeds with valid credentials."""
    ...

# Bad - "what" comment that restates code
# Calculate the total price
total = price + tax

# Good - docstring with command verb
def get_user_by_email(email):
    """Return a user instance based on email address."""
    ...

# Good - implementation detail comment
def complex_calculation(x, y):
    # Adjust for floating point precision issues
    result = round((x / y) * 100, 2)
    return result
```