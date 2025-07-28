---
title: prevent unnecessary operations
description: Identify and eliminate redundant computations, network requests, and
  re-renders in React components to improve performance. Common patterns include memoizing
  functions that recreate on every render, debouncing user input to reduce API calls,
  and conditionally triggering side effects only when necessary.
repository: cline/cline
label: Performance Optimization
language: TSX
comments_count: 3
repository_stars: 48299
---

Identify and eliminate redundant computations, network requests, and re-renders in React components to improve performance. Common patterns include memoizing functions that recreate on every render, debouncing user input to reduce API calls, and conditionally triggering side effects only when necessary.

Use `useCallback` for functions passed as props or used in dependency arrays:
```typescript
const renderSegment = useCallback((segment: DisplaySegment): JSX.Element => {
  // render logic
}, [dependencies])
```

Implement debouncing for user input to prevent excessive state updates:
```typescript
const [localValue, setLocalValue] = useDebouncedInput(initialValue, onChange)
```

Separate side effects to trigger only when specific conditions change:
```typescript
// Instead of combining multiple concerns in one useEffect
useEffect(() => {
  if (isVisible) {
    vscode.postMessage({ type: "fetchLatestMcpServersFromHub" })
  }
}, [isVisible]) // Only fetch when visibility changes, not on dimension changes
```

Before implementing expensive operations, ask: "Is this computation/request/re-render actually necessary?" and "Can I reduce the frequency or scope of this operation?"