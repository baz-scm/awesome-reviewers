---
title: Validate configuration defaults
description: Configuration structs should validate input values and provide sensible
  defaults that work well in production environments. Always check for invalid values
  (like negative timeouts), provide reasonable defaults for production use cases,
  and handle edge cases where users might set unexpected values.
repository: gofiber/fiber
label: Configurations
language: Go
comments_count: 4
repository_stars: 37560
---

Configuration structs should validate input values and provide sensible defaults that work well in production environments. Always check for invalid values (like negative timeouts), provide reasonable defaults for production use cases, and handle edge cases where users might set unexpected values.

Key practices:
- Validate negative or invalid values and reset to defaults
- Choose production-ready defaults (e.g., 10s timeout instead of infinite)
- Handle empty string cases appropriately for string configuration fields
- Consider security implications of default values (e.g., file permissions)

Example from timeout middleware:
```go
func configDefault(config ...Config) Config {
    cfg := config[0]
    
    // Validate negative timeout values
    if cfg.Timeout < 0 {
        cfg.Timeout = ConfigDefault.Timeout
    }
    
    // Use production-ready defaults
    if cfg.ShutdownTimeout == 0 {
        cfg.ShutdownTimeout = 10 * time.Second // Instead of infinite
    }
    
    return cfg
}
```

This ensures configurations work reliably across different environments and prevents common misconfigurations that could cause issues in production.