---
title: API interface design
description: Design APIs with clean abstractions, logical data organization, and proper
  layer separation. Structure interfaces to group related data hierarchically and
  provide convenient helper functions instead of requiring manual object construction.
repository: unionlabs/union
label: API
language: Other
comments_count: 4
repository_stars: 74800
---

Design APIs with clean abstractions, logical data organization, and proper layer separation. Structure interfaces to group related data hierarchically and provide convenient helper functions instead of requiring manual object construction.

Key principles:
- Organize data logically (e.g., group assets under chains rather than as flat lists)
- Separate concerns between API layers (handle filtering in GraphQL queries, not in rendering)
- Provide constructor helpers for complex objects instead of manual assembly
- Use clear, typed interfaces with descriptive field names

Example of good API design:
```typescript
// Instead of manual object construction:
let currentTransactionParams = {
  account: account.address,
  abi: ucs03ZkgmAbi,
  chain: sepolia,
  // ... many more fields
}

// Provide helper constructors:
const params = createTransactionParams({
  sourceChain: Chain,
  ucs03address: Address, 
  value: BigInt,
  baseToken: Address,
  receiver: Hex
});
```

For GraphQL APIs, structure queries to reflect logical relationships and handle data processing at the appropriate layer rather than pushing complexity to consumers.