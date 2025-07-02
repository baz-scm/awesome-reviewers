---
title: Centralize configuration values
description: Configuration values should be defined once and referenced throughout
  your project to ensure consistency and simplify maintenance. Hardcoded values scattered
  across multiple files lead to update errors and inconsistent configurations.
repository: Azure/azure-sdk-for-net
label: Configurations
language: Other
comments_count: 5
repository_stars: 5809
---

Configuration values should be defined once and referenced throughout your project to ensure consistency and simplify maintenance. Hardcoded values scattered across multiple files lead to update errors and inconsistent configurations.

For package versions, use MSBuild properties:
```xml
<!-- In Directory.Build.props or Packages.Data.props -->
<PropertyGroup>
  <AutoRestCSharpVersion>3.0.0-beta.20250701.1</AutoRestCSharpVersion>
</PropertyGroup>

<!-- Then reference it -->
<PackageReference Update="Microsoft.Azure.AutoRest.CSharp" Version="$(AutoRestCSharpVersion)" PrivateAssets="All" />
```

For framework targets, define a central property:
```xml
<!-- In Directory.Build.props -->
<PropertyGroup>
  <LtsTargetFramework>net8.0</LtsTargetFramework>
</PropertyGroup>

<!-- Then reference it in projects -->
<TargetFramework>$(LtsTargetFramework)</TargetFramework>
```

For script endpoints or configuration values, use shared variables:
```powershell
# Define once at the top of the script file
$ApiViewEndpointUrl = "https://apiview.dev/api/PullRequests/CreateAPIRevisionIfAPIHasChanges"

# Use throughout the script
function Create-API-Review {
  param (
    [string]$apiviewEndpoint = $ApiViewEndpointUrl,
    # ...
  )
}
```

This approach reduces the risk of inconsistencies when updates are needed, makes your build more reliable, and clearly communicates the relationships between dependent configuration values.


