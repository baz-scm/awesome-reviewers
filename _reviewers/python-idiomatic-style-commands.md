---
title: Idiomatic Style Commands
description: 'When writing style guidance (including README/CONTRIBUTING snippets),
  keep examples concise and readable:


  1) Use idiomatic tool invocations (avoid redundant arguments)'
repository: TheAlgorithms/Python
label: Code Style
language: Markdown
comments_count: 2
repository_stars: 220912
---

When writing style guidance (including README/CONTRIBUTING snippets), keep examples concise and readable:

1) Use idiomatic tool invocations (avoid redundant arguments)
- Don’t include “current directory” arguments if the tool already defaults to the working directory.
- Prefer the documented, explicit subcommand form when required.

Example:
```bash
# Prefer (defaults to current directory)
ruff check

# Only specify a path when you truly need it
ruff check path/to/package
```

2) Format lists in sentences with consistent punctuation
- Use clear separators and an Oxford comma when listing multiple items (e.g., “filter, and reduce”) to prevent ambiguity.

Example:
```md
List comprehensions and generators are preferred over the use of `lambda`, `map`, `filter`, and `reduce`.
```