---
title: React interface clarity
description: Ensure React interfaces have descriptive names and accurate documentation
  that clearly communicate their purpose and usage. Interface names should be specific
  to their context (e.g., `StdoutContextProps` instead of `StdoutProps` for Context-related
  interfaces), and API documentation should accurately reflect how methods are called
  (e.g., distinguishing...
repository: vadimdemedes/ink
label: React
language: TypeScript
comments_count: 2
repository_stars: 31825
---

Ensure React interfaces have descriptive names and accurate documentation that clearly communicate their purpose and usage. Interface names should be specific to their context (e.g., `StdoutContextProps` instead of `StdoutProps` for Context-related interfaces), and API documentation should accurately reflect how methods are called (e.g., distinguishing between instance methods and callback functions returned from hooks).

Example of good naming:
```typescript
// Good: Context-specific naming
export interface StdoutContextProps {
  // ...
}

// Good: Clear hook documentation
/**
 * Assign an ID to this component, so it can be programmatically focused with `focus(id)`.
 * Note: `focus` is a callback returned from `useFocus`, not an instance method.
 */
```

This practice helps developers quickly understand the purpose and correct usage of React components, hooks, and Context APIs, reducing confusion and implementation errors.