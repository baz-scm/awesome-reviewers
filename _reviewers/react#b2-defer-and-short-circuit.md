---
title: Defer and short-circuit
description: 'For performance-sensitive UI, avoid unnecessary work in two ways: (1)
  defer/lag expensive updates using React primitives before adding custom timing logic,
  and (2) short-circuit before heavy transformations/rendering for content you won’t
  show.'
repository: facebook/react#b2
label: Performance Optimization
language: TSX
comments_count: 2
repository_stars: 251882
---

For performance-sensitive UI, avoid unnecessary work in two ways: (1) defer/lag expensive updates using React primitives before adding custom timing logic, and (2) short-circuit before heavy transformations/rendering for content you won’t show.

1) Prefer React deferral over manual debouncing
- If the problem is “updates happen too quickly while typing,” reuse `useDeferredValue()` (especially if it’s already used elsewhere for the same output path).
- Only fall back to manual debounce when `useDeferredValue` can’t express the needed behavior.

Example pattern:
```tsx
const deferredConfig = useDeferredValue(config);
// Update expensive derived output from deferredConfig (not from raw input)
const compilerErrors = useMemo(() => parse(deferredConfig), [deferredConfig]);
```

2) Don’t compute for UI you’ll ignore
- Memoization/filtering after the fact doesn’t prevent the expensive work from running.
- Instead, filter results first and skip the expensive step (`tabify`, rendering tab contents, etc.) for tabs that shouldn’t be displayed.

Example pattern:
```ts
for (const [passName, results] of compilerOutput.results) {
  const shouldShow = store.showInternals !== false || (passName !== 'Output' && passName !== 'SourceMap');
  if (!shouldShow) continue; // short-circuit before tabify/render
  // tabify/render only for shown passes
}
```

Applying this rule reduces CPU churn during rapid input and prevents wasted rendering work, directly addressing both update “thrash” and avoidable expensive computations.