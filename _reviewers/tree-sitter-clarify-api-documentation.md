---
title: Clarify API documentation
description: API documentation should provide clear, unambiguous explanations of function
  behavior, return values, and edge cases. Avoid vague or obscure wording that leaves
  developers guessing about implementation details.
repository: tree-sitter/tree-sitter
label: Documentation
language: Other
comments_count: 2
repository_stars: 21799
---

API documentation should provide clear, unambiguous explanations of function behavior, return values, and edge cases. Avoid vague or obscure wording that leaves developers guessing about implementation details.

For return values, explicitly state the conditions that lead to each possible return value rather than using generic phrases. For complex or non-obvious functionality, include practical examples that demonstrate real-world usage scenarios.

Example of unclear documentation:
```c
/**
 * Set the range of bytes or (row, column) positions in which the query
 * will be executed.
 *
 * If the provided range was set, return `true`. Otherwise, return `false`.
 */
```

Improved version:
```c
/**
 * Set the range of bytes or (row, column) positions in which the query
 * will be executed.
 *
 * This will return false if the start byte/point is greater than the end 
 * byte/point, otherwise it will return true.
 */
```

For obscure functions, add examples showing practical use cases:
```c
/**
 * Get a child of 'from_parent' which is a parent to the given node.
 * The parent may be indirect.
 *
 * Example: This can be used to efficiently find a path from a root node
 * to traverse up the syntax tree within a specific subtree.
 */
```

Clear documentation benefits both immediate development and automated tooling like language bindings generation.