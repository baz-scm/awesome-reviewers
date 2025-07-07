---
title: Use standard HTTP constants
description: Always use the standard HTTP status constants from the `http` package
  instead of raw numeric values in your networking code. This practice improves code
  readability, maintainability, and helps prevent errors when working with HTTP responses.
repository: gin-gonic/gin
label: Networking
language: Go
comments_count: 2
repository_stars: 83022
---

Always use the standard HTTP status constants from the `http` package instead of raw numeric values in your networking code. This practice improves code readability, maintainability, and helps prevent errors when working with HTTP responses.

For example, instead of:
```go
writer.WriteHeader(500)
c.AsciiJSON(204, []string{"lang", "Go语言"})
```

Use the semantic constants:
```go
writer.WriteHeader(http.StatusInternalServerError)
c.AsciiJSON(http.StatusNoContent, []string{"lang", "Go语言"})
```

This approach makes your code more descriptive and self-documenting. It also ensures consistency across the codebase and makes it easier for other developers to understand the HTTP status codes being used without having to memorize numeric values.