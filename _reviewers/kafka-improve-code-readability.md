---
title: Improve code readability
description: Write code that prioritizes readability through clear string formatting,
  descriptive method calls, and well-organized structure. Use string interpolation
  instead of concatenation for better readability, choose descriptive assertion methods
  that provide meaningful error messages, avoid code duplication by leveraging method
  overloading, and extract complex...
repository: apache/kafka
label: Code Style
language: Other
comments_count: 4
repository_stars: 30575
---

Write code that prioritizes readability through clear string formatting, descriptive method calls, and well-organized structure. Use string interpolation instead of concatenation for better readability, choose descriptive assertion methods that provide meaningful error messages, avoid code duplication by leveraging method overloading, and extract complex logic into focused methods.

For string formatting, prefer interpolated strings:
```scala
// Instead of:
throw new TerseFailure("Unknown metadata.version " + releaseVersion + ". Supported metadata.version are " + metadataVersionsToString(...))

// Use:
throw new TerseFailure(s"Unknown metadata.version $releaseVersion. Supported metadata.version are ${metadataVersionsToString(...)}")
```

For assertions, use descriptive methods:
```scala
// Instead of:
assertTrue(memberId != JoinGroupRequest.UNKNOWN_MEMBER_ID)

// Use:
assertNotEquals(JoinGroupRequest.UNKNOWN_MEMBER_ID, memberId)
```

Avoid code duplication by overloading existing methods rather than creating similar methods with slight variations. When methods become complex, extract the core logic into separate, focused methods that can be easily tested and understood. This approach reduces cognitive load, improves maintainability, and makes code reviews more effective.