---
title: Maintain consistent naming
description: 'Ensure naming conventions are consistent across your codebase and related
  repositories. When naming commands, functions, variables, or attributes:


  1. Check existing conventions in the current and related codebases'
repository: open-telemetry/opentelemetry-python
label: Naming Conventions
language: Markdown
comments_count: 3
repository_stars: 2061
---

Ensure naming conventions are consistent across your codebase and related repositories. When naming commands, functions, variables, or attributes:

1. Check existing conventions in the current and related codebases
2. Use the same terminology for similar concepts (e.g., use "typecheck" instead of tool-specific names like "pyright" if that's the established convention)
3. Distinguish clearly between different types of identifiers in documentation (e.g., variable names like `PROCESS_COMMAND_ARGS` vs. attribute names like `process.command_args`)
4. Choose precise, descriptive terms that accurately reflect the entity's purpose (e.g., prefer "bound metric instrument" over the less specific "metric handle")

Example:
```
# Inconsistent naming (mixing conventions)
tox -e pyright  # in this repo
tox -e typecheck  # in related repo

# Consistent naming (following established conventions)
tox -e typecheck  # in both repos
```

This guideline improves code readability, reduces cognitive load when working across multiple repositories, and helps ensure documentation accurately represents code elements.