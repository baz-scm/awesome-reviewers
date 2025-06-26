---
title: "Type-safe API designs"
description: "Design APIs with strong type safety to improve developer experience and catch errors at compile time. Avoid using any types when possible, carefully order generic parameters to support type inference, and ensure return types accurately reflect API behavior."
repository: "fastify/fastify"
label: "API"
language: "TypeScript"
comments_count: 5
repository_stars: 34000
---

Design APIs with strong type safety to improve developer experience and catch errors at compile time. Avoid using `any` types when possible, carefully order generic parameters to support type inference, and ensure return types accurately reflect API behavior.

When designing APIs with generic parameters:
1. Consider how type inference will work for users of your API
2. Place automatically inferable parameters last in generic lists
3. Ensure return types accurately reflect response possibilities

For example, when defining route handlers that can return different response types:

```typescript
// Good: Strong typing for status codes and responses
server.get<{
  Reply: {
    200: string | { msg: string }
    400: number
    '5xx': { error: string }
  }
}>(
  '/',
  async (_, res) => {
    const option = 1 as 1 | 2 | 3 | 4
    switch (option) {
      case 1: return 'hello'               // typed as 200 response
      case 2: return { msg: 'hello' }      // typed as 200 response
      case 3: return 400                   // typed as 400 response
      case 4: return { error: 'error' }    // typed as 5xx response
    }
  }
)

// Bad: Using 'any' types or improper generic ordering that breaks type inference
function badExample<T = any>(req: any): any {
  // Types are lost, errors not caught until runtime
  return req.data;
}
```

When testing types, verify that constraints work as expected by explicitly checking the type constraints with test assertions.