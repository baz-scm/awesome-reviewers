---
title: avoid implementation detail leakage
description: APIs should provide clean abstraction boundaries without exposing internal
  implementation details or creating unwanted dependencies between modules. When designing
  public interfaces, carefully consider what needs to be exposed versus what can remain
  internal.
repository: denoland/deno
label: API
language: Rust
comments_count: 5
repository_stars: 103714
---

APIs should provide clean abstraction boundaries without exposing internal implementation details or creating unwanted dependencies between modules. When designing public interfaces, carefully consider what needs to be exposed versus what can remain internal.

Common violations include:
- Directly re-exporting third-party types instead of wrapping them
- Exposing complex internal structures when simpler options would suffice  
- Creating dependencies on internal modules from public APIs
- Reaching directly into internal implementation details

Instead, prefer:
- Re-exporting only specific types needed: `pub use quinn::ConnectionError;` rather than `pub use quinn;`
- Exposing configuration options rather than complex internal types
- Creating trait abstractions for internal dependencies
- Providing specialized APIs to avoid viral parameter changes

Example of good abstraction:
```rust
// Instead of exposing complex internal resolver
pub fn op_require_fallback_resolve<T: NodeRequireLoader>(
  state: &mut OpState,
  request: String,
  parent_filename: Option<String>,
) -> Result<String, RequireError>

// Expose simpler options-based API
#[derive(Debug, Default, Clone)]
pub struct ConditionOptions {
  pub conditions: Vec<Cow<'static, str>>,
  pub import_conditions_override: Option<Vec<Cow<'static, str>>>,
}
```

This approach reduces coupling, improves maintainability, and provides cleaner interfaces for API consumers.