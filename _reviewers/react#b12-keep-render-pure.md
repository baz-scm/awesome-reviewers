---
title: Keep Render Pure
description: 'In React components, keep `render` pure: do not rely on mutable refs
  as fallback values during render, and do not perform validation/compilation or other
  side-effect-like logic there. If you need debounced updates or timed work, schedule
  it in `useEffect` and always clean up timers/resources so they can’t dispatch after
  unmount.'
repository: facebook/react#b12
label: React
language: TSX
comments_count: 2
repository_stars: 251896
---

In React components, keep `render` pure: do not rely on mutable refs as fallback values during render, and do not perform validation/compilation or other side-effect-like logic there. If you need debounced updates or timed work, schedule it in `useEffect` and always clean up timers/resources so they can’t dispatch after unmount.

Practical rules:
- If you feel compelled to do `ref.current` as part of what your JSX renders, refactor so the “last valid” value is managed by state/store (updated in an effect or on dispatch), not read during render.
- Move validity/compilation decisions to where updates occur (e.g., the store action/dispatcher) or in a `useEffect` that runs when inputs change.
- For debounces/timers, use an effect with cleanup (`clearTimeout`) and consider canceling pending work when dependencies change or the component unmounts.

Example pattern (debounce + cleanup):
```ts
function useDebouncedDispatch(onDispatch: () => void, delayMs: number) {
  const dispatchTimeoutRef = React.useRef<ReturnType<typeof setTimeout> | null>(null);

  React.useEffect(() => {
    if (dispatchTimeoutRef.current) clearTimeout(dispatchTimeoutRef.current);
    dispatchTimeoutRef.current = setTimeout(() => onDispatch(), delayMs);

    return () => {
      if (dispatchTimeoutRef.current) clearTimeout(dispatchTimeoutRef.current);
    };
  }, [onDispatch, delayMs]);
}
```

If invalid configs are possible, decide validity at update time (store/action/effect) and only store renderable values—so `render` doesn’t need ref fallbacks.