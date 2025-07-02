---
title: Documentation quality standards
description: 'Ensure documentation is specific, complete, and actionable for developers:


  1. **Provide meaningful content** - Avoid vague descriptions like "Test changes"
  in changelogs. Instead, be specific about what was modified or tested:'
repository: Azure/azure-sdk-for-net
label: Documentation
language: Markdown
comments_count: 9
repository_stars: 5809
---

Ensure documentation is specific, complete, and actionable for developers:

1. **Provide meaningful content** - Avoid vague descriptions like "Test changes" in changelogs. Instead, be specific about what was modified or tested:
   ```diff
   - Test changes
   + Conducted internal testing to validate the integration of new features and ensure stability.
   ```

2. **Include context and references** - When mentioning external documentation or specifications, include properly formatted links to those resources. This makes it easier for developers to find related information:
   ```markdown
   `ManagedIdentityCredential` now retries 410 status responses as required by 
   [Azure IMDS documentation](https://learn.microsoft.com/azure/active-directory/managed-identities-azure-resources/how-to-use-vm-token).
   ```

3. **Ensure code examples are valid** - All code examples in documentation should be derived from compiled, tested code snippets to ensure they work correctly and remain valid over time.

4. **Add explanatory comments** - Include comments that explain the purpose of code transformations or complex configurations to help future maintainers understand why certain decisions were made:
   ```
   # This transform removes the `x-nullable` annotation to ensure compatibility 
   # with the generated SDK code, which does not support nullable collections.
   ```

5. **Remove redundancy** - Keep documentation concise by eliminating redundant explanations while maintaining clarity.

For changelogs specifically:
- Only mark changes as "breaking" between stable releases, not for beta versions
- Include specific details rather than placeholder headings
- Remove empty sections when there are no relevant changes


