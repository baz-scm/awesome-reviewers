---
title: Include explanatory examples
description: Always enhance documentation with concrete, illustrative examples that
  demonstrate expected inputs, formats, or outputs. Examples significantly improve
  comprehension and reduce ambiguity, especially for complex parameters, commands,
  or return values.
repository: influxdata/influxdb
label: Documentation
language: Rust
comments_count: 4
repository_stars: 30268
---

Always enhance documentation with concrete, illustrative examples that demonstrate expected inputs, formats, or outputs. Examples significantly improve comprehension and reduce ambiguity, especially for complex parameters, commands, or return values.

When documenting:
- CLI commands: Show sample invocations with typical arguments
- Parameters: Provide examples of valid formats and constraints
- Functions: Include examples of return values or expected output
- Data structures: Demonstrate typical usage patterns

For instance, instead of simply stating:
```rust
/// Which columns in the table to use as keys in the cache
#[clap(long = "key-columns")]
```

Enhance it with format information and an example:
```rust
/// Which columns in the table to use as keys in the cache (comma-separated list)
/// Example: --key-columns="customer_id,region,timestamp"
#[clap(long = "key-columns")]
```

Similarly, when documenting format expectations or naming rules:
```rust
/// The database name to create (alphanumeric with underscore and dash, 
/// must start with a letter or number)
/// Example: "production_metrics" or "test-db-2"
#[clap(required = true)]
```

For code variables that might be unclear, add a comment with sample output:
```rust
// Format: "{package_name}-{version}", e.g. "influxdb3-3.0.1"
let influx_version = format!("{}-{}", influxdb_pkg_name, influxdb_pkg_version);
```

Examples bridge the gap between abstract documentation and practical application, making your code more accessible and easier to use correctly.