---
title: Use consistent error handling
description: Apply standardized error handling patterns across your codebase for improved
  reliability and debugging. For new code, use the `absl` error types instead of `tsl::errors`
  and include descriptive error messages with context.
repository: tensorflow/tensorflow
label: Error Handling
language: Other
comments_count: 9
repository_stars: 190625
---

Apply standardized error handling patterns across your codebase for improved reliability and debugging. For new code, use the `absl` error types instead of `tsl::errors` and include descriptive error messages with context.

Key practices:
1. Use `absl` error types with `absl::StrCat` for error messages
2. Perform validation checks early in functions
3. Use appropriate error handling mechanisms for your function's return type
4. Return `StatusOr<T>` for operations that can fail instead of raw values

```cpp
// Instead of:
return errors::InvalidArgument("Invalid shape: ", shape.DebugString());

// Use:
return absl::InvalidArgumentError(
    absl::StrCat("Invalid shape: ", shape.DebugString()));

// For void functions, use the proper macro:
OP_REQUIRES(ctx, input.shape().dim_size(i) != 0,
           absl::InvalidArgumentError("Invalid input: Dimension cannot be 0."));

// For functions that can fail, return StatusOr:
StatusOr<string> GetDeviceNameFromStreamDeviceName(const string& stream_name) {
  if (!IsValidStreamName(stream_name)) {
    return absl::InvalidArgumentError("Invalid stream device name");
  }
  return ParsedName;
}
```