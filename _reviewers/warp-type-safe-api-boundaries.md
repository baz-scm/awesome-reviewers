---
title: Type-Safe API Boundaries
description: APIs that cross module boundaries, wire formats, or event streams should
  be designed so callers can’t accidentally construct invalid requests or rely on
  unstable semantics.
repository: warpdotdev/warp
label: API
language: Rust
comments_count: 5
repository_stars: 56893
---

APIs that cross module boundaries, wire formats, or event streams should be designed so callers can’t accidentally construct invalid requests or rely on unstable semantics.

Apply these rules:
1) Prefer request objects/enums over ambiguous parameters
- Avoid signatures like `(Option<T>, Option<U>)` when only certain combinations are valid.
- Instead, model the valid states explicitly (e.g., `ReportShutdownRequest`) or split into distinct methods.

Example:
```rust
async fn report_shutdown(&self, req: ReportShutdownRequest) -> Result<()> {
    // handle only valid states; unreachable invalid combinations
}

// vs:
// async fn report_shutdown(&self, error_category: Option<String>, error_message: Option<String>) -> Result<()>;
```

2) Use named fields (and owned inputs) for client interfaces
- Prefer `struct` parameters with named fields so arguments can’t be swapped.
- Prefer owned data (`String`) over `&str` for async/client boundaries unless there’s a strong lifetime reason.

Example:
```rust
pub struct InitializeRequest {
    pub user_id: String,
    pub user_email: String,
    pub crash_reporting_enabled: bool,
}

pub async fn initialize(&self, auth_token: Option<String>, req: InitializeRequest) -> Result<()>;
```

3) Evolve event/wire contracts compatibly
- If changing semantics, introduce an opt-in event/variant rather than overloading an existing one with different meaning.
- Add tests that enforce the old vs new event emission contract.

4) Be cautious with serialization changes
- Adding/altering serde rename behavior can break previously persisted or in-flight data.
- Guard changes with migrations, custom serializers, or compatibility annotations.

5) Keep public API surfaces intentional
- Wrap internal complexity behind a stable facade so consumers use the intended abstraction (and don’t mix incompatible keys/models/types).

These practices reduce misuse at the boundary, make intent obvious at call sites, and prevent subtle regressions when contracts evolve.