---
title: Approve AI dependencies conditionally
description: All AI-related dependencies (Microsoft.Extensions.AI.*, etc.) require
  explicit approval before inclusion and must be restricted to specific packages using
  conditional blocks in Packages.Data.props. Prefer version 8.x dependencies when
  available, and document any exceptions (such as using 9.x) with clear comments explaining
  the approval scope and reasoning.
repository: Azure/azure-sdk-for-net
label: AI
language: Other
comments_count: 2
repository_stars: 5809
---

All AI-related dependencies (Microsoft.Extensions.AI.*, etc.) require explicit approval before inclusion and must be restricted to specific packages using conditional blocks in Packages.Data.props. Prefer version 8.x dependencies when available, and document any exceptions (such as using 9.x) with clear comments explaining the approval scope and reasoning.

```xml
<!-- Example of properly documented and conditionally included AI dependency -->
<PackageReference Update="Microsoft.Extensions.AI" Version="9.5.0" /> <!-- 9.x approved for test project use, as there is no 8.x version available. -->

<!-- Example of conditional block to restrict an AI dependency to specific package -->
<ItemGroup Condition="'$(IsAIInferenceProject)' == 'true'">
  <PackageReference Update="Microsoft.Extensions.AI.Abstractions" Version="9.6.0"/>
</ItemGroup>
```


