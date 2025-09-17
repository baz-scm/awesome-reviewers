---
title: Avoid hardcoded configuration values
description: Configuration values should not be hardcoded in the source code. Instead,
  they should be externalized to configuration files, environment variables, or made
  configurable through application settings. This improves maintainability, allows
  for environment-specific customization, and prevents deployment issues.
repository: juspay/hyperswitch
label: Configurations
language: Rust
comments_count: 6
repository_stars: 34028
---

Configuration values should not be hardcoded in the source code. Instead, they should be externalized to configuration files, environment variables, or made configurable through application settings. This improves maintainability, allows for environment-specific customization, and prevents deployment issues.

Common examples of values that should be configurable:
- Timeout durations and retry intervals
- Buffer times and scheduling delays  
- Currency lists and supported payment methods
- URL endpoints and connection strings
- Feature-specific thresholds and limits

Example of problematic hardcoded values:
```rust
// Bad: Hardcoded timeout
tokio::time::sleep(tokio::time::Duration::from_secs(3)).await;

// Bad: Hardcoded buffer time  
schedule_time + time::Duration::minutes(15)

// Bad: Hardcoded currency check
if option.price.currency_code != common_enums::Currency::USD {
```

Example of proper configuration approach:
```rust
// Good: Configurable timeout
let timeout = config.superposition.initialization_timeout_secs;
tokio::time::sleep(tokio::time::Duration::from_secs(timeout)).await;

// Good: Configurable buffer time
let buffer_minutes = config.revenue_recovery.calculate_workflow_buffer_minutes;
schedule_time + time::Duration::minutes(buffer_minutes)

// Good: Configurable supported currencies
let supported_currencies = &config.amazon_pay.supported_currencies;
if !supported_currencies.contains(&option.price.currency_code) {
```

When reviewing code, look for magic numbers, hardcoded strings, and fixed values that could vary between environments or should be tunable by operators. Require these to be moved to appropriate configuration structures with sensible defaults.