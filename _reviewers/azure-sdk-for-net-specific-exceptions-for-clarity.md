---
title: Specific exceptions for clarity
description: Use specific exception types with meaningful error messages rather than
  generic exceptions to improve error handling, debugging, and API usability. This
  allows callers to distinguish between different error conditions and respond appropriately.
repository: Azure/azure-sdk-for-net
label: Error Handling
language: C#
comments_count: 5
repository_stars: 5809
---

Use specific exception types with meaningful error messages rather than generic exceptions to improve error handling, debugging, and API usability. This allows callers to distinguish between different error conditions and respond appropriately.

Instead of:
```csharp
if (string.IsNullOrEmpty(serviceEndpoint))
    throw new Exception("Invalid service endpoint");
```

Prefer:
```csharp
if (string.IsNullOrEmpty(serviceEndpoint))
    throw new ArgumentException("The service endpoint must be a valid URL", nameof(serviceEndpoint));
```

Key practices:
1. Match exception types to error conditions: Use `ArgumentException` for invalid arguments, `InvalidOperationException` for improper state, and `NotSupportedException` instead of `NotImplementedException` for unsupported operations.

2. Include actionable details in error messages: Specify what went wrong and how to fix it.

3. Use reliable error detection: Check specific exception properties or error codes rather than string matching:
```csharp
// Instead of: 
catch (Exception ex) when (ex.Message.Contains("timed out"))

// Prefer:
catch (RequestFailedException ex) when (ex.Status == 408)
```

4. Validate assumptions explicitly: Check for null or invalid values before operations that assume they exist.
```csharp
// Instead of:
arguments.Add(methodParameters.Single(p => p.Name == parameter.Name));

// Prefer:
var matchingParameter = methodParameters.SingleOrDefault(p => p.Name == parameter.Name);
if (matchingParameter == null)
{
    throw new InvalidOperationException($"No matching parameter found for '{parameter.Name}' in methodParameters.");
}
arguments.Add(matchingParameter);
```
