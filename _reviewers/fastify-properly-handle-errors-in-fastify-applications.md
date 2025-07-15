---
title: "Properly Handle Errors in Fastify Applications"
description: "When implementing error handling in Fastify applications, it is important to always throw instances of the Error class rather than primitive values or non-Error objects. This ensures that errors are properly propagated through the Fastify error handling chain."
repository: "fastify/fastify"
label: "Fastify"
language: "TypeScript"
comments_count: 5
repository_stars: 34000
---

When implementing error handling in Fastify applications, it is important to always throw instances of the Error class rather than primitive values or non-Error objects. This ensures that errors are properly propagated through the Fastify error handling chain.

If a Fastify plugin's error handler re-throws a non-Error value (such as a string or number), it will not propagate to parent context error handlers and instead will be caught by the default error handler. This can lead to unexpected behavior and make it difficult to debug issues.

For example, instead of:
```typescript
fastify.setErrorHandler((error, request, reply) => {
  // This will NOT propagate correctly to parent error handlers
  throw 'foo';
});
```

You should use:
```typescript
fastify.setErrorHandler((error, request, reply) => {
  // This will properly propagate through the error handling chain
  throw new Error('foo');
});
```

By consistently throwing Error instances, you can ensure that errors are properly handled and propagated throughout your Fastify application, leading to more robust and maintainable error handling.