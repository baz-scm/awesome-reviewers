---
title: Use descriptive semantic names
description: Choose names that clearly communicate purpose, intent, and functionality
  rather than generic or abbreviated alternatives. Names should follow Rust conventions
  (snake_case for variables, functions, modules) and accurately describe what they
  represent or do.
repository: unionlabs/union
label: Naming Conventions
language: Rust
comments_count: 8
repository_stars: 74800
---

Choose names that clearly communicate purpose, intent, and functionality rather than generic or abbreviated alternatives. Names should follow Rust conventions (snake_case for variables, functions, modules) and accurately describe what they represent or do.

Key principles:
- Use descriptive field names: `cw20_impl` instead of `cw20_base`
- Method names should reflect their actual behavior: `GetStatusCommitment` instead of `GetCommittedStatus` when returning a hash commitment
- Follow Rust naming conventions: `consensus_state_bytes` not `consensusStateBytes`
- Use proper types with semantic names: `Address` and `B256` instead of generic `&[u8]`
- Choose meaningful type aliases: avoid generic names like `SharedMap` without context

Example:
```rust
// Poor naming
pub fn new_beacon_light_client_update() -> BeaconUpdate { ... }
pub const UNION_IBC: &str = "union:union-ibc";
struct MsgCreateClient {
    bytes consensusStateBytes;  // camelCase, unclear
}

// Better naming  
pub fn into_beacon_light_client_update() -> BeaconUpdate { ... }
pub const UNION_IBC: &str = "union:ibc-union";
struct MsgCreateClient {
    bytes consensus_state_bytes;  // snake_case, clear
}
```

Names are the primary way developers understand code intent - invest in clarity over brevity.