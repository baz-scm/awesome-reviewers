---
title: Use established logging libraries
description: Avoid using print statements (println!, eprintln!) or custom logging
  implementations for application logging. Instead, use established logging libraries
  like `tracing` that provide proper log levels, structured output, and configurable
  destinations.
repository: block/goose
label: Logging
language: Rust
comments_count: 2
repository_stars: 19037
---

Avoid using print statements (println!, eprintln!) or custom logging implementations for application logging. Instead, use established logging libraries like `tracing` that provide proper log levels, structured output, and configurable destinations.

Print statements bypass logging configuration and cannot be controlled at runtime. Custom logging implementations are error-prone and lack the features of mature libraries. Established logging libraries offer better performance, structured data support, and integration with monitoring systems.

Replace debug prints with appropriate log levels:

```rust
// Instead of this:
println!("🔒 SecurityManager::new() called - checking if security should be enabled");

// Use this:
tracing::debug!("SecurityManager::new() called - checking if security should be enabled");
```

For custom logging needs, extend existing logging infrastructure rather than creating new implementations:

```rust
// Instead of rolling your own:
pub fn log_debug_event(event: &str) {
    // custom file writing logic...
}

// Use tracing with appropriate configuration:
tracing::debug!(event = %event, "debug event occurred");
```

This ensures consistent logging behavior, proper log level control, and integration with the application's logging configuration.