---
title: Follow formatting standards
description: 'Maintain consistent code formatting by adhering to the defined standards
  in the .editorconfig file and Azure SDK implementation guidelines at https://azure.github.io/azure-sdk/dotnet_implementation.html.
  Pay attention to these specific formatting rules:'
repository: Azure/azure-sdk-for-net
label: Code Style
language: Markdown
comments_count: 3
repository_stars: 5809
---

Maintain consistent code formatting by adhering to the defined standards in the .editorconfig file and Azure SDK implementation guidelines at https://azure.github.io/azure-sdk/dotnet_implementation.html. Pay attention to these specific formatting rules:

1. Avoid trailing whitespace at the end of lines
2. In tests, do not emit "Act", "Arrange", or "Assert" comments
3. When including code examples in documentation (like README files), ensure they are mirrored in corresponding test files with proper conditional compilation:

```csharp
#if SNIPPET
// Code snippet that appears in README
[DllImport("user32.dll")]
static extern IntPtr GetForegroundWindow();
#endif
```

4. Use correct casing, grammar, and formatting in changelog entries:
   - Use sentence case for the first word (capitalize first letter)
   - Be specific and clear about changes (e.g., "Changed `public IList<string>` to `public IReadOnlyList<string>`")

Consistent formatting improves readability, simplifies code reviews, and helps maintain a professional codebase.


