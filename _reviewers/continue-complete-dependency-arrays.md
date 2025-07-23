---
title: Complete dependency arrays
description: Always include all referenced variables in React hook dependency arrays
  (useEffect, useCallback, useMemo). Missing or incorrect dependencies can lead to
  stale closures, unexpected behavior, and difficult-to-diagnose bugs.
repository: continuedev/continue
label: React
language: TSX
comments_count: 3
repository_stars: 27819
---

Always include all referenced variables in React hook dependency arrays (useEffect, useCallback, useMemo). Missing or incorrect dependencies can lead to stale closures, unexpected behavior, and difficult-to-diagnose bugs.

When using hooks with dependency arrays:
- Include every variable, state, or prop referenced inside the hook callback
- Add context values that might change over time
- Ensure event listeners are properly cleaned up

```tsx
// ❌ Incorrect: Missing dependency
const handleSubmit = useCallback(() => {
  if (currentState.isValid) {
    submitData(formData);
  }
}, [formData]); // currentState is missing

// ✅ Correct: Complete dependency array
const handleSubmit = useCallback(() => {
  if (currentState.isValid) {
    submitData(formData);
  }
}, [formData, currentState]);

// ✅ Correct: useEffect with event listener cleanup
useEffect(() => {
  // Only add the listener if condition is met
  if (toolCallState?.status === "generated") {
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }
}, [toolCallState, handleKeyDown]);
```

Consider using the ESLint plugin 'eslint-plugin-react-hooks' with the exhaustive-deps rule to automatically detect missing dependencies.