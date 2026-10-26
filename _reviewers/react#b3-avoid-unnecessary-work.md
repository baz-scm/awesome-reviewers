---
title: Avoid Unnecessary Work
description: When optimizing UI performance, avoid both (a) thrash from eagerly propagating
  rapid input changes and (b) expensive computation/rendering that’s later discarded.
repository: facebook/react#b3
label: Performance Optimization
language: TSX
comments_count: 2
repository_stars: 251883
---

When optimizing UI performance, avoid both (a) thrash from eagerly propagating rapid input changes and (b) expensive computation/rendering that’s later discarded.

Practical rules:
1) Prefer React-native scheduling for fast-changing inputs
- If your goal is to reduce UI thrash while typing (e.g., parse-error churn), try using React’s built-in mechanisms (like `useDeferredValue`) rather than adding manual debounce timers—especially if the component (or sibling) already uses deferred updates.

2) Filter before you transform/render
- Don’t “compute everything then ignore it.” If a view is filtered, apply the filter before calling heavy transforms (like `tabify`) or mapping all tabs to components.

Example (early filtering to skip expensive work):
```ts
const filteredResults = [];
for (const [passName, results] of compilerOutput.results) {
  const shouldShow =
    store.showInternals ||
    (passName === 'Output' || passName === 'SourceMap');

  if (!shouldShow) continue; // skip expensive tab creation
  filteredResults.push([passName, results]);
}

// Now build/render only from filteredResults
```

Outcome: fewer wasted renders/transforms and less UI thrashing during rapid edits, leading to smoother performance.