[
  {
    "discussion_id": "2170509666",
    "pr_number": 50575,
    "pr_file": ".github/copilot-instructions.md",
    "created_at": "2025-06-27T01:49:30+00:00",
    "commented_code": "# Repository information\nNote that files in this repository are generally organized in the following way:\n- `azure-sdk-for-net/sdk/{service-directory}/{package-name}` holds everything for a specific Azure SDK package.\n- `azure-sdk-for-net/sdk/{service-directory}/{package-name}/src` holds the source code for the package.\n- `azure-sdk-for-net/sdk/{service-directory}/{package-name}/tests` holds the tests for the package.\n- `azure-sdk-for-net/sdk/{service-directory}/{package-name}/samples` holds the samples for the package.\n\nThere are a few exceptions where package-name is replaced with a shorter directory name. For example in the cognitiveservices directory. The package `Microsoft.Azure.CognitiveServices.Language.SpellCheck` can be found in `azure-sdk-for-net/sdk/cognitiveservices/Language.SpellCheck`. When in doubt, you can look at the name of the .csproj file within the src folder to determine the package name.\n\n## Definitions:\n- \"service directory\" refers to the folder under `sdk`. For example, `azure-sdk-for-net/sdk/eventhub`, `eventhub` is the service directory\n- \"data plane\" refers to packages that don't include `ResourceManager` in the package name. They are used to interact with azure resources at application run time.\n- \"management plane\" refers to packages that include `ResourceManager` in the package name. They are used to manage (create/modify/delete) azure resources.\n- \"track 2\" refers to packages that start with `Azure`. Unless otherwise specified, assume that references to \"data plane\" mean \"track 2 data plane\", i.e. packages that start with `Azure` and don't include `ResourceManager` in the package name. Unless otherwise specified, assume that references to \"management plane\" mean \"track 2 management plane\", i.e. packages that start with `Azure.ResourceManager`.\n- \"functions extensions packages\" or sometimes just \"extensions packages\" refers to packages that start with `Microsoft.Azure.WebJobs.Extensions`. They are built on data plane packages and are used with Azure Functions.\n\n# Requirements\n- If you are writing C# code within the `azure-sdk-for-net/sdk` directory:\n    1. Follow the coding guidelines in the \"Coding guidelines\" section below.\n    2. You should never manually make changes to `*/Generated/*` files, e.g. `azure-sdk-for-net/sdk/containerregistry/Azure.Containers.ContainerRegistry/src/Generated/`\n        - Only re-generate these files if instructed to do so. If you are instructed to regenerate an SDK, use `dotnet build /t:GenerateCode`\n        - If you feel like you need to make changes to these files beyond re-generating them in order to complete your task, do not do this, instead see if you can work around the problem in the code that is not in the `Generated` folder. If you can't, report this to the user.\n    3. Code should build successfully using the following steps:\n        - navigate to the root of the repository and run `dotnet build eng\\service.proj /p:ServiceDirectory={service-directory}` for each service directory you modified. For example, if you modified code in `sdk/eventhub` and `sdk/keyvault`, you would run:\n          `dotnet build eng\\service.proj /p:ServiceDirectory=eventhub` and `dotnet build eng\\service.proj /p:ServiceDirectory=keyvault`\n        - If you see build errors, try to fix them, if you can't fix them within 5 iterations, give up, do not do steps 4 or 5, and report this to the user. Do not report success if the build fails!\n    4. Once the code builds, run the unit tests using `dotnet test eng/service.proj /p:ServiceDirectory={service-directory} --filter TestCategory!=Live` for each service directory you modified. Try to fix failures if you can within 5 iterations. If you can't, give up and report this to the user. Do not report success if the tests fail!\n    5. When you're done working, navigate to the root of the repository and run `.\\eng\\scripts\\Export-API.ps1 {service-directory}` for each service directory you modified.\n---\n\n## Coding guidelines\n- Follow implementation guidelines at https://azure.github.io/azure-sdk/dotnet_implementation.html\n- When writing tests, do not emit \"Act\", \"Arrange\" or \"Assert\" comments.\n- Do not add extra whitespace to the end of lines.",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2170509666",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50575,
        "pr_file": ".github/copilot-instructions.md",
        "discussion_id": "2170509666",
        "commented_code": "@@ -0,0 +1,34 @@\n+# Repository information\n+Note that files in this repository are generally organized in the following way:\n+- `azure-sdk-for-net/sdk/{service-directory}/{package-name}` holds everything for a specific Azure SDK package.\n+- `azure-sdk-for-net/sdk/{service-directory}/{package-name}/src` holds the source code for the package.\n+- `azure-sdk-for-net/sdk/{service-directory}/{package-name}/tests` holds the tests for the package.\n+- `azure-sdk-for-net/sdk/{service-directory}/{package-name}/samples` holds the samples for the package.\n+\n+There are a few exceptions where package-name is replaced with a shorter directory name. For example in the cognitiveservices directory. The package `Microsoft.Azure.CognitiveServices.Language.SpellCheck` can be found in `azure-sdk-for-net/sdk/cognitiveservices/Language.SpellCheck`. When in doubt, you can look at the name of the .csproj file within the src folder to determine the package name.\n+\n+## Definitions:\n+- \"service directory\" refers to the folder under `sdk`. For example, `azure-sdk-for-net/sdk/eventhub`, `eventhub` is the service directory\n+- \"data plane\" refers to packages that don't include `ResourceManager` in the package name. They are used to interact with azure resources at application run time.\n+- \"management plane\" refers to packages that include `ResourceManager` in the package name. They are used to manage (create/modify/delete) azure resources.\n+- \"track 2\" refers to packages that start with `Azure`. Unless otherwise specified, assume that references to \"data plane\" mean \"track 2 data plane\", i.e. packages that start with `Azure` and don't include `ResourceManager` in the package name. Unless otherwise specified, assume that references to \"management plane\" mean \"track 2 management plane\", i.e. packages that start with `Azure.ResourceManager`.\n+- \"functions extensions packages\" or sometimes just \"extensions packages\" refers to packages that start with `Microsoft.Azure.WebJobs.Extensions`. They are built on data plane packages and are used with Azure Functions.\n+\n+# Requirements\n+- If you are writing C# code within the `azure-sdk-for-net/sdk` directory:\n+    1. Follow the coding guidelines in the \"Coding guidelines\" section below.\n+    2. You should never manually make changes to `*/Generated/*` files, e.g. `azure-sdk-for-net/sdk/containerregistry/Azure.Containers.ContainerRegistry/src/Generated/`\n+        - Only re-generate these files if instructed to do so. If you are instructed to regenerate an SDK, use `dotnet build /t:GenerateCode`\n+        - If you feel like you need to make changes to these files beyond re-generating them in order to complete your task, do not do this, instead see if you can work around the problem in the code that is not in the `Generated` folder. If you can't, report this to the user.\n+    3. Code should build successfully using the following steps:\n+        - navigate to the root of the repository and run `dotnet build eng\\service.proj /p:ServiceDirectory={service-directory}` for each service directory you modified. For example, if you modified code in `sdk/eventhub` and `sdk/keyvault`, you would run:\n+          `dotnet build eng\\service.proj /p:ServiceDirectory=eventhub` and `dotnet build eng\\service.proj /p:ServiceDirectory=keyvault`\n+        - If you see build errors, try to fix them, if you can't fix them within 5 iterations, give up, do not do steps 4 or 5, and report this to the user. Do not report success if the build fails!\n+    4. Once the code builds, run the unit tests using `dotnet test eng/service.proj /p:ServiceDirectory={service-directory} --filter TestCategory!=Live` for each service directory you modified. Try to fix failures if you can within 5 iterations. If you can't, give up and report this to the user. Do not report success if the tests fail!\n+    5. When you're done working, navigate to the root of the repository and run `.\\eng\\scripts\\Export-API.ps1 {service-directory}` for each service directory you modified.\n+---\n+\n+## Coding guidelines\n+- Follow implementation guidelines at https://azure.github.io/azure-sdk/dotnet_implementation.html\n+- When writing tests, do not emit \"Act\", \"Arrange\" or \"Assert\" comments.\n+- Do not add extra whitespace to the end of lines.",
        "comment_created_at": "2025-06-27T01:49:30+00:00",
        "comment_author": "jsquire",
        "comment_body": "- Follow the formatting standards defined in https://github.com/Azure/azure-sdk-for-net/blob/main/.editorconfig",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2044868457",
    "pr_number": 49414,
    "pr_file": "sdk/identity/Azure.Identity.Broker/README.md",
    "created_at": "2025-04-15T15:09:19+00:00",
    "commented_code": "// Use the credential to authenticate a secret client\nvar client = new SecretClient(new Uri(\"https://myvault.vault.azure.net/\"), credential);\n\n[DllImport(\"user32.dll\")]\nstatic extern IntPtr GetForegroundWindow();",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2044868457",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 49414,
        "pr_file": "sdk/identity/Azure.Identity.Broker/README.md",
        "discussion_id": "2044868457",
        "commented_code": "@@ -55,6 +55,9 @@ var credential = new InteractiveBrowserCredential(\n \n // Use the credential to authenticate a secret client\n var client = new SecretClient(new Uri(\"https://myvault.vault.azure.net/\"), credential);\n+\n+[DllImport(\"user32.dll\")]\n+static extern IntPtr GetForegroundWindow();",
        "comment_created_at": "2025-04-15T15:09:19+00:00",
        "comment_author": "christothes",
        "comment_body": "Thanks for the contribution!\r\n\r\nThis is failing the build because the exact same code needs to be placed in [this file](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/identity/Azure.Identity.Broker/tests/samples/ReadmeSnippets.cs) in the same location. However, the file in question already contains this code, just outside the snippet, so for this to build, you'll need to add it to the .cs file as so:\r\n\r\n```c#\r\n#if SNIPPET\r\n[DllImport(\"user32.dll\")]\r\nstatic extern IntPtr GetForegroundWindow();\r\n#endif\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2139354967",
    "pr_number": 50540,
    "pr_file": "sdk/grafana/Azure.ResourceManager.Grafana/CHANGELOG.md",
    "created_at": "2025-06-11T06:55:09+00:00",
    "commented_code": "- Enable the new model serialization by using the System.ClientModel, refer this [document](https://aka.ms/azsdk/net/mrw) for more details.\n- Exposed `JsonModelWriteCore` for model serialization procedure.\n- customization for Tsp Geneartion diff : public IList<string> RequiredZoneNames { get; } to public IReadOnlyList<string> RequiredZoneNames { get; }",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2139354967",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50540,
        "pr_file": "sdk/grafana/Azure.ResourceManager.Grafana/CHANGELOG.md",
        "discussion_id": "2139354967",
        "commented_code": "@@ -16,6 +16,7 @@\n \n - Enable the new model serialization by using the System.ClientModel, refer this [document](https://aka.ms/azsdk/net/mrw) for more details.\n - Exposed `JsonModelWriteCore` for model serialization procedure.\n+- customization for Tsp Geneartion diff : public IList<string> RequiredZoneNames { get; } to public IReadOnlyList<string> RequiredZoneNames { get; }  ",
        "comment_created_at": "2025-06-11T06:55:09+00:00",
        "comment_author": "Copilot",
        "comment_body": "Fix typos and casing in the changelog entry: e.g., \"Customization for TSP generation: change `RequiredZoneNames` from `IList<string>` to `IReadOnlyList<string>`.\"\n```suggestion\n- Customization for TSP Generation: changed `public IList<string> RequiredZoneNames { get; }` to `public IReadOnlyList<string> RequiredZoneNames { get; }`.\n```",
        "pr_file_module": null
      }
    ]
  }
]
