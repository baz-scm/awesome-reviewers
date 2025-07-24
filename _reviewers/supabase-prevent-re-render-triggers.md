---
title: Prevent re-render triggers
description: Avoid creating new object/array references in component render functions
  and carefully manage state updates to prevent unnecessary re-renders. This improves
  performance by reducing computational overhead and DOM manipulations.
repository: supabase/supabase
label: Performance Optimization
language: TSX
comments_count: 3
repository_stars: 86070
---

Avoid creating new object/array references in component render functions and carefully manage state updates to prevent unnecessary re-renders. This improves performance by reducing computational overhead and DOM manipulations.

Key practices include:

1. Move static arrays/objects outside component functions
2. Use lazy initialization for expensive computations in useState
3. Apply useMemo for computed values that depend on specific props/state
4. Access form field values directly instead of using form.watch() when possible

```jsx
// Bad: Creates new references on every render
const Component = () => {
  // New array created every render
  const defaultPrompts = ['Create a table', 'Write a query'];
  
  // Expensive calculation runs on every render
  const [wrapperTables, setWrapperTables] = useState(formatWrapperTables(wrapper, wrapperMeta));
  
  // Watches entire form state for a single value
  const { max_bytes_per_second } = form.watch();
  
  return <ChildComponent prompts={defaultPrompts} />;
}

// Good: Prevents unnecessary re-renders
// Move constants outside component
const DEFAULT_PROMPTS = ['Create a table', 'Write a query'];

const Component = () => {
  // Lazy initialization runs only once
  const [wrapperTables, setWrapperTables] = useState(() => formatWrapperTables(wrapper, wrapperMeta));
  
  // In form field render functions, use the field value directly
  return (
    <FormField_Shadcn_
      control={form.control}
      name="max_bytes_per_second"
      render={({ field }) => {
        const { value, unit } = convertFromBytes(field.value ?? 0);
        // Rest of rendering logic
      }}
    />
  );
}
```