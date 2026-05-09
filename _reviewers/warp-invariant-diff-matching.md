---
title: Invariant Diff Matching
description: When implementing matching/diff logic (especially for code/entities),
  define and test the algorithmic invariants you rely on, and avoid fragile heuristics.
repository: warpdotdev/warp
label: Algorithms
language: Rust
comments_count: 4
repository_stars: 56893
---

When implementing matching/diff logic (especially for code/entities), define and test the algorithmic invariants you rely on, and avoid fragile heuristics.

Apply:
- Use a staged matcher: (1) exact identity, (2) invariant structural equivalence (e.g., rename/formatting-insensitive hash), (3) fuzzy similarity for remaining candidates.
- Define structural hashes by masking the *exact* varying span (e.g., replace the name bytes with whitespace before hashing), rather than using brittle line-based assumptions.
- For “moved”/positional classifications, prefer local/context-based reasoning over global thresholds, and add regression tests for common false positives (like insertion above without reordering).
- If you generate candidates via multiple discovery paths (e.g., tree indexing vs filesystem probing), ensure both paths use the same filtering rules and dedupe inputs before matching.

Example (structural hash rename-invariant):
```rust
fn compute_body_hash_invariant(content: &str, start: usize, end: usize, body_bytes: &[u8]) -> u64 {
    // Mask the entity name span so renames don’t change the structural hash.
    let mut bytes = body_bytes.to_vec();
    // Replace non-whitespace characters in [start, end) with spaces (conceptually).
    for b in &mut bytes {
        if *b != b' ' && *b != b'\n' && *b != b'\t' { *b = b' '; }
    }
    let mut hasher = std::collections::hash_map::DefaultHasher::new();
    bytes.hash(&mut hasher);
    hasher.finish()
}
```

Outcome: fewer misclassified diffs (renames vs modifications vs moves), deterministic behavior, and safer results under edge cases and degraded indexing.