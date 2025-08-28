---
title: avoid unnecessary computations
description: Optimize algorithms by eliminating redundant work and intermediate data
  structures. Look for opportunities to use lazy evaluation, conditional execution,
  and more efficient operations.
repository: rocicorp/mono
label: Algorithms
language: TypeScript
comments_count: 5
repository_stars: 2091
---

Optimize algorithms by eliminating redundant work and intermediate data structures. Look for opportunities to use lazy evaluation, conditional execution, and more efficient operations.

Key strategies:
- Use lazy evaluation to defer expensive operations until actually needed
- Avoid creating intermediate arrays or objects when direct operations are possible
- Apply conditional logic to skip unnecessary function calls or computations
- Choose more efficient built-in operations when available

Examples:
```typescript
// Instead of always creating intermediate arrays:
const materialized = [...stream()].map(materializeNodeRelationships);

// Use imperative style to avoid extra allocations:
const materialized: Node[] = [];
for (const n of stream()) {
  materialized.push(materializeNodeRelationships(n));
}

// Conditional predicate application:
const matchesConstraintAndFilters = predicate
  ? (row: Row) => matchesConstraint(row) && predicate(row)
  : matchesConstraint; // Avoid wrapping when unnecessary

// Use efficient built-ins:
yield* sorted.slice(0, k); // Instead of manual loop
```

This approach improves performance by reducing computational overhead, memory allocations, and unnecessary operations while maintaining code correctness.