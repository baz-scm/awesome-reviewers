---
title: Short-circuit evaluation strategies
description: When implementing search or traversal algorithms, use short-circuit evaluation
  strategically to avoid unnecessary computation while ensuring correctness. Short-circuiting
  is beneficial when the first match is sufficient, but can lead to incorrect results
  when complete information is needed.
repository: astral-sh/uv
label: Algorithms
language: Rust
comments_count: 3
repository_stars: 60322
---

When implementing search or traversal algorithms, use short-circuit evaluation strategically to avoid unnecessary computation while ensuring correctness. Short-circuiting is beneficial when the first match is sufficient, but can lead to incorrect results when complete information is needed.

For example, when implementing a search function:

```rust
// Good: Use short-circuit when first match is sufficient
fn find_python_installation(installations: &[Installation]) -> Option<&Installation> {
    installations.iter().find(|installation| 
        request.matches_installation(installation))
}

// Good: Use closure to make short-circuit logic clearer
let (db, actual_rev, maybe_task) = || -> Result<(GitDatabase, GitOid, Option<usize>)> {
    // Short-circuit early if we already have the commit
    if let (Some(rev), Some(db)) = (self.git.precise(), &maybe_db) {
        if db.contains(rev) {
            debug!("Using existing Git source `{}`", self.git.repository());
            return Ok((maybe_db.unwrap(), rev, None));
        }
    }
    // Continue with fetching otherwise...
}();

// Bad: Using short-circuit when complete information is needed
// @any isn't sorted by version during discovery because we short-circuit
// when we find an interpreter that meets the request
// @latest needs to scan ALL Python interpreters to select the latest version
```

Consider the full requirements before deciding on a traversal strategy. When implementing algorithms that search or process collections:
1. Use short-circuit (like `.find()`) when the first match is sufficient
2. Use full traversal (like `.filter()` + `.max_by_key()`) when you need to examine all elements
3. Document your choice of strategy, especially when the behavior affects correctness