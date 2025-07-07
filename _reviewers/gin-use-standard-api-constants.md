---
title: Use standard API constants
description: Always use standard library constants for HTTP methods and status codes
  rather than string literals or numeric values. This improves code readability, prevents
  typos, and makes it easier to maintain API consistency.
repository: gin-gonic/gin
label: API
language: Go
comments_count: 3
repository_stars: 83022
---

Always use standard library constants for HTTP methods and status codes rather than string literals or numeric values. This improves code readability, prevents typos, and makes it easier to maintain API consistency.

For HTTP methods:
```go
// Incorrect
switch method {
  case "GET":
    return blue
  case "POST":
    return cyan
  case "DELETE":
    return red
  // ...
}

// Correct
switch method {
  case http.MethodGet:
    return blue
  case http.MethodPost:
    return cyan
  case http.MethodDelete:
    return red
  // ...
}
```

For status codes:
```go
// Incorrect
c.ProtoBuf(201, data)

// Correct
c.ProtoBuf(http.StatusCreated, data)
```

Similarly, keep references to standards (like RFCs) current in code comments and documentation. For example, update content negotiation references from RFC 2616 to the more current RFC 7231 section 5.3.2.

This practice improves code maintainability, leverages compiler checking, provides better IDE support, and ensures your API follows widely accepted conventions.