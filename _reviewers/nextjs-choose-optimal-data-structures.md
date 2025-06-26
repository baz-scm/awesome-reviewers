---
title: "Choose optimal data structures"
description: "Select data structures based on their performance characteristics and actual usage patterns. When implementing algorithms, consider usage patterns, understand API differences, and match data structures to access patterns."
repository: "vercel/next.js"
label: "Algorithms"
language: "Rust"
comments_count: 2
repository_stars: 133000
---

Select data structures based on their performance characteristics and actual usage patterns. When implementing algorithms:

1. **Consider usage patterns**: Analyze how data will be accessed and modified. For collections that might contain duplicates where duplicates add no value (like in discussion 3), prefer Sets over Lists/Arrays:

```rust
// Less efficient: Using Vec when duplicates don't matter
let mut used_exports = Vec::new();
used_exports.push(Export::Named("React"));  // This might be added many times

// More efficient: Using a Set to automatically handle duplicates
let mut used_exports = FxHashSet::default();
used_exports.insert(Export::Named("React"));  // Will only be stored once
```

2. **Understand API differences**: Data structures with similar purposes may have different method behaviors. For example, in discussion 1, changing from HashSet to HashMap required adjusting logic because:

```rust
// HashSet.insert() returns a boolean indicating if the element was newly inserted
if !set.insert(key) {
    return;  // Element was already present
}

// HashMap.insert() returns Option<V> with the previous value, if any
if map.insert(key, value).is_some() {
    return;  // Key was already present (previous value returned)
}
```

3. **Match data structures to access patterns**: Use hashmaps for fast lookups, vectors for sequential access, sets for uniqueness enforcement, and specialized structures for specific needs.

Choosing the right data structure is often the difference between an efficient algorithm and one that performs poorly at scale.