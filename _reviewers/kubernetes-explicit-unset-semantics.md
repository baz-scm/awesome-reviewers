---
title: Explicit Unset Semantics
description: 'For any API field that is optional or whose zero-value may be ambiguous,
  make “unset/absent” semantics explicit and implement them consistently.


  Apply this standard:'
repository: kUbernetes/kUbernetes
label: Null Handling
language: Other
comments_count: 2
repository_stars: 128688
---

For any API field that is optional or whose zero-value may be ambiguous, make “unset/absent” semantics explicit and implement them consistently.

Apply this standard:
- Enums/integers:
  - If you need to distinguish “not provided” from “provided as value 0”, add an explicit `UNSPECIFIED` (or similar) enum value and handle it separately.
  - If absence and value 0 must be equivalent, make value 0 a named default (e.g., `RuntimeDefault = 0`) and ensure your docs + code treat them identically.
- Optional messages/embedded messages:
  - Check whether the message/field was actually set (presence), not only the nested enum value. A zero enum inside an absent message must not be treated as “explicitly requested”.
- Don’t rely on “silently ignored” behavior unless the contract clearly defines it; document the rule and ensure the implementation follows it.

Example pattern (presence vs enum value):
```proto
message SecurityProfileBase {
  enum BaseType {
    BaseTypeUnspecified = 0;
    RuntimeDefault = 0; // if absence and 0 are equivalent by contract
    Localhost = 1;
  }
}
```
```go
if req.SecurityProfile.base_profile != nil {
  // Message is set: enum value controls behavior.
  switch req.SecurityProfile.base_profile.type {
  case RuntimeDefault:
    // Apply runtime default restrictions.
  case Localhost:
    // Apply localhost restrictions.
  default:
    // If you added UNSPECIFIED, handle it explicitly.
  }
} else {
  // Message absent: do NOT apply extra restrictions beyond what the runtime already does.
}
```

This prevents accidental behavior changes caused by conflating “absent” with “0”, and avoids ambiguous null/undefined semantics in API handling.