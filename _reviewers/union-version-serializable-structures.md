---
title: Version serializable structures
description: All serializable data structures that may evolve over time must include
  explicit versioning to enable backward and forward compatibility during migrations.
  This prevents breaking changes when schemas need to evolve and allows for graceful
  handling of different versions.
repository: unionlabs/union
label: Migrations
language: Rust
comments_count: 2
repository_stars: 74800
---

All serializable data structures that may evolve over time must include explicit versioning to enable backward and forward compatibility during migrations. This prevents breaking changes when schemas need to evolve and allows for graceful handling of different versions.

Implement versioning using enums that wrap versioned variants:

```rust
// Instead of this:
#[derive(serde::Serialize, serde::Deserialize)]
pub struct ClientState {
    pub chain_id: U256,
    pub latest_height: u64,
    pub ibc_contract_address: H160,
}

// Do this:
#[derive(serde::Serialize, serde::Deserialize)]
pub enum ClientState {
    V1(ClientStateV1),
}

#[derive(serde::Serialize, serde::Deserialize)]
pub struct ClientStateV1 {
    pub chain_id: U256,
    pub latest_height: u64,
    pub ibc_contract_address: H160,
}
```

For message-based systems, include a version field and define compatibility rules - consumers should reject unsupported versions while maintaining backward compatibility for supported ones. This approach enables controlled schema evolution and prevents runtime failures during system upgrades.