---
title: Avoid render cycle allocations
description: Creating new objects, arrays, or functions inside a component's render
  cycle causes unnecessary allocations on every render, which can degrade performance,
  especially in frequently-rendered components.
repository: mui/material-ui
label: Performance Optimization
language: JavaScript
comments_count: 4
repository_stars: 96063
---

Creating new objects, arrays, or functions inside a component's render cycle causes unnecessary allocations on every render, which can degrade performance, especially in frequently-rendered components.

For non-derived values that don't depend on props or state:
- Extract object/function declarations to module scope outside components
- Use `useRef` or custom hooks like `useLazyRef` for mutable references
- Prefer `styled` over inline `sx` props for static styling

```jsx
// Inefficient: New allocations on every render
function Component() {
  const valueToIndex = new Map(); // ❌ Creates new Map each render
  const handleClick = () => {...}; // ❌ Creates new function each render
  return <Box sx={{ color: 'red' }}>...</Box>; // ❌ Creates new object each render
}

// Optimized: Stable references and static optimizations
const createMap = () => new Map(); // ✅ Defined once in module scope
const StyledBox = styled(Box)({ color: 'red' }); // ✅ Styled component

function Component() {
  const valueToIndex = useLazyRef(createMap).current; // ✅ Stable reference
  const handleClick = useCallback(() => {...}, []); // ✅ Memoized function
  return <StyledBox>...</StyledBox>; // ✅ No new style object created
}
```

For values derived from props or state, use appropriate memoization with `useMemo` and `useCallback` with correct dependency arrays.

Additionally, when working with DOM updates, prefer direct manipulation of CSS variables over context-driven updates when it provides a performance benefit.