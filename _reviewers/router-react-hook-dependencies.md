---
title: React hook dependencies
description: Carefully manage dependencies in React hooks to avoid stale closures
  and ensure correct behavior. When using useCallback, useMemo, or useEffect, include
  all reactive values that the hook depends on in the dependency array, even if it
  affects stability.
repository: TanStack/router
label: React
language: TSX
comments_count: 3
repository_stars: 11590
---

Carefully manage dependencies in React hooks to avoid stale closures and ensure correct behavior. When using useCallback, useMemo, or useEffect, include all reactive values that the hook depends on in the dependency array, even if it affects stability.

Common issues to watch for:
- Stale closures where hooks capture outdated values from their first render
- Trading hook stability for correctness by omitting dependencies
- Complex state management in custom hooks that can lead to race conditions

Example of problematic stale closure:
```tsx
const matchIndex = useMatch({ select: (match) => match.index })

const navigate = React.useCallback((options) => {
  // matchIndex here is stale - captured from first render
  const from = router.state.matches[matchIndex]?.fullPath
  return router.navigate({ from, ...options })
}, [router]) // matchIndex missing from deps

// Better: obtain fresh values inside the callback
const navigate = React.useCallback((options) => {
  const currentMatches = router.state.matches
  const from = currentMatches[currentMatches.length - 1]?.fullPath
  return router.navigate({ from, ...options })
}, [router])
```

For custom hooks with async operations, avoid useState for promises that can become stale in development mode. Instead, create promises only when needed:
```tsx
// Problematic: promise created on every render
const [promise, setPromise] = useState(createPromise)

// Better: create promise only when blocking occurs
const blockerFn = async () => {
  const promise = new Promise((resolve) => {
    setResolver({ proceed: () => resolve(true) })
  })
  return await promise
}
```

Always prioritize correctness over performance optimizations like callback stability.