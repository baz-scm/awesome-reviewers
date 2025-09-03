---
title: API design clarity
description: Maintain clear separation of concerns in API design by avoiding feature
  overlap and ensuring each method has a distinct, well-defined purpose. When designing
  APIs, resist the temptation to add convenience features that blur the boundaries
  between different configuration approaches, as this leads to user confusion and
  maintenance issues.
repository: gofiber/fiber
label: API
language: Markdown
comments_count: 2
repository_stars: 37560
---

Maintain clear separation of concerns in API design by avoiding feature overlap and ensuring each method has a distinct, well-defined purpose. When designing APIs, resist the temptation to add convenience features that blur the boundaries between different configuration approaches, as this leads to user confusion and maintenance issues.

Key principles:
- Each API method should have a single, clear responsibility
- Avoid duplicating functionality across different configuration mechanisms
- When evolving APIs, prefer generic approaches over multiple specific functions
- Consider the conceptual clarity of the API from the user's perspective

For example, when designing middleware configuration:

```go
// Clear separation: route-specific timeout
app.Get("/api/reports", timeout.New(30*time.Second), handler)

// Clear separation: application-wide timeout configuration  
app.Use(timeout.NewWithConfig(timeout.Config{
    DefaultTimeout: 5 * time.Second,
}))

// Avoid: mixing route-specific config within middleware config
// This creates confusion about which timeout value actually applies
app.Get("/reports", timeout.New(handler, timeout.Config{
    Timeout: 5 * time.Second,
    Routes: map[string]time.Duration{
        "/reports": 30 * time.Second, // Confusing overlap
    },
}))
```

Similarly, when evolving APIs, prefer generic solutions that replace multiple specific functions rather than maintaining both approaches, as this reduces cognitive load and maintenance burden.