---
title: API completeness validation
description: Ensure APIs are complete by validating that all necessary cases are handled,
  all required arguments are properly validated, and response structures are consistent
  across similar operations.
repository: apache/kafka
label: API
language: Java
comments_count: 5
repository_stars: 30575
---

Ensure APIs are complete by validating that all necessary cases are handled, all required arguments are properly validated, and response structures are consistent across similar operations.

Key areas to check:
1. **Switch statement completeness**: When adding new enum values or operation types, ensure all switch statements that handle them include the new cases
2. **Argument validation coverage**: Test all invalid argument combinations, not just the happy path scenarios
3. **Response structure consistency**: Maintain consistent field presence across similar API responses (e.g., if one response has top-level error codes, related responses should too)
4. **Parameter naming consistency**: Follow established naming conventions from KIPs and existing APIs

Example from the discussions:
```java
// Incomplete - missing new RPC cases
case UPDATE_VOTER:
    handledSuccessfully = handleUpdateVoterResponse(response, currentTimeMs);
    break;
// Need to add:
case ADD_RAFT_VOTER:
    handledSuccessfully = handleAddVoterResponse(response, currentTimeMs);
    break;
case REMOVE_RAFT_VOTER:
    handledSuccessfully = handleRemoveVoterResponse(response, currentTimeMs);
    break;
```

This prevents runtime failures from unhandled cases and ensures consistent developer experience across the API surface.