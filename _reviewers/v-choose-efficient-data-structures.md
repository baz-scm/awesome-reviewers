---
title: Choose efficient data structures
description: Select data structures and algorithms based on performance characteristics
  and actual usage patterns rather than convenience or familiarity. Consider memory
  efficiency, computational complexity, and scaling behavior when making implementation
  choices.
repository: vlang/v
label: Algorithms
language: Other
comments_count: 7
repository_stars: 36582
---

Select data structures and algorithms based on performance characteristics and actual usage patterns rather than convenience or familiarity. Consider memory efficiency, computational complexity, and scaling behavior when making implementation choices.

Key principles:
- Use builtin data structures when they provide sufficient functionality (e.g., arrays for simple push/pop operations instead of external Stack libraries)
- Choose memory-efficient representations (e.g., `map[T]bool` instead of `map[T]T` for sets, since `sizeof(bool) < sizeof(T)` for most types)
- Select algorithms that scale appropriately (e.g., use maps instead of arrays for duplicate detection in large datasets)
- Order sum type variants by frequency or size for better performance (put common/smaller types first)
- Optimize boolean expressions by placing cheaper comparisons first to leverage short-circuiting
- Use appropriate data types for intermediate calculations to avoid overflow checks in tight loops

Example of efficient set implementation:
```v
// Inefficient - stores redundant data
struct BadSet[T] {
mut:
    main_set map[T]T
}

// Efficient - minimal memory usage
struct GoodSet[T] {
mut:
    main_set map[T]bool
}

fn (g GoodSet[T]) elements() []T {
    return g.main_set.keys() // Use builtin method instead of manual iteration
}
```

Example of algorithm selection for duplicate removal:
```v
// Inefficient for large datasets - O(n²) complexity
fn remove_duplicates_slow[T](arr []T) []T {
    mut results := []T{}
    for val in arr {
        if val !in results { // Linear search each time
            results << val
        }
    }
    return results
}

// Efficient - O(n) complexity
fn remove_duplicates_fast[T](arr []T) []T {
    mut seen := map[T]bool{}
    mut results := []T{}
    for val in arr {
        if !seen[val] {
            seen[val] = true
            results << val
        }
    }
    return results
}
```