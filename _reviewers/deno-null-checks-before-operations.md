---
title: null checks before operations
description: Always check for null or undefined values before performing operations
  on objects, accessing properties, or calling methods. This prevents runtime errors
  that occur when attempting to operate on null/undefined values.
repository: denoland/deno
label: Null Handling
language: TypeScript
comments_count: 2
repository_stars: 103714
---

Always check for null or undefined values before performing operations on objects, accessing properties, or calling methods. This prevents runtime errors that occur when attempting to operate on null/undefined values.

When working with potentially nullable objects, add explicit null checks before accessing properties or calling methods:

```javascript
// Before - can throw if response is null
if (typeof response === "object" && ReflectHas(response, "then")) {
  // ...
}

// After - safe with null check
if (response !== null && typeof response === "object" && ReflectHas(response, "then")) {
  // ...
}
```

Similarly, check for property existence before using them:

```javascript
// Check if optional properties exist before use
if (span) {
  span.recordException(err);
  if (err.name) {  // Check err.name exists before using
    span.setAttribute("error.type", err.name);
  }
}
```

This pattern is especially important when calling methods like `Reflect.has()`, `Object.keys()`, or accessing properties on objects that might be null or undefined. The small overhead of these checks prevents difficult-to-debug runtime errors.