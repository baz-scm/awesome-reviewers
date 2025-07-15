---
title: "Separate conditional paths"
description: "When working with concurrent operations, separate conditional logic from potentially expensive or suspenseful execution paths. This improves performance, prevents race conditions, and makes concurrent code more predictable and maintainable."
repository: "facebook/react"
label: "Concurrency"
language: "JavaScript"
comments_count: 3
repository_stars: 237000
---

When working with concurrent operations, separate conditional logic from potentially expensive or suspenseful execution paths. This improves performance, prevents race conditions, and makes concurrent code more predictable and maintainable.

**Why it matters:**
- Prevents unnecessary work in hot paths
- Reduces the risk of duplicate invocations and race conditions
- Makes concurrent code easier to reason about

**How to apply it:**
1. Hoist conditional checks higher in the call stack
2. Only invoke complex operations when necessary
3. Structure tests to properly simulate real concurrency patterns

**Example - Before:**
```js
function preloadInstanceAndSuspendIfNeeded(type, props, workInProgress, renderLanes) {
  // This check happens on every call, even when it's not needed
  if (!maySuspendCommit(type, props)) {
    // Regular path...
  } else {
    // Suspending path...
  }
}
```

**Example - After:**
```js
// In the calling function (e.g., completeWork):
const maySuspend = checkInstanceMaySuspend(type, props);
if (maySuspend) {
  preloadInstanceAndSuspendIfNeeded(type, props, workInProgress, renderLanes);
}

// Then the function only handles suspension cases
function preloadInstanceAndSuspendIfNeeded(type, props, workInProgress, renderLanes) {
  // Only suspension logic here
}
```

For testing concurrent operations, model tests to match real-world behavior using appropriate timing mechanisms:
```js
await act(async () => {
  submitButton.current.click();
  await waitForMicrotasks(); // Allow natural processing cycles
  submitButton.current.click(); // Second interaction
});
```