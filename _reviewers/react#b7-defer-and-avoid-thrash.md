---
title: Defer and avoid thrash
description: 'When updates are expensive (e.g., parsing errors, heavy rendering),
  optimize at the source:


  - Prefer React’s built-in deferral/concurrency mechanisms (e.g., `useDeferredValue`)
  before writing custom throttling logic.'
repository: facebook/react#b7
label: Performance Optimization
language: TSX
comments_count: 3
repository_stars: 251888
---

When updates are expensive (e.g., parsing errors, heavy rendering), optimize at the source:

- Prefer React’s built-in deferral/concurrency mechanisms (e.g., `useDeferredValue`) before writing custom throttling logic.
- If you implement manual debouncing/throttling, cancel pending timers on unmount when it matters (especially if timers/side effects could outlive the component or keep doing work).
- Avoid expensive work entirely for filtered/hidden UI paths; memoizing computed output is not enough if the expensive computation (e.g., tabification/rendering for all tabs) still runs.

Example (debounce with lifecycle-safe cleanup):

```ts
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

Example (skip expensive work instead of memoizing the result):

```ts
for (const [passName, results] of compilerOutput.results) {
  if (!store.showInternals && passName !== 'Output' && passName !== 'SourceMap') {
    continue; // don’t tabify/render these
  }
  // render only the needed pass results
}
```