---
title: Minimize memory allocations
description: Avoid unnecessary memory allocations to improve performance. Each allocation
  has both CPU and memory overhead that can accumulate significantly, especially in
  hot code paths.
repository: huggingface/tokenizers
label: Performance Optimization
language: Rust
comments_count: 5
repository_stars: 9868
---

Avoid unnecessary memory allocations to improve performance. Each allocation has both CPU and memory overhead that can accumulate significantly, especially in hot code paths.

Follow these practices:

1. Avoid intermediate collections - prefer direct processing over collect-then-process patterns:
```rust
// Inefficient: Creates a temporary collection
let collected = items.map(process).collect::<Vec<_>>();
let result = collected.iter().sum();

// Better: Process directly without temporary collection
let result = items.map(process).reduce(|a, b| a + b).unwrap_or_default();
```

2. Don't allocate in getter methods - return references or copy small values instead:
```rust
// Avoid: Returning newly allocated vectors
pub fn get_added_tokens(&self) -> Vec<String> {
    self.added_vocabulary.get_added_tokens()
}

// Better: Return a reference to existing data
pub fn get_added_tokens(&self) -> &[String] {
    self.added_vocabulary.tokens()
}
```

3. Use references/slices for parameter passing to avoid copies:
```rust
// Avoid: Taking ownership of a vector that requires allocation
fn process(data: Vec<u8>) { /* ... */ }

// Better: Accept a slice reference
fn process(data: &[u8]) { /* ... */ }
```

4. Consider extending existing structures rather than creating and combining new ones:
```rust
// Instead of creating multiple encodings and merging them later,
// extend a single encoding incrementally
let mut encoding = Encoding::default();
for item in items {
    let tokens = tokenize(item);
    encoding.extend(tokens);
}
```

Performance optimizations often involve trading readability for speed - make these tradeoffs intentionally and document when necessary.