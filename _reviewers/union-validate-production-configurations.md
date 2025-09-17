---
title: Validate production configurations
description: Always validate configuration values and ensure production safety by
  avoiding hardcoded values, implementing proper defaults, and requiring explicit
  configuration for production-critical settings. Configuration should be validated
  at runtime to prevent deployment of incorrect values.
repository: unionlabs/union
label: Configurations
language: Other
comments_count: 6
repository_stars: 74800
---

Always validate configuration values and ensure production safety by avoiding hardcoded values, implementing proper defaults, and requiring explicit configuration for production-critical settings. Configuration should be validated at runtime to prevent deployment of incorrect values.

Key practices:
- Use placeholder variables instead of hardcoded addresses or tokens: `$CONTRACT_ADDRESS` instead of specific addresses
- Make production-critical configurations required rather than optional with unsafe defaults: "required BC the default is intended for local devnet scenarios, and is not viable for production"
- Validate configuration constraints: "The `path` field in the packet must be zero for staking operations. The staked token must match the governance token configured for the channel"
- Verify configuration values are correct: ensure constants like `keccak256("wasm")` vs just `"wasm"` are accurate
- Test configuration updates safely before deployment, especially for dependency versions

Example:
```rust
// Bad - hardcoded production address
contract_addr: "union1m87a5scxnnk83wfwapxlufzm58qe2v65985exff70z95a2yr86yq7hl08h"

// Good - configurable with validation
contract_addr: env::var("CONTRACT_ADDRESS")
    .expect("CONTRACT_ADDRESS must be set for production")
```

This prevents production footguns and ensures configurations are explicit, validated, and safe for deployment.