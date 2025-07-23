---
title: Use async/await pattern
description: Prefer async/await syntax over promise chains or callback patterns when
  working with asynchronous operations. This improves code readability, makes error
  handling more straightforward, and maintains consistency across the codebase.
repository: continuedev/continue
label: Concurrency
language: TSX
comments_count: 2
repository_stars: 27819
---

Prefer async/await syntax over promise chains or callback patterns when working with asynchronous operations. This improves code readability, makes error handling more straightforward, and maintains consistency across the codebase.

Example (converting from promise chain to async/await):
```typescript
// Instead of this:
ideMessenger
  .request("controlPlane/getFreeTrialStatus", undefined)
  .then(response => {
    // handle response
  })
  .catch(error => {
    // handle error
  });

// Prefer this:
async function getFreeTrialStatus() {
  try {
    const response = await ideMessenger.request("controlPlane/getFreeTrialStatus", undefined);
    // handle response
  } catch (error) {
    // handle error
  }
}
```

This pattern not only enhances readability but also helps avoid the "callback hell" that can occur with chained promises in complex asynchronous operations. Code written with async/await tends to follow a more natural top-to-bottom execution flow that's easier to reason about when dealing with concurrent operations.