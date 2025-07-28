---
title: Avoid unnecessary allocations
description: Minimize memory allocations by avoiding intermediate objects, sharing
  underlying buffers, and eliminating unnecessary array operations. This is particularly
  important in hot code paths and when processing large datasets.
repository: prisma/prisma
label: Performance Optimization
language: TypeScript
comments_count: 5
repository_stars: 42967
---

Minimize memory allocations by avoiding intermediate objects, sharing underlying buffers, and eliminating unnecessary array operations. This is particularly important in hot code paths and when processing large datasets.

Key strategies:
- Share underlying buffers instead of copying data: `Buffer.from(arg.buffer, arg.byteOffset, arg.byteLength)` instead of `Buffer.from(arg)`
- Avoid creating intermediate arrays when chaining operations: inline map operations rather than creating separate arrays
- Construct objects directly when possible: `new Uint8Array(value)` instead of `new Uint8Array(Buffer.from(value).buffer)`
- Move expensive computations out of frequently called functions to constructors or initialization phases
- Only store data structures when the intermediate results are actually needed

Example of optimization:
```typescript
// Before: Creates unnecessary intermediate array
const results: Value[] = []
for (const arg of node.args) {
  results.push(await this.interpretNode(arg, queryable, scope, generators))
}
return results[results.length - 1]

// After: Only compute what's needed
let lastResult: Value
for (const arg of node.args) {
  lastResult = await this.interpretNode(arg, queryable, scope, generators)
}
return lastResult
```