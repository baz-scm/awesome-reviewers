---
title: Use functional null handling
description: 'Leverage Rust''s functional operators for handling nullable and optional
  values. Instead of using unwrap() or explicit if-statements, prefer combinators
  like ok(), and_then(), map_or_else() and the ? operator with Option types. This
  leads to more concise, readable, and null-safe code:'
repository: vercel/turborepo
label: Null Handling
language: Rust
comments_count: 3
repository_stars: 28115
---

Leverage Rust's functional operators for handling nullable and optional values. Instead of using unwrap() or explicit if-statements, prefer combinators like ok(), and_then(), map_or_else() and the ? operator with Option types. This leads to more concise, readable, and null-safe code:

```rust
// Instead of this:
let package_manager = PackageJson::load(&base.repo_root.join_component("package.json"))
    .and_then(|package_json| {
        Ok(PackageManager::read_or_detect_package_manager(
            &package_json,
            &base.repo_root,
        ))
    })
    .map_or_else(|_| "Not found".to_owned(), |pm| pm.unwrap().to_string());

// Prefer this:
let package_manager = PackageJson::load(&base.repo_root.join_component("package.json"))
    .ok()
    .and_then(|package_json| {
        PackageManager::read_or_detect_package_manager(&package_json, &base.repo_root).ok()
    })
    .map_or_else(|| "Not found".to_owned(), |pm| pm.to_string());

// Instead of this:
if self.commits.is_empty() {
    return None;
}
if let Some(first_commit) = self.commits.first() {
    let id = &first_commit.id;
    return Some(format!("{id}^"));
}

// Prefer this:
let first_commit = self.commits.first()?; 
let id = &first_commit.id;
Some(format!("{id}^"))
```

Additionally, prefer using Option<T> over returning default values for nullable fields. This makes the absence of a value explicit at the type level and forces consumers to handle both cases appropriately.