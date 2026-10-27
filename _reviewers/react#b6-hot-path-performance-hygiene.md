---
title: Hot-Path Performance Hygiene
description: When code runs on hot paths (render loops, parsers, chunking/waking,
  input handlers, tight server-client serialization loops), avoid adding avoidable
  CPU, allocation, recursion, and synchronous browser work.
repository: facebook/react#b6
label: Performance Optimization
language: JavaScript
comments_count: 6
repository_stars: 251888
---

When code runs on hot paths (render loops, parsers, chunking/waking, input handlers, tight server-client serialization loops), avoid adding avoidable CPU, allocation, recursion, and synchronous browser work.

**Standard**
1. **Guard fast paths**: if most inputs shouldn’t take the expensive branch, check early and skip the heavy function (including argument setup).
2. **Minimize allocations/closures**: don’t create closures/bound callbacks unless the branch is actually taken; hoist reusable helpers to module scope.
3. **Avoid recursion in unbounded fan-out paths**: if a wake/notify mechanism can recurse repeatedly (or overflow), restructure to iterative/state-based updates (e.g., check status and directly call wake/reject when resolved).
4. **Avoid `try/catch/finally` in performance-critical code**: if needed, isolate into a smaller helper so the main function stays optimizable.
5. **Defer expensive work**: for UI/devtools searches or large traversals, derive results from deferred values / transitions so typing/render isn’t blocked; optionally show a spinner.
6. **Avoid sync layout thrash**: don’t call APIs like `getBoundingClientRect()` inside render-time logic that can force layout.
7. **Prefer native/engine implementations** for heavy conversions when possible (e.g., `TextDecoder('latin1')` for byte→string with stable bijection), and only fall back to manual chunking when required for correctness.

**Example (closure allocated only when needed)**
```js
function addDebugInfoNow(entry) {
  // ...
}
function addDebugInfoLater(entry) {
  // ...
}

if (chunk.status === PENDING) {
  const bound = addDebugInfoLater.bind(null, entry);
  chunk.then(bound, bound);
} else {
  addDebugInfoNow(entry);
}
```

**Example (defer expensive tree work)**
```js
const deferredText = useDeferredValue(searchText);
const matches = useMemo(() => computeMatches(tree, deferredText), [tree, deferredText]);
const pending = searchText !== deferredText;
```

**Goal:** keep hot-path code allocation-light, non-recursive (or bounded), and free of synchronous layout/overly-blocking work; then validate with targeted benchmarks/tests where behavior or perf is subtle.