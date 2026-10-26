---
title: Avoid Hot-Path Allocations
description: For performance-sensitive code, proactively prevent avoidable allocations
  and engine-deopt triggers (closures, repeated array/object creation, recursion/Set
  creation in loops), and prefer native/fast primitives. Also keep semantic contracts
  explicit—don’t silently change measurements used by heuristics.
repository: facebook/react#b3
label: Performance Optimization
language: JavaScript
comments_count: 9
repository_stars: 251883
---

For performance-sensitive code, proactively prevent avoidable allocations and engine-deopt triggers (closures, repeated array/object creation, recursion/Set creation in loops), and prefer native/fast primitives. Also keep semantic contracts explicit—don’t silently change measurements used by heuristics.

How to apply:
- Hoist reusable functions/data to module scope when a conditional would otherwise allocate a closure per call.
- Avoid patterns that allocate repeatedly (e.g., chunk loops that create new arrays just to build arguments); instead use native APIs (e.g., TextDecoder) or a single reusable decoder.
- Avoid forced layout work in render paths (e.g., getBoundingClientRect) unless absolutely necessary.
- Don’t change the meaning of measurements (e.g., byteLength) without renaming and updating call sites; “fast path” approximations require an explicit “approx” contract.
- Avoid per-iteration Set allocations when the common case can be handled with cheaper checks.

Example patterns:

1) Replace closure allocation in hot conditions
```js
// Bad (may allocate per call depending on branch shape)
if (needDelay) {
  const f = () => addDebugInfo(entry);
  promise.then(f, f);
} else {
  addDebugInfo(entry);
}

// Better
function addDebugInfoEntry(entry) {
  addDebugInfo(entry);
}

if (needDelay) {
  const f = addDebugInfoEntry.bind(null, entry); // or pass a stable module-level wrapper
  promise.then(f, f);
} else {
  addDebugInfo(entry);
}
```

2) Avoid apply+chunk allocations; use a native decoder
```js
const latin1Decoder = new TextDecoder('latin1');
function binaryToComparableString(view) {
  // Decode uses a native fast path; keeps byte->codepoint mapping bijective.
  return latin1Decoder.decode(view);
}
```

3) Avoid forced layout
```js
// Bad in a tight loop
const r = el.getBoundingClientRect();

// Better: compute via your own cached geometry / parent traversal
// (avoid layout flush during drawing)
```