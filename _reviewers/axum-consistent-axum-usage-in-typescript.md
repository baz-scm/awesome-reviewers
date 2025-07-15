---
title: "Consistent axum Usage in TypeScript"
description: "When implementing TypeScript code that uses the axum package, maintain consistent and idiomatic usage: always use lowercase 'axum', leverage axum's built-in types correctly, follow best practices for state and dependencies, ensure proper error handling, and use routing and middleware features effectively."
repository: "tokio-rs/axum"
label: "Axum"
language: "TypeScript"
comments_count: 5
repository_stars: 22100
---

When implementing TypeScript code that uses the axum package, maintain consistent and idiomatic usage:

1. Always use the lowercase "axum" when referring to the framework, not "Axum".
2. Leverage axum's built-in types and utilities correctly, such as `Router`, `Middleware`, and `RequestBody`.
3. Follow best practices for handling state and dependencies in axum applications, such as using `task_local` to pass state between middleware and handlers.
4. Ensure error handling is properly implemented, with clear and informative error messages returned to clients.
5. Use axum's routing and middleware features effectively to structure your application, avoiding overly complex or nested routing.

Example of correct axum usage in TypeScript:

```typescript
import { Router, RequestBody } from '@awslabs/aws-lambda-typescript-runtime';

const router = new Router();

router.get('/', (req) => {
  return { message: 'Hello, axum!' };
});

router.post('/users', async (req: RequestBody<{ name: string }>) => {
  const { name } = req.body;
  // Handle user creation logic here
  return { id: 1, name };
});

export default router;