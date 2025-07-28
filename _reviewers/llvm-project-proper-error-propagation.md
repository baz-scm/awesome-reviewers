---
title: proper error propagation
description: Ensure errors are properly propagated to callers rather than handled
  locally with exits or fatal errors. Library functions should return error information
  to allow callers to make appropriate decisions about error handling and recovery.
repository: llvm/llvm-project
label: Error Handling
language: C++
comments_count: 5
repository_stars: 33702
---

Ensure errors are properly propagated to callers rather than handled locally with exits or fatal errors. Library functions should return error information to allow callers to make appropriate decisions about error handling and recovery.

Key principles:
1. **Return errors, don't exit**: Library functions should return error codes or use error types like `llvm::Expected` instead of calling `exit()` or `llvm::report_fatal_error()`
2. **Handle multiple errors systematically**: Use proper error handling APIs like `handleAllErrors()` instead of just converting errors to strings with `toString()`
3. **Check all return values**: Always check return values from functions that can fail, even if they currently always succeed
4. **Use existing error infrastructure**: Leverage existing diagnostic systems instead of creating custom error handling

Example of proper error propagation:
```cpp
// Bad: Fatal error in library function
void parseDataAccessPerfTraces(StringRef File) {
  auto BufferOrErr = MemoryBuffer::getFile(File);
  if (auto EC = BufferOrErr.getError())
    llvm::report_fatal_error(StringRef(Error)); // Don't do this
}

// Good: Return error to caller
std::error_code parseDataAccessPerfTraces(StringRef File) {
  auto BufferOrErr = MemoryBuffer::getFile(File);
  if (auto EC = BufferOrErr.getError())
    return EC; // Let caller decide how to handle
  // ... continue processing
  return std::error_code{};
}

// Good: Handle multiple errors properly
if (!RSDOrErr) {
  handleAllErrors(RSDOrErr.takeError(), [&](ErrorInfoBase &EIB) {
    Ctx->emitError(EIB.message());
  });
} // Instead of: toString(std::move(Err))
```

This approach enables better error recovery, testing, and allows different callers to handle errors appropriately for their context.