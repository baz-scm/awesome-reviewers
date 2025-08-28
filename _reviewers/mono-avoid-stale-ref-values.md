---
title: avoid stale ref values
description: When using React refs in hooks like useLayoutEffect or useEffect, pass
  the ref object itself rather than ref.current to avoid stale values. The ref.current
  value captured at hook definition time may be outdated when the effect callback
  executes.
repository: rocicorp/mono
label: React
language: TypeScript
comments_count: 2
repository_stars: 2091
---

When using React refs in hooks like useLayoutEffect or useEffect, pass the ref object itself rather than ref.current to avoid stale values. The ref.current value captured at hook definition time may be outdated when the effect callback executes.

Example of the problem:
```typescript
// ❌ Problematic - elm will be stale
export function useElementSize(elm: HTMLElement | null) {
  useLayoutEffect(() => {
    // elm here is the stale value from when hook was defined
    if (elm) {
      // This may operate on wrong/null element
    }
  }, [elm]);
}
```

Correct approach:
```typescript
// ✅ Better - pass the ref object
export function useElementSize(elm: React.RefObject<HTMLElement>) {
  useLayoutEffect(() => {
    // elm.current will always be the current value
    if (elm.current) {
      // This operates on the correct element
    }
  }, [elm]);
}
```

This pattern ensures your effects always work with the current DOM element rather than a potentially stale reference, preventing subtle bugs that might only surface under specific rendering conditions.