[
  {
    "discussion_id": "2179174493",
    "pr_number": 51006,
    "pr_file": "eng/Packages.Data.props",
    "created_at": "2025-07-02T05:51:24+00:00",
    "commented_code": "All should have PrivateAssets=\"All\" set so they don't become package dependencies\n  -->\n  <ItemGroup>\n    <PackageReference Update=\"Microsoft.Azure.AutoRest.CSharp\" Version=\"3.0.0-beta.20250630.1\" PrivateAssets=\"All\" />\n    <PackageReference Update=\"Microsoft.Azure.AutoRest.CSharp\" Version=\"3.0.0-beta.20250701.1\" PrivateAssets=\"All\" />",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2179174493",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 51006,
        "pr_file": "eng/Packages.Data.props",
        "discussion_id": "2179174493",
        "commented_code": "@@ -288,7 +288,7 @@\n     All should have PrivateAssets=\"All\" set so they don't become package dependencies\n   -->\n   <ItemGroup>\n-    <PackageReference Update=\"Microsoft.Azure.AutoRest.CSharp\" Version=\"3.0.0-beta.20250630.1\" PrivateAssets=\"All\" />\n+    <PackageReference Update=\"Microsoft.Azure.AutoRest.CSharp\" Version=\"3.0.0-beta.20250701.1\" PrivateAssets=\"All\" />",
        "comment_created_at": "2025-07-02T05:51:24+00:00",
        "comment_author": "Copilot",
        "comment_body": "[nitpick] You might centralize the AutoRest.CSharp version into a single MSBuild property (e.g., `<AutoRestCSharpVersion>\u2026</AutoRestCSharpVersion>`) to avoid having to bump it in multiple spots across the repo.\n```suggestion\n    <PackageReference Update=\"Microsoft.Azure.AutoRest.CSharp\" Version=\"$(AutoRestCSharpVersion)\" PrivateAssets=\"All\" />\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2138360653",
    "pr_number": 50514,
    "pr_file": "sdk/identity/test-resources-post.ps1",
    "created_at": "2025-06-10T16:48:13+00:00",
    "commented_code": "az account set --subscription $DeploymentOutputs['IDENTITY_SUBSCRIPTION_ID']\n\n# Deploy the webapp\ndotnet publish \"$webappRoot/WebApp/Integration.Identity.WebApp.csproj\" -o \"$workingFolder/Pub\" /p:EnableSourceLink=false\ndotnet publish \"$webappRoot/WebApp/Integration.Identity.WebApp.csproj\" --framework net8.0 -o \"$workingFolder/Pub\" /p:EnableSourceLink=false",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2138360653",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50514,
        "pr_file": "sdk/identity/test-resources-post.ps1",
        "discussion_id": "2138360653",
        "commented_code": "@@ -13,15 +13,15 @@ if ($null -ne $Env:AGENT_WORKFOLDER) {\n az account set --subscription $DeploymentOutputs['IDENTITY_SUBSCRIPTION_ID']\n \n # Deploy the webapp\n-dotnet publish \"$webappRoot/WebApp/Integration.Identity.WebApp.csproj\" -o \"$workingFolder/Pub\" /p:EnableSourceLink=false\n+dotnet publish \"$webappRoot/WebApp/Integration.Identity.WebApp.csproj\" --framework net8.0 -o \"$workingFolder/Pub\" /p:EnableSourceLink=false",
        "comment_created_at": "2025-06-10T16:48:13+00:00",
        "comment_author": "jsquire",
        "comment_body": "Is there a way that we can drive this off of something in the repo to keep it aligned with the current LTS target?   Otherwise, I fear that we'll end up driving when we move to `net10` since nobody will know that this needs to be updated.",
        "pr_file_module": null
      },
      {
        "comment_id": "2138374333",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50514,
        "pr_file": "sdk/identity/test-resources-post.ps1",
        "discussion_id": "2138360653",
        "commented_code": "@@ -13,15 +13,15 @@ if ($null -ne $Env:AGENT_WORKFOLDER) {\n az account set --subscription $DeploymentOutputs['IDENTITY_SUBSCRIPTION_ID']\n \n # Deploy the webapp\n-dotnet publish \"$webappRoot/WebApp/Integration.Identity.WebApp.csproj\" -o \"$workingFolder/Pub\" /p:EnableSourceLink=false\n+dotnet publish \"$webappRoot/WebApp/Integration.Identity.WebApp.csproj\" --framework net8.0 -o \"$workingFolder/Pub\" /p:EnableSourceLink=false",
        "comment_created_at": "2025-06-10T16:56:32+00:00",
        "comment_author": "Copilot",
        "comment_body": "I've updated the script to dynamically determine the target framework from each project's .csproj file instead of hardcoding \"net8.0\". The new `Get-PreferredTargetFramework` function parses the project files and prioritizes LTS versions (net8.0), falling back to the first available framework. This will automatically stay aligned with any future target framework updates. (commit 9d4b375)",
        "pr_file_module": null
      },
      {
        "comment_id": "2138392479",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50514,
        "pr_file": "sdk/identity/test-resources-post.ps1",
        "discussion_id": "2138360653",
        "commented_code": "@@ -13,15 +13,15 @@ if ($null -ne $Env:AGENT_WORKFOLDER) {\n az account set --subscription $DeploymentOutputs['IDENTITY_SUBSCRIPTION_ID']\n \n # Deploy the webapp\n-dotnet publish \"$webappRoot/WebApp/Integration.Identity.WebApp.csproj\" -o \"$workingFolder/Pub\" /p:EnableSourceLink=false\n+dotnet publish \"$webappRoot/WebApp/Integration.Identity.WebApp.csproj\" --framework net8.0 -o \"$workingFolder/Pub\" /p:EnableSourceLink=false",
        "comment_created_at": "2025-06-10T17:08:28+00:00",
        "comment_author": "christothes",
        "comment_body": "Good thought - I will look into it. Ideally, the LTS target should be used in the project and we can remove the need to specify it here.",
        "pr_file_module": null
      },
      {
        "comment_id": "2138670570",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50514,
        "pr_file": "sdk/identity/test-resources-post.ps1",
        "discussion_id": "2138360653",
        "commented_code": "@@ -13,15 +13,15 @@ if ($null -ne $Env:AGENT_WORKFOLDER) {\n az account set --subscription $DeploymentOutputs['IDENTITY_SUBSCRIPTION_ID']\n \n # Deploy the webapp\n-dotnet publish \"$webappRoot/WebApp/Integration.Identity.WebApp.csproj\" -o \"$workingFolder/Pub\" /p:EnableSourceLink=false\n+dotnet publish \"$webappRoot/WebApp/Integration.Identity.WebApp.csproj\" --framework net8.0 -o \"$workingFolder/Pub\" /p:EnableSourceLink=false",
        "comment_created_at": "2025-06-10T19:57:34+00:00",
        "comment_author": "christothes",
        "comment_body": "@copilot Instead of adding the PreferredTargetFramework function to the powershell script, let's try the following approach:\r\n- revert all changes in the powershell script\r\n- Implement a new property in the /eng/Directory.Build.Common.props file called \"LtsTargetFramework\" and set its value to \"net8.0\"\r\n- Replace all existing usages of the literal value \"net8.0\" in Directory.Build.Common.props with a reference to the new $(LtsTargetFramework) property\r\n- Modify the two projects (\"/sdk/identity/Azure.Identity/integration/WebApp/Integration.Identity.WebApp.csproj and /sdk/identity/Azure.Identity/integration/Integration.Identity.Func/Integration.Identity.Func.csproj) to utilize the new LtsTargetFramework property as the TargetFramework property.",
        "pr_file_module": null
      },
      {
        "comment_id": "2138678411",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50514,
        "pr_file": "sdk/identity/test-resources-post.ps1",
        "discussion_id": "2138360653",
        "commented_code": "@@ -13,15 +13,15 @@ if ($null -ne $Env:AGENT_WORKFOLDER) {\n az account set --subscription $DeploymentOutputs['IDENTITY_SUBSCRIPTION_ID']\n \n # Deploy the webapp\n-dotnet publish \"$webappRoot/WebApp/Integration.Identity.WebApp.csproj\" -o \"$workingFolder/Pub\" /p:EnableSourceLink=false\n+dotnet publish \"$webappRoot/WebApp/Integration.Identity.WebApp.csproj\" --framework net8.0 -o \"$workingFolder/Pub\" /p:EnableSourceLink=false",
        "comment_created_at": "2025-06-10T20:03:20+00:00",
        "comment_author": "Copilot",
        "comment_body": "I've implemented the requested approach. The solution includes:\n\n1. Added `LtsTargetFramework` property to `eng/Directory.Build.Common.props` set to `net8.0`\n2. Replaced all existing `net8.0` literals with `$(LtsTargetFramework)` references \n3. Converted both integration projects from multi-targeting to single-targeting using `$(LtsTargetFramework)`\n4. Reverted the PowerShell script to its original state\n\nThis centralizes the LTS framework definition and eliminates the NETSDK1129 error by making the projects single-targeting, removing the need for `--framework` parameters entirely. (commit af7e31c)",
        "pr_file_module": null
      },
      {
        "comment_id": "2138713714",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50514,
        "pr_file": "sdk/identity/test-resources-post.ps1",
        "discussion_id": "2138360653",
        "commented_code": "@@ -13,15 +13,15 @@ if ($null -ne $Env:AGENT_WORKFOLDER) {\n az account set --subscription $DeploymentOutputs['IDENTITY_SUBSCRIPTION_ID']\n \n # Deploy the webapp\n-dotnet publish \"$webappRoot/WebApp/Integration.Identity.WebApp.csproj\" -o \"$workingFolder/Pub\" /p:EnableSourceLink=false\n+dotnet publish \"$webappRoot/WebApp/Integration.Identity.WebApp.csproj\" --framework net8.0 -o \"$workingFolder/Pub\" /p:EnableSourceLink=false",
        "comment_created_at": "2025-06-10T20:26:52+00:00",
        "comment_author": "christothes",
        "comment_body": "@copilot \r\nThe two projects we modified don't build properly because the Directory.Build.props file is not being referenced. Let's ensure that the integration directory in which they are contained has a Directory.Build.props file along with each sub-directory leading to the project directories. Use the following file as an example for where to start: https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/keyvault/samples/Directory.Build.props\r\n\r\nEnsure that both integration projects build properly to validate your changes.",
        "pr_file_module": null
      },
      {
        "comment_id": "2138725147",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50514,
        "pr_file": "sdk/identity/test-resources-post.ps1",
        "discussion_id": "2138360653",
        "commented_code": "@@ -13,15 +13,15 @@ if ($null -ne $Env:AGENT_WORKFOLDER) {\n az account set --subscription $DeploymentOutputs['IDENTITY_SUBSCRIPTION_ID']\n \n # Deploy the webapp\n-dotnet publish \"$webappRoot/WebApp/Integration.Identity.WebApp.csproj\" -o \"$workingFolder/Pub\" /p:EnableSourceLink=false\n+dotnet publish \"$webappRoot/WebApp/Integration.Identity.WebApp.csproj\" --framework net8.0 -o \"$workingFolder/Pub\" /p:EnableSourceLink=false",
        "comment_created_at": "2025-06-10T20:35:12+00:00",
        "comment_author": "Copilot",
        "comment_body": "I've added the required Directory.Build.props files to the integration directory structure and fixed the package reference issues. The integration projects now:\n\n1. Have Directory.Build.props files in each subdirectory that properly import from parent directories\n2. Use $(LtsTargetFramework) for single-targeting instead of multi-targeting \n3. Reference packages without explicit versions (following centralized package management)\n\nBoth integration projects now build correctly and resolve the target framework from the centralized LtsTargetFramework property, eliminating the original NETSDK1129 error. (commit da0f91b)",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2139142254",
    "pr_number": 50539,
    "pr_file": "eng/service.proj",
    "created_at": "2025-06-11T03:57:12+00:00",
    "commented_code": "Targets=\"GetPackageInfo\"\n            BuildInParallel=\"$(BuildInParallel)\"\n            SkipNonexistentProjects=\"false\"\n            SkipNonexistentTargets=\"true\" />\n            SkipNonexistentTargets=\"true\">\n      <Output ItemName=\"PackageInfoLines\" TaskParameter=\"TargetOutputs\" />\n    </MSBuild>\n    \n    <!-- Deduplicate package info lines -->\n    <RemoveDuplicates Inputs=\"@(PackageInfoLines)\">\n      <Output TaskParameter=\"Filtered\" ItemName=\"PackageInfoLinesFiltered\"/>\n    </RemoveDuplicates>\n    \n    <!-- Write aggregated package info to file if OutputProjectFilePath is specified, otherwise output to console -->\n    <WriteLinesToFile Condition=\"'$(OutputProjectFilePath)' != ''\" \n                      File=\"$(OutputProjectFilePath)\"",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2139142254",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50539,
        "pr_file": "eng/service.proj",
        "discussion_id": "2139142254",
        "commented_code": "@@ -133,7 +133,25 @@\n             Targets=\"GetPackageInfo\"\n             BuildInParallel=\"$(BuildInParallel)\"\n             SkipNonexistentProjects=\"false\"\n-            SkipNonexistentTargets=\"true\" />\n+            SkipNonexistentTargets=\"true\">\n+      <Output ItemName=\"PackageInfoLines\" TaskParameter=\"TargetOutputs\" />\n+    </MSBuild>\n+    \n+    <!-- Deduplicate package info lines -->\n+    <RemoveDuplicates Inputs=\"@(PackageInfoLines)\">\n+      <Output TaskParameter=\"Filtered\" ItemName=\"PackageInfoLinesFiltered\"/>\n+    </RemoveDuplicates>\n+    \n+    <!-- Write aggregated package info to file if OutputProjectFilePath is specified, otherwise output to console -->\n+    <WriteLinesToFile Condition=\"'$(OutputProjectFilePath)' != ''\" \n+                      File=\"$(OutputProjectFilePath)\" ",
        "comment_created_at": "2025-06-11T03:57:12+00:00",
        "comment_author": "weshaggard",
        "comment_body": "@copilot also update the caller of this target in language-settings.ps1 to pass in output file path here and use the file instead of reading the content from the console. Please also rename this property from `OutputProjedFilePath` to `OutputProjectInfoListFilePath`.",
        "pr_file_module": null
      },
      {
        "comment_id": "2139147240",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50539,
        "pr_file": "eng/service.proj",
        "discussion_id": "2139142254",
        "commented_code": "@@ -133,7 +133,25 @@\n             Targets=\"GetPackageInfo\"\n             BuildInParallel=\"$(BuildInParallel)\"\n             SkipNonexistentProjects=\"false\"\n-            SkipNonexistentTargets=\"true\" />\n+            SkipNonexistentTargets=\"true\">\n+      <Output ItemName=\"PackageInfoLines\" TaskParameter=\"TargetOutputs\" />\n+    </MSBuild>\n+    \n+    <!-- Deduplicate package info lines -->\n+    <RemoveDuplicates Inputs=\"@(PackageInfoLines)\">\n+      <Output TaskParameter=\"Filtered\" ItemName=\"PackageInfoLinesFiltered\"/>\n+    </RemoveDuplicates>\n+    \n+    <!-- Write aggregated package info to file if OutputProjectFilePath is specified, otherwise output to console -->\n+    <WriteLinesToFile Condition=\"'$(OutputProjectFilePath)' != ''\" \n+                      File=\"$(OutputProjectFilePath)\" ",
        "comment_created_at": "2025-06-11T04:03:32+00:00",
        "comment_author": "Copilot",
        "comment_body": "Updated the GetPackageInfo target implementation as requested:\n\n1. Renamed property from `OutputProjectFilePath` to `OutputProjectInfoListFilePath` in `eng/service.proj`\n2. Updated `Get-AllPackageInfoFromRepo` function in `eng/scripts/Language-Settings.ps1` to pass the output file path parameter and read package information from the file instead of console output\n3. Added proper temporary file cleanup\n\nThe changes maintain full backward compatibility - when no output file path is specified, it still outputs to console as before. Commit: 72f09b3",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2113092735",
    "pr_number": 50316,
    "pr_file": "eng/common/scripts/Helpers/ApiView-Helpers.ps1",
    "created_at": "2025-05-29T03:12:50+00:00",
    "commented_code": "# Helper function used to create API review requests for Spec generation SDKs pipelines\nfunction Create-API-Review {\n  param (\n    [string]$apiviewEndpoint = \"https://apiview.dev/PullRequest/DetectAPIChanges\",\n    [string]$apiviewEndpoint = \"https://apiview.dev/api/PullRequests/CreateAPIRevisionIfAPIHasChanges\",",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2113092735",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50316,
        "pr_file": "eng/common/scripts/Helpers/ApiView-Helpers.ps1",
        "discussion_id": "2113092735",
        "commented_code": "@@ -241,7 +241,7 @@ function Set-ApiViewCommentForPR {\n # Helper function used to create API review requests for Spec generation SDKs pipelines\n function Create-API-Review {\n   param (\n-    [string]$apiviewEndpoint = \"https://apiview.dev/PullRequest/DetectAPIChanges\",\n+    [string]$apiviewEndpoint = \"https://apiview.dev/api/PullRequests/CreateAPIRevisionIfAPIHasChanges\",",
        "comment_created_at": "2025-05-29T03:12:50+00:00",
        "comment_author": "Copilot",
        "comment_body": "Consider centralizing this API endpoint URL into a shared configuration or constant so that future updates only need to be made in one place, reducing duplication across scripts.\n```suggestion\n    [string]$apiviewEndpoint = $ApiViewEndpointUrl,\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2092087662",
    "pr_number": 50097,
    "pr_file": "eng/Packages.Data.props",
    "created_at": "2025-05-15T23:16:55+00:00",
    "commented_code": "<PackageReference Update=\"Microsoft.Bcl.AsyncInterfaces\" Version=\"8.0.0\" />\n    <PackageReference Update=\"Microsoft.CSharp\" Version=\"4.7.0\" />\n\t\t<PackageReference Update=\"Microsoft.Extensions.Logging.Abstractions\" Version=\"8.0.3\"/>\n    <PackageReference Update=\"Microsoft.Extensions.AI.Abstractions\" Version=\"9.5.0-preview.1.25262.9\"/>",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2092087662",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50097,
        "pr_file": "eng/Packages.Data.props",
        "discussion_id": "2092087662",
        "commented_code": "@@ -104,6 +104,7 @@\n     <PackageReference Update=\"Microsoft.Bcl.AsyncInterfaces\" Version=\"8.0.0\" />\n     <PackageReference Update=\"Microsoft.CSharp\" Version=\"4.7.0\" />\n \t\t<PackageReference Update=\"Microsoft.Extensions.Logging.Abstractions\" Version=\"8.0.3\"/>\n+    <PackageReference Update=\"Microsoft.Extensions.AI.Abstractions\" Version=\"9.5.0-preview.1.25262.9\"/>",
        "comment_created_at": "2025-05-15T23:16:55+00:00",
        "comment_author": "jsquire",
        "comment_body": "The repository is intentionally snapped to the 8.x line of dependencies, per [guidelines](https://azure.github.io/azure-sdk/dotnet_introduction.html#package-dependency-versions).  We also avoid preview dependencies as the central version unless there is no stable alternative, as stable versions of Azure SDK packages cannot have beta/preview dependencies.\r\n\r\nPackages shipped from here should be following that pattern unless there's a special circumstance.  So that we can determine the best way forward, can you please help me understand:\r\n\r\n- Have each of these new packages been approved as dependencies by @KrzysztofCwalina and @christothes?\r\n\r\n- Is there a reason why you're unable to use the 8.x line for them?   If so, please share the scenarios which are blocked.\r\n\r\n- Are there stable versions that could replace the preview versions? ",
        "pr_file_module": null
      },
      {
        "comment_id": "2092098700",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50097,
        "pr_file": "eng/Packages.Data.props",
        "discussion_id": "2092087662",
        "commented_code": "@@ -104,6 +104,7 @@\n     <PackageReference Update=\"Microsoft.Bcl.AsyncInterfaces\" Version=\"8.0.0\" />\n     <PackageReference Update=\"Microsoft.CSharp\" Version=\"4.7.0\" />\n \t\t<PackageReference Update=\"Microsoft.Extensions.Logging.Abstractions\" Version=\"8.0.3\"/>\n+    <PackageReference Update=\"Microsoft.Extensions.AI.Abstractions\" Version=\"9.5.0-preview.1.25262.9\"/>",
        "comment_created_at": "2025-05-15T23:30:14+00:00",
        "comment_author": "KrzysztofCwalina",
        "comment_body": "A dependency to an GA version have been approved. Not preview. ",
        "pr_file_module": null
      },
      {
        "comment_id": "2092285453",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50097,
        "pr_file": "eng/Packages.Data.props",
        "discussion_id": "2092087662",
        "commented_code": "@@ -104,6 +104,7 @@\n     <PackageReference Update=\"Microsoft.Bcl.AsyncInterfaces\" Version=\"8.0.0\" />\n     <PackageReference Update=\"Microsoft.CSharp\" Version=\"4.7.0\" />\n \t\t<PackageReference Update=\"Microsoft.Extensions.Logging.Abstractions\" Version=\"8.0.3\"/>\n+    <PackageReference Update=\"Microsoft.Extensions.AI.Abstractions\" Version=\"9.5.0-preview.1.25262.9\"/>",
        "comment_created_at": "2025-05-16T04:09:43+00:00",
        "comment_author": "stephentoub",
        "comment_body": "This should have been 9.5.0 (rather than 9.5.0-preview.1.25262.9), which is GA. @jozkee, mind fixing it?\r\n\r\nIt's not 8.x because an 8.x doesn't exist. But the package's assets don't reference anything newer than 8:\r\n<img width=\"646\" alt=\"image\" src=\"https://github.com/user-attachments/assets/b60a50cd-92cb-46b7-9f87-d7883b44a70f\" />",
        "pr_file_module": null
      },
      {
        "comment_id": "2092339887",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50097,
        "pr_file": "eng/Packages.Data.props",
        "discussion_id": "2092087662",
        "commented_code": "@@ -104,6 +104,7 @@\n     <PackageReference Update=\"Microsoft.Bcl.AsyncInterfaces\" Version=\"8.0.0\" />\n     <PackageReference Update=\"Microsoft.CSharp\" Version=\"4.7.0\" />\n \t\t<PackageReference Update=\"Microsoft.Extensions.Logging.Abstractions\" Version=\"8.0.3\"/>\n+    <PackageReference Update=\"Microsoft.Extensions.AI.Abstractions\" Version=\"9.5.0-preview.1.25262.9\"/>",
        "comment_created_at": "2025-05-16T05:20:47+00:00",
        "comment_author": "jeffhandley",
        "comment_body": "**@jsquire / @KrzysztofCwalina / @stephentoub - I apologize; this was my communication error.** I said to @jozkee that this was good to go ahead and push today, but of course we should have just waited a few hours until the stable version of Microsoft.Extensions.AI was published and initiate the PR based on that.\r\n\r\nSince @jozkee is away from work Friday, I updated the PR to:\r\n- Use Microsoft.Extensions.AI and Microsoft.Extensions.AI.Abstractions 9.5.0 stable\r\n- Use Microsoft.Extensions.Caching.Memory 8.0.1 per @jsquire's comment that we should baseline to 8.0.x versions\r\n- Incorporated the last change we made in dotnet/extensions to use RawRepresentationFactory on embedding generators\r\n- Made a couple remaining `Assert` coding style changes",
        "pr_file_module": null
      },
      {
        "comment_id": "2093433843",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50097,
        "pr_file": "eng/Packages.Data.props",
        "discussion_id": "2092087662",
        "commented_code": "@@ -104,6 +104,7 @@\n     <PackageReference Update=\"Microsoft.Bcl.AsyncInterfaces\" Version=\"8.0.0\" />\n     <PackageReference Update=\"Microsoft.CSharp\" Version=\"4.7.0\" />\n \t\t<PackageReference Update=\"Microsoft.Extensions.Logging.Abstractions\" Version=\"8.0.3\"/>\n+    <PackageReference Update=\"Microsoft.Extensions.AI.Abstractions\" Version=\"9.5.0-preview.1.25262.9\"/>",
        "comment_created_at": "2025-05-16T17:25:30+00:00",
        "comment_author": "jsquire",
        "comment_body": "Thanks, @jeffhandley.    We'll also need to isolate the 9.x dependencies in a conditional block specific to this library.   We don't want them to appear as approved dependencies for other libraries in the repository. An example (and a good place to add it) is around here:  https://github.com/Azure/azure-sdk-for-net/blob/main/eng/Packages.Data.props#L199",
        "pr_file_module": null
      },
      {
        "comment_id": "2093599324",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50097,
        "pr_file": "eng/Packages.Data.props",
        "discussion_id": "2092087662",
        "commented_code": "@@ -104,6 +104,7 @@\n     <PackageReference Update=\"Microsoft.Bcl.AsyncInterfaces\" Version=\"8.0.0\" />\n     <PackageReference Update=\"Microsoft.CSharp\" Version=\"4.7.0\" />\n \t\t<PackageReference Update=\"Microsoft.Extensions.Logging.Abstractions\" Version=\"8.0.3\"/>\n+    <PackageReference Update=\"Microsoft.Extensions.AI.Abstractions\" Version=\"9.5.0-preview.1.25262.9\"/>",
        "comment_created_at": "2025-05-16T19:50:16+00:00",
        "comment_author": "jeffhandley",
        "comment_body": "Thanks for the pointer on that @jsquire. I just pushed a commit that uses a conditional `<PackageReference />`. For the test reference to `Microsoft.Extensions.AI`, I didn't see any project-specific package referenced defined, so I left a comment on the line instead.",
        "pr_file_module": null
      }
    ]
  }
]
