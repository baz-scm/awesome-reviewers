---
title: Avoid Wasted UI Work
description: When UI updates are driven by fast-changing input (typing), and when
  only a subset of computed results will be shown, optimize by (1) deferring/cadencing
  updates and (2) short-circuiting expensive computation.
repository: facebook/react#b4
label: Performance Optimization
language: TSX
comments_count: 2
repository_stars: 251885
---

When UI updates are driven by fast-changing input (typing), and when only a subset of computed results will be shown, optimize by (1) deferring/cadencing updates and (2) short-circuiting expensive computation.

1) Prefer built-in deferred updates over ad-hoc debouncing
- If React already has a suitable mechanism (e.g., `useDeferredValue`) to reduce render/parse thrash, prefer it.
- Only add manual debounce/throttle when built-ins don’t provide enough control, and always clean up timers on unmount.

Example pattern (manual debounce with cleanup):
```ts
const debounceTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
useEffect(() => () => {
  if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);
}, []);

function onChange(value?: string) {
  if (!value) return;
  if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);
  debounceTimerRef.current = setTimeout(() => {
    dispatchStore({ type: 'updateConfig', payload: { config: value } });
  }, 500);
}
```

2) Filter early; don’t compute/render everything then ignore
- If you’re conditionally displaying items (like tabs), apply the filter/skip logic before expensive steps (e.g., before calling `tabify` or building heavy tab content).
- Don’t rely on memoization if the expensive work still runs on every source change.

Rule of thumb:
- If “we still do the work then ignore most of it,” move the condition earlier so the expensive work never happens for hidden items.