---
title: Choose efficient data structures
description: Select data structures and algorithms that optimize for the specific
  use case rather than defaulting to generic collections. Consider computational complexity,
  memory usage, and access patterns when making these choices.
repository: unionlabs/union
label: Algorithms
language: Rust
comments_count: 7
repository_stars: 74800
---

Select data structures and algorithms that optimize for the specific use case rather than defaulting to generic collections. Consider computational complexity, memory usage, and access patterns when making these choices.

Key principles:
- Use HashMap/BTreeMap for key-value lookups instead of Vec when you need efficient searching: `HashMap<String, i32>` instead of `Vec<(String, i32)>`
- Choose fixed-size types when the size is known: use `[u8; 32]` for commit hashes instead of `Vec<u8>`
- Use appropriate algorithms for bit manipulation: `i.count_ones()` instead of casting to usize for bit counting
- Leverage established, well-tested libraries for complex parsing instead of custom implementations (e.g., use `peg` for grammar parsing)
- Design enums with non-zero discriminants when differentiating from empty storage values: `Active = 1` instead of `Active = 0`
- Avoid redundant computations by using operations that combine checks: use `checked_sub()` and match on the result instead of separate comparison and subtraction

Example of efficient data structure selection:
```rust
// Instead of this:
let chain_ids_and_ids: Vec<(String, i32)> = fetch_data();
// Use this for lookups:
let chain_lookup: HashMap<String, i32> = fetch_data().into_iter().collect();

// Instead of this for bit counting:
sync_committee_bits.iter().map(|i| *i as usize).sum::<usize>()
// Use this:
sync_committee_bits.iter().map(|i| i.count_ones() as usize).sum::<usize>()
```