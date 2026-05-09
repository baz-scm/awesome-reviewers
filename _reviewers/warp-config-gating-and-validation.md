---
title: Config Gating And Validation
description: 'When behavior depends on platform features, build features, feature
  flags, or user-provided configuration, keep it explicitly scoped and validated.


  Apply this checklist:'
repository: warpdotdev/warp
label: Configurations
language: Rust
comments_count: 7
repository_stars: 56893
---

When behavior depends on platform features, build features, feature flags, or user-provided configuration, keep it explicitly scoped and validated.

Apply this checklist:
- **Gate compilation and code paths**: Put platform/build-specific modules behind the correct `#[cfg(...)]` so non-target platforms don’t even compile unix/fs-only imports.
- **Use the same predicate for behavior**: Action availability should follow the exact feature-flag + settings predicate used elsewhere (and include a correct fallback flow when disabled).
- **Provide deterministic fallbacks**: If a feature like `local_fs` is off, return a safe default (e.g., `None`/empty map) without referencing unavailable functionality.
- **Validate at configuration boundaries**: Parse helpers should enforce invariants (e.g., positive numbers) and surface structured errors.
- **Centralize config source/precedence**: When using env vars or other configuration channels, document and implement a clear precedence model (and consider refactoring into shared “prepare config” logic).
- **Remove or document dead toggles**: Don’t leave production config flags that only exist in tests; either remove them or clearly document which caller toggles them.

Example pattern (cfg + validated parsing):
```rust
// Build gating: don't compile unix-only code on Windows.
#[cfg(unix)]
mod local_api;

// Validation: enforce invariants at parse time.
fn parse_positive_usize_query_param(url: &Url, name: &str) -> Result<Option<usize>> {
    let Some(raw) = url.query_pairs().find(|(k, _)| k == name).map(|(_, v)| v) else {
        return Ok(None);
    };
    let value = raw.parse::<usize>()?;
    ensure!(value > 0, "`{name}` must be greater than 0");
    Ok(Some(value))
}
```

These practices prevent cross-platform build breaks, mis-scoped feature behavior, and silent misconfiguration—while keeping configuration-driven behavior predictable and maintainable.