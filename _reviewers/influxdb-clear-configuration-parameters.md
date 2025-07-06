---
title: Clear configuration parameters
description: Configuration parameters should be descriptively named, well documented,
  and have sensible defaults that are visible to users. This makes your application
  more user-friendly and reduces confusion.
repository: influxdata/influxdb
label: Configurations
language: Rust
comments_count: 5
repository_stars: 30268
---

Configuration parameters should be descriptively named, well documented, and have sensible defaults that are visible to users. This makes your application more user-friendly and reduces confusion.

**Descriptive naming:**
- Use precise, unambiguous names that clearly indicate the parameter's purpose
- Example: Use `query-file-limit` instead of `file-limit`, or `snapshotted-wal-files-to-keep` instead of `num-wal-files-to-keep`

**Document defaults:**
- Make default values visible in CLI documentation to match coded defaults
- Example:
```rust
/// The maximum number of distinct value combinations to hold in the cache
#[clap(long = "max-cardinality", default_value = "100000")]
max_cardinality: Option<NonZeroUsize>,
```

**Use user-friendly units:**
- Choose appropriate units for your configurations
- Consider using percentages for memory limits to work across different system configurations
- For file sizes, use MB instead of bytes when appropriate

**Provide helpful documentation:**
- Include examples in help text for required parameters
- Explain valid types and formats
- Add contextual information to help users understand the implications of settings

Following these guidelines will reduce support issues and improve the usability of your application's configuration interface.