---
title: Clear technical writing
description: Ensure technical documentation uses clear, grammatically correct language
  with consistent formatting when explaining naming conventions and code structure.
  This includes proper capitalization, precise word choice, consistent code formatting
  with backticks, and clear sentence structure.
repository: vlang/v
label: Naming Conventions
language: Markdown
comments_count: 7
repository_stars: 36582
---

Ensure technical documentation uses clear, grammatically correct language with consistent formatting when explaining naming conventions and code structure. This includes proper capitalization, precise word choice, consistent code formatting with backticks, and clear sentence structure.

Key practices:
- Use proper grammar and sentence structure ("the first line will be" not "first line will be")
- Apply consistent formatting for code elements (use backticks around `module names`)
- Choose precise terminology ("such as a function or const" not "such function or variable")
- Maintain consistent spacing and punctuation
- Capitalize appropriately ("Modules names" not "modules names")

Example of good technical writing:
```
Modules names in .v files must match the name of their directory.

A .v file `./abc/source.v` must start with `module abc`. All .v files in this directory belong to the same module `abc`. They should also start with `module abc`.
```

Clear technical writing helps developers understand naming conventions and reduces confusion when implementing code structure requirements.