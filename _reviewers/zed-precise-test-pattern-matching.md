---
title: Precise test pattern matching
description: When identifying test patterns in code, use specific equality predicates
  (`#eq?`) instead of list inclusion predicates (`#any-of?`) when matching against
  a single value. This improves clarity and can avoid potential false positives in
  test detection.
repository: zed-industries/zed
label: Testing
language: Other
comments_count: 2
repository_stars: 62119
---

When identifying test patterns in code, use specific equality predicates (`#eq?`) instead of list inclusion predicates (`#any-of?`) when matching against a single value. This improves clarity and can avoid potential false positives in test detection.

For example, when matching the "each" method for parameterized tests:

```javascript
// Prefer this:
(#eq? @_property "each")

// Instead of this when there's only one value:
(#any-of? @_property "each")
```

This practice ensures more precise test pattern recognition, especially important for parameterized tests where accurate detection affects test execution and reporting.