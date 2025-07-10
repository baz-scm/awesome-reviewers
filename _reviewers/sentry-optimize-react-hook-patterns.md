---
title: Optimize React hook patterns
description: 'Design React hooks with performance and maintainability in mind by following
  these key principles:


  1. Minimize useEffect usage - Update values directly when possible instead of using
  effects. Effects should only be used for true side effects, not for derived state
  updates.'
repository: getsentry/sentry
label: React
language: TSX
comments_count: 4
repository_stars: 41297
---

Design React hooks with performance and maintainability in mind by following these key principles:

1. Minimize useEffect usage - Update values directly when possible instead of using effects. Effects should only be used for true side effects, not for derived state updates.

2. Use the latest ref pattern for hook options to avoid unnecessary re-renders and ensure proper memoization:

```typescript
function useCustomHook(options: Options) {
  const optionsRef = useRef(options);
  useLayoutEffect(() => {
    optionsRef.current = options;
  });
  
  // Access latest options in callbacks
  const handleChange = useCallback(() => {
    const currentOptions = optionsRef.current;
    // ... use currentOptions
  }, []); // No options dependency needed
}
```

3. Prefer useMemo for complex operations over useCallback when dealing with dependencies:

```typescript
// Better approach
const handleSearchChange = useMemo(
  () => debounce((value: string) => {
    // Handle search
  }), 
  []
);

// Clean up on unmount
useEffect(() => {
  return () => handleSearchChange.cancel();
}, []);
```

4. Consider state management alternatives before reaching for useEffect - often state updates can be handled directly in event handlers or through proper component composition.

These patterns help avoid common pitfalls like unnecessary re-renders, stale closures, and complex dependency arrays while maintaining clean, performant React code.