---
title: defensive error handling
description: Implement defensive programming practices to prevent runtime errors and
  provide meaningful error information when failures occur. This includes validating
  object state before operations and ensuring error messages contain specific contextual
  details.
repository: gravitational/teleport
label: Error Handling
language: TypeScript
comments_count: 2
repository_stars: 19109
---

Implement defensive programming practices to prevent runtime errors and provide meaningful error information when failures occur. This includes validating object state before operations and ensuring error messages contain specific contextual details.

Key practices:
1. **State validation**: Check if objects are in a valid state before performing operations, especially for resources that can be destroyed or become invalid
2. **Informative error messages**: Include specific values, versions, or context in error messages rather than generic references

Example from window management:
```typescript
// Bad - can crash if window is destroyed
showWindow() {
  this.window.show(); // TypeError: Object has been destroyed
}

// Good - validate state first
showWindow() {
  if (!this.window.isDestroyed()) {
    this.window.show();
  }
}
```

Example from error construction:
```typescript
// Bad - vague error message
throw new Error(`Cannot update to this version`);

// Good - specific error message
throw new Error(`Cannot update to version ${actualVersion}. Minimum supported version is ${minVersion}`);
```

This approach prevents crashes from invalid operations and provides developers with actionable information when errors do occur.