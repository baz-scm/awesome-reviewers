---
title: Use structured logging fields
description: Always use structured logging with descriptive field names rather than
  string interpolation. Include relevant context variables such as identifiers, durations,
  and parameters to make logs more useful for debugging and monitoring. This practice
  makes logs more searchable, filterable, and easier to analyze.
repository: influxdata/influxdb
label: Logging
language: Rust
comments_count: 4
repository_stars: 30268
---

Always use structured logging with descriptive field names rather than string interpolation. Include relevant context variables such as identifiers, durations, and parameters to make logs more useful for debugging and monitoring. This practice makes logs more searchable, filterable, and easier to analyze.

```rust
// Bad: String interpolation lacks structured fields
info!("Created new instance id {:?}", instance_id);
error!("Error splitting table buffer: {}", e);

// Good: Structured logging with descriptive field names
info!(instance_id = ?instance_id, "catalog not found, creating new instance id");
error!(error = %e, table = %table_name, db = %db_name, "Error splitting table buffer for persistence");
```

When logging errors, use descriptive field names like `error` rather than single-letter variables to improve log readability. For logging important operations, include all relevant parameters to provide context for later analysis.