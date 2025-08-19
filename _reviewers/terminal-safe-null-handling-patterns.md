---
title: Safe null handling patterns
description: Always use consistent and safe patterns when dealing with potentially
  null or undefined values. This includes using safe casting methods, explicit null
  checks, proper initialization, and immutable variables after validation.
repository: microsoft/terminal
label: Null Handling
language: Other
comments_count: 4
repository_stars: 99242
---

Always use consistent and safe patterns when dealing with potentially null or undefined values. This includes using safe casting methods, explicit null checks, proper initialization, and immutable variables after validation.

Key practices:
1. **Consistent safe casting**: Use `try_as<T>()` instead of `as<T>()` to avoid runtime exceptions when casting might fail
2. **Explicit null validation**: Check for null/empty values before using them, especially in serialization contexts
3. **Proper initialization**: Initialize all member variables to prevent undefined behavior
4. **Immutable variables after checks**: Use `const auto` when storing results of null checks to prevent accidental modification

Example from the codebase:
```cpp
// Inconsistent - uses try_as in one place but as in another
if (const auto newTermArgs = _ContentArgs.try_as<NewTerminalArgs>())
{
    return newTermArgs->GetArgCount() + gsl::narrow<uint32_t>(_argDescriptors.size());
}
// Should also use try_as here for consistency
return _ContentArgs.as<NewTerminalArgs>()->GetArgDescriptorAt(index - additionalArgCount);

// Better approach - consistent safe casting
if (const auto newTermArgs = _ContentArgs.try_as<NewTerminalArgs>())
{
    return newTermArgs->GetArgDescriptorAt(index - additionalArgCount);
}

// Proper null handling in serialization
if (json.isNull())
{
    return MediaResource::FromString(L"");
}

// Proper initialization to prevent undefined behavior
UINT _systemMenuNextItemId = 0;  // Instead of leaving uninitialized
```

This pattern prevents runtime crashes, undefined behavior, and makes code more predictable and maintainable.