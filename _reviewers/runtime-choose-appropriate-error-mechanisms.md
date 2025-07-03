---
title: Choose appropriate error mechanisms
description: 'Use the right error handling mechanism for each scenario: exceptions
  for recoverable situations, assertions only for true programming bugs, and consistent
  error codes for API boundaries. Don''t assert unreachable for scenarios that could
  legitimately occur, such as in this example:'
repository: dotnet/runtime
label: Error Handling
language: C++
comments_count: 4
repository_stars: 16578
---

Use the right error handling mechanism for each scenario: exceptions for recoverable situations, assertions only for true programming bugs, and consistent error codes for API boundaries. Don't assert unreachable for scenarios that could legitimately occur, such as in this example:

```cpp
// Instead of this:
if (!BlockRange().TryGetUse(mask, &use))
{
    unreached(); // Bad: this could legitimately occur
}

// Do this:
if (BlockRange().TryGetUse(mask, &use))
{
    use.ReplaceWith(node);
}
else 
{
    node->SetUnusedValue(); // Gracefully handle the case
}
```

Always validate input values to prevent runtime errors like division-by-zero:

```cpp
DWORD cacheSize = CLRConfig::GetConfigValue(CLRConfig::UNSUPPORTED_NativeToILOffsetCacheSize);
if (cacheSize < 1)
{
    cacheSize = 1; // Ensure cache size is at least 1 to prevent division-by-zero
}
```

For API design, use standard error reporting mechanisms rather than boolean out parameters. When throwing exceptions, select appropriate exception types that reflect the nature of the error, such as `PlatformNotSupportedException` for unsupported hardware features instead of failing fast with generic errors.
