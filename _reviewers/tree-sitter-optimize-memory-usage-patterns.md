---
title: optimize memory usage patterns
description: Focus on reducing memory footprint and improving cache efficiency through
  careful data structure design and function parameter optimization. Consider using
  smaller data types when the value range permits, and design function interfaces
  to minimize memory overhead.
repository: tree-sitter/tree-sitter
label: Performance Optimization
language: C
comments_count: 2
repository_stars: 21799
---

Focus on reducing memory footprint and improving cache efficiency through careful data structure design and function parameter optimization. Consider using smaller data types when the value range permits, and design function interfaces to minimize memory overhead.

Key strategies include:
- Use appropriately sized data types (e.g., `uint8_t` instead of `int` when values fit in 8 bits)
- Design function parameters to reduce buffer copying and improve access patterns
- Be mindful of allocation frequency, especially in frequently called code paths

Example: Instead of using `Array(TSQuantifier)` which may use 4 bytes per element, consider `Array(uint8_t)` and cast to `TSQuantifier` when reading, reducing memory usage by 75% when the enum values fit in a byte. Similarly, prefer passing buffer parameters directly rather than relying on global transfer buffers to improve function interface efficiency.