[
  {
    "discussion_id": "2169802413",
    "pr_number": 50898,
    "pr_file": "eng/Packages.Data.props",
    "created_at": "2025-06-26T19:21:52+00:00",
    "commented_code": "<PackageReference Update=\"System.ValueTuple\" Version=\"4.5.0\" />\n    <PackageReference Update=\"Microsoft.Bcl.AsyncInterfaces\" Version=\"8.0.0\" />\n    <PackageReference Update=\"Microsoft.CSharp\" Version=\"4.7.0\" />\n\t\t<PackageReference Update=\"Microsoft.Extensions.AI.Abstractions\" Version=\"9.6.0\"/>",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2169802413",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50898,
        "pr_file": "eng/Packages.Data.props",
        "discussion_id": "2169802413",
        "commented_code": "@@ -103,6 +103,7 @@\n     <PackageReference Update=\"System.ValueTuple\" Version=\"4.5.0\" />\n     <PackageReference Update=\"Microsoft.Bcl.AsyncInterfaces\" Version=\"8.0.0\" />\n     <PackageReference Update=\"Microsoft.CSharp\" Version=\"4.7.0\" />\n+\t\t<PackageReference Update=\"Microsoft.Extensions.AI.Abstractions\" Version=\"9.6.0\"/>",
        "comment_created_at": "2025-06-26T19:21:52+00:00",
        "comment_author": "jsquire",
        "comment_body": "@KrzysztofCwalina: Would you please confirm approval of this dependency and, if approved, whether that is specific to AI Agents or generally?",
        "pr_file_module": null
      },
      {
        "comment_id": "2170313212",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50898,
        "pr_file": "eng/Packages.Data.props",
        "discussion_id": "2169802413",
        "commented_code": "@@ -103,6 +103,7 @@\n     <PackageReference Update=\"System.ValueTuple\" Version=\"4.5.0\" />\n     <PackageReference Update=\"Microsoft.Bcl.AsyncInterfaces\" Version=\"8.0.0\" />\n     <PackageReference Update=\"Microsoft.CSharp\" Version=\"4.7.0\" />\n+\t\t<PackageReference Update=\"Microsoft.Extensions.AI.Abstractions\" Version=\"9.6.0\"/>",
        "comment_created_at": "2025-06-26T23:53:17+00:00",
        "comment_author": "KrzysztofCwalina",
        "comment_body": "yes. it's approved for this package. ",
        "pr_file_module": null
      },
      {
        "comment_id": "2170487188",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50898,
        "pr_file": "eng/Packages.Data.props",
        "discussion_id": "2169802413",
        "commented_code": "@@ -103,6 +103,7 @@\n     <PackageReference Update=\"System.ValueTuple\" Version=\"4.5.0\" />\n     <PackageReference Update=\"Microsoft.Bcl.AsyncInterfaces\" Version=\"8.0.0\" />\n     <PackageReference Update=\"Microsoft.CSharp\" Version=\"4.7.0\" />\n+\t\t<PackageReference Update=\"Microsoft.Extensions.AI.Abstractions\" Version=\"9.6.0\"/>",
        "comment_created_at": "2025-06-27T01:41:08+00:00",
        "comment_author": "jsquire",
        "comment_body": "@dmytrostruk:   Since the dependency approval is specific to this library, we'll need to create a conditional block for it so that it is not usable across the repository.   Please follow the pattern [here](https://github.com/Azure/azure-sdk-for-net/blob/main/eng/Packages.Data.props#L209) and create a block right above the one for `AI.Projects`",
        "pr_file_module": null
      },
      {
        "comment_id": "2172731404",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50898,
        "pr_file": "eng/Packages.Data.props",
        "discussion_id": "2169802413",
        "commented_code": "@@ -103,6 +103,7 @@\n     <PackageReference Update=\"System.ValueTuple\" Version=\"4.5.0\" />\n     <PackageReference Update=\"Microsoft.Bcl.AsyncInterfaces\" Version=\"8.0.0\" />\n     <PackageReference Update=\"Microsoft.CSharp\" Version=\"4.7.0\" />\n+\t\t<PackageReference Update=\"Microsoft.Extensions.AI.Abstractions\" Version=\"9.6.0\"/>",
        "comment_created_at": "2025-06-27T19:32:07+00:00",
        "comment_author": "dmytrostruk",
        "comment_body": "@jsquire Done.",
        "pr_file_module": null
      },
      {
        "comment_id": "2173045145",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50898,
        "pr_file": "eng/Packages.Data.props",
        "discussion_id": "2169802413",
        "commented_code": "@@ -103,6 +103,7 @@\n     <PackageReference Update=\"System.ValueTuple\" Version=\"4.5.0\" />\n     <PackageReference Update=\"Microsoft.Bcl.AsyncInterfaces\" Version=\"8.0.0\" />\n     <PackageReference Update=\"Microsoft.CSharp\" Version=\"4.7.0\" />\n+\t\t<PackageReference Update=\"Microsoft.Extensions.AI.Abstractions\" Version=\"9.6.0\"/>",
        "comment_created_at": "2025-06-28T00:37:20+00:00",
        "comment_author": "jsquire",
        "comment_body": "Thanks.  Looks good.   Once we're able to work through the account configuration, I'll remove my block.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2093720588",
    "pr_number": 50097,
    "pr_file": "eng/Packages.Data.props",
    "created_at": "2025-05-16T21:59:26+00:00",
    "commented_code": "<PackageReference Update=\"Microsoft.CodeAnalysis.CSharp.Workspaces\" Version=\"4.8.0\" />\n    <PackageReference Update=\"Microsoft.CSharp\" Version=\"4.7.0\" />\n    <PackageReference Update=\"Microsoft.Data.SqlClient\" Version=\"5.2.2\" />\n    <PackageReference Update=\"Microsoft.Extensions.AI\" Version=\"9.5.0\" /> <!-- Approved for Azure.AI.Inference.Tests -->",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2093720588",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50097,
        "pr_file": "eng/Packages.Data.props",
        "discussion_id": "2093720588",
        "commented_code": "@@ -374,7 +379,9 @@\n     <PackageReference Update=\"Microsoft.CodeAnalysis.CSharp.Workspaces\" Version=\"4.8.0\" />\n     <PackageReference Update=\"Microsoft.CSharp\" Version=\"4.7.0\" />\n     <PackageReference Update=\"Microsoft.Data.SqlClient\" Version=\"5.2.2\" />\n+    <PackageReference Update=\"Microsoft.Extensions.AI\" Version=\"9.5.0\" /> <!-- Approved for Azure.AI.Inference.Tests -->",
        "comment_created_at": "2025-05-16T21:59:26+00:00",
        "comment_author": "jsquire",
        "comment_body": "```suggestion\r\n    <PackageReference Update=\"Microsoft.Extensions.AI\" Version=\"9.5.0\" /> <!-- 9.x approved for test project use, as there is no 8.x version available.  -->\r\n```",
        "pr_file_module": null
      }
    ]
  }
]
