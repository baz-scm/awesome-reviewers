---
title: Complete authentication testing
description: Always verify both positive and negative authentication scenarios in
  your security tests. For each authentication mechanism, test that credentials are
  properly included when required and correctly absent when not needed. This comprehensive
  approach prevents potential authentication bypasses and ensures proper access control.
repository: Azure/azure-sdk-for-net
label: Security
language: C#
comments_count: 1
repository_stars: 5809
---

Always verify both positive and negative authentication scenarios in your security tests. For each authentication mechanism, test that credentials are properly included when required and correctly absent when not needed. This comprehensive approach prevents potential authentication bypasses and ensures proper access control.

For example, when testing Authorization headers:

```csharp
// Test when authentication should NOT be applied
if (noAuthCondition)
{
    Assert.IsFalse(request.Headers.TryGetValue("Authorization", out _), 
        "Request should not have an Authorization header.");
}
// Test when authentication SHOULD be applied
else
{
    Assert.IsTrue(request.Headers.TryGetValue("Authorization", out var authHeader), 
        "Request should have an Authorization header.");
    Assert.IsFalse(string.IsNullOrEmpty(authHeader), 
        "Authorization header should be populated.");
}
```

This pattern ensures your authentication mechanisms work correctly in all scenarios, which is critical for maintaining security boundaries.
