---
title: Defer Updates, Skip Work
description: 'When optimizing for UI thrash or expensive rendering:


  - Prefer React’s built-in deferral (e.g., `useDeferredValue`) over manual debouncing
  when the problem is “updates feel too fast while typing,” especially if that same
  app already uses `useDeferredValue` for similar concerns.'
repository: facebook/react#b6
label: Performance Optimization
language: TSX
comments_count: 3
repository_stars: 251888
---

When optimizing for UI thrash or expensive rendering:

- Prefer React’s built-in deferral (e.g., `useDeferredValue`) over manual debouncing when the problem is “updates feel too fast while typing,” especially if that same app already uses `useDeferredValue` for similar concerns.
- If you do use timers (`setTimeout`/`setInterval`) to reduce work, clean up only when it matters: clear timers on unmount (or otherwise cancel) so the callback can’t run after the component is gone and won’t trigger unwanted side effects.
- Don’t “memoize after the fact.” If an expensive computation still runs (e.g., building/rendering tabs) and you only filter the results later, move the filtering/early-exit checks upstream so the costly work is skipped entirely.

Example (skipping expensive work instead of memoizing filtered output):

```ts
const tabsToRender = [];
for (const [passName, results] of compilerOutput.results) {
  if (!store.showInternals && (passName !== 'Output' && passName !== 'SourceMap')) continue;
  tabsToRender.push([passName, results]);
}
// render only tabsToRender; avoid running tabify for ignored passes
```

Example (timer cleanup when side effects are possible):

```ts
const debounceTimerRef = useRef<number | null>(null);
useEffect(() => {
  return () => {
    if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);
  };
}, []);
```