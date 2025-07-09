---
title: Ensure algorithm robustness
description: When implementing algorithms, ensure they handle all edge cases correctly
  and robustly. Code should gracefully manage exceptional conditions rather than producing
  incorrect results or panicking.
repository: neondatabase/neon
label: Algorithms
language: Rust
comments_count: 4
repository_stars: 19015
---

When implementing algorithms, ensure they handle all edge cases correctly and robustly. Code should gracefully manage exceptional conditions rather than producing incorrect results or panicking.

Key practices:

1. **Test boundary conditions**: Verify your algorithm works correctly with empty collections, maximum/minimum values, and other edge cases.

2. **Handle hash functions comprehensively**: Include all relevant state in hash functions to prevent unintended collisions.

```rust
// Suboptimal: Missing important fields
impl Hash for ImportTask {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.key_range.hash(state);
        self.path.hash(state);
    }
}

// Better: Includes all relevant fields
impl Hash for ImportTask {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.shard_identity.hash(state);  // Include this for robustness
        self.key_range.hash(state);
        self.path.hash(state);
    }
}
```

3. **Be cautious with floating-point comparisons**: Don't assume exact equality or that values will sum to expected amounts due to precision errors.

```rust
// Problematic: Assumes perfect precision
if total_percentage == 100.0 {
    // ...
}

// Better: Use appropriate epsilon or handle the last case separately
let last_variant = variants.last().unwrap();
if mapped_user_id <= total_percentage / 100.0 {
    return Some(last_variant.key.clone());
}
```

4. **Verify logical conditions carefully**: Double-check complex conditionals to ensure they express exactly what you intend.

```rust
// Incorrect: Complex condition with a logic error
if !(plan_hash == progress.import_plan_hash || progress.jobs != plan.jobs.len()) {
    anyhow::bail!("Import plan does not match storcon metadata");
}

// Correct: Simplified, clear conditions
if plan_hash != progress.import_plan_hash {
    anyhow::bail!("Import plan hash does not match storcon metadata hash");
}
if progress.jobs != plan.jobs.len() {
    anyhow::bail!("Import plan job length does not match storcon metadata");
}
```

5. **Document known limitations**: When an algorithm doesn't handle certain cases, clearly document these limitations to prevent misuse.