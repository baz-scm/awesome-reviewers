---
title: Choose efficient data structures
description: Select data structures and algorithms based on their performance characteristics
  and expected usage patterns. Consider the size of collections, access patterns,
  and computational complexity when making implementation choices.
repository: jj-vcs/jj
label: Algorithms
language: Rust
comments_count: 6
repository_stars: 21171
---

Select data structures and algorithms based on their performance characteristics and expected usage patterns. Consider the size of collections, access patterns, and computational complexity when making implementation choices.

**Key considerations:**
- Use `HashSet` instead of `Vec` for membership testing when collections can be large
- Choose data structures that preserve order when sequence matters (e.g., `IndexMap` vs `HashMap`)
- Prefer more efficient algorithms when available (e.g., checking if a commit is a head vs. evaluating all children)
- Combine operations to reduce computational overhead (e.g., union revset expressions rather than evaluating separately)

**Example:**
```rust
// Instead of Vec for large collections with frequent lookups
let already_tracked_bookmarks: Vec<String> = ...;
if already_tracked_bookmarks.contains(&bookmark) { ... } // O(n) lookup

// Use HashSet for O(1) average lookup time
let already_tracked_bookmarks: HashSet<String> = ...;
if already_tracked_bookmarks.contains(&bookmark) { ... } // O(1) lookup
```

This applies especially when dealing with user-facing operations that may scale with repository size or when processing large collections where the choice of data structure significantly impacts performance.