---
title: avoid unnecessary custom hooks
description: Before creating custom hooks, evaluate whether existing solutions or
  simpler patterns can address the need. Custom hooks should provide clear value beyond
  what's available through established libraries, built-in React patterns, or direct
  component logic.
repository: cline/cline
label: React
language: TypeScript
comments_count: 2
repository_stars: 48299
---

Before creating custom hooks, evaluate whether existing solutions or simpler patterns can address the need. Custom hooks should provide clear value beyond what's available through established libraries, built-in React patterns, or direct component logic.

Ask these questions when reviewing custom hook implementations:
1. Does this hook abstract meaningful logic or just wrap existing functionality?
2. Are there established libraries (like react-use) that already provide this functionality?
3. Would direct usage of existing hooks or patterns be clearer?

For example, instead of creating a custom `useClickOutside` hook, leverage existing solutions:

```typescript
// Avoid: Custom implementation
export function useClickOutside<T extends HTMLElement = HTMLElement>(
  ref: RefObject<T>,
  callback: () => void
) {
  // Custom click outside logic...
}

// Prefer: Existing library solution
import { useClickAway } from 'react-use';

// Use directly in component
useClickAway(ref, callback);
```

Custom hooks are valuable for encapsulating complex stateful logic, but avoid creating them when they merely wrap existing functionality without adding meaningful abstraction or reusability.