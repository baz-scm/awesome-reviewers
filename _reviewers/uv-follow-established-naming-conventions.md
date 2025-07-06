---
title: Follow established naming conventions
description: Adhere to established naming conventions for files, variables, functions,
  and configuration options to maintain consistency and clarity throughout the codebase
  and documentation.
repository: astral-sh/uv
label: Naming Conventions
language: Markdown
comments_count: 3
repository_stars: 60322
---

Adhere to established naming conventions for files, variables, functions, and configuration options to maintain consistency and clarity throughout the codebase and documentation.

- Use standardized capitalization for common files (`README.md` instead of `Readme.md`, `LICENSE` without file extension)
- Maintain consistency when referring to environment variables (use either `$HOME` or `~` throughout, don't mix styles)
- Avoid using special name patterns (like dunders `__name__`) for regular functions to prevent confusion
- Choose names that clearly communicate purpose and scope

```python
# Incorrect: Using dunder name for regular function
def __main__():
    process_data()

# Correct: Use standard naming for regular functions
def main():
    process_data()
```

In documentation, maintain consistent reference style:
```
# Inconsistent
- `$XDG_CACHE_HOME/uv` or `~/.cache/uv` on Unix systems

# Consistent
- `$XDG_CACHE_HOME/uv` or `$HOME/.cache/uv` on Unix systems
```