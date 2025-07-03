---
title: Specific exceptions with context
description: Always throw the most specific exception type appropriate for the error
  condition and include contextual information in the error message. This helps developers
  quickly identify and fix issues.
repository: dotnet/runtime
label: Error Handling
language: C#
comments_count: 9
repository_stars: 16578
---

Always throw the most specific exception type appropriate for the error condition and include contextual information in the error message. This helps developers quickly identify and fix issues.

Key practices:
1. Use derived exception types instead of base types (e.g., `PlatformNotSupportedException` instead of `NotSupportedException`)
2. For cancellation scenarios, accept both `OperationCanceledException` and `TaskCanceledException`
3. Include relevant context in exception messages, avoiding generic "unknown error" messages
4. Test exception messages to ensure they provide meaningful information

Example:
```csharp
// Bad
throw new Exception("Operation failed");
// or
throw new CryptographicException("Unknown error (0xc100000d)");

// Good
throw new PlatformNotSupportedException(
    SR.Format(SR.ProcessStartSingleFeatureNotSupported, nameof(feature)));
// or
await Assert.ThrowsAnyAsync<OperationCanceledException>(() => 
    operation.ExecuteAsync(cancellationToken));
```
