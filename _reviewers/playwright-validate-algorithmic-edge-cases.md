---
title: validate algorithmic edge cases
description: Algorithms must be thoroughly tested at boundary conditions and edge
  cases to prevent subtle bugs. Pay special attention to off-by-1 errors in mathematical
  calculations, empty collections, and boundary values that might cause unexpected
  behavior.
repository: microsoft/playwright
label: Algorithms
language: TypeScript
comments_count: 4
repository_stars: 76113
---

Algorithms must be thoroughly tested at boundary conditions and edge cases to prevent subtle bugs. Pay special attention to off-by-1 errors in mathematical calculations, empty collections, and boundary values that might cause unexpected behavior.

Common edge cases to validate:
- Mathematical boundaries (e.g., `Math.log10(10)` edge case)
- Empty or single-element collections
- Maximum/minimum values in ranges
- Conditional logic branches with complex state

Example from the codebase:
```javascript
// Problematic - fails for totalTestCount === 10
const indexLength = Math.ceil(Math.log10(this.totalTestCount));

// Correct - handles the edge case properly  
const indexLength = Math.ceil(Math.log10(this.totalTestCount + 1));
```

When implementing algorithms, create test cases that specifically target these boundary conditions. Consider reusing existing, well-tested algorithmic logic rather than reimplementing similar functionality, as proven algorithms are less likely to contain edge case bugs.