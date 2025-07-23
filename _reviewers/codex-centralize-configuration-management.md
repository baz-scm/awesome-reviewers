---
title: Centralize configuration management
description: Prefer centralized configuration objects over environment variables for
  application settings. Environment variables create inconsistent configuration sources
  and can lead to maintenance challenges.
repository: openai/codex
label: Configurations
language: Rust
comments_count: 5
repository_stars: 31275
---

Prefer centralized configuration objects over environment variables for application settings. Environment variables create inconsistent configuration sources and can lead to maintenance challenges.

Guidelines:
- Use a single, centralized `Config` structure as the "one true way" to configure your application
- When adding new settings, place them in the appropriate configuration structure rather than reading from environment variables
- Reserve environment variables primarily for bootstrap settings or when absolutely required

For feature flags or experimental options, use structured configuration with appropriate prefixes:
```rust
// Preferred
config.experimental_resume = true;

// Instead of
if std::env::var("CODEX_EXPERIMENTAL_RESUME").is_ok() { ... }
```

When environment variables must be used:
- Load them as early as possible in the application lifecycle before any threads are created
- Document the thread-safety implications clearly
- In tests, configure components explicitly rather than modifying process-wide environment variables

Remember that modifying environment variables is inherently racy in multi-threaded contexts and has been marked as `unsafe` in recent Rust editions.