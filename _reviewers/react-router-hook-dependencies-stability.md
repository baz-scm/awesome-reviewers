---
title: Hook dependencies stability
description: 'Ensure hook dependencies are minimal, stable, and follow React''s rules
  to prevent unnecessary re-renders and maintain predictable behavior. This includes:'
repository: remix-run/react-router
label: React
language: TSX
comments_count: 6
repository_stars: 55270
---

Ensure hook dependencies are minimal, stable, and follow React's rules to prevent unnecessary re-renders and maintain predictable behavior. This includes:

1. **Remove unnecessary dependencies**: Only include dependencies that actually change the hook's behavior. For example, remove `state.revalidation` from dependency arrays when the function doesn't need to recreate on state changes.

2. **Avoid writing to refs during render**: Never write to `ref.current` inside `useMemo` or during component render, as this violates React's rules and can cause unpredictable behavior with transitions.

3. **Use stable references**: Ensure objects passed as dependencies maintain stable identity to prevent cascading re-renders.

4. **Proper useEffect cleanup**: Don't return promises from `useEffect` and ensure dependency arrays include all referenced values.

Example of problematic code:
```javascript
// Bad - writes to ref during render in useMemo
const searchParams = useMemo(() => {
  searchParamsRef.current = getSearchParamsForLocation(location.search);
  return searchParamsRef.current;
}, [location.search]);

// Bad - unstable state object in dependencies
useEffect(() => {
  navigate(to, { replace, state, relative });
}, [navigate, to, replace, state, relative]); // state might be unstable
```

Example of improved code:
```javascript
// Good - use useEffect to update ref
useEffect(() => {
  searchParamsRef.current = getSearchParamsForLocation(location.search);
}, [location.search]);

// Good - resolve path outside effect for stability
const path = resolveTo(to, matches, locationPathname, relative);
const jsonPath = JSON.stringify(path);
useEffect(() => {
  navigate(JSON.parse(jsonPath), { replace, state, relative });
}, [navigate, jsonPath, relative, replace, state]);
```

This approach ensures components re-render only when necessary and maintains predictable behavior across React's concurrent features.