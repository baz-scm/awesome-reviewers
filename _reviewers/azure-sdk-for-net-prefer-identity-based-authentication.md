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


[
  {
    "discussion_id": "2135910121",
    "pr_number": 50436,
    "pr_file": "sdk/extensions/Microsoft.Extensions.Azure/CHANGELOG.md",
    "created_at": "2025-06-09T15:09:40+00:00",
    "commented_code": "### Features Added\n\n- Added support for [federated managed identity](https://learn.microsoft.com/entra/workload-id/workload-identity-federation-config-app-trust-managed-identity?tabs=microsoft-entra-admin-center#azureidentity) support in the client factory by specifying configuration item `credential` as \"managedidentityasfederatedidentity\" and providing the following named configuration items:",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2135910121",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50436,
        "pr_file": "sdk/extensions/Microsoft.Extensions.Azure/CHANGELOG.md",
        "discussion_id": "2135910121",
        "commented_code": "@@ -4,6 +4,16 @@\n \n ### Features Added\n \n+- Added support for [federated managed identity](https://learn.microsoft.com/entra/workload-id/workload-identity-federation-config-app-trust-managed-identity?tabs=microsoft-entra-admin-center#azureidentity) support in the client factory by specifying configuration item `credential` as \"managedidentityasfederatedidentity\" and providing the following named configuration items:",
        "comment_created_at": "2025-06-09T15:09:40+00:00",
        "comment_author": "scottaddie",
        "comment_body": "```suggestion\r\n- Added support for [managed identity as a federated identity credential](https://learn.microsoft.com/entra/workload-id/workload-identity-federation-config-app-trust-managed-identity?tabs=microsoft-entra-admin-center#azureidentity) in the client factory by specifying configuration item `credential` as \"managedidentityasfederatedidentity\" and providing the following named configuration items:\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2130868142",
    "pr_number": 50457,
    "pr_file": "sdk/identity/Azure.Identity.Broker/CHANGELOG.md",
    "created_at": "2025-06-05T23:15:49+00:00",
    "commented_code": "# Release History\n\n## 1.3.0-beta.3 (Unreleased)\n## 1.3.0-beta.3 (2025-06-10)\n\n### Features Added\n\n- Support broker on Linux.\n\n### Breaking Changes\n\n### Bugs Fixed\n- Support Microsoft Broker on Linux platforms. This library relies on the Microsoft Authentication Library (MSAL) to handle the broker, for more information about pre-requisites and how to utilize the Broker on Linux, visit [Enable SSO in native Linux apps using MSAL.NET\n](https://learn.microsoft.com/entra/msal/dotnet/acquiring-tokens/desktop-mobile/linux-dotnet-sdk?tabs=ubuntudep)",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2130868142",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50457,
        "pr_file": "sdk/identity/Azure.Identity.Broker/CHANGELOG.md",
        "discussion_id": "2130868142",
        "commented_code": "@@ -1,14 +1,11 @@\n # Release History\n \n-## 1.3.0-beta.3 (Unreleased)\n+## 1.3.0-beta.3 (2025-06-10)\n \n ### Features Added\n \n-- Support broker on Linux.\n-\n-### Breaking Changes\n-\n-### Bugs Fixed\n+- Support Microsoft Broker on Linux platforms. This library relies on the Microsoft Authentication Library (MSAL) to handle the broker, for more information about pre-requisites and how to utilize the Broker on Linux, visit [Enable SSO in native Linux apps using MSAL.NET\n+](https://learn.microsoft.com/entra/msal/dotnet/acquiring-tokens/desktop-mobile/linux-dotnet-sdk?tabs=ubuntudep)",
        "comment_created_at": "2025-06-05T23:15:49+00:00",
        "comment_author": "scottaddie",
        "comment_body": "```suggestion\r\n- Support Microsoft Broker on Linux and WSL. This library relies on the Microsoft Authentication Library (MSAL) to handle the broker. For more information about prerequisites and how to utilize the broker, see [Enable SSO in native Linux apps using MSAL.NET](https://learn.microsoft.com/entra/msal/dotnet/acquiring-tokens/desktop-mobile/linux-dotnet-sdk)\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2076996977",
    "pr_number": 49837,
    "pr_file": "sdk/hdinsight/Azure.ResourceManager.HDInsight/CHANGELOG.md",
    "created_at": "2025-05-07T07:37:09+00:00",
    "commented_code": "# Release History\n\n## 1.2.0-beta.5 (Unreleased)\n## 1.2.0-beta.5 (2025-05-07)\n\n### Features Added\n\n### Breaking Changes\n\n### Bugs Fixed\n- Upgraded api-version tag from 'package-2024-08-preview' to 'package-2025-01-preview'. Tag detail available at https://github.com/Azure/azure-rest-api-specs/blob/4c0f7731c93696af01bd2bb9927bf28d2afcbc98/specification/hdinsight/resource-manager/readme.md.\n    - Support for setting Entra User during HDInsight cluster creation.",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2076996977",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 49837,
        "pr_file": "sdk/hdinsight/Azure.ResourceManager.HDInsight/CHANGELOG.md",
        "discussion_id": "2076996977",
        "commented_code": "@@ -1,15 +1,19 @@\n # Release History\n \n-## 1.2.0-beta.5 (Unreleased)\n+## 1.2.0-beta.5 (2025-05-07)\n \n ### Features Added\n \n-### Breaking Changes\n-\n-### Bugs Fixed\n+- Upgraded api-version tag from 'package-2024-08-preview' to 'package-2025-01-preview'. Tag detail available at https://github.com/Azure/azure-rest-api-specs/blob/4c0f7731c93696af01bd2bb9927bf28d2afcbc98/specification/hdinsight/resource-manager/readme.md.\n+    - Support for setting Entra User during HDInsight cluster creation.",
        "comment_created_at": "2025-05-07T07:37:09+00:00",
        "comment_author": "aim-for-better",
        "comment_body": "Support to use Entra User as cluster administrator credential instead of using username/password during HDInsight cluster creation",
        "pr_file_module": null
      }
    ]
  }
]
