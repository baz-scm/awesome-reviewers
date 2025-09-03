---
title: comprehensive null checks
description: When checking for null or undefined values in conditional statements,
  ensure all related nullable dependencies are validated together in the same condition.
  Partial null checks can lead to runtime errors when some dependencies are validated
  while others are not.
repository: novuhq/novu
label: Null Handling
language: TSX
comments_count: 2
repository_stars: 37700
---

When checking for null or undefined values in conditional statements, ensure all related nullable dependencies are validated together in the same condition. Partial null checks can lead to runtime errors when some dependencies are validated while others are not.

This prevents scenarios where code proceeds with some required values present but others potentially null or undefined. Always group related null checks to maintain consistency and prevent edge cases.

Example:
```typescript
// Before - incomplete null checking
if (!user || !currentEnvironment) {
  return;
}
// currentOrganization could still be null/undefined

// After - comprehensive null checking  
if (!user || !currentEnvironment || !currentOrganization) {
  return;
}
```

Additionally, consider simplifying complex union types that include nullable variants, as they can make comprehensive null checking more difficult and error-prone.