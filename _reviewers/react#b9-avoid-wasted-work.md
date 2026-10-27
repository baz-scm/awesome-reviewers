---
title: Avoid wasted work
description: When user input or derived UI triggers expensive work (parsing, tabification,
  heavy rendering), structure code so you either *reduce how often* the expensive
  work runs or *skip the work entirely* for views that won’t be shown.
repository: facebook/react#b9
label: Performance Optimization
language: TSX
comments_count: 2
repository_stars: 251891
---

When user input or derived UI triggers expensive work (parsing, tabification, heavy rendering), structure code so you either *reduce how often* the expensive work runs or *skip the work entirely* for views that won’t be shown.

**Apply two rules:**
1) **Throttle/deflect rapid updates.** If typing causes costly downstream parsing/render (e.g., parse errors thrash), use `useDeferredValue` where it fits, or debounce the dispatch that triggers the expensive path. Always clean up timers.
2) **Filter before expensive derivation/render.** Don’t compute/instantiate components for data you’ll ignore. Move filtering/guards to the point before tabifying/transforming/rendering.

**Example (debounce with cleanup):**
```ts
const debounceTimerRef = useRef<NodeJS.Timeout | null>(null);
useEffect(() => () => {
  if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);
}, []);

const handleChange = (value?: string) => {
  if (value === undefined) return;
  if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);

  debounceTimerRef.current = setTimeout(() => {
    dispatchStore({ type: 'updateConfig', payload: { config: value } });
  }, 500);
};
```

**Example (skip tabify work by filtering early):**
```ts
for (const [passName, results] of compilerOutput.results) {
  if (!store.showInternals && (passName !== 'Output' && passName !== 'SourceMap')) {
    continue; // avoid rendering work for filtered-out tabs
  }

  // tabify/render only the tabs you will show
  // render<TextTabContent ...>(...)
}
```