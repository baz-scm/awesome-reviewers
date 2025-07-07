---
title: Method chaining for clarity
description: Design API methods that favor chaining over multiple parameters to improve
  readability and maintainability. When implementing methods that require both a resource
  and configuration options (like status codes), prefer method chaining patterns that
  clearly separate concerns and make the purpose of each parameter explicit.
repository: expressjs/express
label: API
language: Markdown
comments_count: 2
repository_stars: 67300
---

Design API methods that favor chaining over multiple parameters to improve readability and maintainability. When implementing methods that require both a resource and configuration options (like status codes), prefer method chaining patterns that clearly separate concerns and make the purpose of each parameter explicit.

**Example - Avoid:**
```javascript
// Unclear parameter order and purpose
res.json(obj, status);
res.send(body, status);
```

**Example - Prefer:**
```javascript
// Clear separation of concerns through method chaining
res.status(status).json(obj);
res.status(status).send(body);
```

This pattern improves API usability by making method calls self-documenting, reducing the need to remember parameter order, and creating more intuitive interfaces for developers. It also allows for more flexible extension of the API in the future without breaking changes to parameter signatures.