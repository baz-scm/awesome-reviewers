---
title: Skip Work; Defer Updates
description: When optimizing UI performance under frequent user input, (1) prefer
  React’s built-in deferral mechanisms to ad-hoc timing where they solve the same
  problem, and (2) avoid “compute/render then ignore” flows by filtering/short-circuiting
  *before* expensive work (parsing, tabification, building large lists).
repository: facebook/react#b11
label: Performance Optimization
language: TSX
comments_count: 2
repository_stars: 251894
---

When optimizing UI performance under frequent user input, (1) prefer React’s built-in deferral mechanisms to ad-hoc timing where they solve the same problem, and (2) avoid “compute/render then ignore” flows by filtering/short-circuiting *before* expensive work (parsing, tabification, building large lists).

Apply this as a standard:
- Prefer `useDeferredValue` (or similar) to reduce update thrash while typing instead of adding custom debouncing logic—especially if the app already uses it for output updates.
- If a view is filtered (e.g., show/hide internals), don’t memoize the filtered result while still running the heavy transformation for every tab; filter the input/passes first and only process/render what will be displayed.

Example pattern (skip expensive tabify work early):
```ts
const visibleTabs: Array<[string, unknown]> = [];
for (const [passName, results] of compilerOutput.results) {
  const hideInternals = store.showInternals === false;
  const isAllowed = !(hideInternals && (passName !== 'Output' && passName !== 'SourceMap'));
  if (!isAllowed) continue;
  visibleTabs.push([passName, results]);
}
// Only render/transform visibleTabs
```

And if you’re dealing with typing-induced output thrash, first check whether a `useDeferredValue` approach already used elsewhere can be extended—use manual debouncing only when the built-in deferral doesn’t address the specific bottleneck (e.g., parse-error churn).