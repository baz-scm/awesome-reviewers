---
title: Clean documentation links
description: When writing Rust documentation links, separate the display name from
  the full path to improve readability of generated docs. Use the short type name
  as the display text and provide the full path as the link target. This makes the
  documentation less noisy and easier to read.
repository: unionlabs/union
label: Documentation
language: Rust
comments_count: 2
repository_stars: 74800
---

When writing Rust documentation links, separate the display name from the full path to improve readability of generated docs. Use the short type name as the display text and provide the full path as the link target. This makes the documentation less noisy and easier to read.

**Pattern to follow:**
```rust
// Instead of this (noisy):
/// The returned [`Op`] ***MUST*** resolve to an [`crate::data::OrderedHeaders`] data.

// Use this (clean):
/// The returned [`Op`] ***MUST*** resolve to an [`OrderedHeaders`][crate::data::OrderedHeaders] data.
```

This approach keeps the inline text readable while still providing the full path information needed for proper linking in the generated documentation.