---
title: Explicit error handling
description: Always handle error conditions explicitly rather than silently ignoring
  them or using generic error responses. Use specific error codes that reflect business
  logic rather than low-level system errors, and throw exceptions for unexpected states
  instead of using assertions or returning generic failure indicators.
repository: ClickHouse/ClickHouse
label: Error Handling
language: C++
comments_count: 7
repository_stars: 42425
---

Always handle error conditions explicitly rather than silently ignoring them or using generic error responses. Use specific error codes that reflect business logic rather than low-level system errors, and throw exceptions for unexpected states instead of using assertions or returning generic failure indicators.

Key principles:
1. **Throw specific exceptions** for unexpected conditions rather than using assertions that can cause segfaults
2. **Use business-logic error codes** instead of generic system-level codes to provide better context
3. **Explicitly check expected error conditions** and throw exceptions for unexpected ones
4. **Avoid silent failures** - parse and validate inputs completely, throwing unsupported exceptions for unhandled cases

Example of good explicit error handling:
```cpp
// Instead of silent failure or generic error
if (code != Coordination::Error::ZOK)
    return false;  // BAD: silently ignores all error types

// Be explicit about expected vs unexpected errors
if (code == Coordination::Error::ZNONODE || code == Coordination::Error::ZNOAUTH)
    return false;  // Expected errors
else if (Coordination::isHardwareError(code))
    throw Exception(ErrorCodes::ZOOKEEPER_EXCEPTION, "Hardware error: {}", code);  // Unexpected errors

// Use specific error codes that reflect business context
throw Exception(ErrorCodes::UDF_EXECUTION_FAILED, "UDF execution failed: {}", details);
// Instead of generic: ErrorCodes::CANNOT_WRITE_TO_FILE_DESCRIPTOR

// Replace assertions with proper exceptions
chassert(tuple_function->arguments->children.size() == partition_columns.size());  // BAD
if (tuple_function->arguments->children.size() != partition_columns.size())
    throw Exception(ErrorCodes::LOGICAL_ERROR, "Partition argument count mismatch");  // GOOD
```

This approach improves debugging, provides better user experience, and prevents silent corruption of program state.