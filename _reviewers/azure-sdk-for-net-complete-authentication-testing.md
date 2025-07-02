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


[
  {
    "discussion_id": "2152576930",
    "pr_number": 50644,
    "pr_file": "sdk/core/System.ClientModel/tests/Auth/AuthenticationTokenProviderTests.cs",
    "created_at": "2025-06-17T15:31:33+00:00",
    "commented_code": "options.Transport = new MockPipelineTransport(\"foo\",\n            m =>\n            {\n                // Assert that the request has no authentication headers\n                Assert.IsFalse(m.Request.Headers.TryGetValue(\"Authorization\", out _), \"Request should not have an Authorization header.\");\n                m.TryGetProperty(typeof(GetTokenOptions), out var flowsObj);\n                if (\n                    flowsObj == null ||\n                    (flowsObj is Dictionary<string, object>[] flowsArr && flowsArr.Length == 0)\n                )\n                {\n                    // Only assert no Authorization header if operation does not override the service level flows.\n                    Assert.IsFalse(m.Request.Headers.TryGetValue(\"Authorization\", out _), \"Request should not have an Authorization header.\");\n                }",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2152576930",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50644,
        "pr_file": "sdk/core/System.ClientModel/tests/Auth/AuthenticationTokenProviderTests.cs",
        "discussion_id": "2152576930",
        "commented_code": "@@ -123,17 +194,27 @@ public NoAuthClient(Uri uri, AuthenticationTokenProvider credential)\n             options.Transport = new MockPipelineTransport(\"foo\",\n             m =>\n             {\n-                // Assert that the request has no authentication headers\n-                Assert.IsFalse(m.Request.Headers.TryGetValue(\"Authorization\", out _), \"Request should not have an Authorization header.\");\n+                m.TryGetProperty(typeof(GetTokenOptions), out var flowsObj);\n+                if (\n+                    flowsObj == null ||\n+                    (flowsObj is Dictionary<string, object>[] flowsArr && flowsArr.Length == 0)\n+                )\n+                {\n+                    // Only assert no Authorization header if operation does not override the service level flows.\n+                    Assert.IsFalse(m.Request.Headers.TryGetValue(\"Authorization\", out _), \"Request should not have an Authorization header.\");\n+                }",
        "comment_created_at": "2025-06-17T15:31:33+00:00",
        "comment_author": "christothes",
        "comment_body": "we need an else block here to assert that the Authorization header is present and populated.",
        "pr_file_module": null
      }
    ]
  }
]
