---
title: ensure exception safety
description: Always ensure proper exception safety by placing cleanup code in @finally
  blocks, using stack-allocated exceptions, and implementing comprehensive exception
  handling for different types. Resource cleanup must occur even when exceptions are
  thrown to prevent memory leaks.
repository: facebook/react-native
label: Error Handling
language: Other
comments_count: 3
repository_stars: 123178
---

Always ensure proper exception safety by placing cleanup code in @finally blocks, using stack-allocated exceptions, and implementing comprehensive exception handling for different types. Resource cleanup must occur even when exceptions are thrown to prevent memory leaks.

Key practices:
- Place cleanup code like `[retainedObjectsForInvocation removeAllObjects]` in @finally blocks, not after catch blocks
- Use `throw std::runtime_error(...)` instead of `throw new std::runtime_error(...)` for C++ exceptions
- Implement comprehensive exception handling for different types (NSException, NSError, NSString, std::exception, etc.)

Example:
```cpp
@try {
  [inv invokeWithTarget:strongModule];
} @catch (NSException *exception) {
  caughtException = maybeCatchException(shouldCatchException, exception);
} @catch (NSError *error) {
  caughtException = maybeCatchException(shouldCatchException, error);
} @finally {
  [retainedObjectsForInvocation removeAllObjects]; // Always cleanup
}

// For C++ exceptions, use stack allocation
throw std::runtime_error("Error message");
```

This ensures robust error handling while preventing resource leaks and maintaining proper exception semantics.