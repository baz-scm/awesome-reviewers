---
title: "Proper Handling of Promises in Fastify Implementations"
description: "When implementing Fastify applications in TypeScript, it is important to follow consistent patterns for handling promises and respecting the framework's specific constraints. Avoid mixing async/await with callback styles, especially when registering routes, plugins, or parsers."
repository: "fastify/fastify"
label: "Fastify"
language: "TypeScript"
comments_count: 4
repository_stars: 34000
---

When implementing Fastify applications in TypeScript, it is important to follow consistent patterns for handling promises and respecting the framework's specific constraints. Avoid mixing async/await with callback styles, especially when registering routes, plugins, or parsers. Be aware that some Fastify methods are designed as thenables and do not require explicit awaiting.

For example, when registering content type parsers, do not use `await` as this can cause issues in Fastify:

```typescript
// INCORRECT: Mixing await with registration methods
await fastify.addContentTypeParser('application/json', async (req, body) => {
  // This causes issues in Fastify
});

// CORRECT: Don't use await when registering content type parsers
fastify.addContentTypeParser('application/json', async (req, body) => {
  // Proper usage without await
});
```

When decorating reply methods, ensure they return values for proper chaining:

```typescript
// INCORRECT: Missing return value
fastify.decorateReply('sendSuccess', function (data) {
  this.send({ success: true })
})

// CORRECT: Return this for chaining
fastify.decorateReply('sendSuccess', function (data) {
  return this.send({ success: true })
})
```

If using ESLint with `no-floating-promises`, configure exceptions for Fastify-specific promise patterns to avoid unnecessary warnings.