---
title: Boundary case handling
description: 'Always handle boundary conditions explicitly in algorithms to prevent
  unexpected behavior. When implementing algorithms that involve iteration, traversal,
  or boundary checks, consider different approaches based on the specific requirements:'
repository: vercel/turborepo
label: Algorithms
language: Rust
comments_count: 4
repository_stars: 28115
---

Always handle boundary conditions explicitly in algorithms to prevent unexpected behavior. When implementing algorithms that involve iteration, traversal, or boundary checks, consider different approaches based on the specific requirements:

1. **For cyclic collections**:
   - Use modulo arithmetic for elegant wraparound behavior:
   ```rust
   // When implementing next/previous functionality
   if num_rows > 0 {
       self.selected_task_index = (self.selected_task_index + 1) % num_rows;
       // Instead of manual clamping which would stop at boundaries
   }
   ```

2. **For underflow prevention**:
   - Consider using checked operations with fallbacks:
   ```rust
   // Alternative to modulo for previous index
   self.selected_task_index = self.selected_task_index.checked_sub(1).unwrap_or(num_rows - 1);
   ```

3. **For tree/graph traversal**:
   - Be explicit about traversal depth (shallow vs deep):
   ```rust
   // When shallow references are needed (not the whole graph)
   let references = all_modules_iter([self.source].into_iter())
   ```
   
   - Implement early termination for efficiency:
   ```rust
   fn visit_stmt(&mut self, stmt: &Stmt) {
       if self.abort {
           return; // Skip further traversal if abort flag is set
       }
       stmt.visit_children_with(self);
   }
   ```

4. **For pattern matching**:
   - Consider all possible matching paths:
   ```rust
   // Instead of hard if/else for pattern matching
   let (matches_pattern, does_not_match) = pattern.split_could_match("./");
   // Handle both possibilities appropriately
   ```

Explicit boundary handling improves code correctness, readability, and helps prevent subtle bugs that appear only in edge cases.