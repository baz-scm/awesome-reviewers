---
title: "Explicit Configuration Usage in Fastify"
description: "When using the Fastify framework in TypeScript, ensure that all configuration options are explicitly declared and properly documented. This includes clearly defining all required configuration parameters, explicitly specifying any configuration constraints or mutually exclusive options, and providing comprehensive examples."
repository: "fastify/fastify"
label: "Fastify"
language: "TypeScript"
comments_count: 5
repository_stars: 34000
---

When using the Fastify framework in TypeScript, ensure that all configuration options are explicitly declared and properly documented. This includes:

1. Clearly defining all required configuration parameters, including their data types and default values (with units where applicable).
2. Explicitly specifying any configuration constraints or mutually exclusive options.
3. Providing comprehensive examples that demonstrate the correct usage of Fastify configuration settings.

**Example - Poor Usage:**
```typescript
// Unclear timeout setting with no units
const fastify = Fastify({
  http2SessionTimeout: 72000 
});

// Incomplete schema definition
fastify.get('/route', {
  schema: {
    querystring: { name: { type: 'string' } }
  }
});
```

**Example - Recommended Usage:**
```typescript
// Clear timeout setting with units
const fastify = Fastify({
  http2SessionTimeout: 72000 // Timeout in milliseconds for HTTP/2 sessions
});

// Fully defined schema requirements
fastify.get('/route', {
  schema: {
    querystring: {
      type: 'object',
      properties: {
        name: { type: 'string' }
      },
      required: ['name']
    }
  }
});
```

By following these guidelines, you can ensure that your Fastify-based applications are properly configured and documented, reducing the risk of user confusion and configuration errors.