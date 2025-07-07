---
title: Clear and relevant comments
description: 'Ensure all comments in the codebase provide value and clarity rather
  than creating confusion. Remove comments that are:


  1. Not applicable to the current framework (e.g., linter directives for tools you''re
  not using)'
repository: astral-sh/ruff
label: Code Style
language: Python
comments_count: 2
repository_stars: 40619
---

Ensure all comments in the codebase provide value and clarity rather than creating confusion. Remove comments that are:

1. Not applicable to the current framework (e.g., linter directives for tools you're not using)
2. Potentially misleading about code behavior or intent
3. Redundant or no longer relevant to the surrounding code

In test files, be particularly cautious with comments that could be misinterpreted about what's being tested. For example, avoid trailing comments that might suggest a different behavior than what the test is actually checking.

Example of problematic comments:
```python
# pylint: disable=unused-import  # Not helpful if not using pylint
foo.__dict__.get("not__annotations__")  # RUF061  # Misleading - suggests this should trigger a warning
```

Example of improved approach:
```python
# Cases that should NOT trigger the violation
foo.__dict__.get("not__annotations__")
```

Regularly review and clean up comments when code changes make them obsolete. Comments should enhance understanding, not create confusion.