---
title: justified nolint exceptions
description: When style linters cannot be applied universally across a codebase due
  to architectural constraints or legitimate use cases, use targeted `//nolint` comments
  with clear explanations rather than disabling the linter entirely. This approach
  maintains code style standards while allowing necessary exceptions.
repository: gofiber/fiber
label: Code Style
language: Yaml
comments_count: 2
repository_stars: 37560
---

When style linters cannot be applied universally across a codebase due to architectural constraints or legitimate use cases, use targeted `//nolint` comments with clear explanations rather than disabling the linter entirely. This approach maintains code style standards while allowing necessary exceptions.

For example, when a linter like `interfacebloat` conflicts with a core interface design, apply a specific exemption:
```go
//nolint:interfacebloat // Ignore fiber.Ctx - core interface requires many methods
type Ctx interface {
    // ... many methods
}
```

Similarly, for packages that are dangerous but sometimes necessary:
```go
//nolint:depguard // Using unsafe for performance-critical memory operations
import "unsafe"
```

This strategy preserves the value of style linters by catching violations in most of the codebase while providing documented exceptions where the rules don't apply. Each exception should include a brief explanation of why the violation is justified, making the codebase more maintainable and helping future developers understand the reasoning behind style rule exceptions.