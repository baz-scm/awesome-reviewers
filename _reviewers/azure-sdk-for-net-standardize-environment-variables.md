---
title: Standardize environment variables
description: Ensure environment variable names are consistently spelled, properly
  referenced, and follow established naming conventions across test files. Replace
  hardcoded values with environment variables for credentials, endpoints, and other
  configurable test parameters. Always provide meaningful defaults when environment
  variables aren't available to ensure tests...
repository: Azure/azure-sdk-for-net
label: Configurations
language: C#
comments_count: 4
repository_stars: 5809
---

Ensure environment variable names are consistently spelled, properly referenced, and follow established naming conventions across test files. Replace hardcoded values with environment variables for credentials, endpoints, and other configurable test parameters. Always provide meaningful defaults when environment variables aren't available to ensure tests can run in various environments.

```csharp
// Instead of hardcoding test values:
var principalId = "22fdaec1-8b9f-49dc-bd72-ddaf8f215577";
var tenantId = "72f988af-86f1-41af-91ab-2d7cd011db47";
var connectionId = TestEnvironment.SHAREPOINT_CONECTION_ID; // Typo!

// Use environment variables with fallbacks and correct naming:
var principalId = Environment.GetEnvironmentVariable("TEST_PRINCIPAL_ID") ?? "22fdaec1-8b9f-49dc-bd72-ddaf8f215577";
var tenantId = Environment.GetEnvironmentVariable("TEST_TENANT_ID") ?? "72f988af-86f1-41af-91ab-2d7cd011db47";
var connectionId = TestEnvironment.SHAREPOINT_CONNECTION_ID; // Fixed spelling
```

When defining environment variable names in test environments or documentation, follow consistent naming patterns like using all caps with underscores for separators. Double-check for typos, as misspelled environment variable names will silently return null values and may cause tests to fail in unexpected ways.


