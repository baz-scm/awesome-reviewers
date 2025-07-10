---
title: Hook and state correctness
description: 'Ensure React hooks and state updates follow best practices to prevent
  subtle bugs:


  1. **Call hooks unconditionally** at the top level of your component or custom hook
  - never inside conditionals, loops, or nested functions:'
repository: langfuse/langfuse
label: React
language: TSX
comments_count: 6
repository_stars: 13574
---

Ensure React hooks and state updates follow best practices to prevent subtle bugs:

1. **Call hooks unconditionally** at the top level of your component or custom hook - never inside conditionals, loops, or nested functions:

```jsx
// INCORRECT
function Component() {
  const someCondition = true;
  if (someCondition) {
    useEffect(() => {/* effect */}, []);  // Violation of hook rules
  }
  
  const memoizedData = useMemo(() => {
    const { getNavigationPath } = useTracePeekNavigation();  // Hooks inside other hooks
    return { getNavigationPath };
  }, []);
}

// CORRECT
function Component() {
  const { getNavigationPath } = useTracePeekNavigation();
  const memoizedData = useMemo(() => {
    return { getNavigationPath };  // Use hook result inside memo
  }, [getNavigationPath]);
}
```

2. **Include all dependencies** in hook dependency arrays (useEffect, useMemo, useCallback) to avoid stale closures:

```jsx
// INCORRECT - missing 'canEdit' dependency
const handleWidthChange = useCallback(
  (containerWidth) => {
    setEditable(canEdit && cols === 12);  // Uses canEdit but missing from deps
  },
  [cols]
);

// CORRECT
const handleWidthChange = useCallback(
  (containerWidth) => {
    setEditable(canEdit && cols === 12);
  },
  [cols, canEdit]  // All dependencies listed
);
```

3. **Use proper state update patterns** to prevent stale state:

```jsx
// INCORRECT - may use stale state
setOpen((value) => {
  const newValue = typeof value === "function" ? value(open) : value;
  // Using 'open' can be stale
});

// CORRECT - always uses fresh state
setOpen((currentOpen) => {
  const newValue = typeof value === "function" ? value(currentOpen) : value;
  return newValue;
});
```

4. **Use reactive state access methods** for form libraries and other state:

```jsx
// INCORRECT - not reactive
disabled={isInProgress.data || !form.getValues().targetId}

// CORRECT - reacts to field changes
disabled={isInProgress.data || !form.watch('targetId')}
```

Following these patterns helps prevent difficult-to-debug issues like inconsistent renders, stale closures, and unpredictable component behavior.