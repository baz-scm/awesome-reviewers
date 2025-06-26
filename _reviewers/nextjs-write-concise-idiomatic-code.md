---
title: "Write concise idiomatic code"
description: "Favor concise and idiomatic expressions in your Rust code to improve readability and maintainability."
repository: "vercel/next.js"
label: "Code Style"
language: "Rust"
comments_count: 3
repository_stars: 133000
---

Favor concise and idiomatic expressions in your Rust code to improve readability and maintainability. Specifically:

1. Use Rust's expressive methods instead of verbose alternatives
   ```rust
   // Prefer this
   ident_ref.query.owned().await?
   
   // Instead of this
   (*ident_ref.query.await?).clone()
   ```

2. Avoid redundant `.to_string()` calls in `format!` arguments when the type already implements `Display`
   ```rust
   // Prefer this
   format!("Check {} and {}", this.page, this.other_page)
   
   // Instead of this
   format!("Check {} and {}", this.page.to_string(), this.other_page.to_string())
   ```

3. Only derive the traits you actually need, removing unnecessary derives like `serde::Serialize` and `serde::Deserialize` when they're not used
   ```rust
   // Prefer this
   #[derive(Debug, Clone, Eq, PartialEq, Hash)]
   
   // Instead of this when serialization isn't needed
   #[derive(Debug, Clone, Eq, PartialEq, Hash, serde::Serialize, serde::Deserialize)]
   ```

These practices reduce visual noise and make the intent of your code clearer.