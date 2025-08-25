---
title: default least permissive
description: When implementing security controls, always default to the most restrictive
  option and require explicit opt-in for more permissive behavior. This applies to
  authentication mechanisms, user permissions, and security scanning workflows.
repository: block/goose
label: Security
language: Rust
comments_count: 3
repository_stars: 19037
---

When implementing security controls, always default to the most restrictive option and require explicit opt-in for more permissive behavior. This applies to authentication mechanisms, user permissions, and security scanning workflows.

For authentication, use centralized middleware instead of manual verification in each handler:
```rust
// Instead of manual verification in each handler
async fn start_agent(
    State(state): State<Arc<AppState>>,
    headers: HeaderMap,
    Json(payload): Json<StartAgentRequest>,
) -> Result<Json<StartAgentResponse>, (StatusCode, Json<ErrorResponse>)> {
    verify_secret_key(&headers, &state).map_err(|_| {
        // ... error handling
    })?;
    // ... handler logic
}

// Use middleware for consistent auth across all protected routes
```

For permission systems, implement security checks before user interaction and default to the most restrictive option available. When multiple security mechanisms exist (like permission checking and security scanning), apply the least permissive result from all checks.

This principle ensures that security is the default state, reducing the risk of accidentally exposing functionality or data through overly permissive configurations.