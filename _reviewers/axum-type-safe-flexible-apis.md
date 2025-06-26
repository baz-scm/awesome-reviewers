---
title: "Type-safe flexible APIs"
description: "Design APIs that favor both type safety and flexibility. Use strongly typed wrappers instead of primitive types, but accept generic parameters where flexibility is beneficial."
repository: "tokio-rs/axum"
label: "API"
language: "Rust"
comments_count: 10
repository_stars: 22100
---

Design APIs that favor both type safety and flexibility. Use strongly typed wrappers instead of primitive types, but accept generic parameters where flexibility is beneficial.

For headers and content types, use typed wrappers rather than strings:

```rust
// Instead of:
fn get_page(app: Router, path: &str) -> (StatusCode, String, String) // String for content-type
    
// Prefer:
fn get_page(app: Router, path: &str) -> (StatusCode, headers::ContentType, Vec<u8>)
```

Accept more general trait bounds instead of specific types for parameters:

```rust
// Instead of:
pub async fn from_path(path: PathBuf) -> io::Result<FileStream<AsyncReaderStream>>

// Prefer:
pub async fn from_path(path: impl AsRef<Path>) -> io::Result<FileStream<AsyncReaderStream>>
```

Use more general parameter types when possible:

```rust
// Instead of:
pub fn from_bytes(bytes: &Bytes) -> Result<Self, JsonRejection>

// Prefer:
pub fn from_bytes(bytes: &[u8]) -> Result<Self, JsonRejection>
```

Leverage existing conversion mechanisms rather than duplicating types, allowing users to map between your API and domain types:

```rust
// Instead of copying a CloseCode enum, expose a u16 and let users convert
socket.send(Message::Close(Some(CloseFrame {
    code: axum::extract::ws::close_code::NORMAL, // Use constants instead of magic numbers
    // ...
})))
```

Provide ergonomic builder methods, but also implement standard traits like `FromIterator` to support more idiomatic usage patterns:

```rust
// Support both explicit additions and collection-based construction
let form1 = MultipartForm::new().add_part(part1).add_part(part2);
let form2 = MultipartForm::from_iter([part1, part2]);
```

For constructors, follow consistent patterns across related types, making both empty initialization and conversion from domain objects simple:

```rust
// Empty jar: CookieJar::new(), SignedCookieJar::new(key)
// With headers: CookieJar::from_headers(headers), SignedCookieJar::from_headers(headers, key)
```

When documenting your API, explicitly mention behaviors like content-type handling to avoid surprises:
"The Protocol Buffer extractor does not check the `content-type` header."