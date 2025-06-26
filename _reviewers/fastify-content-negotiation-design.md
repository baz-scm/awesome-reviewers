---
title: "Content negotiation design"
description: "When building APIs, implement proper content negotiation to handle various media types in both requests and responses. This ensures your API can work with different client requirements and maintain compatibility with diverse ecosystems."
repository: "fastify/fastify"
label: "API"
language: "JavaScript"
comments_count: 4
repository_stars: 34000
---

When building APIs, implement proper content negotiation to handle various media types in both requests and responses. This ensures your API can work with different client requirements and maintain compatibility with diverse ecosystems.

Key practices include:

1. Explicitly define and check content types for requests
2. Implement content type-specific validation schemas
3. Handle different response formats appropriately (JSON, streams, buffers)
4. Support both native and polyfill implementations of web standards

For example, when defining route schemas with content-specific validation:

```js
fastify.post('/', {
  schema: {
    body: {
      content: {
        'application/json': {
          schema: jsonSchema
        },
        'application/octet-stream': {
          schema: binarySchema
        }
      }
    }
  }
})
```

When handling response objects, avoid tight coupling to specific implementations:

```js
// Instead of:
if (payload instanceof Response) {
  // handle response
}

// Prefer more flexible detection:
if (
  // node:stream
  typeof payload.pipe === 'function' ||
  // node:stream/web
  typeof payload.getReader === 'function' ||
  // Response (works with polyfills too)
  Object.prototype.toString.call(payload) === '[object Response]'
) {
  // handle response
}
```

This approach enables your API to work correctly with various clients and frameworks while maintaining a clean, standards-compliant design.