---
title: Validate network addresses
description: Always validate network addresses according to their specific protocol
  requirements and maintain consistent encoding throughout the application. Different
  blockchain networks have distinct address formats and validation rules that must
  be enforced to prevent communication failures.
repository: unionlabs/union
label: Networking
language: Other
comments_count: 2
repository_stars: 74800
---

Always validate network addresses according to their specific protocol requirements and maintain consistent encoding throughout the application. Different blockchain networks have distinct address formats and validation rules that must be enforced to prevent communication failures.

For each destination network, implement proper validation:
- EVM chains: Validate checksum and format (0x prefixed, 40 hex characters)
- Cosmos-based chains: Validate bech32 encoding with correct prefix
- Other protocols: Apply their specific validation rules

Ensure address encoding consistency across all network operations. Inconsistent encoding (like using checksummed vs non-checksummed addresses) can cause lookup failures and break packet transmission.

Example validation approach:
```javascript
// Validate based on destination chain
if (isEvmChain(destinationChain)) {
  if (!isValidEvmAddress(address) || !hasValidChecksum(address)) {
    throw new Error('Invalid EVM address or checksum');
  }
} else if (isCosmosChain(destinationChain)) {
  if (!isValidBech32Address(address, expectedPrefix)) {
    throw new Error('Invalid bech32 address or prefix');
  }
}
```

This prevents network communication failures and ensures reliable cross-chain operations.