---
title: Lifecycle effects management
description: Properly manage component lifecycle effects and cleanup in React components
  to prevent memory leaks and performance issues. Use appropriate dependency arrays
  in useEffect hooks, and ensure cleanup functions are implemented for subscriptions,
  event listeners, and other side effects.
repository: vuejs/core
label: React
language: TypeScript
comments_count: 3
repository_stars: 50769
---

Properly manage component lifecycle effects and cleanup in React components to prevent memory leaks and performance issues. Use appropriate dependency arrays in useEffect hooks, and ensure cleanup functions are implemented for subscriptions, event listeners, and other side effects.

When working with async components or operations:
1. Make sure effects properly handle both resolved and pending states
2. Consider component mounting/unmounting timing when dealing with async operations

```jsx
// Poor implementation
useEffect(() => {
  const subscription = someAPI.subscribe(data => {
    setData(data);
  });
  // Missing cleanup function
}, []); // Missing proper dependencies

// Better implementation
useEffect(() => {
  let isMounted = true;
  const subscription = someAPI.subscribe(data => {
    if (isMounted) {
      setData(data);
    }
  });
  
  return () => {
    isMounted = false;
    subscription.unsubscribe();
  };
}, [someAPI]); // Proper dependencies listed
```

Effects in parent components can impact child component performance. Be mindful of effect hierarchies and consider using more targeted state management approaches when effects cascade across many components.