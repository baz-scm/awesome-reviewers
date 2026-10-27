---
title: Performance Delay And Short-Circuit
description: 'For performance-sensitive, input-driven UI updates:

  1) Prefer React-native deferral mechanisms (e.g., `useDeferredValue`) over custom
  debouncing when the goal is to reduce typing-driven re-render thrash.'
repository: facebook/react#b10
label: Performance Optimization
language: TSX
comments_count: 3
repository_stars: 251894
---

For performance-sensitive, input-driven UI updates:
1) Prefer React-native deferral mechanisms (e.g., `useDeferredValue`) over custom debouncing when the goal is to reduce typing-driven re-render thrash.
2) If you must manually debounce/throttle, implement it with a timer reference and consider canceling on unmount to prevent stale side effects after the component lifecycle ends.
3) Avoid “compute-then-discard” patterns: filter/short-circuit *before* expensive work (e.g., skip tab generation or parsing/rendering for hidden views) rather than memoizing around results that were still computed.

Example (manual debounce with safe cancellation):
```ts
const debounceTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
useEffect(() => {
  return () => {
    if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);
  };
}, []);

const onChange = (value?: string) => {
  if (!value) return;
  if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);
  debounceTimerRef.current = setTimeout(() => {
    dispatchStore({ type: 'updateConfig', payload: { config: value } });
  }, 500);
};
```

And when filtering expensive UI, short-circuit upstream:
```ts
for (const [passName, results] of compilerOutput.results) {
  if (!store.showInternals) {
    if (passName !== 'Output' || passName !== 'SourceMap') continue; // or correct allowlist logic
  }
  // only tabify/render what you will actually show
}
```