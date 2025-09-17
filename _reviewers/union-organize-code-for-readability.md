---
title: organize code for readability
description: Structure code to maximize readability and maintainability through clear
  organization patterns. Use top-level control flow structures (like switch/match
  statements) to make logic paths obvious and easy to follow. Extract reusable functionality
  into separate modules or helper libraries to promote code reuse and reduce duplication.
  Isolate different concerns...
repository: unionlabs/union
label: Code Style
language: Other
comments_count: 3
repository_stars: 74800
---

Structure code to maximize readability and maintainability through clear organization patterns. Use top-level control flow structures (like switch/match statements) to make logic paths obvious and easy to follow. Extract reusable functionality into separate modules or helper libraries to promote code reuse and reduce duplication. Isolate different concerns into their own components or functions to maintain clear boundaries and responsibilities.

For example, instead of nested conditional logic, prefer top-level pattern matching:

```solidity
function _verifyTokenOrderV2(
    uint32 channelId,
    uint256 path,
    TokenOrderV2 calldata order
) internal {
    // Switch on order.kind at top level for clarity
    if (order.kind == TokenKind.FUNGIBLE) {
        // Handle fungible token logic
    } else if (order.kind == TokenKind.NON_FUNGIBLE) {
        // Handle NFT logic
    }
    // This approach is easier to read, more gas-efficient, and less error-prone
}
```

When you notice repeated patterns or functionality that could benefit multiple parts of the codebase, extract them into dedicated modules or helper libraries. This makes the code more modular and allows developers to "plug and go" with proven solutions.