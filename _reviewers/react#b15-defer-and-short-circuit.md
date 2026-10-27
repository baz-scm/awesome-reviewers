---
title: Defer and Short-Circuit
description: When changes drive expensive parsing or rendering (e.g., compiler output),
  optimize by (1) reducing how often updates propagate and (2) preventing costly derived
  work from running for views that won’t use it.
repository: facebook/react#b15
label: Performance Optimization
language: TSX
comments_count: 2
repository_stars: 251891
---

When changes drive expensive parsing or rendering (e.g., compiler output), optimize by (1) reducing how often updates propagate and (2) preventing costly derived work from running for views that won’t use it.

Apply this in two steps:

1) Prefer deferred/concurrent updates, but verify they actually reduce “thrash”.
- If output rendering is heavy, consider `useDeferredValue()` (or similar) to delay expensive UI updates while typing.
- If deferred rendering is still too responsive and causes thrash (e.g., frequent parse-error churn), use targeted debouncing around the specific state update that triggers the heavy work.
- If you debounce, always clear pending timers on unmount.

2) Short-circuit before expensive computation/rendering.
- Avoid patterns where you compute/render everything (e.g., `tabify` producing tab components) and then “filter” the result.
- Instead, skip the expensive branch early when the view should not include those passes.

Example patterns:

```tsx
// 1) Targeted debounce for expensive downstream updates
const debounceTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
useEffect(() => () => {
  if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);
}, []);

const handleChange = (value: string | undefined) => {
  if (value === undefined) return;
  if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);

  debounceTimerRef.current = setTimeout(() => {
    dispatchStore({
      type: 'updateConfig',
      payload: { config: value },
    });
  }, 500);
};
```

```tsx
// 2) Short-circuit before tabifying/rendering
for (const [passName, results] of compilerOutput.results) {
  if (!store.showInternals) {
    const allowed = passName === 'Output' || passName === 'SourceMap';
    if (!allowed) continue; // skip expensive work for excluded passes
  }
  // render/create only the tabs you actually need
}
```

Rule of thumb: memoization helps only if it prevents recomputation; if the expensive work still runs every change, refactor to defer/throttle or to skip the work before it happens.