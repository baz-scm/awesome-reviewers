---
title: Optimize loop operations
description: Avoid repeated computations and object creation in loops or high-frequency
  operations. Move invariant calculations outside the loop and reuse objects rather
  than creating new instances on each iteration. This reduces CPU overhead, memory
  churn, and improves performance in critical code paths.
repository: n8n-io/n8n
label: Performance Optimization
language: TypeScript
comments_count: 5
repository_stars: 122978
---

Avoid repeated computations and object creation in loops or high-frequency operations. Move invariant calculations outside the loop and reuse objects rather than creating new instances on each iteration. This reduces CPU overhead, memory churn, and improves performance in critical code paths.

**Key practices:**
1. Pre-calculate values that don't change between iterations
2. Initialize objects before loops when they can be reused
3. Cache expensive operation results rather than recalculating
4. Avoid unnecessary object creation with spreads or concatenations

**Example - Before:**
```typescript
const searchByName = (query: string, limit: number = 20): NodeSearchResult[] => {
  const normalizedQuery = query.toLowerCase();
  const results: NodeSearchResult[] = [];

  for (const nodeType of this.nodeTypes) {
    // Name is lowercased on every iteration
    if (nodeType.name.toLowerCase().includes(normalizedQuery)) {
      // Score calculation logic...
    }
  }
  // ...
};
```

**After:**
```typescript
// Pre-calculate lowercase names when loading node types
const initNodeTypes = (types) => {
  return types.map(type => ({
    ...type,
    nameLower: type.name.toLowerCase(),
  }));
};

const searchByName = (query: string, limit: number = 20): NodeSearchResult[] => {
  const normalizedQuery = query.toLowerCase();
  const results: NodeSearchResult[] = [];

  for (const nodeType of this.nodeTypes) {
    // Use pre-calculated lowercase name
    if (nodeType.nameLower.includes(normalizedQuery)) {
      // Score calculation logic...
    }
  }
  // ...
};
```