[
  {
    "discussion_id": "2166970984",
    "pr_number": 50879,
    "pr_file": "sdk/ai/Azure.AI.Agents.Persistent/tests/Samples/Sample_PersistentAgents_Bing_Custom_Search.cs",
    "created_at": "2025-06-25T15:08:57+00:00",
    "commented_code": "// Copyright (c) Microsoft Corporation. All rights reserved.\n// Licensed under the MIT License.\n\n#nullable disable\n\nusing System;\nusing System.Threading;\nusing System.Threading.Tasks;\nusing Azure.Core.TestFramework;\nusing NUnit.Framework;\n\nnamespace Azure.AI.Agents.Persistent.Tests;\n\npublic partial class Sample_PersistentAgents_Bing_Custom_Search : SamplesBase<AIAgentsTestEnvironment>\n{\n    [Test]\n    [AsyncOnly]\n    public async Task BingCustomSearchExampleAsync()\n    {\n        #region Snippet:AgentsBingCustomSearch_CreateProject\n#if SNIPPET\n        var projectEndpoint = System.Environment.GetEnvironmentVariable(\"PROJECT_ENDPOINT\");\n        var modelDeploymentName = System.Environment.GetEnvironmentVariable(\"MODEL_DEPLOYMENT_NAME\");\n        var connectionId = System.Environment.GetEnvironmentVariable(\"BING_CUSTOM_CONNECTION_ID\");\n#else\n        var projectEndpoint = TestEnvironment.PROJECT_ENDPOINT;\n        var modelDeploymentName = TestEnvironment.MODELDEPLOYMENTNAME;\n        var connectionId = TestEnvironment.BING_CONECTION_ID;",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2166970984",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50879,
        "pr_file": "sdk/ai/Azure.AI.Agents.Persistent/tests/Samples/Sample_PersistentAgents_Bing_Custom_Search.cs",
        "discussion_id": "2166970984",
        "commented_code": "@@ -0,0 +1,199 @@\n+// Copyright (c) Microsoft Corporation. All rights reserved.\n+// Licensed under the MIT License.\n+\n+#nullable disable\n+\n+using System;\n+using System.Threading;\n+using System.Threading.Tasks;\n+using Azure.Core.TestFramework;\n+using NUnit.Framework;\n+\n+namespace Azure.AI.Agents.Persistent.Tests;\n+\n+public partial class Sample_PersistentAgents_Bing_Custom_Search : SamplesBase<AIAgentsTestEnvironment>\n+{\n+    [Test]\n+    [AsyncOnly]\n+    public async Task BingCustomSearchExampleAsync()\n+    {\n+        #region Snippet:AgentsBingCustomSearch_CreateProject\n+#if SNIPPET\n+        var projectEndpoint = System.Environment.GetEnvironmentVariable(\"PROJECT_ENDPOINT\");\n+        var modelDeploymentName = System.Environment.GetEnvironmentVariable(\"MODEL_DEPLOYMENT_NAME\");\n+        var connectionId = System.Environment.GetEnvironmentVariable(\"BING_CUSTOM_CONNECTION_ID\");\n+#else\n+        var projectEndpoint = TestEnvironment.PROJECT_ENDPOINT;\n+        var modelDeploymentName = TestEnvironment.MODELDEPLOYMENTNAME;\n+        var connectionId = TestEnvironment.BING_CONECTION_ID;",
        "comment_created_at": "2025-06-25T15:08:57+00:00",
        "comment_author": "Copilot",
        "comment_body": "This sample references `BING_CONECTION_ID` but the new property is `BING_CUSTOM_CONNECTION_ID`. Please update to use `TestEnvironment.BING_CUSTOM_CONNECTION_ID`.\n```suggestion\n        var connectionId = TestEnvironment.BING_CUSTOM_CONNECTION_ID;\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2156832075",
    "pr_number": 50705,
    "pr_file": "sdk/resourcemanager/Azure.ResourceManager/tests/Unit/ManagedServiceIdentityTest.cs",
    "created_at": "2025-06-19T11:54:21+00:00",
    "commented_code": "using Azure.ResourceManager.Models;\nusing NUnit.Framework;\n\n#nullable enable\n\nnamespace Azure.ResourceManager.Tests\n{\n    [Parallelizable]\n    public class ManagedServiceIdentityTests\n    {\n        private static readonly string TestAssetPath = Path.Combine(TestContext.CurrentContext.TestDirectory, \"Unit\", \"TestAssets\", \"Identity\");\n        private static readonly ModelReaderWriterOptions V3Options = new ModelReaderWriterOptions(\"W|v3\");\n\n        public JsonProperty DeserializerHelper(string filename)\n        private JsonElement DeserializerHelper(string filename, out string json)\n        {\n            var json = File.ReadAllText(Path.Combine(TestAssetPath, filename));\n            using JsonDocument document = JsonDocument.Parse(json);\n            JsonElement rootElement = document.RootElement.Clone();\n            return rootElement.EnumerateObject().First();\n            var originalJson = File.ReadAllText(Path.Combine(TestAssetPath, filename));\n            json = originalJson.Replace(\"\\r\\n\", \"\").Replace(\"\\n\", \"\").Replace(\" \", \"\").Replace(\"'principalId':'22fdaec1-8b9f-49dc-bd72-ddaf8f215577','tenantId':'72f988af-86f1-41af-91ab-2d7cd011db47',\".Replace('\\'', '\\\"'), \"\");",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2156832075",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50705,
        "pr_file": "sdk/resourcemanager/Azure.ResourceManager/tests/Unit/ManagedServiceIdentityTest.cs",
        "discussion_id": "2156832075",
        "commented_code": "@@ -8,40 +9,44 @@\n using Azure.ResourceManager.Models;\n using NUnit.Framework;\n \n+#nullable enable\n+\n namespace Azure.ResourceManager.Tests\n {\n     [Parallelizable]\n     public class ManagedServiceIdentityTests\n     {\n         private static readonly string TestAssetPath = Path.Combine(TestContext.CurrentContext.TestDirectory, \"Unit\", \"TestAssets\", \"Identity\");\n+        private static readonly ModelReaderWriterOptions V3Options = new ModelReaderWriterOptions(\"W|v3\");\n \n-        public JsonProperty DeserializerHelper(string filename)\n+        private JsonElement DeserializerHelper(string filename, out string json)\n         {\n-            var json = File.ReadAllText(Path.Combine(TestAssetPath, filename));\n-            using JsonDocument document = JsonDocument.Parse(json);\n-            JsonElement rootElement = document.RootElement.Clone();\n-            return rootElement.EnumerateObject().First();\n+            var originalJson = File.ReadAllText(Path.Combine(TestAssetPath, filename));\n+            json = originalJson.Replace(\"\\r\\n\", \"\").Replace(\"\\n\", \"\").Replace(\" \", \"\").Replace(\"'principalId':'22fdaec1-8b9f-49dc-bd72-ddaf8f215577','tenantId':'72f988af-86f1-41af-91ab-2d7cd011db47',\".Replace('\\'', '\\\"'), \"\");",
        "comment_created_at": "2025-06-19T11:54:21+00:00",
        "comment_author": "Copilot",
        "comment_body": "The hard-coded JSON normalization (including fixed principal and tenant ID values) is brittle; consider deriving these values dynamically or clarifying the intent with inline documentation.\n```suggestion\n            var principalId = Environment.GetEnvironmentVariable(\"TEST_PRINCIPAL_ID\") ?? \"22fdaec1-8b9f-49dc-bd72-ddaf8f215577\";\n            var tenantId = Environment.GetEnvironmentVariable(\"TEST_TENANT_ID\") ?? \"72f988af-86f1-41af-91ab-2d7cd011db47\";\n            json = originalJson.Replace(\"\\r\\n\", \"\").Replace(\"\\n\", \"\").Replace(\" \", \"\")\n                .Replace($\"'principalId':'{principalId}','tenantId':'{tenantId}',\".Replace('\\'', '\\\"'), \"\");\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2141202156",
    "pr_number": 50559,
    "pr_file": "sdk/ai/Azure.AI.Agents.Persistent/tests/Samples/Sample_PersistentAgents_Sharepoint.cs",
    "created_at": "2025-06-11T22:17:07+00:00",
    "commented_code": "\ufeff// Copyright (c) Microsoft Corporation. All rights reserved.\n// Licensed under the MIT License.\n\n#nullable disable\n\nusing System;\nusing System.Threading;\nusing System.Threading.Tasks;\nusing Azure.Core.TestFramework;\nusing NUnit.Framework;\n\nnamespace Azure.AI.Agents.Persistent.Tests;\n\npublic partial class Sample_PersistentAgents_Sharepoint : SamplesBase<AIAgentsTestEnvironment>\n{\n    [Test]\n    [AsyncOnly]\n    public async Task SharepointExampleAsync()\n    {\n#if SNIPPET\n        var projectEndpoint = System.Environment.GetEnvironmentVariable(\"PROJECT_ENDPOINT\");\n        var modelDeploymentName = System.Environment.GetEnvironmentVariable(\"MODEL_DEPLOYMENT_NAME\");\n        var connectionId = System.Environment.GetEnvironmentVariable(\"AZURE_SHAREPOINT_CONECTION_ID\");",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2141202156",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50559,
        "pr_file": "sdk/ai/Azure.AI.Agents.Persistent/tests/Samples/Sample_PersistentAgents_Sharepoint.cs",
        "discussion_id": "2141202156",
        "commented_code": "@@ -0,0 +1,185 @@\n+\ufeff// Copyright (c) Microsoft Corporation. All rights reserved.\n+// Licensed under the MIT License.\n+\n+#nullable disable\n+\n+using System;\n+using System.Threading;\n+using System.Threading.Tasks;\n+using Azure.Core.TestFramework;\n+using NUnit.Framework;\n+\n+namespace Azure.AI.Agents.Persistent.Tests;\n+\n+public partial class Sample_PersistentAgents_Sharepoint : SamplesBase<AIAgentsTestEnvironment>\n+{\n+    [Test]\n+    [AsyncOnly]\n+    public async Task SharepointExampleAsync()\n+    {\n+#if SNIPPET\n+        var projectEndpoint = System.Environment.GetEnvironmentVariable(\"PROJECT_ENDPOINT\");\n+        var modelDeploymentName = System.Environment.GetEnvironmentVariable(\"MODEL_DEPLOYMENT_NAME\");\n+        var connectionId = System.Environment.GetEnvironmentVariable(\"AZURE_SHAREPOINT_CONECTION_ID\");",
        "comment_created_at": "2025-06-11T22:17:07+00:00",
        "comment_author": "Copilot",
        "comment_body": "The environment variable name is misspelled as 'AZURE_SHAREPOINT_CONECTION_ID'. It should be 'AZURE_SHAREPOINT_CONNECTION_ID' to match the test environment and avoid null values.\n```suggestion\n        var connectionId = System.Environment.GetEnvironmentVariable(\"AZURE_SHAREPOINT_CONNECTION_ID\");\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "2141205489",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50559,
        "pr_file": "sdk/ai/Azure.AI.Agents.Persistent/tests/Samples/Sample_PersistentAgents_Sharepoint.cs",
        "discussion_id": "2141202156",
        "commented_code": "@@ -0,0 +1,185 @@\n+\ufeff// Copyright (c) Microsoft Corporation. All rights reserved.\n+// Licensed under the MIT License.\n+\n+#nullable disable\n+\n+using System;\n+using System.Threading;\n+using System.Threading.Tasks;\n+using Azure.Core.TestFramework;\n+using NUnit.Framework;\n+\n+namespace Azure.AI.Agents.Persistent.Tests;\n+\n+public partial class Sample_PersistentAgents_Sharepoint : SamplesBase<AIAgentsTestEnvironment>\n+{\n+    [Test]\n+    [AsyncOnly]\n+    public async Task SharepointExampleAsync()\n+    {\n+#if SNIPPET\n+        var projectEndpoint = System.Environment.GetEnvironmentVariable(\"PROJECT_ENDPOINT\");\n+        var modelDeploymentName = System.Environment.GetEnvironmentVariable(\"MODEL_DEPLOYMENT_NAME\");\n+        var connectionId = System.Environment.GetEnvironmentVariable(\"AZURE_SHAREPOINT_CONECTION_ID\");",
        "comment_created_at": "2025-06-11T22:20:52+00:00",
        "comment_author": "dargilco",
        "comment_body": "Good catch from Copilot!",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2141202161",
    "pr_number": 50559,
    "pr_file": "sdk/ai/Azure.AI.Agents.Persistent/tests/Samples/Sample_PersistentAgents_Sharepoint.cs",
    "created_at": "2025-06-11T22:17:07+00:00",
    "commented_code": "\ufeff// Copyright (c) Microsoft Corporation. All rights reserved.\n// Licensed under the MIT License.\n\n#nullable disable\n\nusing System;\nusing System.Threading;\nusing System.Threading.Tasks;\nusing Azure.Core.TestFramework;\nusing NUnit.Framework;\n\nnamespace Azure.AI.Agents.Persistent.Tests;\n\npublic partial class Sample_PersistentAgents_Sharepoint : SamplesBase<AIAgentsTestEnvironment>\n{\n    [Test]\n    [AsyncOnly]\n    public async Task SharepointExampleAsync()\n    {\n#if SNIPPET\n        var projectEndpoint = System.Environment.GetEnvironmentVariable(\"PROJECT_ENDPOINT\");\n        var modelDeploymentName = System.Environment.GetEnvironmentVariable(\"MODEL_DEPLOYMENT_NAME\");\n        var connectionId = System.Environment.GetEnvironmentVariable(\"AZURE_SHAREPOINT_CONECTION_ID\");\n#else\n        var projectEndpoint = TestEnvironment.PROJECT_ENDPOINT;\n        var modelDeploymentName = TestEnvironment.MODELDEPLOYMENTNAME;\n        var connectionId = TestEnvironment.SHAREPOINT_CONNECTION_ID;\n#endif\n        PersistentAgentsClient agentClient = new(projectEndpoint, new DefaultAzureCredential());\n        SharepointToolDefinition sharepointTool = new(\n            new SharepointGroundingToolParameters(\n                connectionId\n            )\n        );\n        PersistentAgent agent = await agentClient.Administration.CreateAgentAsync(\n           model: modelDeploymentName,\n           name: \"my-agent\",\n           instructions: \"You are a helpful agent.\",\n           tools: [ sharepointTool ]);\n\n        // Create thread for communication\n        PersistentAgentThread thread = await agentClient.Threads.CreateThreadAsync();\n\n        // Create message to thread\n        PersistentThreadMessage message = await agentClient.Messages.CreateMessageAsync(\n            thread.Id,\n            MessageRole.User,\n            \"<Your Sharepoint Query Here>\");\n\n        // Run the agent\n        ThreadRun run = await agentClient.Runs.CreateRunAsync(thread, agent);\n        do\n        {\n            await Task.Delay(TimeSpan.FromMilliseconds(500));\n            run = await agentClient.Runs.GetRunAsync(thread.Id, run.Id);\n        }\n        while (run.Status == RunStatus.Queued\n            || run.Status == RunStatus.InProgress);\n\n        Assert.AreEqual(\n            RunStatus.Completed,\n            run.Status,\n            run.LastError?.Message);\n\n        AsyncPageable<PersistentThreadMessage> messages = agentClient.Messages.GetMessagesAsync(\n            threadId: thread.Id,\n            order: ListSortOrder.Ascending\n        );\n\n        await foreach (PersistentThreadMessage threadMessage in messages)\n        {\n            Console.Write($\"{threadMessage.CreatedAt:yyyy-MM-dd HH:mm:ss} - {threadMessage.Role,10}: \");\n            foreach (MessageContent contentItem in threadMessage.ContentItems)\n            {\n                if (contentItem is MessageTextContent textItem)\n                {\n                    string response = textItem.Text;\n                    if (textItem.Annotations != null)\n                    {\n                        foreach (MessageTextAnnotation annotation in textItem.Annotations)\n                        {\n                            if (annotation is MessageTextUriCitationAnnotation uriAnnotation)\n                            {\n                                response = response.Replace(uriAnnotation.Text, $\" [{uriAnnotation.UriCitation.Title}]({uriAnnotation.UriCitation.Uri})\");\n                            }\n                        }\n                    }\n                    Console.Write($\"Agent response: {response}\");\n                }\n                else if (contentItem is MessageImageFileContent imageFileItem)\n                {\n                    Console.Write($\"<image from ID: {imageFileItem.FileId}\");\n                }\n                Console.WriteLine();\n            }\n        }\n        await agentClient.Threads.DeleteThreadAsync(threadId: thread.Id);\n        await agentClient.Administration.DeleteAgentAsync(agentId: agent.Id);\n    }\n\n    [Test]\n    [SyncOnly]\n    public void SharepointExample()\n    {\n#if SNIPPET\n        var projectEndpoint = System.Environment.GetEnvironmentVariable(\"PROJECT_ENDPOINT\");\n        var modelDeploymentName = System.Environment.GetEnvironmentVariable(\"MODEL_DEPLOYMENT_NAME\");\n        var connectionId = System.Environment.GetEnvironmentVariable(\"AZURE_SHAREPOINT_CONECTION_ID\");",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2141202161",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50559,
        "pr_file": "sdk/ai/Azure.AI.Agents.Persistent/tests/Samples/Sample_PersistentAgents_Sharepoint.cs",
        "discussion_id": "2141202161",
        "commented_code": "@@ -0,0 +1,185 @@\n+\ufeff// Copyright (c) Microsoft Corporation. All rights reserved.\n+// Licensed under the MIT License.\n+\n+#nullable disable\n+\n+using System;\n+using System.Threading;\n+using System.Threading.Tasks;\n+using Azure.Core.TestFramework;\n+using NUnit.Framework;\n+\n+namespace Azure.AI.Agents.Persistent.Tests;\n+\n+public partial class Sample_PersistentAgents_Sharepoint : SamplesBase<AIAgentsTestEnvironment>\n+{\n+    [Test]\n+    [AsyncOnly]\n+    public async Task SharepointExampleAsync()\n+    {\n+#if SNIPPET\n+        var projectEndpoint = System.Environment.GetEnvironmentVariable(\"PROJECT_ENDPOINT\");\n+        var modelDeploymentName = System.Environment.GetEnvironmentVariable(\"MODEL_DEPLOYMENT_NAME\");\n+        var connectionId = System.Environment.GetEnvironmentVariable(\"AZURE_SHAREPOINT_CONECTION_ID\");\n+#else\n+        var projectEndpoint = TestEnvironment.PROJECT_ENDPOINT;\n+        var modelDeploymentName = TestEnvironment.MODELDEPLOYMENTNAME;\n+        var connectionId = TestEnvironment.SHAREPOINT_CONNECTION_ID;\n+#endif\n+        PersistentAgentsClient agentClient = new(projectEndpoint, new DefaultAzureCredential());\n+        SharepointToolDefinition sharepointTool = new(\n+            new SharepointGroundingToolParameters(\n+                connectionId\n+            )\n+        );\n+        PersistentAgent agent = await agentClient.Administration.CreateAgentAsync(\n+           model: modelDeploymentName,\n+           name: \"my-agent\",\n+           instructions: \"You are a helpful agent.\",\n+           tools: [ sharepointTool ]);\n+\n+        // Create thread for communication\n+        PersistentAgentThread thread = await agentClient.Threads.CreateThreadAsync();\n+\n+        // Create message to thread\n+        PersistentThreadMessage message = await agentClient.Messages.CreateMessageAsync(\n+            thread.Id,\n+            MessageRole.User,\n+            \"<Your Sharepoint Query Here>\");\n+\n+        // Run the agent\n+        ThreadRun run = await agentClient.Runs.CreateRunAsync(thread, agent);\n+        do\n+        {\n+            await Task.Delay(TimeSpan.FromMilliseconds(500));\n+            run = await agentClient.Runs.GetRunAsync(thread.Id, run.Id);\n+        }\n+        while (run.Status == RunStatus.Queued\n+            || run.Status == RunStatus.InProgress);\n+\n+        Assert.AreEqual(\n+            RunStatus.Completed,\n+            run.Status,\n+            run.LastError?.Message);\n+\n+        AsyncPageable<PersistentThreadMessage> messages = agentClient.Messages.GetMessagesAsync(\n+            threadId: thread.Id,\n+            order: ListSortOrder.Ascending\n+        );\n+\n+        await foreach (PersistentThreadMessage threadMessage in messages)\n+        {\n+            Console.Write($\"{threadMessage.CreatedAt:yyyy-MM-dd HH:mm:ss} - {threadMessage.Role,10}: \");\n+            foreach (MessageContent contentItem in threadMessage.ContentItems)\n+            {\n+                if (contentItem is MessageTextContent textItem)\n+                {\n+                    string response = textItem.Text;\n+                    if (textItem.Annotations != null)\n+                    {\n+                        foreach (MessageTextAnnotation annotation in textItem.Annotations)\n+                        {\n+                            if (annotation is MessageTextUriCitationAnnotation uriAnnotation)\n+                            {\n+                                response = response.Replace(uriAnnotation.Text, $\" [{uriAnnotation.UriCitation.Title}]({uriAnnotation.UriCitation.Uri})\");\n+                            }\n+                        }\n+                    }\n+                    Console.Write($\"Agent response: {response}\");\n+                }\n+                else if (contentItem is MessageImageFileContent imageFileItem)\n+                {\n+                    Console.Write($\"<image from ID: {imageFileItem.FileId}\");\n+                }\n+                Console.WriteLine();\n+            }\n+        }\n+        await agentClient.Threads.DeleteThreadAsync(threadId: thread.Id);\n+        await agentClient.Administration.DeleteAgentAsync(agentId: agent.Id);\n+    }\n+\n+    [Test]\n+    [SyncOnly]\n+    public void SharepointExample()\n+    {\n+#if SNIPPET\n+        var projectEndpoint = System.Environment.GetEnvironmentVariable(\"PROJECT_ENDPOINT\");\n+        var modelDeploymentName = System.Environment.GetEnvironmentVariable(\"MODEL_DEPLOYMENT_NAME\");\n+        var connectionId = System.Environment.GetEnvironmentVariable(\"AZURE_SHAREPOINT_CONECTION_ID\");",
        "comment_created_at": "2025-06-11T22:17:07+00:00",
        "comment_author": "Copilot",
        "comment_body": "The environment variable name is misspelled as 'AZURE_SHAREPOINT_CONECTION_ID'. It should be 'AZURE_SHAREPOINT_CONNECTION_ID' to match the test environment and avoid null values.\n```suggestion\n        var connectionId = System.Environment.GetEnvironmentVariable(\"AZURE_SHAREPOINT_CONNECTION_ID\");\n```",
        "pr_file_module": null
      }
    ]
  }
]
