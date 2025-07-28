---
title: consistent algorithm interfaces
description: When designing interfaces for filtering, traversal, or search algorithms,
  research existing codebase patterns to maintain consistency in terminology and boolean
  logic. Before introducing new parameter names like "skip", "filter", "match", or
  "predicate", analyze which terms are already established in similar contexts.
repository: neovim/neovim
label: Algorithms
language: Txt
comments_count: 3
repository_stars: 91433
---

When designing interfaces for filtering, traversal, or search algorithms, research existing codebase patterns to maintain consistency in terminology and boolean logic. Before introducing new parameter names like "skip", "filter", "match", or "predicate", analyze which terms are already established in similar contexts.

Ensure clear documentation of predicate behavior, explicitly stating the expected return values and their effects:

```lua
-- Good: Clear documentation with explicit boolean logic
• {filter}? (`fun(dir: string): boolean`) Predicate that
  decides if a directory is traversed. Return true to traverse
  a directory, or false to skip.

-- Avoid: Ambiguous or inconsistent terminology
• {skip}? (`fun(dir: string): boolean`) Do not traverse
```

This consistency reduces cognitive load for developers and prevents confusion about whether predicates use positive logic (return true to include) or negative logic (return true to exclude). Research shows that "match" and "filter" are the most common patterns in established codebases, making them safer choices for new algorithm interfaces.