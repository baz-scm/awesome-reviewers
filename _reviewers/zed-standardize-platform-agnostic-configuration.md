---
title: Standardize platform-agnostic configuration
description: 'Ensure configuration handling is consistent and platform-agnostic by
  following these guidelines:


  1. Use environment variables with fallbacks:

  ```rust'
repository: zed-industries/zed
label: Configurations
language: Rust
comments_count: 10
repository_stars: 62119
---

Ensure configuration handling is consistent and platform-agnostic by following these guidelines:

1. Use environment variables with fallbacks:
```rust
// Good
let sample_count = std::env::var("ZED_SAMPLE_COUNT")
    .or_else(|_| std::env::var("ZED_PATH_SAMPLE_COUNT"))
    .unwrap_or_default();

// Bad
let sample_count = std::env::var("ZED_SAMPLE_COUNT").unwrap_or_default();
```

2. Implement proper default values using serde attributes:
```rust
#[derive(Deserialize)]
pub struct Config {
    #[serde(default = "default_true")]
    pub enabled: bool,
    
    #[serde(default)]
    pub custom_path: String,
}
```

3. Use platform-agnostic paths and commands:
```rust
// Good
let config_dir = dirs::config_dir()
    .or_else(|| std::env::var_os("XDG_CONFIG_HOME")
    .map(PathBuf::from));

// Bad
let config_dir = PathBuf::from("/usr/local/etc");
```

4. Provide clear validation for configuration:
- Validate all required fields
- Include schema documentation
- Support cross-platform paths
- Handle missing values gracefully

5. Allow configuration overrides through multiple layers:
- Environment variables
- User configuration files
- System defaults
- Platform-specific defaults

This ensures configurations work consistently across different platforms while maintaining flexibility and robustness.