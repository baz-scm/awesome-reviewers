---
title: consistent parameter naming
description: Maintain consistent naming and symbol choices throughout code and documentation,
  prioritizing readability and avoiding ambiguity. When choosing between equivalent
  representations (like φ vs phi), select the more widely understood option and use
  it consistently across all related contexts.
repository: prometheus/prometheus
label: Naming Conventions
language: Markdown
comments_count: 2
repository_stars: 59616
---

Maintain consistent naming and symbol choices throughout code and documentation, prioritizing readability and avoiding ambiguity. When choosing between equivalent representations (like φ vs phi), select the more widely understood option and use it consistently across all related contexts.

Special characters or symbols that may not be familiar to all readers should be avoided in favor of their more accessible alternatives. This ensures that parameter names, function signatures, and documentation remain clear and understandable to developers with varying backgrounds.

For example, instead of mixing φ and phi in function documentation:
```
// Inconsistent - confusing for readers
quantile(φ, v)  // in one place
quantile(phi, v)  // in another place

// Consistent - clear for all readers  
quantile(phi, v)  // used everywhere
```

This principle applies to variable names, function parameters, mathematical symbols in documentation, and any identifier that has multiple valid representations.