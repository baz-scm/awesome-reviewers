---
title: Document code reasoning
description: 'Add clear, concise comments that explain the "why" behind complex logic,
  non-obvious decisions, and implicit behaviors. Focus on documenting:


  1. **Algorithmic choices and control flow** - Explain why loops are broken, conditions
  are checked, or specific approaches are used.'
repository: Azure/azure-sdk-for-net
label: Documentation
language: C#
comments_count: 6
repository_stars: 5809
---

Add clear, concise comments that explain the "why" behind complex logic, non-obvious decisions, and implicit behaviors. Focus on documenting:

1. **Algorithmic choices and control flow** - Explain why loops are broken, conditions are checked, or specific approaches are used.

```csharp
// Break if the next page is null
// Break the loop if the next page variable is null, indicating no more pages to process.
```

2. **Parameter handling details** - Document implicit conversions, default values, and edge cases.

```csharp
// The premiumPageBlobAccessTier parameter specifies the access tier for the page blob.
// If null, the REST API will apply the default tier or handle it gracefully.
```

3. **Version-specific logic or format handling** - Explain format parsing, version checks, or compatibility code.

```csharp
// This method checks if the format string in options.Format ends with the "|v3" suffix.
// The "|v3" suffix indicates that the ManagedServiceIdentity format is version 3.
// If the suffix is present, it is removed, and the base format is returned.
```

4. **Complex operations or type conversions** - Make non-obvious operations clear to future maintainers.

```csharp
// Convert ShareProtocols (multi-valued) to ShareProtocol (single-valued).
// If effectiveProtocol is ShareProtocols.Smb, map to ShareProtocol.Smb.
// Otherwise, default to ShareProtocol.Nfs.
```

Comments should benefit future maintainers by providing context that isn't immediately obvious from the code itself. When complex code can't be simplified, comprehensive documentation becomes essential for long-term maintainability.


