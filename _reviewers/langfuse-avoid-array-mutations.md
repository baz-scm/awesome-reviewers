---
title: Avoid array mutations
description: Always clone arrays before performing operations that would mutate the
  original array, especially when working with component state or props. Direct mutations
  can cause subtle bugs and unexpected side effects in React applications.
repository: langfuse/langfuse
label: Code Style
language: TSX
comments_count: 5
repository_stars: 13574
---

Always clone arrays before performing operations that would mutate the original array, especially when working with component state or props. Direct mutations can cause subtle bugs and unexpected side effects in React applications.

**Common mutating operations to avoid:**
- Using `sort()`, `reverse()`, or `splice()` directly on state arrays
- Calling `push()`, `pop()`, `shift()` or `unshift()` on existing arrays

**Instead, create a copy first:**
```javascript
// ❌ Avoid: This mutates the original array
messagePlaceholders.sort((a, b) => { ... });

// ✅ Better: Create a copy before sorting
messagePlaceholders.slice().sort((a, b) => { ... });
// or
[...messagePlaceholders].sort((a, b) => { ... });
```

For comparing sorted arrays:
```javascript
// ❌ Avoid: This mutates both arrays during comparison
JSON.stringify(selectedLabels.sort()) !== JSON.stringify(prompt.labels.sort())

// ✅ Better: Create copies before sorting
JSON.stringify([...selectedLabels].sort()) !== JSON.stringify([...prompt.labels].sort())
```

When accessing array elements, prefer direct indexing over chained methods that create unnecessary intermediate arrays:
```javascript
// ❌ Avoid: Creates an intermediate copy unnecessarily
widget.data.dimensions.slice().shift()?.field ?? "none";

// ✅ Better: Direct access is clearer and more efficient
widget.data.dimensions[0]?.field ?? "none";
```