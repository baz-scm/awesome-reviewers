---
title: Preserve security configurations
description: 'Always respect explicitly set security attributes and properly sanitize
  user inputs to prevent security vulnerabilities. When modifying security-related
  configurations:'
repository: gin-gonic/gin
label: Security
language: Go
comments_count: 2
repository_stars: 83022
---

Always respect explicitly set security attributes and properly sanitize user inputs to prevent security vulnerabilities. When modifying security-related configurations:

1. Only apply default values when the attribute is not explicitly set
2. Thoroughly validate and sanitize URL paths and other user inputs to prevent path traversal attacks

**Example 1:** When handling cookie security attributes:
```go
// Good: Only override SameSite when not explicitly set
if cookie.SameSite == http.SameSiteDefaultMode {
    cookie.SameSite = c.sameSite
}

// Bad: Unconditionally overriding security attributes
cookie.SameSite = c.sameSite
```

**Example 2:** For URL path sanitization:
```go
// Good: Initialize regex patterns once, outside of functions
var pathSanitizer = regexp.MustCompile("[^a-zA-Z0-9/-]+")

// Use the pre-compiled pattern to sanitize paths
sanitizedPath := pathSanitizer.ReplaceAllString(path, "")
```

Properly preserving security configurations and sanitizing inputs helps prevent CSRF, XSS, and path traversal vulnerabilities.