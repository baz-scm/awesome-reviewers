---
title: Structure API doc blocks
description: 'Each public API documentation block should follow a consistent structure:


  1. Start with a single-line summary that concisely describes the item

  2. Add an empty line after the summary'
repository: tokio-rs/tokio
label: Documentation
language: Rust
comments_count: 5
repository_stars: 28989
---

Each public API documentation block should follow a consistent structure:

1. Start with a single-line summary that concisely describes the item
2. Add an empty line after the summary
3. Follow with detailed documentation paragraphs
4. Use empty lines between sections (paragraphs, code blocks, headers)
5. Format Rust types using backticks (e.g., [`String`])

Example:

```rust
/// Receives the next value from the channel.
///
/// This method returns `None` if the channel has been closed and there are
/// no remaining messages in the channel's queue. The channel is closed when
/// all senders have been dropped.
///
/// # Examples
///
/// ```
/// use tokio::sync::mpsc;
///
/// #[tokio::main]
/// async fn main() {
///     let (tx, mut rx) = mpsc::channel(100);
///     assert!(rx.recv().await.is_none());
/// }
/// ```
pub async fn recv(&mut self) -> Option<T> {
    // Implementation
}
```

This structure improves readability and ensures documentation is both scannable and detailed when needed. The single-line summary is particularly important as it appears in module documentation and IDE tooltips.