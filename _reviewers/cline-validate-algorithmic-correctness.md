---
title: validate algorithmic correctness
description: Always verify algorithms work correctly across edge cases and boundary
  conditions through concrete examples and mathematical validation. Pay special attention
  to preventing infinite recursion and ensuring mathematical formulas produce expected
  results.
repository: cline/cline
label: Algorithms
language: TypeScript
comments_count: 3
repository_stars: 48299
---

Always verify algorithms work correctly across edge cases and boundary conditions through concrete examples and mathematical validation. Pay special attention to preventing infinite recursion and ensuring mathematical formulas produce expected results.

Key practices:
- Test algorithms with minimal input sizes and edge cases
- Use concrete examples to verify mathematical calculations step-by-step
- Implement cycle detection for recursive operations that traverse potentially circular structures
- Validate formulas by working through the math with specific values

Example from message truncation logic:
```typescript
// Incorrect: Can result in zero when it shouldn't
messagesToRemove = Math.floor((messages.length - startOfRest) / 8) * 3 * 2
// With messages.length=5, startOfRest=1: floor(4/8) * 3 * 2 = 0 * 6 = 0

// Correct: Properly calculates 3/4 of remaining pairs  
messagesToRemove = Math.floor(((messages.length - startOfRest) * 3) / 4 / 2) * 2
// With messages.length=5, startOfRest=1: floor((4*3)/4/2) * 2 = floor(1.5) * 2 = 2
```

For recursive operations, implement safeguards:
```typescript
// Prevent infinite recursion with cycle detection
const visitedPaths = new Set<string>()
if (visitedPaths.has(resolvedPath)) {
    continue // Skip already processed paths
}
visitedPaths.add(resolvedPath)
```