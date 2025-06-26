---
title: "Prefer descriptive over brief"
description: "Choose clear, descriptive names over abbreviated or shortened versions. Names should be self-documenting and follow Rust conventions. While brevity can be tempting, the clarity and maintainability benefits of descriptive names outweigh the extra characters."
repository: "tokio-rs/axum"
label: "Naming Conventions"
language: "Rust"
comments_count: 5
repository_stars: 22100
---

Choose clear, descriptive names over abbreviated or shortened versions. Names should be self-documenting and follow Rust conventions. While brevity can be tempting, the clarity and maintainability benefits of descriptive names outweigh the extra characters.

Good practices:
- Use full, meaningful names instead of abbreviations
- Follow Rust naming conventions (snake_case for variables/functions, PascalCase for types)
- Use semantic names that describe the purpose
- If external conventions conflict with Rust's, use attributes to maintain both

Example:
```rust
// Instead of:
use axum::http::StatusCode as SC;
const HTML: &str = "text/html";
struct User { _id: u32 }

// Prefer:
use axum::http::StatusCode;
const CONTENT_TYPE_HTML: &str = "text/html";
struct User {
    #[serde(rename = "_id")]  // maintains MongoDB convention while using Rust style
    id: u32
}
```