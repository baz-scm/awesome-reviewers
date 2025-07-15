---
title: Effect hook best practices
description: 'When using React effect hooks, follow these practices to ensure predictable
  behavior and prevent memory leaks:


  1. **Use stable dependency arrays**: Create a reusable constant for empty dependency
  arrays rather than creating a new array on each render.'
repository: mui/material-ui
label: React
language: TypeScript
comments_count: 3
repository_stars: 96063
---

When using React effect hooks, follow these practices to ensure predictable behavior and prevent memory leaks:

1. **Use stable dependency arrays**: Create a reusable constant for empty dependency arrays rather than creating a new array on each render.

```jsx
// ❌ Avoid: Creates a new array reference on each render
useEnhancedEffect(timeout.disposeEffect, []);

// ✅ Better: Use a stable reference
const EMPTY = [] as unknown[];
useEnhancedEffect(timeout.disposeEffect, EMPTY);
```

2. **Choose the appropriate effect type**: Use `useLayoutEffect` for DOM operations that need to be synchronized with painting (like aria-hidden management), and `useEffect` for everything else. Consider using a utility like `useEnhancedEffect` that handles SSR scenarios.

```jsx
// For DOM manipulations that affect visual appearance
React.useLayoutEffect(() => {
  // DOM operations that need to happen before painting
}, [dependency]);

// For side effects that don't require synchronous DOM updates
React.useEffect(() => {
  // Other side effects
}, [dependency]);
```

3. **Always implement cleanup functions**: Ensure that all event listeners, subscriptions, and other resources are properly released in the effect's cleanup function.

```jsx
React.useEffect(() => {
  // Add event listener
  media.addListener(handler);
  handler(media);
  
  // Properly clean up in the return function
  return () => {
    media.removeListener(handler);
  };
}, []);
```

These practices prevent unexpected behavior, memory leaks, and render inconsistencies in your React components.