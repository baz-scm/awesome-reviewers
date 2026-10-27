---
title: Throttle Expensive Updates
description: 'When UI updates are triggered by high-frequency events (e.g., typing)
  or when rendering derived UI is expensive, reduce wasted work *before* it happens:'
repository: facebook/react#b5
label: Performance Optimization
language: TSX
comments_count: 3
repository_stars: 251886
---

When UI updates are triggered by high-frequency events (e.g., typing) or when rendering derived UI is expensive, reduce wasted work *before* it happens:

1) Prefer built-in deferral when appropriate
- If React already uses deferral for related output, consider extending that approach before adding new manual timers (e.g., `useDeferredValue`).

2) Otherwise debounce/throttle expensive side effects
- Debounce calls that trigger costly parsing/rendering (e.g., dispatches that lead to parse-error churn in an output panel).

3) Clean up timers/resources
- If you introduce `setTimeout`/`setInterval` or any async handle, cancel it on unmount so you don’t dispatch after the component is gone.

4) Avoid “compute-then-ignore” optimizations
- Memoization may not help if the expensive computation still runs and you later discard results. Filter/short-circuit earlier so the heavy work is skipped.

Example (debounce with safe cleanup):
```tsx
const debounceTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

useEffect(() => {
  return () => {
    if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);
  };
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

Example (skip expensive work):
```tsx
// Instead of tabifying everything and then filtering the view,
// filter the passes first, then render only what you need.
for (const [passName, results] of compilerOutput.results) {
  if (!store.showInternals && passName !== 'Output' && passName !== 'SourceMap') {
    continue; // skip expensive derived component creation
  }
  // render for this pass only
}
```