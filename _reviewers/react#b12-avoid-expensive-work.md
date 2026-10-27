---
title: Avoid Expensive Work
description: 'When state changes rapidly (e.g., typing), optimize for *preventing*
  expensive downstream work—not just memoizing outputs.


  Apply this standard:

  1. Prefer React’s built-in deferred/concurrent primitives for high-frequency updates
  (e.g., `useDeferredValue`) before introducing manual debouncing.'
repository: facebook/react#b12
label: Performance Optimization
language: TSX
comments_count: 2
repository_stars: 251896
---

When state changes rapidly (e.g., typing), optimize for *preventing* expensive downstream work—not just memoizing outputs.

Apply this standard:
1. Prefer React’s built-in deferred/concurrent primitives for high-frequency updates (e.g., `useDeferredValue`) before introducing manual debouncing.
2. If manual debouncing is necessary to reduce UI thrash (e.g., parse errors), debounce the update safely and clean up timers on unmount.
3. When rendering/filtering expensive derived views, short-circuit *before* the heavy transformation/rendering step. Don’t rely on memoization if the expensive work (like tabification) still runs for all items.

Example patterns:

**Debounce safely (only if needed):**
```ts
const debounceTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
useEffect(() => () => {
  if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);
}, []);

const handleChange = (value?: string) => {
  if (value === undefined) return;
  if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);
  debounceTimerRef.current = setTimeout(() => {
    dispatch({ type: 'updateConfig', payload: { config: value } });
  }, 500);
};
```

**Filter before heavy work:**
```ts
for (const [passName, results] of compilerOutput.results) {
  if (!store.showInternals) {
    if (passName !== 'Output' && passName !== 'SourceMap') continue;
  }
  // Only tabify/render the included passes
}
```