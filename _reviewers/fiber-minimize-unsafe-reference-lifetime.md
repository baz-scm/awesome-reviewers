---
title: minimize unsafe reference lifetime
description: When working with methods that return potentially unsafe references or
  data that could become invalid, pass the results directly to safety/copy methods
  rather than storing them in intermediate variables. This minimizes the lifetime
  of unsafe references and reduces the risk of using invalidated data.
repository: gofiber/fiber
label: Null Handling
language: Markdown
comments_count: 2
repository_stars: 37560
---

When working with methods that return potentially unsafe references or data that could become invalid, pass the results directly to safety/copy methods rather than storing them in intermediate variables. This minimizes the lifetime of unsafe references and reduces the risk of using invalidated data.

Intermediate variables that hold unsafe references extend their lifetime unnecessarily and create additional opportunities for null reference errors or use-after-free scenarios.

```go
// Avoid - extends lifetime of unsafe reference
name := c.Cookies("name")  // unsafe reference stored
safe := c.CopyString(name) // used later

// Prefer - immediate safety conversion
safe := c.CopyString(c.Cookies("name"))

// Avoid - extends lifetime of unsafe reference  
body := c.Body()           // unsafe reference stored
safe := c.CopyBytes(body)  // used later

// Prefer - immediate safety conversion
safe := c.CopyBytes(c.Body())
```

This pattern is especially important when working with frameworks or APIs that explicitly warn about reference validity, such as Fiber's context methods that are "only valid within the handler."