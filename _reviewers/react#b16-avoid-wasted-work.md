---
title: Avoid wasted work
description: 'When optimizing performance, focus on preventing expensive work from
  happening unnecessarily.


  - For high-frequency input (e.g., typing in an editor that triggers parse errors/re-renders),
  use React’s deferral tools when they suffice; otherwise apply targeted debouncing
  to throttle expensive downstream updates (e.g., output recomputation).'
repository: facebook/react#b16
label: Performance Optimization
language: TSX
comments_count: 3
repository_stars: 251891
---

When optimizing performance, focus on preventing expensive work from happening unnecessarily.

- For high-frequency input (e.g., typing in an editor that triggers parse errors/re-renders), use React’s deferral tools when they suffice; otherwise apply targeted debouncing to throttle expensive downstream updates (e.g., output recomputation).
- Manage asynchronous resources created for throttling (timers). Cancel/cleanup on unmount when there’s any risk the callback would still run and trigger work after the component is gone.
- Don’t rely on memoization alone if it doesn’t stop the expensive computation/rendering. If you’re going to ignore most of the generated UI, restructure to filter/short-circuit *before* the expensive work (avoid “compute then discard”).

Example (debounced dispatch with safe cleanup):
```ts
const debounceTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

useEffect(() => {
  return () => {
    if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);
  };
}, []);

const handleChange = (value?: string) => {
  if (!value) return;

  if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);

  debounceTimerRef.current = setTimeout(() => {
    dispatchStore({
      type: 'updateConfig',
      payload: { config: value },
    });
  }, 500);
};
```

Example (skip expensive tab construction by filtering first):
```ts
const shouldShow = (passName: string) => {
  return store.showInternals || (passName !== 'Output' && passName !== 'SourceMap');
};

for (const [passName, results] of compilerOutput.results) {
  if (!shouldShow(passName)) continue; // short-circuit before expensive rendering
  // render/create tab content here
}
```