---
title: Optimize hot paths
description: Identify and optimize frequently executed code paths by moving invariant
  calculations and conditional logic outside of loops, recursive functions, and other
  performance-critical sections. This reduces repeated evaluations and improves algorithm
  efficiency.
repository: grafana/grafana
label: Algorithms
language: TypeScript
comments_count: 3
repository_stars: 68825
---

Identify and optimize frequently executed code paths by moving invariant calculations and conditional logic outside of loops, recursive functions, and other performance-critical sections. This reduces repeated evaluations and improves algorithm efficiency.

For example, instead of this:
```typescript
if (query.sort) {
  const collator = new Intl.Collator();
  filtered = filtered.sort((a, b) => {
    if (query.sort === 'alpha-asc') {
      return collator.compare(a.title, b.title);
    }
    if (query.sort === 'alpha-desc') {
      return collator.compare(b.title, a.title);
    }
  });
}
```

Prefer this:
```typescript
if (query.sort) {
  const collator = new Intl.Collator();
  const mult = query.sort === 'alpha-desc' ? -1 : 1;
  filtered = filtered.sort((a, b) => mult * collator.compare(a.title, b.title));
}
```

This principle applies broadly to:
- Move constant value calculations outside loops
- Pre-calculate branching decisions before entering recursive functions
- Avoid repeated condition checks in graph traversal algorithms
- Identify invariant parts of complex computations that can be lifted out of hot code paths

When optimizing recursive algorithms, also ensure you have proper termination conditions to prevent infinite recursion, particularly when dealing with self-referential data structures.