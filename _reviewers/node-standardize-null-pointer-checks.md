---
title: Standardize null pointer checks
description: Always use standard null-checking patterns like CHECK_NOT_NULL for pointer
  validation instead of manual null checks. This ensures consistent error handling
  and improves code readability. For functions that may return null objects, consider
  using wrapper types like MaybeLocal to properly propagate null states.
repository: nodejs/node
label: Null Handling
language: Other
comments_count: 5
repository_stars: 112178
---

Always use standard null-checking patterns like CHECK_NOT_NULL for pointer validation instead of manual null checks. This ensures consistent error handling and improves code readability. For functions that may return null objects, consider using wrapper types like MaybeLocal to properly propagate null states.

Example:
```cpp
// Incorrect - manual null check
if (network_resource_manager_ == nullptr) {
  return protocol::DispatchResponse::ServerError("...");
}

// Correct - using standard macro
CHECK_NOT_NULL(network_resource_manager_);

// Correct - using MaybeLocal for nullable returns
MaybeLocal<Object> CreateObject(Isolate* isolate) {
  if (some_condition) return MaybeLocal<Object>();  // Return empty handle
  return Object::New(isolate);
}
```