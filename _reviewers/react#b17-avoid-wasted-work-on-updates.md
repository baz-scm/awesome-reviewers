---
title: Avoid wasted work on updates
description: 'When optimizing typing-driven or render-heavy flows, minimize unnecessary
  work end-to-end:


  1) Prefer built-in deferral over manual throttling

  - If React already provides a better-fit mechanism (e.g., `useDeferredValue`) for
  typing/output lag, use it first.'
repository: facebook/react#b17
label: Performance Optimization
language: TSX
comments_count: 3
repository_stars: 251891
---

When optimizing typing-driven or render-heavy flows, minimize unnecessary work end-to-end:

1) Prefer built-in deferral over manual throttling
- If React already provides a better-fit mechanism (e.g., `useDeferredValue`) for typing/output lag, use it first.
- Add manual debouncing only when it’s clearly needed to prevent downstream thrash (e.g., expensive parse errors/redraws) and after confirming the built-in approach isn’t sufficient.

2) If using timers, make unmount behavior explicit
- If you debounce with a `setTimeout`/interval, cancel it on unmount to avoid dispatching after the component is gone.

3) Don’t “filter after expensive work”
- `useMemo`/filtering that still performs the heavy computation/render for every update doesn’t actually fix the bottleneck.
- Instead, skip the work before it happens (early `continue`, conditional branches, or avoid calling the expensive “tabify”/render path for hidden tabs).

Example (debounced dispatch with unmount cleanup):
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

Example (skip expensive tab content creation):
```ts
for (const [passName, results] of compilerOutput.results) {
  const showInternals = store.showInternals;
  const isAllowed =
    showInternals || (passName !== 'Output' && passName !== 'SourceMap');
  if (!isAllowed) continue; // skip tabify/render work entirely

  // create/render only the needed tab content
}
```

Apply this standard by profiling/observing typing latency and CPU churn: aim to reduce the amount of work performed per keystroke, not just to cache the final output.