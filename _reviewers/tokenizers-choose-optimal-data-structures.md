---
title: Choose optimal data structures
description: 'Select data structures based on their algorithmic complexity and usage
  patterns. Consider the tradeoffs between different structures (e.g., Vec vs HashMap)
  and their impact on performance. Key considerations:'
repository: huggingface/tokenizers
label: Algorithms
language: Rust
comments_count: 4
repository_stars: 9868
---

Select data structures based on their algorithmic complexity and usage patterns. Consider the tradeoffs between different structures (e.g., Vec vs HashMap) and their impact on performance. Key considerations:

1. Use HashSet/HashMap for O(1) lookups when uniqueness checking is primary concern
2. Prefer Vec when order matters or when performing sequential operations
3. Consider memory layout and cache locality for performance-critical code

Example:
```rust
// Suboptimal: Using HashMap when order matters
let mut pieces: HashMap<String, f64> = HashMap::new();

// Better: Using Vec with HashSet for uniqueness
let mut pieces: Vec<(String, f64)> = vec![];
let mut inserted: HashSet<String> = HashSet::new();

// Best: Single pass implementation for pattern matching
let mut prev = 0;
let mut splits = Vec::with_capacity(inside.len());
for m in self.find_iter(inside) {
    if prev != m.start() {
        splits.push(((prev, m.start()), false));
    }
    splits.push(((m.start(), m.end()), true));
    prev = m.end();
}
```