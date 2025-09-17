---
title: Improve code modularity
description: Organize code into well-structured, reusable components by extracting
  specific functionality into separate functions, using flexible parameter patterns,
  and consolidating duplicate logic. This improves readability, maintainability, and
  extensibility.
repository: microsoft/markitdown
label: Code Style
language: Python
comments_count: 3
repository_stars: 76602
---

Organize code into well-structured, reusable components by extracting specific functionality into separate functions, using flexible parameter patterns, and consolidating duplicate logic. This improves readability, maintainability, and extensibility.

Key practices:
1. **Extract validation logic**: When you have complex validation checks, create dedicated validation functions rather than embedding them inline
2. **Use parameter forwarding**: When passing parameters to nested functions, consider using `**kwargs` to create a flexible foundation for future extensions
3. **Consolidate duplicate functionality**: When similar logic appears in multiple places, refactor it into a shared, reusable function

Example of good modularity:
```python
# Instead of inline validation
def process_file(file_path):
    if not file_path.exists():
        _exit_with_error(f"File does not exist: {file_path}")
    if not file_path.is_file():
        _exit_with_error(f"Path is not a file: {file_path}")
    # ... processing logic

# Extract validation into separate function
def _validate_file_path(file_path):
    if not file_path.exists():
        _exit_with_error(f"File does not exist: {file_path}")
    if not file_path.is_file():
        _exit_with_error(f"Path is not a file: {file_path}")

def process_file(file_path):
    _validate_file_path(file_path)
    # ... processing logic

# Use parameter forwarding for flexibility
def create_converter(**kwargs):
    return CustomConverter(**kwargs)  # Instead of passing individual params
```