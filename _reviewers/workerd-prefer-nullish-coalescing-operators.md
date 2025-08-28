---
title: prefer nullish coalescing operators
description: Use nullish coalescing operators (`??`) and logical OR with safe defaults
  (`|| {}`) to handle null and undefined values more safely and concisely. This prevents
  runtime errors when accessing properties on potentially null/undefined objects and
  provides cleaner, more readable code.
repository: cloudflare/workerd
label: Null Handling
language: TypeScript
comments_count: 3
repository_stars: 6989
---

Use nullish coalescing operators (`??`) and logical OR with safe defaults (`|| {}`) to handle null and undefined values more safely and concisely. This prevents runtime errors when accessing properties on potentially null/undefined objects and provides cleaner, more readable code.

Instead of explicit null/undefined checks:
```typescript
// Avoid
return this._eventsCount > 0 && this._events !== undefined
  ? Reflect.ownKeys(this._events)
  : [];

// Prefer
return this._eventsCount > 0 ? Reflect.ownKeys(this._events || {}) : [];
```

For numeric values, use nullish coalescing to distinguish between falsy values and null/undefined:
```typescript
// Avoid - treats 0 as falsy
this.errno = options.errno || 1;

// Prefer - only coalesces null/undefined
this.errno = options.errno ?? 1;
```

This approach reduces boilerplate code while providing better null safety and more predictable behavior when dealing with optional properties and parameters.