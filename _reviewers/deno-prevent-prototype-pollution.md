---
title: prevent prototype pollution
description: When implementing security measures around JavaScript's `__proto__` property,
  disable the setter to prevent prototype pollution attacks while carefully considering
  whether getter access is needed for compatibility. Prototype pollution occurs when
  attackers can modify Object.prototype, potentially affecting all objects in the
  application.
repository: denoland/deno
label: Security
language: JavaScript
comments_count: 2
repository_stars: 103714
---

When implementing security measures around JavaScript's `__proto__` property, disable the setter to prevent prototype pollution attacks while carefully considering whether getter access is needed for compatibility. Prototype pollution occurs when attackers can modify Object.prototype, potentially affecting all objects in the application.

Use `Object.defineProperty` to disable the setter while optionally preserving getter functionality:

```javascript
// Disables setting `__proto__` and emits a warning instead, for security reasons.
Object.defineProperty(Object.prototype, "__proto__", {
  get: Object.prototype.__proto__, // Keep getter if needed for compatibility
  set: function() {
    console.warn("Setting __proto__ is disabled for security reasons");
  }
});
```

Consider the compatibility impact on dependencies that may rely on `__proto__` functionality. In environments where no user code executes (like TypeScript compilation), completely removing `__proto__` access may be appropriate. For runtime environments, emitting warnings helps identify problematic dependencies while maintaining security.