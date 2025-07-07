---
title: Test edge cases
description: When writing tests, prioritize coverage of edge cases and non-standard
  code patterns to ensure robust functionality. Particularly for linting rules or
  code transformations, identify scenarios that might behave unexpectedly or require
  special handling.
repository: astral-sh/ruff
label: Testing
language: Python
comments_count: 2
repository_stars: 40619
---

When writing tests, prioritize coverage of edge cases and non-standard code patterns to ensure robust functionality. Particularly for linting rules or code transformations, identify scenarios that might behave unexpectedly or require special handling.

Include tests for:
- Code with comments in various positions
- Unusual formatting or line continuations
- Nested object constructions
- Dependencies on multiple variables
- Different parameter passing styles (positional vs. keyword)

For example, when testing a rule that transforms string paths to Path objects:

```python
# Test with comments in different positions
func_name( # comment
    "filename")

func_name( # comment
    "filename",
    #comment
)

# Test with line continuations
func_name \
 \
        ( # comment
        "filename",
    )

# Test with nested objects
func_name(Path("filename").resolve())

# Test with dependencies on other variables
for x, y in some_pairs:
    result.add((x, y))
```

Testing these edge cases early prevents subtle bugs from surfacing in production code and makes your code more maintainable over time.