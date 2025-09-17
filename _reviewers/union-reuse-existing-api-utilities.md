---
title: Reuse existing API utilities
description: Before implementing custom API utilities, serializers, or type identification
  methods, check if equivalent functionality already exists in the codebase or standard
  libraries. This prevents code duplication, ensures consistency across the API surface,
  and leverages well-tested implementations.
repository: unionlabs/union
label: API
language: Rust
comments_count: 3
repository_stars: 74800
---

Before implementing custom API utilities, serializers, or type identification methods, check if equivalent functionality already exists in the codebase or standard libraries. This prevents code duplication, ensures consistency across the API surface, and leverages well-tested implementations.

Key practices:
- Search for existing utilities in shared crates before writing custom implementations
- Use trait-provided methods for standard operations like type identification
- Verify API feature compatibility with the target environment before usage

Examples from the codebase:
```rust
// Instead of custom deserializer:
#[serde(default, deserialize_with = "deserialize_opt_u64_from_string")]
// Use existing utility:
// Available in serde_utils crate

// Instead of hardcoded type URLs:
type_url: "/ibc.applications.transfer.v1.MsgTransfer".to_string(),
// Use trait method:
type_url: MsgTransfer::type_url(),

// Avoid incompatible features:
#[sol(rpc, all_derives)] // Don't use 'rpc' in cosmwasm contracts
```

This approach reduces maintenance burden, improves code reliability, and maintains API consistency across the project.