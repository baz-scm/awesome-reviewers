---
title: Design stable APIs
description: When creating or modifying APIs, carefully consider what becomes part
  of your public API surface to ensure backward compatibility and consistent developer
  experience.
repository: Azure/azure-sdk-for-net
label: API
language: Markdown
comments_count: 7
repository_stars: 5809
---

When creating or modifying APIs, carefully consider what becomes part of your public API surface to ensure backward compatibility and consistent developer experience.

Key practices:
1. Use specific, descriptive names for API elements that follow established patterns (e.g., `TerraformAuthorizationScopeFilter` instead of generic `AuthorizationScopeFilter`)
2. Avoid exposing implementation details or utility methods that might need to change later
3. Ensure consistent behavior between related API methods (e.g., streaming and non-streaming variants should follow similar patterns)
4. Prefer strongly-typed parameters over generic types like Dictionary when possible
5. Maintain consistent terminology throughout code and documentation

Example:
```csharp
// GOOD: Specific, descriptive client name with consistent method naming
PersistentAgentsClient agentClient = projectClient.GetPersistentAgentsClient();

// BAD: Generic naming or inconsistent patterns
AgentsClient agentClient = projectClient.GetAgentsClient();

// GOOD: Strongly-typed parameters
private int GetHumidityByAddress(Address address)
{
    return (address.City == "Seattle") ? 60 : 80;
}

// BAD: Generic dictionary parameters that hide the actual structure
private int GetHumidityByAddress(Dictionary<string, string> address)
{
    return (address["City"] == "Seattle") ? 60 : 80;
}
```

Before adding new public API members, consider if they're truly necessary and ensure they won't need breaking changes in the future.
