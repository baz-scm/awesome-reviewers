---
title: Follow API conventions
description: 'Design APIs following modern conventions and best practices to improve
  usability, maintainability, and consistency across your codebase. APIs should prioritize:'
repository: influxdata/influxdb
label: API
language: Rust
comments_count: 6
repository_stars: 30268
---

Design APIs following modern conventions and best practices to improve usability, maintainability, and consistency across your codebase. APIs should prioritize:

1. **Use intuitive method naming** that clearly expresses purpose and follows a consistent pattern:

```rust
// Instead of:
.query_sql("foo").with_query("SELECT * FROM bar")

// Prefer:
.query("foo").with_sql("SELECT * FROM bar")
```

2. **Reuse existing functionality** rather than reimplementing similar features:

```rust
// Instead of:
let now = self.time_provider.now().timestamp_nanos();
Some(now - retention_period as i64)

// Prefer:
self.time_provider.now().checked_sub(Duration::nanoseconds(retention_period))
```

3. **Leverage library conveniences** for cleaner API construction:

```rust
// Instead of:
let db_query_param = format!("db={}", db.into());
let mut url = self.base_url.join(api_path)?;
url.set_query(Some(&db_query_param));
let mut req = self.http_client.delete(url);

// Prefer:
let mut url = self.base_url.join(api_path)?;
let mut req = self.http_client.delete(url).query(&[("db", db.as_ref())]);
```

4. **Standardize types across API boundaries** to maintain consistency:

```rust
// Instead of duplicating types in multiple crates:
// influxdb3_client::Precision and influxdb3_server::Precision

// Consider moving shared types to a common crate or re-exporting
// from a single source to ensure they're always identical
```

5. **Maintain proper encapsulation** - public APIs should hide implementation details and provide only the intended functionality to consumers.