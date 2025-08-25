---
title: avoid environment variable proliferation
description: Prefer the consolidated config system over adding new environment variables.
  Environment variables should only be used for deployment-specific overrides, not
  as the primary configuration mechanism.
repository: block/goose
label: Configurations
language: Rust
comments_count: 6
repository_stars: 19037
---

Prefer the consolidated config system over adding new environment variables. Environment variables should only be used for deployment-specific overrides, not as the primary configuration mechanism.

**Guidelines:**
- Use the existing `Config::global().get_param()` system for new configuration options
- Pass configuration values as explicit parameters to functions rather than accessing global config deep in the call stack
- Environment variables should override config file values, maintaining consistent precedence
- Avoid adding new `GOOSE_*` environment variables unless absolutely necessary for deployment scenarios

**Example:**
```rust
// ❌ Avoid: Adding new environment variables
const GOOSE_RECIPE_RETRY_TIMEOUT_SECONDS: &str = "GOOSE_RECIPE_RETRY_TIMEOUT_SECONDS";

fn get_retry_timeout(retry_config: &RetryConfig) -> Duration {
    let timeout_seconds = env::var(GOOSE_RECIPE_RETRY_TIMEOUT_SECONDS)
        .ok()
        .and_then(|s| s.parse().ok())
        .unwrap_or(DEFAULT_RETRY_TIMEOUT_SECONDS);
    Duration::from_secs(timeout_seconds)
}

// ✅ Prefer: Use config system with parameter passing
fn get_retry_timeout(retry_config: &RetryConfig, config_timeout: Option<u64>) -> Duration {
    let timeout_seconds = retry_config.timeout_seconds
        .or(config_timeout)
        .unwrap_or(DEFAULT_RETRY_TIMEOUT_SECONDS);
    Duration::from_secs(timeout_seconds)
}

// At call site:
let config = Config::global();
let timeout = config.get_param("RETRY_TIMEOUT_SECONDS").unwrap_or(DEFAULT_RETRY_TIMEOUT_SECONDS);
get_retry_timeout(&retry_config, Some(timeout))
```

This approach reduces environment variable sprawl while maintaining flexibility for deployment-specific configuration through the existing config system.