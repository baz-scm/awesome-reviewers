---
title: Follow naming conventions
description: "Choose names that follow established API conventions and guidelines\
  \ to create a consistent, intuitive codebase:\n\n1. For conversions or views:\n\
  \   - Use `as_*` for cheap, reference-based conversions"
repository: tokio-rs/tokio
label: Naming Conventions
language: Rust
comments_count: 7
repository_stars: 28981
---

Choose names that follow established API conventions and guidelines to create a consistent, intuitive codebase:

1. For conversions or views:
   - Use `as_*` for cheap, reference-based conversions
   ```rust
   // Prefer this
   fn as_socket(&self) -> socket2::SockRef<'_> {
       socket2::SockRef::from(self)
   }
   // Instead of
   fn to_socket(&self) -> socket2::SockRef<'_>
   ```

2. For clarity through qualified names:
   - Prefer context-specific names over generic ones
   ```rust
   // Prefer this
   pub fn sender_strong_count(&self) -> usize
   // Instead of
   pub fn strong_count(&self) -> usize
   ```
   - Use semantic descriptors over technical ones
   ```rust
   // Prefer this
   pub fn notify_one_last_in(&self)
   // Instead of
   pub fn notify_one_lifo(&self)
   ```

3. When using plurals in parameters:
   - Make method names reflect plurality
   ```rust
   // Prefer this
   pub async fn copy_bidirectional_with_sizes<A, B>
   // Instead of
   pub async fn copy_bidirectional_with_size<A, B>
   ```

4. Avoid naming conflicts:
   - Don't add methods with the same name as trait implementations when your type implements `Deref`
   - For similar functionality, use qualified names
   ```rust
   // Prefer this
   pub fn clone_inner(&'static self) -> T
   // Instead of
   pub fn clone(&'static self) -> T  // Confusing with Clone trait
   ```

Even when verbosity increases, prioritize clarity and prevention of API confusion. `AbortOnDropHandle` may be verbose, but it clearly communicates the type's behavior.