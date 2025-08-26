---
title: Algorithm and data optimization
description: Choose efficient algorithms and appropriate data structures based on
  access patterns and computational requirements. Use built-in comparison methods
  like `cmp()` to avoid redundant checks, select data structures that match usage
  patterns (HashSet for lookups, Vec for iteration), and ensure algorithmic correctness
  by handling edge cases properly.
repository: tree-sitter/tree-sitter
label: Algorithms
language: Rust
comments_count: 6
repository_stars: 21799
---

Choose efficient algorithms and appropriate data structures based on access patterns and computational requirements. Use built-in comparison methods like `cmp()` to avoid redundant checks, select data structures that match usage patterns (HashSet for lookups, Vec for iteration), and ensure algorithmic correctness by handling edge cases properly.

Key practices:
- Use `match` with `cmp()` for version/ordering comparisons instead of multiple if-else conditions
- Choose HashSet over Vec when doing frequent containment checks: "Since we're just doing contains lookups, a hashset would be better, no?"
- Ensure total ordering in comparison functions - consider topological sorting when dependencies exist: "You'll most likely have to do a topological sort, if the intention is to arrange the nodes in their dep order"
- Handle edge cases in tree traversal algorithms, especially with zero-width nodes or empty ranges
- Avoid brittle algorithmic assumptions like "the name field is always within the first three lines"
- Implement iterator protocols correctly, ensuring `size_hint()` returns remaining elements count

Example of efficient comparison:
```rust
// Instead of multiple if-else conditions
match new_version.cmp(&current_version) {
    Ordering::Less => eprintln!("Warning: new version is lower than current!"),
    Ordering::Greater => println!("Bumping version {current_version} to {new_version}"),
    Ordering::Equal => println!("Keeping version {current_version}"),
}
```