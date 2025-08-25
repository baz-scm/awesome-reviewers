---
title: consolidate API parameters
description: Prefer consolidating common configuration and parameters in API constructors
  or base methods rather than requiring multiple method calls, complex parameter passing,
  or external configuration loading. This reduces API surface area and makes interfaces
  easier to use for consumers.
repository: block/goose
label: API
language: Rust
comments_count: 4
repository_stars: 19037
---

Prefer consolidating common configuration and parameters in API constructors or base methods rather than requiring multiple method calls, complex parameter passing, or external configuration loading. This reduces API surface area and makes interfaces easier to use for consumers.

When designing APIs, favor approaches that:
- Accept optional parameters in base methods instead of creating separate methods for each variation
- Load common configuration automatically in constructors rather than requiring explicit setup calls
- Pass parameters directly to constructors instead of requiring consumers to load and parse configuration
- Use native types (like JSON schemas) directly rather than requiring string serialization

Example of preferred approach:
```rust
// Instead of separate methods for each model type
pub async fn complete_with_model(&self, model: Option<String>) -> Result<Message> {
    let model = model.unwrap_or_else(|| self.default_model());
    // implementation
}

// Instead of requiring multiple setup calls
pub fn new(api_key: String) -> Result<Self> {
    let mut client = ApiClient::new(host, auth)?;
    
    // Load common config automatically
    if let Some(tls_config) = TlsConfig::from_config()? {
        client = client.with_tls_config(tls_config)?;
    }
    
    Ok(Self { client })
}

// Instead of string-based parameters, use direct types
pub fn create_tool(schema: serde_json::Value) -> Tool {
    // Use schema directly instead of requiring JSON string
}
```

This approach reduces the cognitive load on API consumers and prevents the need to understand complex setup sequences or parameter serialization formats.