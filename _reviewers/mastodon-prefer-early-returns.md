---
title: prefer early returns
description: Use early returns and guard clauses to reduce nested conditionals and
  improve code readability. This pattern makes the main logic flow clearer by handling
  edge cases upfront and avoiding deeply nested if-else structures.
repository: mastodon/mastodon
label: Code Style
language: TSX
comments_count: 4
repository_stars: 48691
---

Use early returns and guard clauses to reduce nested conditionals and improve code readability. This pattern makes the main logic flow clearer by handling edge cases upfront and avoiding deeply nested if-else structures.

Instead of complex nested conditions:
```typescript
const handleClick = (e: MouseEvent) => {
  const target = (e.target as HTMLElement).closest('a');
  
  if (e.button !== 0 || e.ctrlKey || e.metaKey) {
    return;
  }
  
  if (isHashtagLink(target)) {
    // main logic here with multiple nested conditions
    if (condition1) {
      if (condition2) {
        // deeply nested logic
      }
    }
  }
};
```

Prefer early returns to flatten the structure:
```typescript
const handleClick = (e: MouseEvent) => {
  const target = (e.target as HTMLElement).closest('a');
  
  if (e.button !== 0 || e.ctrlKey || e.metaKey) {
    return;
  }
  
  if (!isHashtagLink(target)) {
    return;
  }
  
  if (!condition1) {
    return;
  }
  
  if (!condition2) {
    return;
  }
  
  // main logic here at the top level
};
```

This approach also applies to component logic where complex conditional rendering can be simplified by handling edge cases early and returning null or alternative components before the main render logic.