---
title: explicit type checking
description: Always perform explicit type and existence checks before operations that
  could fail with null or undefined values. Instead of relying on truthiness checks,
  use specific type guards to prevent runtime errors.
repository: vadimdemedes/ink
label: Null Handling
language: TypeScript
comments_count: 3
repository_stars: 31825
---

Always perform explicit type and existence checks before operations that could fail with null or undefined values. Instead of relying on truthiness checks, use specific type guards to prevent runtime errors.

For function calls, check the actual type before invocation:
```typescript
// Instead of just checking truthiness
if (rootNode.onRender) {
    rootNode.onRender();
}

// Use explicit type checking
if (typeof rootNode.onRender === 'function') {
    rootNode.onRender();
}
```

For value operations, handle edge cases explicitly:
```typescript
// Instead of assuming non-empty
const outputHeight = output.split('\n').length;

// Handle empty values explicitly
const outputHeight = output === '' ? 0 : output.split('\n').length;
```

This pattern prevents common runtime errors caused by attempting operations on null, undefined, or incorrectly typed values, and makes the code's assumptions explicit and safer.