---
title: Follow hooks rules
description: 'Adhere strictly to React hooks rules and best practices to ensure your
  components behave correctly and predictably. Common issues include:


  1. **Manage dependencies properly**: Always include all dependencies in useEffect/useCallback
  dependency arrays or use useLatest() for values you intentionally exclude to prevent
  stale data issues.'
repository: supabase/supabase
label: React
language: TSX
comments_count: 4
repository_stars: 86070
---

Adhere strictly to React hooks rules and best practices to ensure your components behave correctly and predictably. Common issues include:

1. **Manage dependencies properly**: Always include all dependencies in useEffect/useCallback dependency arrays or use useLatest() for values you intentionally exclude to prevent stale data issues.

```jsx
// INCORRECT: Missing snap.enforceExactCount and error.code in dependencies
useEffect(() => {
  if (isError && snap.enforceExactCount && error.code === 408) {
    // ...
  }
}, [isError]);

// CORRECT: Include all dependencies
useEffect(() => {
  if (isError && snap.enforceExactCount && error.code === 408) {
    // ...
  }
}, [isError, snap.enforceExactCount, error.code]);

// ALTERNATIVE: Use useLatest for values you want to read but not trigger re-runs
const latestSnap = useLatest(snap);
const latestError = useLatest(error);
useEffect(() => {
  if (isError && latestSnap.current.enforceExactCount && latestError.current.code === 408) {
    // ...
  }
}, [isError]);
```

2. **Never conditionally call hooks**: Instead of conditionally calling hooks, use the enabled option or similar patterns.

```jsx
// INCORRECT: Conditionally calling a hook breaks the rules of hooks
const { hasAcceptedConsent } = IS_PLATFORM ? useConsentToast() : { hasAcceptedConsent: true }

// CORRECT: Use a parameter to conditionally enable the hook's behavior
const { hasAcceptedConsent } = useConsentToast({ enabled: IS_PLATFORM })
```

3. **Use useCallback for function props**: When passing function props to memoized components, wrap them in useCallback to preserve memoization.

```jsx
// INCORRECT: Inline function breaks memoization on each render
<MemoizedComponent 
  onResults={(props) => snap.updateMessage({ id: message.id, ...props })}
/>

// CORRECT: Preserve memoization with useCallback
const handleResults = useCallback((props) => {
  snap.updateMessage({ id: message.id, ...props })
}, [message.id, snap])

<MemoizedComponent onResults={handleResults} />
```

4. **Avoid hooks in loops**: Never use hooks inside loops, conditions, or nested functions. Extract them to custom hooks if needed.

Remember that hook calls must be at the top level of your component to ensure they're called in the same order on each render.