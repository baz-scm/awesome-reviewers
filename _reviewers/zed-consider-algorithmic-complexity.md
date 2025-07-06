---
title: Consider algorithmic complexity
description: "When implementing algorithms, be mindful of their computational complexity\
  \ and choose appropriate data structures for operations. \n\n1. **Use specialized\
  \ collections for their strengths**:"
repository: zed-industries/zed
label: Algorithms
language: Rust
comments_count: 6
repository_stars: 62119
---

When implementing algorithms, be mindful of their computational complexity and choose appropriate data structures for operations. 

1. **Use specialized collections for their strengths**:
   - For deduplication, prefer `HashSet` over repeatedly checking `Vec.contains()`.
   - Consider specialized libraries like `Itertools` for common operations.
   - Choose data structures based on access patterns:
     ```rust
     // Instead of:
     let mut models = BTreeMap::default();  // Causes unwanted sorting
     
     // Use:
     let mut models = Vec::new();  // Preserves insertion order when sorting isn't needed
     ```

2. **Avoid quadratic complexity**:
   - Watch for hidden O(N²) operations, especially nested loops over the same data:
     ```rust
     // Inefficient O(N²) - iterating outlines twice:
     for outline in fetched_outlines {
         // ... then for each outline we iterate again
         if outline_panel.has_outline_children(&outline_entry, cx) {
             // ...
         }
     }
     
     // Better: Process in a single pass with appropriate data structures
     ```

3. **Eliminate unnecessary operations**:
   - Avoid creating intermediate allocations when passing predicates or filters:
     ```rust
     // Inefficient - unnecessarily clones data:
     tasks.retain_mut(|(task_source_kind, target_task)| {
         predicate(&(task_source_kind.clone(), target_task.clone()))
     });
     
     // Better - uses references:
     tasks.retain_mut(|(task_source_kind, target_task)| {
         predicate(&(task_source_kind, target_task))
     });
     ```
   
4. **Use functional patterns for string operations**:
   - Replace imperative loops with more expressive functional alternatives:
     ```rust
     // Instead of manual character loop:
     let mut common_prefix_len = 0;
     for (a, b) in old_text.chars().zip(new_text.chars()) {
         if a == b {
             common_prefix_len += a.len_utf8();
         } else {
             break;
         }
     }
     
     // More expressive functional approach:
     let common_prefix_len = old_text
         .chars()
         .zip(new_text.chars())
         .take_while(|(a, b)| a == b)
         .map(|(a, _)| a.len_utf8())
         .sum::<usize>();
     ```

By consistently applying these principles, you'll create more efficient, maintainable code that performs well even as input sizes grow.