---
title: Surface errors appropriately
description: Ensure errors are visible and properly handled rather than silently processed
  or hidden. Provide mechanisms for developers to handle errors explicitly, especially
  in libraries or frameworks with automated processes. Hidden or automatically handled
  errors can mask bugs and make debugging difficult.
repository: Azure/azure-sdk-for-net
label: Error Handling
language: Markdown
comments_count: 3
repository_stars: 5809
---

Ensure errors are visible and properly handled rather than silently processed or hidden. Provide mechanisms for developers to handle errors explicitly, especially in libraries or frameworks with automated processes. Hidden or automatically handled errors can mask bugs and make debugging difficult.

When implementing automated processes:
1. Offer explicit error handling hooks or overridable methods
2. Consider logging errors appropriately before taking automated action
3. For retry mechanisms, follow service documentation for proper backoff strategies and durations

Example:
```csharp
// Instead of auto-handling errors silently:
options.EnableAutoFunctionCalls(delegates);

// Provide an override mechanism for error handling:
options.EnableAutoFunctionCalls(delegates, errorHandler: (exception, context) => {
    // Log the error
    logger.LogWarning($"Function call error: {exception.Message}");
    
    // Allow custom handling logic
    if (exception is TimeoutException)
        return ErrorResolution.Retry;
    else
        return ErrorResolution.Rethrow;
});
```

When dealing with transient errors like throttling or service unavailability, implement retry policies that respect documented service requirements (e.g., retrying for adequate duration) rather than failing immediately or using generic retry strategies.
