---
title: Check exceptions consistently
description: Always check for exceptions immediately after operations that might throw
  them, especially before using the results in control flow decisions. When accessing
  properties that might be used in conditionals, retrieve the property first, check
  for exceptions, and then use the property in the conditional.
repository: oven-sh/bun
label: Error Handling
language: C++
comments_count: 6
repository_stars: 79093
---

Always check for exceptions immediately after operations that might throw them, especially before using the results in control flow decisions. When accessing properties that might be used in conditionals, retrieve the property first, check for exceptions, and then use the property in the conditional.

**Incorrect pattern:**
```cpp
if (JSValue property = object->getIfPropertyExists(globalObject, propertyName)) {
    // Use property...
    RETURN_IF_EXCEPTION(scope, {});  // Too late - exception may have occurred during getIfPropertyExists
}
```

**Correct pattern:**
```cpp
JSValue property = object->getIfPropertyExists(globalObject, propertyName);
RETURN_IF_EXCEPTION(scope, {});  // Check immediately after the operation
if (property) {
    // Now safe to use property...
}
```

This pattern applies to any function that might throw exceptions, including property access, method calls, and object construction. Ensure exception checking occurs after each potentially throwing operation and before using its results. Use consistent macros like `RETURN_IF_EXCEPTION` or `RELEASE_AND_RETURN` based on your codebase's conventions.

For property chains or multiple operations, check after each step:
```cpp
auto value = params->get(globalObject, property);
RETURN_IF_EXCEPTION(scope, nullptr);
// Now safe to use value
```

Following this pattern prevents hard-to-debug crashes and ensures exceptions are properly handled throughout all code paths.