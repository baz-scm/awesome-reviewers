---
title: Avoid wasted work on change
description: When rapid inputs drive expensive downstream work, optimize by (a) reducing
  how often the expensive work is triggered (defer/schedule rather than immediately
  updating) and (b) skipping the expensive computation/rendering for items you won’t
  use.
repository: facebook/react#b1
label: Performance Optimization
language: TSX
comments_count: 3
repository_stars: 251878
---

When rapid inputs drive expensive downstream work, optimize by (a) reducing how often the expensive work is triggered (defer/schedule rather than immediately updating) and (b) skipping the expensive computation/rendering for items you won’t use.

Apply this in two parts:
1) Throttle/Defer expensive updates triggered by typing
- Prefer React scheduling tools (e.g., `useDeferredValue`) if they already solve the “updates are still happening too quickly while typing” issue.
- If manual debouncing is necessary to prevent thrash (e.g., parse-error churn), debounce the *dispatch* and cancel pending timers on unmount.

Example:
```ts
const debounceTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

useEffect(() => {
  return () => {
    if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);
  };
}, []);

const handleChange = (value?: string) => {
  if (value === undefined) return;
  if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);

  debounceTimerRef.current = setTimeout(() => {
    dispatchStore({ type: 'updateConfig', payload: { config: value } });
  }, 500);
};
```

2) Filter/short-circuit before heavy transforms/rendering
- Don’t memoize the final result if the expensive step still runs for every change.
- Instead, iterate and `continue`/short-circuit so the heavy tabification/rendering work never happens for filtered-out entries.

Example (conceptual):
```ts
for (const [passName, results] of compilerOutput.results) {
  const shouldShow =
    store.showInternals || (passName === 'Output' || passName === 'SourceMap');
  if (!shouldShow) continue; // skip expensive tabification/rendering

  // tabify/render only what you will display
}
```

Net effect: fewer expensive updates are triggered, and each update performs only the work that will actually be shown—improving responsiveness and reducing CPU/memory churn.