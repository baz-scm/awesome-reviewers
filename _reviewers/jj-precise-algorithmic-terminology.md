---
title: precise algorithmic terminology
description: When documenting or describing algorithmic operations, use precise, unambiguous
  terminology that clearly distinguishes between different types of operations. Avoid
  reusing terms that already have specific meanings in the domain, as this can lead
  to confusion about the actual algorithmic behavior.
repository: jj-vcs/jj
label: Algorithms
language: Markdown
comments_count: 2
repository_stars: 21171
---

When documenting or describing algorithmic operations, use precise, unambiguous terminology that clearly distinguishes between different types of operations. Avoid reusing terms that already have specific meanings in the domain, as this can lead to confusion about the actual algorithmic behavior.

For example, when describing set operations and graph traversals:
- Don't describe `x..y` as a "set-difference operator" when there's already a dedicated `~` operator for set difference
- Instead, describe it functionally: "`x..y` is the set of revisions introduced from x to y" (equivalent to `::y ~ ::x`)
- For graph operations like `x::y`, be specific about the traversal: "all commits along all direct paths from x to y"

This precision is especially important when operations involve complex algorithmic concepts like graph traversals, set operations, or range queries, where subtle differences in behavior can significantly impact correctness and performance. Clear terminology helps developers understand the computational complexity and expected behavior of the operations they're using.