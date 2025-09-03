---
title: Use context for configuration
description: When accessing application state or configuration within request handlers,
  always use the context method `c.App().State()` instead of direct app instance references.
  This pattern ensures proper context isolation, supports dependency injection, and
  works correctly in multi-file applications where the app instance may not be directly
  accessible.
repository: gofiber/fiber
label: Configurations
language: Markdown
comments_count: 4
repository_stars: 37560
---

When accessing application state or configuration within request handlers, always use the context method `c.App().State()` instead of direct app instance references. This pattern ensures proper context isolation, supports dependency injection, and works correctly in multi-file applications where the app instance may not be directly accessible.

Direct app references create tight coupling and break when handlers are moved to separate files or packages. The context-aware approach maintains loose coupling and follows proper architectural patterns.

**Example:**

```go
// ❌ Avoid: Direct app reference
app.Get("/config", func(c fiber.Ctx) error {
    config := map[string]any{
        "apiUrl": fiber.GetStateWithDefault(app.State(), "apiUrl", ""),
        "debug":  fiber.GetStateWithDefault(app.State(), "debug", false),
    }
    return c.JSON(config)
})

// ✅ Prefer: Context-aware access
app.Get("/config", func(c fiber.Ctx) error {
    config := map[string]any{
        "apiUrl": fiber.GetStateWithDefault(c.App().State(), "apiUrl", ""),
        "debug":  fiber.GetStateWithDefault(c.App().State(), "debug", false),
    }
    return c.JSON(config)
})
```

This pattern is especially important when handlers are defined in separate packages or when using dependency injection, as it ensures configuration access works regardless of the application's structure.