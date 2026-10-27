---
title: Prevent Input Thrash
description: For performance-sensitive UI paths triggered by rapid user input (e.g.,
  typing that causes parsing and heavy rendering), reduce work *before* it fans out.
repository: facebook/react#b8
label: Performance Optimization
language: TSX
comments_count: 3
repository_stars: 251889
---

For performance-sensitive UI paths triggered by rapid user input (e.g., typing that causes parsing and heavy rendering), reduce work *before* it fans out.

- Prefer built-in React deferral when it fits (`useDeferredValue`) over ad-hoc timing where possible.
- If debouncing is needed, debounce the state/dispatch that triggers expensive downstream work (parsing, error rendering), and keep the delay long enough to meaningfully cut thrash.
- Timer cleanup: only add cleanup when the timer/resource could cause side effects after unmount (e.g., persistent intervals, subscriptions). For a one-shot debounce that naturally expires, cleanup may be optional—but be intentional.
- Avoid memoization patterns that still perform expensive computation and then discard most results; filter/short-circuit inputs so expensive work doesn’t run.

Example (debounce dispatch to reduce parse thrash):
```ts
const debounceTimerRef = useRef<NodeJS.Timeout | null>(null);

useEffect(() => {
  return () => {
    if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);
  };
}, []);

const handleChange = (value?: string) => {
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

Example (skip expensive tabification by filtering early):
```ts
for (const [passName, results] of compilerOutput.results) {
  if (!store.showInternals && passName !== 'Output' && passName !== 'SourceMap') {
    continue; // short-circuit before rendering tab content
  }
  // ...render only the needed pass results
}
```