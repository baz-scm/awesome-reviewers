---
title: prioritize code readability
description: 'Write code that prioritizes clarity and readability over cleverness
  or brevity. This includes several key practices:


  **Extract static functions**: Move functions that don''t depend on component state
  outside the component to reduce complexity and make their static nature clear.'
repository: rocicorp/mono
label: Code Style
language: TSX
comments_count: 7
repository_stars: 2091
---

Write code that prioritizes clarity and readability over cleverness or brevity. This includes several key practices:

**Extract static functions**: Move functions that don't depend on component state outside the component to reduce complexity and make their static nature clear.

```tsx
// Instead of defining inside component:
export function MyComponent() {
  const validateFile = (file: File): string | null => {
    // validation logic
  };
  // ...
}

// Extract to module level:
function validateFile(file: File): string | null {
  // validation logic
}

export function MyComponent() {
  // component logic only
}
```

**Separate concerns**: Extract styles to CSS modules rather than embedding them inline, and separate business logic from presentation logic.

**Prefer simple procedural code**: Choose clear, step-by-step code over complex one-liners or overly clever patterns, even if the latter appears more "elegant."

```tsx
// Prefer this clear approach:
let q = z.query.issue.orderBy(sortField, sortDirection);
if (open !== undefined) {
  q = q.where('open', open);
}
if (creator) {
  q = q.whereExists('creator', q => q.where('login', creator));
}

// Over complex one-liners that are harder to follow
```

**Avoid unnecessary complexity**: Question whether complex patterns or abstractions truly add value, especially when simpler alternatives exist. Save complexity budget for features that genuinely require it.