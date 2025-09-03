---
title: Update documentation proactively
description: When code behavior changes, new features are added, or potential usage
  pitfalls are identified, proactively update all relevant documentation including
  API docs, inline comments, and usage warnings. This ensures developers have accurate
  information about execution order, blocking operations, and proper usage patterns.
repository: gofiber/fiber
label: Documentation
language: Go
comments_count: 3
repository_stars: 37560
---

When code behavior changes, new features are added, or potential usage pitfalls are identified, proactively update all relevant documentation including API docs, inline comments, and usage warnings. This ensures developers have accurate information about execution order, blocking operations, and proper usage patterns.

Key areas requiring documentation updates:
- Behavioral changes (e.g., execution order modifications)
- New public methods and their purpose
- Usage warnings for blocking operations or common pitfalls
- Migration notes when functionality is moved or refactored

Example from the codebase:
```go
// Important: app.Listen() must be called in a separate goroutine, otherwise shutdown hooks will not work
// as Listen() is a blocking operation. Example:
//
//	go app.Listen(":3000")
//	// ...
```

This proactive approach prevents confusion, reduces support burden, and improves the overall developer experience by keeping documentation synchronized with code reality.