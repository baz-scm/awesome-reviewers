---
title: Strict mode-proof hooks
description: 'Ensure your React components work correctly in both development (Strict
  Mode) and production environments by writing hooks that handle React''s intentional
  double-rendering behavior. When using side effects in initializers, guard them with
  refs to prevent duplicate executions:'
repository: mui/material-ui
label: React
language: JavaScript
comments_count: 4
repository_stars: 96063
---

Ensure your React components work correctly in both development (Strict Mode) and production environments by writing hooks that handle React's intentional double-rendering behavior. When using side effects in initializers, guard them with refs to prevent duplicate executions:

```jsx
// Bad: Side effect in initializer without guard
const [{ finalValue, assignedIndex }] = React.useState(() => {
  // This runs twice in development with Strict Mode
  registerTab(value); // Could register the same tab twice!
  return { finalValue: value || childIndex++, assignedIndex: childIndex };
});

// Good: Guard side effects with a ref
const hasRegisteredRef = React.useRef(false);

const [{ finalValue, assignedIndex }] = React.useState(() => {
  if (!hasRegisteredRef.current) {
    hasRegisteredRef.current = true;
    // Only runs once even in Strict Mode
    registerTab(value);
  }
  return { finalValue: value || childIndex, assignedIndex: childIndex };
});
```

For expensive calculations, use `useMemo` to prevent unnecessary recalculation during re-renders:

```jsx
// Before: No memoization
return getThemeProps({ theme, name, props });

// After: With memoization
return React.useMemo(() => getThemeProps({ theme, name, props }), [theme, name, props]);
```

Remember that React's Strict Mode intentionally calls initializers and effects twice to detect impure logic. Treat props as immutable to enable further compiler optimizations. When designing components that must work with SSR, ensure your initialization logic doesn't cause hydration mismatches by consistently handling state across server and client renders.