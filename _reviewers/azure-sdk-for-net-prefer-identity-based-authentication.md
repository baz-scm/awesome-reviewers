---
title: Prefer identity-based authentication
description: Always prioritize modern identity-based authentication methods over traditional
  username/password credentials. This improves security by reducing credential exposure
  and management overhead.
repository: Azure/azure-sdk-for-net
label: Security
language: Markdown
comments_count: 3
repository_stars: 5809
---

Always prioritize modern identity-based authentication methods over traditional username/password credentials. This improves security by reducing credential exposure and management overhead.

Specifically:
- Use managed identities where available in Azure services
- Consider federated identity credentials for cross-service authentication
- Leverage Entra User authentication instead of username/password for administrative access

This approach eliminates the need to store and manage sensitive credentials in your code or configuration files, reducing the risk of credential leakage.

Example implementation for using managed identity with a client factory:

```csharp
// Configure the client factory to use managed identity
builder.Services.AddAzureClients(clientBuilder =>
{
    // Using managed identity as a federated identity credential
    clientBuilder.UseCredential("managedidentityasfederatedidentity")
        .ConfigureDefaults(azureDefaults =>
        {
            azureDefaults.Authentication.ManagedIdentityClientId = "your-client-id";
        });
});
```

When creating services like HDInsight clusters, prefer specifying Entra User as the administrator credential rather than username/password combinations.
