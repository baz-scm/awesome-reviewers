---
title: REST principles first
description: 'When designing APIs with Express, prioritize proper REST principles
  and HTTP semantics over convenience. This ensures your API is predictable, standards-compliant,
  and maintainable:'
repository: expressjs/express
label: API
language: JavaScript
comments_count: 5
repository_stars: 67300
---

When designing APIs with Express, prioritize proper REST principles and HTTP semantics over convenience. This ensures your API is predictable, standards-compliant, and maintainable:

1. **Use appropriate HTTP verbs** for different operations:
   - GET for retrieval
   - POST for creation
   - PUT for complete entity updates
   - PATCH for partial updates
   - DELETE for removal

```javascript
// Implement both PUT and PATCH for different update scenarios
router.put('/:id', controller.replaceEntity.bind(controller));    // Full entity replacement
router.patch('/:id', controller.updateFields.bind(controller));   // Partial update
```

2. **Handle HTTP headers correctly**:
   - Respect existing Content-Type headers before applying defaults
   - Follow established patterns for setting headers (use `res.type()` where appropriate)
   - Handle Link headers according to RFC specifications
   - Process Accept headers intelligently, considering priorities

3. **Follow consistent response patterns**:
   - Use `res.status()` with appropriate status codes (200 OK, 201 Created, 204 No Content)
   - For error responses, use semantic status codes (400 Bad Request, 404 Not Found)
   - Use `res.sendStatus()` for simple status-only responses

Remember that proper HTTP semantics help clients understand your API intuitively without requiring extensive documentation for basic operations.