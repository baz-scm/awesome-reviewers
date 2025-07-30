---
title: Use descriptive specific names
description: Choose names that clearly indicate their context and purpose rather than
  generic terms. Generic names can be ambiguous and make code harder to understand,
  especially when the same codebase handles multiple contexts or domains.
repository: Unstructured-IO/unstructured
label: Naming Conventions
language: Markdown
comments_count: 2
repository_stars: 12117
---

Choose names that clearly indicate their context and purpose rather than generic terms. Generic names can be ambiguous and make code harder to understand, especially when the same codebase handles multiple contexts or domains.

When naming variables, parameters, methods, or classes, prefer specific descriptive names that include relevant context over broad generic terms. This makes the code self-documenting and reduces the cognitive load for other developers.

Examples of improvements:
- Use `library` instead of `repo` when referring to a software library specifically
- Use `pdf_hi_res_max_pages` instead of `max_pages` when the parameter specifically limits PDF processing in high-resolution mode
- Use `source` and `destination` (lowercase) instead of capitalized `Source` and `Destination` for common technical terms

The goal is to make names immediately clear about what they represent without requiring additional context or documentation.