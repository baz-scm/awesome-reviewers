---
title: "Ensure Proper Null Handling When Using Fastify Decorators"
description: "When working with Fastify decorators, always perform explicit null checks before accessing potentially undefined properties. Relying on implicit null handling can lead to subtle bugs and unexpected behavior."
repository: "fastify/fastify"
label: "Fastify"
language: "TypeScript"
comments_count: 2
repository_stars: 34000
---

When working with Fastify decorators, always perform explicit null checks before accessing potentially undefined properties. Relying on implicit null handling can lead to subtle bugs and unexpected behavior. Instead, leverage Fastify's type-safe decorator APIs and type guards to ensure null safety at compile-time.

**Why?** Fastify decorators provide a powerful way to extend the functionality of your application, but they can also introduce the risk of accessing undefined values. Explicit null checks help make your code's intent clear and prevent cascading errors caused by missing dependencies.

**Example:**

```typescript
// ❌ Problematic - unclear if user decorator is missing
const user = request.user;
if (user && user.isAdmin) {
  // Execute admin tasks
}

// ✅ Better - use Fastify's type-safe decorator API
try {
  const user = request.getDecorator<User>('user');
  if (user.isAdmin) {
    // Execute admin tasks
  }
} catch (err) {
  // Handle missing decorator case explicitly
}

// ✅ Also good - use type guards to ensure null safety
request.raw.on('close', () => {
  if (isRequestDestroyed(request.raw)) {
    // Handle aborted request
  }
});

function isRequestDestroyed(raw: FastifyRawRequest): raw is FastifyRawRequest & { destroyed: true } {
  return raw.destroyed;
}
```

By following these practices, you can write more robust and maintainable Fastify applications that are less prone to null-related errors.