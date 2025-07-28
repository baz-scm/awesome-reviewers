---
title: Eliminate unnecessary complexity
description: Remove unnecessary default parameters and consolidate related conditional
  logic to improve code clarity and maintainability. When parameters are always provided
  in practice, avoid adding default values that create false optionality. Similarly,
  combine related conditions into single, more readable expressions.
repository: apache/spark
label: Code Style
language: Python
comments_count: 2
repository_stars: 41554
---

Remove unnecessary default parameters and consolidate related conditional logic to improve code clarity and maintainability. When parameters are always provided in practice, avoid adding default values that create false optionality. Similarly, combine related conditions into single, more readable expressions.

Examples of improvements:
- Remove default parameters that are never used: Change `def run(spec_path: Path, full_refresh: Optional[Sequence[str]] = None)` to `def run(spec_path: Path, full_refresh: Optional[Sequence[str]])` when the parameter is always provided
- Consolidate related conditions: Replace separate `if full_refresh:` and `if refresh:` checks with `if full_refresh or refresh:` when they serve the same logical purpose

This approach reduces cognitive load for readers and eliminates misleading code patterns that suggest optional behavior when none exists.