[
  {
    "discussion_id": "2165164048",
    "pr_number": 50850,
    "pr_file": "eng/packages/http-client-csharp/generator/Azure.Generator/src/Providers/CollectionResultDefinition.cs",
    "created_at": "2025-06-25T00:03:13+00:00",
    "commented_code": "// Extract next page\n                doWhileStatement.Add(nextPageVariable.Assign(BuildGetNextPage(responseWithTypeVariable, responseVariable)).Terminate());\n\n                // Break if the next page is null",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2165164048",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50850,
        "pr_file": "eng/packages/http-client-csharp/generator/Azure.Generator/src/Providers/CollectionResultDefinition.cs",
        "discussion_id": "2165164048",
        "commented_code": "@@ -213,6 +216,9 @@ private MethodBodyStatement[] BuildAsPagesMethodBody()\n                 // Extract next page\n                 doWhileStatement.Add(nextPageVariable.Assign(BuildGetNextPage(responseWithTypeVariable, responseVariable)).Terminate());\n \n+                // Break if the next page is null",
        "comment_created_at": "2025-06-25T00:03:13+00:00",
        "comment_author": "Copilot",
        "comment_body": "[nitpick] Consider adding a code comment for clarity and remove redundant parentheses to improve readability.\n```suggestion\n                // Break if the next page is null\n                // Break the loop if the next page variable is null, indicating no more pages to process.\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2160611331",
    "pr_number": 50777,
    "pr_file": "eng/packages/http-client-csharp/generator/Azure.Generator/test/Visitors/NamespaceVisitorTests.cs",
    "created_at": "2025-06-23T02:26:18+00:00",
    "commented_code": "Assert.AreEqual(\"Samples\", updatedModel!.Type.Namespace);\n        }\n\n        [Test]\n        public void DoesNotChangeNamespaceOfCustomizedModel()\n        {\n            MockHelpers.LoadMockPlugin(configurationJson: \"{ \\\"package-name\\\": \\\"TestLibrary\\\", \\\"model-namespace\\\": true }\");\n            var visitor = new TestNamespaceVisitor();\n            var inputType = InputFactory.Model(\"TestModel\", \"Samples\");\n            var model = new ModelProvider(inputType);\n\n            // simulate a customized model\n            model.GetType().BaseType!.GetField(\n                \"_customCodeView\",\n                System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance)?\n                .SetValue(model, new Lazy<TypeProvider>(() => new TestTypeProvider()));",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2160611331",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50777,
        "pr_file": "eng/packages/http-client-csharp/generator/Azure.Generator/test/Visitors/NamespaceVisitorTests.cs",
        "discussion_id": "2160611331",
        "commented_code": "@@ -38,6 +39,25 @@ public void DoesNotUseModelsNamespaceIfConfigSetToFalse()\n             Assert.AreEqual(\"Samples\", updatedModel!.Type.Namespace);\n         }\n \n+        [Test]\n+        public void DoesNotChangeNamespaceOfCustomizedModel()\n+        {\n+            MockHelpers.LoadMockPlugin(configurationJson: \"{ \\\"package-name\\\": \\\"TestLibrary\\\", \\\"model-namespace\\\": true }\");\n+            var visitor = new TestNamespaceVisitor();\n+            var inputType = InputFactory.Model(\"TestModel\", \"Samples\");\n+            var model = new ModelProvider(inputType);\n+\n+            // simulate a customized model\n+            model.GetType().BaseType!.GetField(\n+                \"_customCodeView\",\n+                System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance)?\n+                .SetValue(model, new Lazy<TypeProvider>(() => new TestTypeProvider()));",
        "comment_created_at": "2025-06-23T02:26:18+00:00",
        "comment_author": "Copilot",
        "comment_body": "Consider extracting the reflection logic used to set _customCodeView into a helper method or documenting its purpose to improve maintainability and reduce the risk of breakage if the field name changes.\n```suggestion\n            SetCustomCodeView(model, new Lazy<TypeProvider>(() => new TestTypeProvider()));\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2156832104",
    "pr_number": 50705,
    "pr_file": "sdk/resourcemanager/Azure.ResourceManager/src/Common/Custom/Models/ManagedServiceIdentity.Serialization.cs",
    "created_at": "2025-06-19T11:54:22+00:00",
    "commented_code": "[JsonConverter(typeof(ManagedServiceIdentityConverter))]\n    public partial class ManagedServiceIdentity : IJsonModel<ManagedServiceIdentity>\n    {\n        internal void Write(Utf8JsonWriter writer, ModelReaderWriterOptions options, JsonSerializerOptions jOptions = default)\n        private const string SystemAssignedUserAssignedV3Value = \"SystemAssigned,UserAssigned\";",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2156832104",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50705,
        "pr_file": "sdk/resourcemanager/Azure.ResourceManager/src/Common/Custom/Models/ManagedServiceIdentity.Serialization.cs",
        "discussion_id": "2156832104",
        "commented_code": "@@ -18,22 +18,51 @@ namespace Azure.ResourceManager.Models\n     [JsonConverter(typeof(ManagedServiceIdentityConverter))]\n     public partial class ManagedServiceIdentity : IJsonModel<ManagedServiceIdentity>\n     {\n-        internal void Write(Utf8JsonWriter writer, ModelReaderWriterOptions options, JsonSerializerOptions jOptions = default)\n+        private const string SystemAssignedUserAssignedV3Value = \"SystemAssigned,UserAssigned\";\n+",
        "comment_created_at": "2025-06-19T11:54:22+00:00",
        "comment_author": "Copilot",
        "comment_body": "[nitpick] Consider adding a comment explaining the rationale behind checking for the '|v3' suffix in options.Format to improve future maintainability and clarity.\n```suggestion\n\n        // This method checks if the format string in options.Format ends with the \"|v3\" suffix.\n        // The \"|v3\" suffix indicates that the ManagedServiceIdentity format is version 3.\n        // If the suffix is present, it is removed, and the base format is returned via the 'format' parameter.\n        // This allows the method to handle version-specific logic while preserving the base format.\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "2157828757",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50705,
        "pr_file": "sdk/resourcemanager/Azure.ResourceManager/src/Common/Custom/Models/ManagedServiceIdentity.Serialization.cs",
        "discussion_id": "2156832104",
        "commented_code": "@@ -18,22 +18,51 @@ namespace Azure.ResourceManager.Models\n     [JsonConverter(typeof(ManagedServiceIdentityConverter))]\n     public partial class ManagedServiceIdentity : IJsonModel<ManagedServiceIdentity>\n     {\n-        internal void Write(Utf8JsonWriter writer, ModelReaderWriterOptions options, JsonSerializerOptions jOptions = default)\n+        private const string SystemAssignedUserAssignedV3Value = \"SystemAssigned,UserAssigned\";\n+",
        "comment_created_at": "2025-06-20T00:42:53+00:00",
        "comment_author": "live1206",
        "comment_body": "added comment after rewording based on this.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2130331367",
    "pr_number": 50456,
    "pr_file": "sdk/storage/Azure.Storage.Blobs/src/PageBlobClient.cs",
    "created_at": "2025-06-05T20:53:25+00:00",
    "commented_code": "response = await PageBlobRestClient.CreateAsync(\n                            contentLength: 0,\n                            blobContentLength: size,",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2130331367",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50456,
        "pr_file": "sdk/storage/Azure.Storage.Blobs/src/PageBlobClient.cs",
        "discussion_id": "2130331367",
        "commented_code": "@@ -999,7 +1018,7 @@ private async Task<Response<BlobContentInfo>> CreateInternal(\n                         response = await PageBlobRestClient.CreateAsync(\n                             contentLength: 0,\n                             blobContentLength: size,",
        "comment_created_at": "2025-06-05T20:53:25+00:00",
        "comment_author": "Copilot",
        "comment_body": "Consider adding an inline comment clarifying the implicit conversion of PremiumPageBlobAccessTier and the intended handling of default or null values. This will help future maintainers understand how the premium tier parameter is propagated to the REST API call.\n```suggestion\n                            blobContentLength: size,\n                            // The premiumPageBlobAccessTier parameter specifies the access tier for the page blob.\n                            // If null, the REST API will apply the default tier or handle it gracefully.\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2124976966",
    "pr_number": 50394,
    "pr_file": "sdk/servicebus/Azure.Messaging.ServiceBus/src/Primitives/ServiceBusRetryPolicy.cs",
    "created_at": "2025-06-03T21:40:01+00:00",
    "commented_code": "bool logTimeoutRetriesAsVerbose = false)\n      {\n            var failedAttemptCount = 0;\n            var tryTimeout = CalculateTryTimeout(0);\n\n            TimeSpan tryTimeout = CalculateTryTimeout(0);\n            if (IsServerBusy && tryTimeout < ServerBusyBaseSleepTime)\n            {\n                // We are in a server busy state before we start processing.\n                // Since ServerBusyBaseSleepTime > remaining time for the operation, we don't wait for the entire Sleep time.\n                await Task.Delay(tryTimeout, cancellationToken).ConfigureAwait(false);\n                throw new ServiceBusException(\n                    ServerBusyExceptionMessage,\n                    ServiceBusFailureReason.ServiceBusy);\n                while (IsServerBusy && !cancellationToken.IsCancellationRequested)",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2124976966",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50394,
        "pr_file": "sdk/servicebus/Azure.Messaging.ServiceBus/src/Primitives/ServiceBusRetryPolicy.cs",
        "discussion_id": "2124976966",
        "commented_code": "@@ -130,17 +133,42 @@ internal async ValueTask<TResult> RunOperation<T1, TResult>(\n             bool logTimeoutRetriesAsVerbose = false)\n       {\n             var failedAttemptCount = 0;\n+            var tryTimeout = CalculateTryTimeout(0);\n \n-            TimeSpan tryTimeout = CalculateTryTimeout(0);\n             if (IsServerBusy && tryTimeout < ServerBusyBaseSleepTime)\n             {\n-                // We are in a server busy state before we start processing.\n-                // Since ServerBusyBaseSleepTime > remaining time for the operation, we don't wait for the entire Sleep time.\n-                await Task.Delay(tryTimeout, cancellationToken).ConfigureAwait(false);\n-                throw new ServiceBusException(\n-                    ServerBusyExceptionMessage,\n-                    ServiceBusFailureReason.ServiceBusy);\n+                while (IsServerBusy && !cancellationToken.IsCancellationRequested)",
        "comment_created_at": "2025-06-03T21:40:01+00:00",
        "comment_author": "Copilot",
        "comment_body": "[nitpick] Add an inline comment within the while loop explaining the rationale behind recalculating the try timeout and the exit condition. This can help future maintainers understand how the retry logic adapts to a persisting server busy state.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2103555145",
    "pr_number": 50225,
    "pr_file": "sdk/storage/Azure.Storage.DataMovement.Files.Shares/src/DataMovementSharesExtensions.cs",
    "created_at": "2025-05-22T23:21:04+00:00",
    "commented_code": "try\n                {\n                    ShareProperties properties = await parentShareClient.GetPropertiesAsync(cancellationToken).ConfigureAwait(false);\n                    ShareProtocols expectedProtocol = options?.ShareProtocol ?? ShareProtocols.Smb;\n                    ShareProtocols actualProtocol = properties.Protocols ?? ShareProtocols.Smb;\n                    ShareProtocol expectedProtocol = options?.ShareProtocol ?? ShareProtocol.Smb;\n                    ShareProtocols effectiveProtocol = properties.Protocols ?? ShareProtocols.Smb;",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2103555145",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50225,
        "pr_file": "sdk/storage/Azure.Storage.DataMovement.Files.Shares/src/DataMovementSharesExtensions.cs",
        "discussion_id": "2103555145",
        "commented_code": "@@ -728,8 +728,9 @@ public static async Task ValidateProtocolAsync(\n                 try\n                 {\n                     ShareProperties properties = await parentShareClient.GetPropertiesAsync(cancellationToken).ConfigureAwait(false);\n-                    ShareProtocols expectedProtocol = options?.ShareProtocol ?? ShareProtocols.Smb;\n-                    ShareProtocols actualProtocol = properties.Protocols ?? ShareProtocols.Smb;\n+                    ShareProtocol expectedProtocol = options?.ShareProtocol ?? ShareProtocol.Smb;\n+                    ShareProtocols effectiveProtocol = properties.Protocols ?? ShareProtocols.Smb;",
        "comment_created_at": "2025-05-22T23:21:04+00:00",
        "comment_author": "Copilot",
        "comment_body": "Consider adding a clarifying comment explaining the conversion from ShareProtocols to ShareProtocol to improve readability, as this conversion may not be immediately clear to future maintainers.\n```suggestion\n                    ShareProtocols effectiveProtocol = properties.Protocols ?? ShareProtocols.Smb;\n                    // Convert ShareProtocols (multi-valued) to ShareProtocol (single-valued).\n                    // If effectiveProtocol is ShareProtocols.Smb, map to ShareProtocol.Smb.\n                    // Otherwise, default to ShareProtocol.Nfs.\n```",
        "pr_file_module": null
      }
    ]
  }
]
