---
title: React rendering safeguards
description: 'This standard ensures your React components render correctly and efficiently,
  preventing common pitfalls that cause errors or performance issues.


  ### Proper key usage'
repository: shadcn-ui/ui
label: React
language: TSX
comments_count: 4
repository_stars: 90568
---

This standard ensures your React components render correctly and efficiently, preventing common pitfalls that cause errors or performance issues.

### Proper key usage
Always use stable, unique identifiers as keys when rendering lists:

```jsx
// ❌ Avoid using array index as key when items can reorder
{payload.map((item, index) => (
  <div key={index}>...</div>
))}

// ✅ Use a unique, stable identifier when available
{payload.map((item) => (
  <div key={item.value || `${item.dataKey}-${item.name}`}>...</div>
))}
```

### Hydration safety
When dealing with components that might render differently on server vs. client, implement hydration safety checks:

```jsx
const [isMounted, setMounted] = React.useState(false);

React.useEffect(() => {
  setMounted(true);
  // Additional initialization if needed
}, []);

// Avoid hydration mismatch by not rendering on server
if (!isMounted) {
  return null;
}

return <Component {...props} />;
```

### Context-aware rendering
When conditionally showing UI elements or handling state that depends on browser APIs:
1. Check for document/window availability
2. Use useLayoutEffect for DOM measurements
3. Defer client-side-only logic to useEffect

This prevents hydration errors, improves SSR compatibility, and ensures consistent rendering across environments.