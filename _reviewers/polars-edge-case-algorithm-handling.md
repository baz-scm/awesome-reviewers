---
title: Edge case algorithm handling
description: When implementing algorithms, pay special attention to edge cases, particularly
  empty collections. Define and document how your algorithm behaves in these boundary
  conditions following consistent mathematical or programming conventions.
repository: pola-rs/polars
label: Algorithms
language: Markdown
comments_count: 2
repository_stars: 34296
---

When implementing algorithms, pay special attention to edge cases, particularly empty collections. Define and document how your algorithm behaves in these boundary conditions following consistent mathematical or programming conventions.

Different paradigms handle edge cases differently. For example, when aggregating empty collections:
- Set theory and Python conventions might return a default value (e.g., sum of empty collection = 0)
- SQL conventions might return NULL or None

Example from Polars data processing library:
```python
# Polars follows Python conventions for empty collections
pl.Series([], dtype=pl.Int32).sum()  # Returns 0

# This differs from SQL which would return NULL
# Document these differences when your algorithm implementation 
# might surprise users familiar with other systems
```

Document your chosen approach clearly, especially when it differs from related systems. This improves predictability and prevents unexpected behavior when algorithms operate at boundary conditions. Consider adding explicit tests for edge cases to verify consistent handling across your system.