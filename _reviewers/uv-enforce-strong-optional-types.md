---
title: Enforce strong optional types
description: Use strong typing and early validation to handle optional values and
  prevent null-related issues. Prefer enums and specific types over strings when dealing
  with optional data, and validate optional values as early as possible in the data
  flow.
repository: astral-sh/uv
label: Null Handling
language: Rust
comments_count: 3
repository_stars: 60322
---

Use strong typing and early validation to handle optional values and prevent null-related issues. Prefer enums and specific types over strings when dealing with optional data, and validate optional values as early as possible in the data flow.

Key practices:
1. Use enums instead of strings for known value sets
2. Leverage bool::then for cleaner optional handling
3. Validate optional data at structure boundaries

Example:
```rust
// Instead of
struct Config {
    kind: String,  // Could be "realm" or "index"
    value: Option<String>
}

// Prefer
enum ConfigKind {
    Realm(String),
    Index(String)
}
struct Config {
    kind: ConfigKind,
    value: Option<String>
}

// Use bool::then for cleaner optional handling
let value = condition.then(|| compute_value());

// Validate optional data early
fn get_project_version(doc: &mut Document) -> Result<Version, Error> {
    let project = doc.get("project")
        .ok_or(Error::MissingProject)?;
    
    let version = project
        .get("version")
        .and_then(Item::as_value)
        .and_then(Value::as_str)
        .ok_or(Error::MissingVersion)?;

    Version::from_str(version)
}