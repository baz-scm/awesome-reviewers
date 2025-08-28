---
title: Use appropriate exception types
description: Choose the correct exception handling mechanism and type based on the
  error condition's nature and audience. Use JSG_REQUIRE for user-controllable conditions
  that should result in JavaScript exceptions, and KJ_ASSERT for internal invariants
  that indicate programming errors. Provide friendly, actionable error messages for
  user-facing exceptions.
repository: cloudflare/workerd
label: Error Handling
language: Other
comments_count: 8
repository_stars: 6989
---

Choose the correct exception handling mechanism and type based on the error condition's nature and audience. Use JSG_REQUIRE for user-controllable conditions that should result in JavaScript exceptions, and KJ_ASSERT for internal invariants that indicate programming errors. Provide friendly, actionable error messages for user-facing exceptions.

For reachable error paths that users might trigger, use JSG_FAIL_REQUIRE with descriptive messages instead of KJ_UNIMPLEMENTED, which generates internal Sentry errors. When constructing error messages, avoid kj::str() in KJ_ASSERT/KJ_LOG calls as this creates different Sentry fingerprints for each unique message and wastes allocations.

Example of proper exception type usage:
```cpp
// Good: User-controllable condition
JSG_REQUIRE(constructor.isFunction(), TypeError, "registerRpcTargetClass() requires a constructor function");

// Good: Internal invariant  
KJ_ASSERT(console->IsObject());

// Bad: Reachable user error as internal error
KJ_UNIMPLEMENTED("connect() not supported on StreamWorkerInterface");

// Good: Reachable user error with friendly message
JSG_FAIL_REQUIRE(Error, "connect() not supported on StreamWorkerInterface");

// Bad: String allocation in assertion
KJ_ASSERT(res.statusCode == 200, kj::str("Request failed with status ", res.statusCode));

// Good: Let KJ_ASSERT format the message
KJ_ASSERT(res.statusCode == 200, "Request failed", res.statusCode);
```

This approach ensures appropriate error handling for different audiences (users vs developers), improves error reporting and debugging, and avoids unnecessary performance overhead.