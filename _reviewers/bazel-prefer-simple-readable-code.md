---
title: prefer simple readable code
description: Favor simple, readable implementations over complex or overly abstracted
  solutions. This includes eliminating code duplication through better function design,
  simplifying complex expressions, and using standard library functions instead of
  custom helpers.
repository: bazelbuild/bazel
label: Code Style
language: Other
comments_count: 7
repository_stars: 24489
---

Favor simple, readable implementations over complex or overly abstracted solutions. This includes eliminating code duplication through better function design, simplifying complex expressions, and using standard library functions instead of custom helpers.

Key practices:
- **Eliminate duplication**: Instead of duplicating long function calls, use loops or extend existing functions with additional parameters
- **Simplify expressions**: Break down complex regex, conditionals, or string manipulations into more readable forms
- **Use standard libraries**: Prefer established library functions (like `paths.basename` or `AsciiStrToUpper`) over custom helper functions
- **Question complexity**: Ask whether complex class hierarchies or abstractions are truly necessary

Example of simplification:
```starlark
# Instead of duplicating calls:
if generate_no_pic_action:
  _create_helper(..., use_pic=False)
if generate_pic_action:
  _create_helper(..., use_pic=True)

# Use a loop:
use_pic_values = []
if generate_no_pic_action:
  use_pic_values.append(False)
if generate_pic_action:
  use_pic_values.append(True)
for use_pic in use_pic_values:
  _create_helper(..., use_pic=use_pic)
```

This approach reduces maintenance burden, improves readability, and makes code easier to understand for future developers.