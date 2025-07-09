---
title: Design ergonomic APIs
description: 'Create APIs that are both easy to use correctly and hard to use incorrectly.
  Focus on:


  1. **Use pattern matching for safer error handling** instead of unwrapping values
  that might be null:'
repository: vercel/turborepo
label: API
language: Rust
comments_count: 5
repository_stars: 28115
---

Create APIs that are both easy to use correctly and hard to use incorrectly. Focus on:

1. **Use pattern matching for safer error handling** instead of unwrapping values that might be null:

```rust
// Instead of:
let catalog_name = specifier.strip_prefix("catalog:").unwrap_or("default");

// Prefer:
if let Some(catalog_name) = specifier.strip_prefix("catalog:") {
    if let Some(catalogs) = &self.catalogs {
        // Use catalog_name directly
    }
}
```

2. **Accept more flexible parameter types** to improve API usability:

```rust
// Instead of:
fn token(mut self, value: String) -> Self {
    self.output.token = Some(value);
    self
}

// Prefer:
fn token(mut self, value: &str) -> Self {
    self.output.token = Some(value.into());
    self
}
```

3. **Make error states explicit** in return types to force proper error handling:

```rust
// Instead of:
Result<TurboJson, Error>

// Consider:
Result<Option<TurboJson>, Error>
```

4. **Use type-system features** like generics to create more flexible interfaces:

```rust
// Instead of:
fn view(app: &mut App<Box<dyn io::Write + Send>>, f: &mut Frame, rows: u16, cols: u16)

// Prefer:
fn view<W>(app: &mut App<W>, f: &mut Frame, rows: u16, cols: u16)
```

5. **Leverage serialization attributes** instead of manual implementations:

```rust
// Instead of manually implementing Serialize:
impl<'a> Serialize for RepositoryDetails<'a> { ... }

// Prefer using serde attributes:
#[serde(into)]
// With a From implementation to handle the conversion
```

These practices lead to APIs that are more intuitive, safer, and require less documentation to use properly.