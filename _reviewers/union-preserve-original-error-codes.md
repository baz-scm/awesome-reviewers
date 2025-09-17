---
title: preserve original error codes
description: When handling errors, preserve the original error information rather
  than replacing it with generic error constants. This maintains better debugging
  information and error traceability throughout the system.
repository: unionlabs/union
label: Error Handling
language: Other
comments_count: 2
repository_stars: 74800
---

When handling errors, preserve the original error information rather than replacing it with generic error constants. This maintains better debugging information and error traceability throughout the system.

Instead of using generic error constants that lose the specific failure context:
```move
assert!(err == 0, E_INVALID_PROOF);
```

Preserve the original error code to maintain debugging information:
```move
assert!(err == 0, err);
```

This practice ensures that:
- Specific error details are not lost during error propagation
- Debugging becomes easier as the root cause error code is preserved
- Error handling maintains the original context of what actually failed
- Developers can trace back to the exact source of errors

Apply this principle consistently across error handling scenarios where you have access to the original error information. The goal is to maintain error fidelity rather than abstracting away potentially useful diagnostic information.