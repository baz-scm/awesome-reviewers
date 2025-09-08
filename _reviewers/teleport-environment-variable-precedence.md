---
title: Environment variable precedence
description: When working with environment variables in configuration management,
  ensure proper precedence handling and use clean fallback patterns. Environment variables
  can be inherited by subprocesses unexpectedly, potentially overriding command-line
  flags or other configuration sources.
repository: gravitational/teleport
label: Configurations
language: Go
comments_count: 2
repository_stars: 19109
---

When working with environment variables in configuration management, ensure proper precedence handling and use clean fallback patterns. Environment variables can be inherited by subprocesses unexpectedly, potentially overriding command-line flags or other configuration sources.

Key practices:
1. **Explicit precedence control**: When spawning subprocesses, explicitly control which environment variables are passed to prevent unintended inheritance that could override intended configuration
2. **Clean fallback patterns**: Use utilities like `cmp.Or()` for cleaner environment variable fallback chains instead of verbose loops

Example of clean fallback pattern:
```go
// Instead of verbose loops:
editor := "vi"
for _, v := range []string{"TELEPORT_EDITOR", "VISUAL", "EDITOR"} {
    if value := os.Getenv(v); value != "" {
        editor = value
        break
    }
}

// Use clean fallback:
editor := cmp.Or(os.Getenv("TELEPORT_EDITOR"), os.Getenv("VISUAL"), os.Getenv("EDITOR"), "vi")
```

This prevents configuration conflicts where subprocess environment variables might override parent process flags, and makes environment variable fallback logic more readable and maintainable.