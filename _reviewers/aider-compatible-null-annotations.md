---
title: Compatible null annotations
description: 'When annotating optional or nullable types in Python, ensure compatibility
  across all supported Python versions. For codebases supporting Python 3.9:

  '
repository: Aider-AI/aider
label: Null Handling
language: Python
comments_count: 2
repository_stars: 35856
---

When annotating optional or nullable types in Python, ensure compatibility across all supported Python versions. For codebases supporting Python 3.9:

1. Add `from __future__ import annotations` at the top of files using the union type syntax:
   ```python
   from __future__ import annotations
   
   class ExInfo:
       name: str
       retry: bool
       description: str | None
   ```

2. Alternatively, use `typing.Optional[X]` instead of `X | None` syntax:
   ```python
   import typing
   
   class CoderPrompts:
       repo_content_prefix: typing.Optional[str] = """Here are summaries..."""
   ```

This ensures proper null handling with type annotations while maintaining backward compatibility with Python 3.9, preventing runtime errors like `TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'`.