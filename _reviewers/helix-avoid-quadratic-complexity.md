---
title: avoid quadratic complexity
description: When working with data structures, especially ropes and collections,
  avoid algorithms that result in quadratic time complexity when linear alternatives
  exist. Common patterns to watch for include repeated indexing operations and nested
  loops over related data sets.
repository: helix-editor/helix
label: Algorithms
language: Rust
comments_count: 4
repository_stars: 39026
---

When working with data structures, especially ropes and collections, avoid algorithms that result in quadratic time complexity when linear alternatives exist. Common patterns to watch for include repeated indexing operations and nested loops over related data sets.

**Key anti-patterns:**
- Repeatedly indexing into ropes: `(0..=cursor_char).rev().find(|&i| !is_word(text.char(i)))` is O(W*log(N))
- Nested iteration without bounds: `code_actions_on_save.iter().any(|a| match &x.kind { ... })` can be O(M*N)

**Better approaches:**
- Use iterators for rope operations: `text.chars_at(cursor_char).take_while(is_word).count()` is O(log(N)+W)
- Convert frequently-searched collections to HashSet: `let actions_set: HashSet<_> = code_actions_on_save.iter().collect()` makes lookups O(1)
- Leverage built-in optimized methods: use `partition_point` instead of `binary_search_by_key` when you don't need the exact match

Example transformation:
```rust
// Inefficient O(W*log(N)) - repeated rope indexing
let start = (0..=cursor_char)
    .rev()
    .find(|&i| !is_word(text.char(i)))
    .map(|i| i + 1)
    .unwrap_or(0);

// Efficient O(log(N)+W) - iterator-based
let start = cursor_char - text.chars_at(cursor_char)
    .reversed()
    .take_while(|&c| is_word(c))
    .count();
```

Always consider the complexity of your algorithm, especially when dealing with text processing, search operations, or nested data access patterns.