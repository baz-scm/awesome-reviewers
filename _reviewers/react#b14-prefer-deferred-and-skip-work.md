---
title: Prefer deferred and skip work
description: When optimizing render/update performance, (1) prefer built-in React
  mechanisms that reduce perceived urgency (e.g., `useDeferredValue`) before introducing
  manual debouncing, (2) if you add manual timers to throttle expensive downstream
  work, ensure they’re canceled/cleared appropriately (especially on unmount), and
  (3) don’t rely on memoizing filtered...
repository: facebook/react#b14
label: Performance Optimization
language: TSX
comments_count: 3
repository_stars: 251893
---

When optimizing render/update performance, (1) prefer built-in React mechanisms that reduce perceived urgency (e.g., `useDeferredValue`) before introducing manual debouncing, (2) if you add manual timers to throttle expensive downstream work, ensure they’re canceled/cleared appropriately (especially on unmount), and (3) don’t rely on memoizing filtered output if the expensive work still runs—short-circuit earlier to avoid the heavy computation entirely.

Example pattern (debounce with safe cleanup):

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

Example pattern (avoid ineffective memoization by skipping expensive work):

```ts
for (const [passName, results] of compilerOutput.results) {
  if (!store.showInternals && (passName !== 'Output' && passName !== 'SourceMap')) {
    continue; // skip tabify/render work entirely
  }
  // expensive tabify/render here
}
```

Apply this especially when user typing triggers costly downstream processing (e.g., parsing, tabifying, rendering large output).