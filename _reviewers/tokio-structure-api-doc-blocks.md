---
title: Structure API doc blocks
description: 'Each documentation block should follow a consistent structure:


  1. Start with a single-line summary of the item''s purpose

  2. Add an empty line after the summary'
repository: tokio-rs/tokio
label: Documentation
language: Rust
comments_count: 5
repository_stars: 28981
---

Each documentation block should follow a consistent structure:

1. Start with a single-line summary of the item's purpose
2. Add an empty line after the summary
3. Follow with detailed documentation paragraphs
4. Use empty lines between sections (paragraphs, code blocks, headers)
5. Put Rust types in backticks (e.g. `String`, `Option<T>`)

Example:

```rust
/// Copies data between two buffers.
///
/// This function efficiently transfers data from the source buffer
/// to the destination buffer using an internal temporary buffer.
/// 
/// # Examples
///
/// ```
/// let mut src = vec![1, 2, 3];
/// let mut dst = Vec::new();
/// copy_data(&mut src, &mut dst);
/// ```
///
/// The operation will return early if the destination `Buffer` is full
/// or the source is empty.
```

This structure ensures documentation is consistently formatted and easy to read, with clear separation between the summary, detailed explanation, examples, and additional notes.