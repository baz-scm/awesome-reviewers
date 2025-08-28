---
title: minimize hot path allocations
description: Reduce memory allocations and garbage collection pressure in frequently
  executed code paths. Object creation through functional methods like `Object.fromEntries()`,
  `map()`, and repeated `toString()` calls can cause significant performance degradation
  in hot paths.
repository: rocicorp/mono
label: Performance Optimization
language: TypeScript
comments_count: 5
repository_stars: 2091
---

Reduce memory allocations and garbage collection pressure in frequently executed code paths. Object creation through functional methods like `Object.fromEntries()`, `map()`, and repeated `toString()` calls can cause significant performance degradation in hot paths.

**Prefer manual object construction over functional approaches:**

```typescript
// ❌ Avoid - creates multiple intermediate objects
return Object.fromEntries(
  keyColumns.map(col => [col, row[col]])
);

// ✅ Better - single allocation
const result = {};
for (const col of keyColumns) {
  result[col] = row[col];
}
return result;
```

**Accumulate strings efficiently:**
```typescript
// ❌ Avoid - repeated toString() calls
l < r && (this.currVal += chunk.subarray(l, r).toString('utf8'));

// ✅ Better - collect segments, join once
segments.push(chunk.subarray(l, r));
// Later: segments.join('')
```

**Prevent unbounded memory growth:**
Monitor data structures that grow indefinitely (like histograms per keystroke) and implement cleanup strategies or size limits. Consider the memory footprint of operations that scale with user input frequency.

**Use lazy evaluation for expensive operations:**
Only create error stacks, stringify large objects, or perform expensive computations when actually needed, especially in debug scenarios or error paths.