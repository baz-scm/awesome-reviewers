---
title: avoid redundant lookups
description: When working with associative containers (sets, maps, unordered_set,
  unordered_map), avoid performing redundant lookups by using single operations that
  combine lookup and insertion/modification. The common anti-pattern is to first check
  if an element exists with `find()`, then perform a separate `insert()` operation,
  which results in two hash table lookups.
repository: duckdb/duckdb
label: Algorithms
language: C++
comments_count: 3
repository_stars: 32061
---

When working with associative containers (sets, maps, unordered_set, unordered_map), avoid performing redundant lookups by using single operations that combine lookup and insertion/modification. The common anti-pattern is to first check if an element exists with `find()`, then perform a separate `insert()` operation, which results in two hash table lookups.

**Anti-pattern:**
```cpp
if (result.find(index) != result.end()) {
    throw InternalException("Duplicate table index found");
}
result.insert(index);
```

**Preferred approach:**
```cpp
const bool is_new = result.emplace(index).second;
if (!is_new) {
    throw InternalException("Duplicate table index found");
}
```

For sets, use `emplace()` or `insert()` with `.second` to check if insertion occurred. For maps, use `emplace()`, `try_emplace()`, or `insert_or_assign()` depending on the desired semantics. This optimization reduces algorithmic complexity from O(2) to O(1) hash table operations per element, which can significantly improve performance in tight loops or when processing large datasets.

The same principle applies to other associative containers and operations - always prefer single operations that provide the information you need rather than separate lookup and modification steps.