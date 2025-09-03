---
title: prefer existing APIs
description: When adding new functionality, prioritize reusing existing methods and
  interfaces rather than creating new ones. This maintains API consistency, reduces
  cognitive load for developers, and prevents unnecessary duplication.
repository: gofiber/fiber
label: API
language: Go
comments_count: 6
repository_stars: 37560
---

When adding new functionality, prioritize reusing existing methods and interfaces rather than creating new ones. This maintains API consistency, reduces cognitive load for developers, and prevents unnecessary duplication.

Before introducing new methods or interfaces, evaluate whether existing APIs can be extended or composed to achieve the same goal. Consider method chaining, variadic parameters, or interface composition as alternatives to separate implementations.

Example of preferred approach:
```go
// Instead of creating a separate CustomJSON method
func (c *Ctx) CustomJSON(data interface{}, ctype string) error {
    err := c.JSON(data)
    if err != nil {
        return err
    }
    c.fasthttp.Response.Header.SetContentType(ctype)
    return nil
}

// Or better yet, extend existing method with variadic params
func (c *Ctx) JSON(data interface{}, ctype ...string) error {
    raw, err := c.app.config.JSONEncoder(data)
    if err != nil {
        return err
    }
    c.fasthttp.Response.SetBodyRaw(raw)
    
    if len(ctype) > 0 {
        c.fasthttp.Response.Header.SetContentType(ctype[0])
    } else {
        c.fasthttp.Response.Header.SetContentType(MIMEApplicationJSON)
    }
    return nil
}
```

Similarly, prefer existing interfaces like `fiber.Storage` over creating new specialized interfaces when the existing interface provides sufficient functionality, even if some methods remain unused.