---
title: Document design decisions
description: When making architectural choices or modifying existing APIs, document
  your reasoning directly in the code or in type definitions. This helps other developers
  understand the "why" behind changes and prevents future regressions.
repository: mui/material-ui
label: Documentation
language: TSX
comments_count: 2
repository_stars: 96063
---

When making architectural choices or modifying existing APIs, document your reasoning directly in the code or in type definitions. This helps other developers understand the "why" behind changes and prevents future regressions.

For API changes:
```typescript
// Document parameter changes in type definitions, even for internal components
interface GetTabbableProps {
  // Added third parameter to support focusing the first element
  container: HTMLElement;
  firstFocus: boolean;
  forceFirst?: boolean;
}
```

For architectural decisions:
```typescript
// MuiMeta.tsx
// This component is separated from layout components to:
// 1. Minimize changes to core files
// 2. Isolate metadata logic for easier maintenance
// 3. Allow users to update metadata without modifying root structures
import theme from "./theme";

export default function MuiMeta() {
  // Metadata implementation
}
```

By documenting the reasoning behind your decisions, you make the codebase more maintainable and help other developers understand your design choices, reducing questions during code review and simplifying future updates.