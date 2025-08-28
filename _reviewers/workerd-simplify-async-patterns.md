---
title: Simplify async patterns
description: Use modern promise utilities and clean async patterns instead of manual
  promise construction. Prefer Promise.withResolvers() over manual promise creation
  with resolve/reject callbacks, and chain promises directly rather than wrapping
  them in unnecessary async functions.
repository: cloudflare/workerd
label: Concurrency
language: JavaScript
comments_count: 3
repository_stars: 6989
---

Use modern promise utilities and clean async patterns instead of manual promise construction. Prefer Promise.withResolvers() over manual promise creation with resolve/reject callbacks, and chain promises directly rather than wrapping them in unnecessary async functions.

When testing async operations, ensure the tests actually validate the intended concurrency behavior. Async tests should verify that operations complete at the right time and in the right sequence, not just that they eventually resolve.

Example of preferred patterns:
```javascript
// Good: Clean and readable
const { promise, resolve } = Promise.withResolvers();
waitUntil(scheduler.wait(100).then(resolve));
await promise;

// Avoid: Manual promise construction
let resolve;
const promise = new Promise((r) => { resolve = r; });
waitUntil((async () => {
  await scheduler.wait(100);
  resolve();
})());
```

This approach reduces complexity, improves readability, and ensures async operations are tested meaningfully rather than just checking that promises eventually resolve.