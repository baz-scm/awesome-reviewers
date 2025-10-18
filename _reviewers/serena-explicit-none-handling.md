---
title: explicit None handling
description: When operations cannot complete successfully or return meaningful results,
  explicitly return None rather than raising exceptions or using placeholder values.
  Document when None is expected and ensure consistent None handling throughout the
  codebase.
repository: oraios/serena
label: Null Handling
language: Python
comments_count: 4
repository_stars: 14465
---

When operations cannot complete successfully or return meaningful results, explicitly return None rather than raising exceptions or using placeholder values. Document when None is expected and ensure consistent None handling throughout the codebase.

Prefer explicit None returns when:
- A path cannot be converted to a relative path (cross-drive scenarios)
- Required data is missing or invalid (symbols without names/ranges)
- Operations fail in expected ways that callers should handle

Always document when None is possible and what it represents:

```python
def get_relative_path(self) -> str | None:
    """
    Get the relative path of the file containing the symbol.
    
    :return: the relative path, or None if the symbol is defined 
             outside of the project's scope
    """
    return self.symbol.location.relative_path

# Better than using defaults or exceptions
def find_executable() -> str | None:
    """Find the executable path, or None if not found."""
    path = shutil.which("executable")
    return path  # Returns None if not found, caller handles it

# Consistent None handling throughout
if relative_path is None:
    # Handle the None case appropriately
    continue  # or return, or use fallback logic
```

This approach makes error conditions explicit, prevents silent failures, and allows callers to make informed decisions about how to handle missing or invalid data.