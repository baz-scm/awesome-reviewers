---
title: Avoid redundant operations
description: Identify and eliminate duplicate computations, unnecessary object creation,
  and redundant function calls to improve performance. This is especially critical
  in memory-sensitive areas and frequently executed code paths.
repository: microsoft/playwright
label: Performance Optimization
language: TypeScript
comments_count: 4
repository_stars: 76113
---

Identify and eliminate duplicate computations, unnecessary object creation, and redundant function calls to improve performance. This is especially critical in memory-sensitive areas and frequently executed code paths.

Key practices:
- Cache expensive computation results instead of recalculating them
- Reuse existing objects/arrays rather than creating new ones when possible  
- Avoid calling the same function multiple times with identical parameters
- Profile code to identify performance bottlenecks from redundant work

Example from codebase:
```typescript
// Before: Redundant calls
const isVisible1 = isElementVisible(element);
const isVisible2 = isElementVisible(element); // Same element, duplicate call

// After: Cache the result
const isVisible = isElementVisible(element);
// Use 'isVisible' variable in both places

// Before: Creating new array
return annotations.map(annotation => ({ ...annotation, location: absolutePath }));

// After: Modify in place when safe
annotations.forEach(annotation => annotation.location = absolutePath);
return annotations;
```

This optimization becomes increasingly important in hot code paths, loops, and memory-constrained environments where even small inefficiencies can compound into significant performance impacts.