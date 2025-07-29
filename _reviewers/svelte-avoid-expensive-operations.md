---
title: avoid expensive operations
description: Identify and eliminate computationally expensive operations through early
  termination, better data structures, and algorithmic optimizations. Look for opportunities
  to short-circuit loops, cache results, and choose more efficient algorithms.
repository: sveltejs/svelte
label: Algorithms
language: JavaScript
comments_count: 5
repository_stars: 83580
---

Identify and eliminate computationally expensive operations through early termination, better data structures, and algorithmic optimizations. Look for opportunities to short-circuit loops, cache results, and choose more efficient algorithms.

Key strategies:
- **Early termination**: Stop processing when the desired condition is already met
- **Efficient data structures**: Use Sets instead of arrays for membership testing to reduce O(n²) to O(n)
- **Minimize traversals**: Avoid expensive tree walking or DOM traversal operations when possible
- **Optimize bit operations**: Use combined bit checks for better performance

Example of early termination:
```js
// Before: continues checking even after condition is met
for (const item of items) {
  if (checkCondition(item)) {
    hasCondition = true;
  }
  // continues processing...
}

// After: stops as soon as condition is found
for (const item of items) {
  if (checkCondition(item)) {
    hasCondition = true;
    break; // early termination
  }
}
```

Example of better data structure choice:
```js
// Before: O(n²) complexity with array includes
const needsVersionIncrease = !s.reactions?.every(r => version.reactions?.includes(r));

// After: O(n) complexity with Set
const vReactions = version.reactions === null ? null : new Set(version.reactions);
const needsVersionIncrease = vReactions === null || !s.reactions?.every(r => vReactions.has(r));
```