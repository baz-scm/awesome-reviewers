---
title: exact assertion testing
description: Tests should verify exact expected results rather than generic existence
  checks. Avoid assertions like `isinstance()`, `len() > 0`, `is not None`, or `any()`
  that only confirm something exists without validating correctness. Instead, assert
  for specific expected values, names, and properties.
repository: oraios/serena
label: Testing
language: Python
comments_count: 5
repository_stars: 14465
---

Tests should verify exact expected results rather than generic existence checks. Avoid assertions like `isinstance()`, `len() > 0`, `is not None`, or `any()` that only confirm something exists without validating correctness. Instead, assert for specific expected values, names, and properties.

Generic assertions are too weak and don't catch real functionality issues:

```python
# Weak - only checks existence
assert len(references) > 0
assert isinstance(symbols, list)
assert symbol is not None

# Strong - checks exact expected results  
assert "greet" in symbol_names
assert references[0]["uri"].endswith("Main.scala")
assert symbol["name"] == "add"
assert symbol["kind"] == 12  # Function kind
```

This approach catches actual bugs in symbol detection, cross-file references, and language server functionality that generic checks miss. Focus on testing the specific symbols, files, and properties your code is supposed to find or produce. When testing language server functionality, verify that expected function names, type names, and file paths are present in results rather than just confirming non-empty responses.