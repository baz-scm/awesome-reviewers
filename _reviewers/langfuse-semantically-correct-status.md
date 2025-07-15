---
title: Semantically correct status
description: Use HTTP status codes that accurately reflect the outcome of API operations.
  This improves API clarity and allows client applications to handle responses more
  intelligently.
repository: langfuse/langfuse
label: API
language: TypeScript
comments_count: 3
repository_stars: 13574
---

Use HTTP status codes that accurately reflect the outcome of API operations. This improves API clarity and allows client applications to handle responses more intelligently.

- Use 201 (Created) for successful resource creation
- Use 200 (OK) for successful updates or retrievals
- Use 409 (Conflict) for duplicate resource errors, not 404 (Not Found)
- Use 202 (Accepted) for operations that will be processed asynchronously

Example for duplicate resources:
```diff
// For duplicate resource detection:
- expect(response.status).toBe(404);
+ expect(response.status).toBe(409);
```

Example for asynchronous processing:
```javascript
PATCH: createAuthedAPIRoute({
  name: "Update Single Trace",
  // ...
  fn: async ({ query, body, auth }) => {
    // Process the request...
    
    // Return 202 Accepted for async processing
    return { status: 202, body: { 
      message: "Update accepted and will be processed" 
    }};
  }
})
```