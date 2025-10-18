---
title: Use semantically meaningful names
description: Choose names that clearly convey purpose and intent rather than generic
  or ambiguous terms. Prefer specific, descriptive terminology that makes code self-documenting
  and reduces cognitive load for readers.
repository: oraios/serena
label: Naming Conventions
language: Python
comments_count: 4
repository_stars: 14465
---

Choose names that clearly convey purpose and intent rather than generic or ambiguous terms. Prefer specific, descriptive terminology that makes code self-documenting and reduces cognitive load for readers.

Key principles:
- Use precise terminology: prefer "excerpt" or "snippet" over "extract", "find" over "get" for search operations
- Choose descriptive parameter names: `file_reader` is more precise than `content_reader` when the function reads entire files
- Import modules for semantic clarity: `charset_normalizer.from_path` is more meaningful than a bare `from_path` import
- Use specific types with semantic meaning: `IntEnum` with named values instead of raw `int` for severity levels

Example improvements:
```python
# Less clear
from charset_normalizer import from_path
def get_extracts(content_reader: Callable[[str], str]):
    severity: int = 1

# More semantically meaningful  
import charset_normalizer
def find_code_snippets(file_reader: Callable[[str], str]):
    severity: DiagnosticSeverity = DiagnosticSeverity.ERROR
    result = charset_normalizer.from_path(path)
```

This approach makes code more maintainable by reducing ambiguity and making the developer's intent explicit through careful name selection.