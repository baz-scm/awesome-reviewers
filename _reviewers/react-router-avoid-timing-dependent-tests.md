---
title: avoid timing-dependent tests
description: Tests should not rely on fixed delays, arbitrary timeouts, or assume
  deterministic ordering of asynchronous operations. Instead, use proper waiting mechanisms
  and sort results when order doesn't matter.
repository: remix-run/react-router
label: Testing
language: TypeScript
comments_count: 2
repository_stars: 55270
---

Tests should not rely on fixed delays, arbitrary timeouts, or assume deterministic ordering of asynchronous operations. Instead, use proper waiting mechanisms and sort results when order doesn't matter.

Replace fixed delays like `await sleep(LOADER_LATENCY_MS)` with conditional waiting:
```typescript
// Bad: Fixed delay
await sleep(LOADER_LATENCY_MS);
expect(router.getBlocker("KEY", fn)).toEqual({
  state: "unblocked",
  proceed: undefined,
});

// Good: Wait for condition
await waitFor(() =>
  expect(router.getBlocker("KEY", fn)).toEqual({
    state: "unblocked", 
    proceed: undefined,
  })
);
```

For non-deterministic collections, sort before comparison:
```typescript
// Bad: Assumes request order
expect(requests).toEqual([...]);

// Good: Sort for deterministic comparison  
expect(requests.sort()).toEqual([...]);
```

This prevents flaky tests that fail intermittently due to timing variations across different environments and browsers.