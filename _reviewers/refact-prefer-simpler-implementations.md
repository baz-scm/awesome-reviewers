---
title: prefer simpler implementations
description: When writing code, favor simpler, more straightforward implementations
  over complex ones. Look for opportunities to consolidate logic paths, reduce unnecessary
  branching, and reuse existing resources instead of recreating them.
repository: smallcloudai/refact
label: Code Style
language: Rust
comments_count: 2
repository_stars: 3114
---

When writing code, favor simpler, more straightforward implementations over complex ones. Look for opportunities to consolidate logic paths, reduce unnecessary branching, and reuse existing resources instead of recreating them.

This approach improves code readability, reduces maintenance burden, and often leads to better performance. Before implementing complex conditional logic or loading operations, consider if there's a simpler way to achieve the same result.

Examples of simplification:
- Instead of multiple conditional branches for similar operations, use a unified approach that handles all cases
- Reuse existing data structures (like `self.tools`) rather than reloading or recreating them
- Consolidate similar logic paths into a single, more general implementation

The goal is to write code that is easier to understand, test, and maintain while achieving the same functionality.