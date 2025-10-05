---
title: memoize for render optimization
description: Use React memoization techniques strategically to prevent unnecessary
  re-renders and recomputations when values change infrequently. Apply React.memo
  to components that receive stable props, and useMemo for expensive computations
  that depend on rarely-changing values.
repository: TanStack/router
label: Performance Optimization
language: TSX
comments_count: 2
repository_stars: 11590
---

Use React memoization techniques strategically to prevent unnecessary re-renders and recomputations when values change infrequently. Apply React.memo to components that receive stable props, and useMemo for expensive computations that depend on rarely-changing values.

Removing memoization can significantly degrade performance by causing excessive re-renders. Conversely, adding memoization to frequently recomputed values that remain stable can provide substantial performance benefits.

Example of proper memoization:
```tsx
// Memoize component to prevent unnecessary re-renders
export const MatchInner = React.memo(function MatchInnerImpl({
  matchId,
}: { matchId: string }) {
  // Memoize expensive computation when dependencies are stable
  const Comp = useMemo(() => 
    route.options.component ?? router.options.defaultComponent,
    [route.options.component, router.options.defaultComponent]
  )
  
  return <Comp />
})
```

Focus memoization efforts on components and computations where the cost of re-execution outweighs the overhead of memoization checks.