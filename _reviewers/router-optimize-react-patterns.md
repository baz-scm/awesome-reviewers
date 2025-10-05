---
title: Optimize React patterns
description: Prefer derived values over state and use appropriate React hooks for
  better performance and cleaner code. When a value can be computed from existing
  state, props, or context, derive it instead of storing it in separate state. This
  reduces unnecessary re-renders and simplifies state management.
repository: TanStack/router
label: React
language: TypeScript
comments_count: 2
repository_stars: 11590
---

Prefer derived values over state and use appropriate React hooks for better performance and cleaner code. When a value can be computed from existing state, props, or context, derive it instead of storing it in separate state. This reduces unnecessary re-renders and simplifies state management.

For derived values, compute them directly in the component body or use useMemo for expensive calculations. When working with refs, prefer useImperativeHandle over useEffect for ref forwarding as it's more semantically correct and can be optimized with proper dependency arrays.

Example of converting state to derived value:
```typescript
// Before: Storing derived value in state
const [activeLocation, setActiveLocation] = useState<ParsedLocation>(
  location ?? state.location,
)

// After: Computing derived value
const activeLocation = location ?? state.location
```

Example of proper ref handling:
```typescript
// Before: Using useEffect for ref forwarding
React.useEffect(() => {
  if (!ref) return
  if (typeof ref === 'function') {
    ref(innerRef.current)
  } else {
    ref.current = innerRef.current
  }
})

// After: Using useImperativeHandle
React.useImperativeHandle(ref, () => innerRef.current!, [])
```