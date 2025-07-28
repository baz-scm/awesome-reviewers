---
title: Choose appropriate algorithms
description: When implementing functionality, carefully evaluate different algorithmic
  approaches and data structures to choose the most appropriate solution. Consider
  factors like performance requirements, correctness, maintainability, and whether
  existing libraries can be leveraged instead of custom implementations.
repository: denoland/deno
label: Algorithms
language: Rust
comments_count: 3
repository_stars: 103714
---

When implementing functionality, carefully evaluate different algorithmic approaches and data structures to choose the most appropriate solution. Consider factors like performance requirements, correctness, maintainability, and whether existing libraries can be leveraged instead of custom implementations.

Key considerations:
- **Leverage existing libraries**: Before implementing custom algorithms, check if well-tested libraries already solve the problem (e.g., using `deno_semver::Version` for version parsing instead of custom parsing)
- **Choose the right tool**: Select algorithms and data structures that match your specific needs (e.g., using a lexer for simple comment extraction instead of full AST parsing when only comments are needed)
- **Design for efficiency**: Consider the computational complexity and choose data structures that optimize for your use case (e.g., implementing a PathTrie for efficient path matching operations)

Example from the codebase:
```rust
// Instead of custom version parsing:
struct VersionParts {
  major: u64,
  minor: u64, 
  patch: u64,
  pre: Option<String>,
}

// Consider using existing library:
// Should we be using `deno_semver::Version` here?
use deno_semver::Version;
```

This approach reduces bugs, improves maintainability, and often provides better performance than ad-hoc implementations.