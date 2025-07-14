---
title: Propagate errors with context
description: Always propagate errors with their original context instead of swallowing
  them or throwing new errors that hide the original cause. This helps with debugging
  and allows proper error handling up the call stack.
repository: nodejs/node
label: Error Handling
language: Other
comments_count: 5
repository_stars: 112178
---

Always propagate errors with their original context instead of swallowing them or throwing new errors that hide the original cause. This helps with debugging and allows proper error handling up the call stack.

Key practices:
1. Avoid using USE() or Check() which hide errors
2. Return Maybe/MaybeLocal for error propagation
3. Preserve original error context in promise chains
4. Only catch errors when you can properly handle them

Example of proper error propagation:

```cpp
// Bad - Swallows error with USE
USE(promise->Then(context, callback));

// Good - Propagates error
if (promise->Then(context, callback).IsEmpty()) {
  return;  // Error already scheduled
}

// Bad - Hides original error
if (!CreateObject(isolate, context).ToLocal(&obj)) {
  return ThrowError("Failed to create object");
}

// Good - Preserves original error
if (!CreateObject(isolate, context).ToLocal(&obj)) {
  return;  // Original error propagates
}
```

This practice ensures:
- Error stack traces remain intact
- Root causes are easier to identify
- Error handling can be done at appropriate levels
- Debugging is more straightforward