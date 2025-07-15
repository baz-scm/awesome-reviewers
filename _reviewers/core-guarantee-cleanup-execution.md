---
title: Guarantee cleanup execution
description: When implementing features that require cleanup or state restoration,
  always use try-finally blocks to ensure cleanup code executes even when errors occur.
  This pattern prevents resources from being leaked, components from becoming stuck
  in intermediate states, and operations from remaining incomplete after exceptions.
repository: vuejs/core
label: Error Handling
language: TypeScript
comments_count: 4
repository_stars: 50769
---

When implementing features that require cleanup or state restoration, always use try-finally blocks to ensure cleanup code executes even when errors occur. This pattern prevents resources from being leaked, components from becoming stuck in intermediate states, and operations from remaining incomplete after exceptions.

For example, instead of:

```js
if (element._isSpecial) {
  element._beginOperation()
}
performComplexAction()
if (element._isSpecial) {
  element._endOperation()
}
```

Use the more robust pattern:

```js
const isSpecial = !!element._isSpecial
try {
  if (isSpecial) {
    element._beginOperation()
  }
  performComplexAction()
} finally {
  if (isSpecial) {
    element._endOperation()
  }
}
```

This approach:
- Prevents components from remaining in an inconsistent state if errors occur
- Ensures all resources are properly released
- Makes your code more resilient to unexpected failures
- Maintains proper balance of paired operations (begin/end, open/close)

When handling multiple cleanup operations, consider whether to wrap each in its own try-catch to prevent one failure from blocking other cleanups, especially in shutdown sequences.