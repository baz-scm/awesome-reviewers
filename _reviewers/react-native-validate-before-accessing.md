---
title: validate before accessing
description: Always validate parameters for both null values and correct types before
  accessing their properties or methods. Provide safe fallback values when validation
  fails to prevent crashes and undefined behavior.
repository: facebook/react-native
label: Null Handling
language: Other
comments_count: 5
repository_stars: 123178
---

Always validate parameters for both null values and correct types before accessing their properties or methods. Provide safe fallback values when validation fails to prevent crashes and undefined behavior.

This pattern prevents common crashes from null dereference and type mismatches. Instead of assuming parameters are valid, explicitly check both nullability and type before use.

Example from the codebase:
```objective-c
// Bad - assumes parameters are valid
std::string([type UTF8String])

// Good - validates type and null, provides fallback
const char *typeCStr = [type isKindOfClass:[NSString class]] && type ? [type UTF8String] : "";
```

For JavaScript/C++ interop:
```cpp
// Bad - direct access without validation
jsi::String stringValue = value.getString(*runtime);

// Good - check type first, use safe conversion
if (value.isString()) {
  jsi::String stringValue = value.asString(*runtime);
}
```

Apply this pattern when:
- Converting between different type systems (JS/Objective-C/C++)
- Accessing properties of potentially null objects
- Working with optional or nullable parameters
- Processing user input or external data

The key is to fail gracefully with meaningful defaults rather than crashing on unexpected null or wrong-type values.