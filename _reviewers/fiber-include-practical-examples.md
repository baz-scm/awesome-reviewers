---
title: Include practical examples
description: Documentation should include practical, working examples that demonstrate
  real-world usage scenarios. When introducing new features, methods, or concepts,
  provide concrete code examples that show users how to apply them in practice. This
  is especially important when mentioning functionality multiple times without demonstration,
  or when documenting complex...
repository: gofiber/fiber
label: Documentation
language: Markdown
comments_count: 4
repository_stars: 37560
---

Documentation should include practical, working examples that demonstrate real-world usage scenarios. When introducing new features, methods, or concepts, provide concrete code examples that show users how to apply them in practice. This is especially important when mentioning functionality multiple times without demonstration, or when documenting complex features that users need to understand to adopt effectively.

Examples should be complete and runnable where possible, showing both the setup and expected output. For features with multiple use cases or configuration options, demonstrate the differences with separate examples.

```go
// Good: Shows practical usage with complete example
func (r *Request) Headers() iter.Seq2[string, []string]

// Example demonstrating real usage
req := client.AcquireRequest()
req.AddHeader("Content-Type", "application/json")
req.AddHeader("Authorization", "Bearer token123")

// Collect all headers into a map
headers := maps.Collect(req.Headers())
for key, values := range headers {
    fmt.Printf("Header: %s = %v\n", key, values)
}
```

The principle "only a feature that is understandable and well documented will be found and used" should guide documentation decisions. Users need to see how features work in context, not just understand their signatures or theoretical capabilities.