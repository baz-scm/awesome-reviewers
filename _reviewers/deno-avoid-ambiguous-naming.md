---
title: Avoid ambiguous naming
description: Choose names that clearly convey their purpose and avoid ambiguous identifiers
  that can be misinterpreted. This applies to methods, variables, parameters, and
  types.
repository: denoland/deno
label: Naming Conventions
language: Rust
comments_count: 8
repository_stars: 103714
---

Choose names that clearly convey their purpose and avoid ambiguous identifiers that can be misinterpreted. This applies to methods, variables, parameters, and types.

**Key principles:**
- Replace boolean parameters with descriptive enums when the meaning isn't obvious
- Use specific, descriptive names rather than generic ones
- Ensure names accurately reflect what the code does

**Examples:**

Instead of confusing boolean parameters:
```rust
// Bad - unclear what true/false means
fn parse_inner(s: &str, allow_subdomain_wildcard: bool)

// Good - descriptive enum makes intent clear
enum SubdomainWildcardSupport {
  Enabled,
  #[default]
  Disabled
}
fn parse_inner(s: &str, wildcard_support: SubdomainWildcardSupport)
```

Instead of ambiguous method names:
```rust
// Bad - unclear what this cancels
fn op_read_cancel()

// Good - clearly describes the operation
fn op_read_with_cancel_handle()

// Bad - too generic when context matters
fn get_usage()

// Good - specific to the type of usage
fn get_cpu_usage()
```

Instead of unclear type names:
```rust
// Bad - not descriptive enough
struct Unconfigured

// Good - clearly describes the state
struct UnconfiguredRuntime
```

This practice is especially important in permission-related code and public APIs where clarity prevents misuse and security issues.