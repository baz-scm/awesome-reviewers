---
title: Short-Circuit for Performance
description: 'In performance-sensitive code paths, minimize unnecessary work by ordering
  conditions to short-circuit early, and avoid redundant async wrappers.


  **Apply these rules:**'
repository: tanstack/query
label: Performance Optimization
language: JavaScript
comments_count: 3
repository_stars: 49380
---

In performance-sensitive code paths, minimize unnecessary work by ordering conditions to short-circuit early, and avoid redundant async wrappers.

**Apply these rules:**
1. **Guard with cheap predicates first** (e.g., `enabled`/boolean flags) so later conditions/callbacks are never evaluated when they can’t change the outcome.
2. **Don’t call expensive checkers unless needed**: ensure threshold/count/boolean conditions gate any `retryChecker(...)`-style functions.
3. **In `async` functions, return values directly**—don’t wrap them with `Promise.resolve`, and avoid unnecessary `else` after a `return`.

**Example patterns:**
```js
// 1) Guard before evaluating other conditions
const shouldRefetch = query.instances.some(instance =>
  instance.config.enabled && instance.config.refetchIntervalInBackground
);

// 2) Gate expensive retryChecker with cheaper conditions
const canRetryByCount = query.state.failureCount <= query.config.retry;
const shouldRetry =
  query.config.retry === true ||
  (canRetryByCount && query.config.retryChecker(error, query.state.failureCount));

// 3) Avoid redundant Promise.resolve in async functions
async function getData() {
  // ...
  return query.state.data; // no Promise.resolve, no redundant else
}
```

This reduces wasted evaluations and prevents unnecessary function calls, improving execution speed and resource utilization.