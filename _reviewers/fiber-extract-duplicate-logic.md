---
title: Extract duplicate logic
description: When code blocks become large or contain repetitive patterns, extract
  them into separate functions to improve readability and maintainability. This follows
  Clean Code principles of keeping functions short and focused on single responsibilities.
repository: gofiber/fiber
label: Code Style
language: Go
comments_count: 6
repository_stars: 37560
---

When code blocks become large or contain repetitive patterns, extract them into separate functions to improve readability and maintainability. This follows Clean Code principles of keeping functions short and focused on single responsibilities.

Key indicators for extraction:
- Configuration setup blocks that have grown large
- Identical or nearly identical code patterns across multiple locations
- Functions that handle multiple concerns or have grown beyond a reasonable size
- Repetitive error handling or validation logic

Example of extracting configuration logic:
```go
// Before: Large configuration block in main function
func (r *Redirect) Route(name string, config ...RedirectConfig) error {
    cfg := RedirectConfig{CookieConfig: CookieConfigDefault}
    if len(config) > 0 {
        cfg = config[0]
    }
    if cfg.CookieConfig == (CookieConfig{}) {
        cfg.CookieConfig = CookieConfigDefault
    }
    // ... more configuration logic
}

// After: Extract to dedicated function
func (r *Redirect) Route(name string, config ...RedirectConfig) error {
    cfg := r.buildConfig(config...)
    // ... rest of route logic
}

func (r *Redirect) buildConfig(config ...RedirectConfig) RedirectConfig {
    cfg := RedirectConfig{CookieConfig: CookieConfigDefault}
    if len(config) > 0 {
        cfg = config[0]
    }
    // ... configuration logic
    return cfg
}
```

Example of extracting duplicate logic:
```go
// Before: Duplicate proxy logic
func Do(c *fiber.Ctx, addr string, clients ...*fasthttp.Client) error {
    // ... setup code
    return cli.Do(req, res)
}

func DoRedirects(c *fiber.Ctx, addr string, maxRedirects int, clients ...*fasthttp.Client) error {
    // ... identical setup code
    return cli.DoRedirects(req, res, maxRedirects)
}

// After: Extract common logic
func do(c *fiber.Ctx, addr string, action func(*fasthttp.Client, *fasthttp.Request, *fasthttp.Response) error, clients ...*fasthttp.Client) error {
    // ... common setup code
    return action(cli, req, res)
}
```

This practice reduces code duplication, makes functions easier to test, and improves overall code organization.