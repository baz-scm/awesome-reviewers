---
title: Structure endpoints for REST
description: 'Organize API endpoints hierarchically by resource type and use appropriate
  HTTP methods based on operation semantics. Group related operations under resource-based
  paths, use debug prefixes for administrative endpoints, and select HTTP methods
  that match the operation''s behavior:'
repository: neondatabase/neon
label: API
language: Rust
comments_count: 7
repository_stars: 19015
---

Organize API endpoints hierarchically by resource type and use appropriate HTTP methods based on operation semantics. Group related operations under resource-based paths, use debug prefixes for administrative endpoints, and select HTTP methods that match the operation's behavior:

- Use resource paths like `/v1/resource/sub-resource`
- Place debug/admin endpoints under `/debug/v1/`
- Use GET for retrieval
- Use POST for async operations
- Use PUT for synchronous updates
- Return 202 Accepted for async operations

Example:
```rust
Router::new()
    // Resource endpoints
    .route("/v1/lfc/prewarm", get(get_prewarm_status))
    .route("/v1/lfc/prewarm", post(start_prewarm))
    .route("/v1/lfc/offload", get(get_offload_status)) 
    .route("/v1/lfc/offload", post(start_offload))
    // Debug endpoints
    .route("/debug/v1/feature_flag", put(override_flag))
```