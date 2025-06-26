---
title: "Complete hook dependencies"
description: "Always specify complete dependency arrays in React hooks to prevent bugs from stale closures and avoid unnecessary rerenders. When using hooks like useEffect, useMemo, or useCallback, include all values from the component scope that are referenced inside the hook's callback function."
repository: "facebook/react"
label: "React"
language: "JavaScript"
comments_count: 3
repository_stars: 237000
---

Always specify complete dependency arrays in React hooks to prevent bugs from stale closures and avoid unnecessary rerenders. When using hooks like `useEffect`, `useMemo`, or `useCallback`, include all values from the component scope that are referenced inside the hook's callback function.

For custom hooks that wrap React's built-in hooks:
1. Pass through dependency arrays correctly rather than hardcoding them
2. Avoid type assertions (like `as any`) that bypass dependency checking
3. Remember that global variables and constants defined outside the component don't need to be dependencies

```javascript
// ❌ Incorrect: Missing dependencies
function Component({foo, bar}) {
  useEffect(() => {
    console.log(foo, bar);
  }, []); // Missing foo and bar

  // ❌ Incorrect: Bypassing dependency checks
  useCustomCallback(callback, [] as any);
}

// ✅ Correct: All dependencies included
function Component({foo, bar}) {
  const nonreactive = 0; // Local constant
  
  useEffect(() => {
    console.log(foo, bar, nonreactive);
  }, [foo, bar]); // nonreactive is a constant, doesn't need to be a dependency
  
  // ✅ Correct: Properly passing dependencies through
  useCustomCallback(callback, [callback]);
}
```

ESLint's exhaustive-deps rule can help identify missing dependencies automatically, preventing subtle bugs caused by stale closures.