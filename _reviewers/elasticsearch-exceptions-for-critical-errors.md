---
title: Exceptions for critical errors
description: Use exceptions rather than assertions for handling critical error conditions
  that need to be caught in production. Assertions should only be used for development-time
  invariant checking that should never occur in production code.
repository: elastic/elasticsearch
label: Error Handling
language: Java
comments_count: 4
repository_stars: 73104
---

Use exceptions rather than assertions for handling critical error conditions that need to be caught in production. Assertions should only be used for development-time invariant checking that should never occur in production code.

Bad:
```java
assert bestAssignment != -1 : "Failed to assign vector to centroid";
```

Good:
```java
if (bestAssignment == -1) {
    throw new IllegalStateException("Failed to assign vector to centroid");
}
```

Assertions are disabled by default in production environments, which means critical error conditions could be silently ignored. This can lead to data corruption or system instability. Instead:

1. Use exceptions for error conditions that:
   - Need to be handled by calling code
   - Represent invalid states that could occur in production
   - Should trigger error reporting/monitoring
   
2. Reserve assertions for:
   - Validating internal implementation invariants
   - Checking preconditions during development/testing
   - Documenting assumptions that should never be violated

When choosing between exceptions and assertions, ask "Should this error be caught and handled in production?" If yes, use an exception.
