---
title: Catch specific exceptions
description: Always catch specific exception types rather than using general catch
  blocks. This improves error handling precision, enables targeted recovery strategies,
  and maintains consistency across your codebase.
repository: octokit/octokit.net
label: Error Handling
language: C#
comments_count: 4
repository_stars: 2793
---

Always catch specific exception types rather than using general catch blocks. This improves error handling precision, enables targeted recovery strategies, and maintains consistency across your codebase.

When implementing error handling:

1. **Catch specific exceptions** that you can meaningfully handle, not broad exception types
2. **Create custom exception types** for distinct error conditions rather than relying on string parsing
3. **Maintain consistency** with existing error handling patterns in your codebase

```csharp
// Avoid:
try {
    var httpStatusCode = await Connection.Delete(endpoint, new object(), AcceptHeaders.InvitationsApiPreview);
    return httpStatusCode == HttpStatusCode.NoContent;
} catch {
    return false; // Swallows ALL exceptions, including unexpected ones
}

// Preferred:
try {
    var httpStatusCode = await Connection.Delete(endpoint, new object(), AcceptHeaders.InvitationsApiPreview);
    return httpStatusCode == HttpStatusCode.NoContent;
} catch (NotFoundException) {
    // Only handle the specific case we expect and understand
    return false;
}

// When detecting specific error conditions, create custom exceptions:
if (body.Contains("secondary rate limit")) {
    // Don't rely on string matching
    throw new SecondaryRateLimitExceededException();
}
```

Catching specific exceptions ensures your error handling is predictable and that unexpected errors are properly propagated rather than silently ignored. This leads to more robust code that fails fast when encountering truly exceptional conditions.