[
  {
    "discussion_id": "2162687007",
    "pr_number": 50510,
    "pr_file": "sdk/keyvault/Azure.Security.KeyVault.Keys/CHANGELOG.md",
    "created_at": "2025-06-23T23:35:14+00:00",
    "commented_code": "### Breaking Changes\n\n> [!NOTE]",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2162687007",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50510,
        "pr_file": "sdk/keyvault/Azure.Security.KeyVault.Keys/CHANGELOG.md",
        "discussion_id": "2162687007",
        "commented_code": "@@ -12,12 +12,19 @@ Thank you to our developer community members who helped to make the Key Vault cl\n \n ### Breaking Changes\n \n+> [!NOTE]  ",
        "comment_created_at": "2025-06-23T23:35:14+00:00",
        "comment_author": "jsquire",
        "comment_body": "There are no breaking changes in a beta, because there is no stability guarantee.   Please don't list beta => beta or beta => stable changes as breaking.",
        "pr_file_module": null
      },
      {
        "comment_id": "2163412938",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50510,
        "pr_file": "sdk/keyvault/Azure.Security.KeyVault.Keys/CHANGELOG.md",
        "discussion_id": "2162687007",
        "commented_code": "@@ -12,12 +12,19 @@ Thank you to our developer community members who helped to make the Key Vault cl\n \n ### Breaking Changes\n \n+> [!NOTE]  ",
        "comment_created_at": "2025-06-24T09:15:12+00:00",
        "comment_author": "JonathanCrd",
        "comment_body": "What's the recommendation for features that were introduced in a beta? Should they be listed again in \"Features added\"? Since they were not present in the last stable.",
        "pr_file_module": null
      },
      {
        "comment_id": "2164880804",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50510,
        "pr_file": "sdk/keyvault/Azure.Security.KeyVault.Keys/CHANGELOG.md",
        "discussion_id": "2162687007",
        "commented_code": "@@ -12,12 +12,19 @@ Thank you to our developer community members who helped to make the Key Vault cl\n \n ### Breaking Changes\n \n+> [!NOTE]  ",
        "comment_created_at": "2025-06-24T20:53:14+00:00",
        "comment_author": "jsquire",
        "comment_body": "Yeah.   Stable release notes should concentrate on the delta between stable releases.   Its fine to say something like \"Includes all of the features from Beta.3\" if we want to be lazy or call them out specifically to make it easier to read for people.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2164197766",
    "pr_number": 50725,
    "pr_file": "sdk/identity/Azure.Identity/CHANGELOG.md",
    "created_at": "2025-06-24T14:35:19+00:00",
    "commented_code": "### Bugs Fixed\n\n- `ManagedIdentityCredential` now retries 410 status responses for at least 70 seconds total duration as required by Azure IMDS documentation. Previously, 410 responses were retried with the same short exponential backoff as other status codes, resulting in insufficient retry duration ([#50724](https://github.com/Azure/azure-sdk-for-net/issues/50724)).",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2164197766",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50725,
        "pr_file": "sdk/identity/Azure.Identity/CHANGELOG.md",
        "discussion_id": "2164197766",
        "commented_code": "@@ -8,6 +8,7 @@\n \n ### Bugs Fixed\n \n+- `ManagedIdentityCredential` now retries 410 status responses for at least 70 seconds total duration as required by Azure IMDS documentation. Previously, 410 responses were retried with the same short exponential backoff as other status codes, resulting in insufficient retry duration ([#50724](https://github.com/Azure/azure-sdk-for-net/issues/50724)).",
        "comment_created_at": "2025-06-24T14:35:19+00:00",
        "comment_author": "scottaddie",
        "comment_body": "Is that Azure IMDS doc on Learn? If so, I recommend linking to it here.",
        "pr_file_module": null
      },
      {
        "comment_id": "2164205754",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50725,
        "pr_file": "sdk/identity/Azure.Identity/CHANGELOG.md",
        "discussion_id": "2164197766",
        "commented_code": "@@ -8,6 +8,7 @@\n \n ### Bugs Fixed\n \n+- `ManagedIdentityCredential` now retries 410 status responses for at least 70 seconds total duration as required by Azure IMDS documentation. Previously, 410 responses were retried with the same short exponential backoff as other status codes, resulting in insufficient retry duration ([#50724](https://github.com/Azure/azure-sdk-for-net/issues/50724)).",
        "comment_created_at": "2025-06-24T14:37:49+00:00",
        "comment_author": "Copilot",
        "comment_body": "Added the link to the Azure IMDS documentation on Learn in the CHANGELOG entry. Commit a67b24f.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2104075370",
    "pr_number": 50238,
    "pr_file": "sdk/template/Azure.Template/CHANGELOG.md",
    "created_at": "2025-05-23T08:19:40+00:00",
    "commented_code": "# Release History\n\n## 1.0.3-beta.21 (2022-04-27)\n\n### Other Changes\n- Test changes",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2104075370",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50238,
        "pr_file": "sdk/template/Azure.Template/CHANGELOG.md",
        "discussion_id": "2104075370",
        "commented_code": "@@ -1,5 +1,10 @@\n # Release History\n \n+## 1.0.3-beta.21 (2022-04-27)\n+\n+### Other Changes\n+- Test changes",
        "comment_created_at": "2025-05-23T08:19:40+00:00",
        "comment_author": "Copilot",
        "comment_body": "[nitpick] The changelog entry 'Test changes' is too vague; please provide a more descriptive summary of the actual updates in this release.\n```suggestion\n- Conducted internal testing to validate the integration of new features and ensure stability.\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2020381792",
    "pr_number": 49145,
    "pr_file": "sdk/resourcemanager/Azure.ResourceManager/README.md",
    "created_at": "2025-03-31T03:49:47+00:00",
    "commented_code": "## Examples\n\nFor more detailed examples, take a look at [samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/resourcemanager/Azure.ResourceManager/samples) we have available.",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2020381792",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 49145,
        "pr_file": "sdk/resourcemanager/Azure.ResourceManager/README.md",
        "discussion_id": "2020381792",
        "commented_code": "@@ -271,6 +271,8 @@ else\n \n ## Examples\n \n+For more detailed examples, take a look at [samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/resourcemanager/Azure.ResourceManager/samples) we have available.",
        "comment_created_at": "2025-03-31T03:49:47+00:00",
        "comment_author": "live1206",
        "comment_body": "```suggestion\r\nWe are only listing samples for key features below. For more detailed examples, take a look at [samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/resourcemanager/Azure.ResourceManager/samples) we have available.\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2138882671",
    "pr_number": 50531,
    "pr_file": "README.md",
    "created_at": "2025-06-10T22:43:55+00:00",
    "commented_code": "Telemetry collection is on by default.\n\nTo opt out, you can disable telemetry at client construction. Creating a [synchronous policy](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/core/Azure.Core/samples/Pipeline.md#implementing-a-synchronous-policy) in your application gives you access to the headers sent with each request, allowing you to remove the `User-Agent` header containing client telemetry.  To use the policy, you will add it to the options for your specific client as part of client creation.  This will disable Azure SDK telemetry for all methods in the client. You will need to register the policy with each client created.\nTo opt out, you can disable telemetry by setting the `IsTelemetryEnabled` property to `false` in the client's `DiagnosticsOptions`. This will prevent the Azure SDK from adding telemetry information to the `User-Agent` header for all requests made by the client.",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2138882671",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50531,
        "pr_file": "README.md",
        "discussion_id": "2138882671",
        "commented_code": "@@ -60,32 +60,25 @@ The software may collect information about you and your use of the software and\n \n Telemetry collection is on by default.\n \n-To opt out, you can disable telemetry at client construction. Creating a [synchronous policy](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/core/Azure.Core/samples/Pipeline.md#implementing-a-synchronous-policy) in your application gives you access to the headers sent with each request, allowing you to remove the `User-Agent` header containing client telemetry.  To use the policy, you will add it to the options for your specific client as part of client creation.  This will disable Azure SDK telemetry for all methods in the client. You will need to register the policy with each client created.\n+To opt out, you can disable telemetry by setting the `IsTelemetryEnabled` property to `false` in the client's `DiagnosticsOptions`. This will prevent the Azure SDK from adding telemetry information to the `User-Agent` header for all requests made by the client.",
        "comment_created_at": "2025-06-10T22:43:55+00:00",
        "comment_author": "heaths",
        "comment_body": "This sentence is just a longer, more complex version of the concise sentence on line 67 with a nice sample immediately following it. I would consider removing this longer sentence.",
        "pr_file_module": null
      },
      {
        "comment_id": "2138886220",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50531,
        "pr_file": "README.md",
        "discussion_id": "2138882671",
        "commented_code": "@@ -60,32 +60,25 @@ The software may collect information about you and your use of the software and\n \n Telemetry collection is on by default.\n \n-To opt out, you can disable telemetry at client construction. Creating a [synchronous policy](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/core/Azure.Core/samples/Pipeline.md#implementing-a-synchronous-policy) in your application gives you access to the headers sent with each request, allowing you to remove the `User-Agent` header containing client telemetry.  To use the policy, you will add it to the options for your specific client as part of client creation.  This will disable Azure SDK telemetry for all methods in the client. You will need to register the policy with each client created.\n+To opt out, you can disable telemetry by setting the `IsTelemetryEnabled` property to `false` in the client's `DiagnosticsOptions`. This will prevent the Azure SDK from adding telemetry information to the `User-Agent` header for all requests made by the client.",
        "comment_created_at": "2025-06-10T22:48:12+00:00",
        "comment_author": "Copilot",
        "comment_body": "You're absolutely right. I've removed the redundant longer sentence to improve clarity and flow. The documentation now goes directly from the basic statement to the concise explanation with code example. Commit: 4522a76",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2087144670",
    "pr_number": 50011,
    "pr_file": "README.md",
    "created_at": "2025-05-13T15:46:03+00:00",
    "commented_code": "* File an issue via [Github Issues](https://github.com/Azure/azure-sdk-for-net/issues/new/choose).\n* Check [previous questions](https://stackoverflow.com/questions/tagged/azure+.net) or ask new ones on StackOverflow using `azure` and `.net` tags.\n\n\n## Data Collection\nThe software may collect information about you and your use of the software and send it to Microsoft. Microsoft may use this information to provide services and improve our products and services. You may turn off the telemetry as described below. You can learn more about data collection and use in the help documentation and Microsoft\u2019s [privacy statement](https://go.microsoft.com/fwlink/?LinkID=824704). For more information on the data collected by the Azure SDK, please visit the [Telemetry Guidelines](https://azure.github.io/azure-sdk/general_azurecore.html#telemetry-policy) page.\n\n### Telemetry Configuration\nTelemetry collection is on by default.\n\nTo opt out, you can disable telemetry at client construction. Create a `ClientOptions` for your specific client, every service client has an option class. Set `ApplicationId` as empty under `Diagnostics` inside service client option. Then pass service client option as argument during client creation. This will disable telemetry for all methods in the client. Do this for every new client.\n\nThe example below uses the `Azure.Storage.Blobs` package. In your code, you can replace `Azure.Storage.Blobs` with the package you are using and use the corresponding `<Service>ClientOptions` instead of `BlobClientOptions`.\n\n```csharp",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2087144670",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50011,
        "pr_file": "README.md",
        "discussion_id": "2087144670",
        "commented_code": "@@ -52,6 +52,54 @@ Documentation and code samples for these libraries can be found [here](https://a\n * File an issue via [Github Issues](https://github.com/Azure/azure-sdk-for-net/issues/new/choose).\n * Check [previous questions](https://stackoverflow.com/questions/tagged/azure+.net) or ask new ones on StackOverflow using `azure` and `.net` tags.\n \n+\n+## Data Collection\n+The software may collect information about you and your use of the software and send it to Microsoft. Microsoft may use this information to provide services and improve our products and services. You may turn off the telemetry as described below. You can learn more about data collection and use in the help documentation and Microsoft\u2019s [privacy statement](https://go.microsoft.com/fwlink/?LinkID=824704). For more information on the data collected by the Azure SDK, please visit the [Telemetry Guidelines](https://azure.github.io/azure-sdk/general_azurecore.html#telemetry-policy) page.\n+\n+### Telemetry Configuration\n+Telemetry collection is on by default.\n+\n+To opt out, you can disable telemetry at client construction. Create a `ClientOptions` for your specific client, every service client has an option class. Set `ApplicationId` as empty under `Diagnostics` inside service client option. Then pass service client option as argument during client creation. This will disable telemetry for all methods in the client. Do this for every new client.\n+\n+The example below uses the `Azure.Storage.Blobs` package. In your code, you can replace `Azure.Storage.Blobs` with the package you are using and use the corresponding `<Service>ClientOptions` instead of `BlobClientOptions`.\n+\n+```csharp",
        "comment_created_at": "2025-05-13T15:46:03+00:00",
        "comment_author": "jsquire",
        "comment_body": "Any code sample needs to be driving off of a code snippet to ensure that it is compiled and remains valid.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2108055491",
    "pr_number": 50267,
    "pr_file": "sdk/mongodbatlas/Azure.ResourceManager.MongoDBAtlas/CHANGELOG.md",
    "created_at": "2025-05-27T02:55:00+00:00",
    "commented_code": "# Release History\n\n## 1.0.0-beta.1 (Unreleased)\n\n### Features Added\n\n### Breaking Changes\n\n### Bugs Fixed\n\n### Other Changes",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2108055491",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50267,
        "pr_file": "sdk/mongodbatlas/Azure.ResourceManager.MongoDBAtlas/CHANGELOG.md",
        "discussion_id": "2108055491",
        "commented_code": "@@ -0,0 +1,11 @@\n+# Release History\n+\n+## 1.0.0-beta.1 (Unreleased)\n+\n+### Features Added\n+\n+### Breaking Changes\n+\n+### Bugs Fixed\n+\n+### Other Changes",
        "comment_created_at": "2025-05-27T02:55:00+00:00",
        "comment_author": "ArcturusZhang",
        "comment_body": "please update the changelog according to your change, and update the release date to your desire release date.\r\nAlso please remove the empty subsections.\r\nSince this is your first release, you could write some initial release stuff in Features Added subsection and remove others.",
        "pr_file_module": null
      },
      {
        "comment_id": "2108258769",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50267,
        "pr_file": "sdk/mongodbatlas/Azure.ResourceManager.MongoDBAtlas/CHANGELOG.md",
        "discussion_id": "2108055491",
        "commented_code": "@@ -0,0 +1,11 @@\n+# Release History\n+\n+## 1.0.0-beta.1 (Unreleased)\n+\n+### Features Added\n+\n+### Breaking Changes\n+\n+### Bugs Fixed\n+\n+### Other Changes",
        "comment_created_at": "2025-05-27T06:08:25+00:00",
        "comment_author": "ajaykumarmehra",
        "comment_body": "updated",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2097256698",
    "pr_number": 50157,
    "pr_file": "sdk/loadtestservice/Azure.Developer.Playwright.MSTest/tests/samples/README.md",
    "created_at": "2025-05-20T07:58:53+00:00",
    "commented_code": "Source files in this directory are written as tests from which samples are extracted.\nThey are not intended to be viewed directly and help ensure our samples compile and work correctly.\nSee our <!--[list of samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/loadtestservice/Azure.Developer.Playwright.MSTest/samples)--> for more explanation about how to use this client library.",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2097256698",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50157,
        "pr_file": "sdk/loadtestservice/Azure.Developer.Playwright.MSTest/tests/samples/README.md",
        "discussion_id": "2097256698",
        "commented_code": "@@ -0,0 +1,3 @@\n+Source files in this directory are written as tests from which samples are extracted.\n+They are not intended to be viewed directly and help ensure our samples compile and work correctly.\n+See our <!--[list of samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/loadtestservice/Azure.Developer.Playwright.MSTest/samples)--> for more explanation about how to use this client library.",
        "comment_created_at": "2025-05-20T07:58:53+00:00",
        "comment_author": "Copilot",
        "comment_body": "The 'list of samples' link is wrapped in an HTML comment and won\u2019t render; convert it to a proper Markdown link so users can click through.\n```suggestion\nSee our [list of samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/loadtestservice/Azure.Developer.Playwright.MSTest/samples) for more explanation about how to use this client library.\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "2097273568",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50157,
        "pr_file": "sdk/loadtestservice/Azure.Developer.Playwright.MSTest/tests/samples/README.md",
        "discussion_id": "2097256698",
        "commented_code": "@@ -0,0 +1,3 @@\n+Source files in this directory are written as tests from which samples are extracted.\n+They are not intended to be viewed directly and help ensure our samples compile and work correctly.\n+See our <!--[list of samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/loadtestservice/Azure.Developer.Playwright.MSTest/samples)--> for more explanation about how to use this client library.",
        "comment_created_at": "2025-05-20T08:06:50+00:00",
        "comment_author": "Sid200026",
        "comment_body": "Kept temporarily to bypass link checks",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2105455433",
    "pr_number": 50255,
    "pr_file": "sdk/search/Azure.Search.Documents/src/autorest.md",
    "created_at": "2025-05-23T21:38:17+00:00",
    "commented_code": "$[\"discriminator\"] = \"@odata.type\";\n```\n\n### Remove nullable annotations",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2105455433",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50255,
        "pr_file": "sdk/search/Azure.Search.Documents/src/autorest.md",
        "discussion_id": "2105455433",
        "commented_code": "@@ -59,6 +59,16 @@ directive:\n     $[\"discriminator\"] = \"@odata.type\";\n ```\n \n+### Remove nullable annotations\n+",
        "comment_created_at": "2025-05-23T21:38:17+00:00",
        "comment_author": "Copilot",
        "comment_body": "[nitpick] This new transform lacks an explanation of why nullable annotations are removed. Adding a brief note or a link to the related issue will help future maintainers understand its purpose.\n```suggestion\n\n# This transform removes the `x-nullable` annotation from the specified property in the Swagger document.\n# Nullable annotations are removed to ensure compatibility with the generated SDK code, which does not\n# support nullable collections. For more details, see issue #12345 (replace with actual issue link if available).\n```",
        "pr_file_module": null
      }
    ]
  }
]
