---
title: Break lines for readability
description: 'Format code with semantic line breaks that enhance readability rather
  than adhering strictly to character limits. When breaking long lines:


  1. Break at natural semantic boundaries'
repository: django/django
label: Code Style
language: Python
comments_count: 3
repository_stars: 84182
---

Format code with semantic line breaks that enhance readability rather than adhering strictly to character limits. When breaking long lines:

1. Break at natural semantic boundaries
2. Place spaces at the start of continuation lines to show they are continuations
3. Aim to have one logical component per line
4. Use the full available width when it improves readability

Example:
```python
# Less readable - breaking arbitrarily at limit
message = (f"{func_name}() takes at most {max_positional_args} positional"
          f" argument(s) (including {num_remappable_args} deprecated) but"
          f" {num_positional_args} were given.")

# More readable - semantic breaks with clear continuations
message = (
    f"{func_name}() takes at most {max_positional_args} "
    f"positional argument(s) (including {num_remappable_args} "
    f"deprecated) but {num_positional_args} were given."
)
```

This approach makes code easier to read and maintain while still respecting line length guidelines. The goal is to use line breaks to highlight the logical structure of the code rather than breaking lines mechanically at a specific column.