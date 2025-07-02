---
title: Check before dereferencing
description: Always verify objects are not null before dereferencing them, particularly
  when using methods that might return null like FirstOrDefault(), LastOrDefault(),
  or 'as' casts. Prevent NullReferenceExceptions by adding explicit null checks before
  accessing members.
repository: Azure/azure-sdk-for-net
label: Null Handling
language: C#
comments_count: 7
repository_stars: 5809
---

Always verify objects are not null before dereferencing them, particularly when using methods that might return null like FirstOrDefault(), LastOrDefault(), or 'as' casts. Prevent NullReferenceExceptions by adding explicit null checks before accessing members.

// Risky code:
var lastContextualParameter = ContextualParameters.LastOrDefault();
if (parameter.Name.Equals(lastContextualParameter, StringComparison.InvariantCultureIgnoreCase))
{
    // This will throw if lastContextualParameter is null
}

// Safe code:
var lastContextualParameter = ContextualParameters.LastOrDefault();
if (lastContextualParameter != null && parameter.Name.Equals(lastContextualParameter, StringComparison.InvariantCultureIgnoreCase))
{
    // Only executes if lastContextualParameter is not null
}

For type conversions, prefer direct casts over 'as' when you expect the type to be present:

// Risky code:
(content.HttpContent as System.Net.Http.MultipartFormDataContent).Add(_dataStream, "file");

// Safe code - option 1 (direct cast):
((System.Net.Http.MultipartFormDataContent)content.HttpContent).Add(_dataStream, "file");

// Safe code - option 2 (explicit check):
var multipartContent = content.HttpContent as System.Net.Http.MultipartFormDataContent;
if (multipartContent != null)
{
    multipartContent.Add(_dataStream, "file");
}

When using LINQ's Single() method, consider using FirstOrDefault() with null checking instead to handle cases where the element might not exist:

// Risky code:
var resource = convenienceMethod.Signature.Parameters
    .Single(p => p.Type.Equals(ResourceData.Type));

// Safe code:
var resource = convenienceMethod.Signature.Parameters
    .FirstOrDefault(p => p.Type.Equals(ResourceData.Type));
if (resource != null)
{
    // Use resource
}
else
{
    // Handle the case where no matching parameter exists
}


[
  {
    "discussion_id": "2174433301",
    "pr_number": 50954,
    "pr_file": "eng/packages/http-client-csharp-mgmt/generator/Azure.Generator.Management/src/Providers/ResourceClientProvider.cs",
    "created_at": "2025-06-30T07:41:56+00:00",
    "commented_code": "}\n                // TODO: handle parents\n                // Handle resource name - the last contextual parameter\n                else if (parameter.Name.Equals(ContextualParameters.Last(), StringComparison.InvariantCultureIgnoreCase))\n                else if (parameter.Name.Equals(ContextualParameters.LastOrDefault(), StringComparison.InvariantCultureIgnoreCase))",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2174433301",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50954,
        "pr_file": "eng/packages/http-client-csharp-mgmt/generator/Azure.Generator.Management/src/Providers/ResourceClientProvider.cs",
        "discussion_id": "2174433301",
        "commented_code": "@@ -357,7 +357,7 @@ public ValueExpression[] PopulateArguments(\n                 }\n                 // TODO: handle parents\n                 // Handle resource name - the last contextual parameter\n-                else if (parameter.Name.Equals(ContextualParameters.Last(), StringComparison.InvariantCultureIgnoreCase))\n+                else if (parameter.Name.Equals(ContextualParameters.LastOrDefault(), StringComparison.InvariantCultureIgnoreCase))",
        "comment_created_at": "2025-06-30T07:41:56+00:00",
        "comment_author": "Copilot",
        "comment_body": "[nitpick] Consider storing the result of `ContextualParameters.LastOrDefault()` in a local variable and checking for null before calling `Equals` to improve readability and make the null comparison explicit.\n```suggestion\n                var lastContextualParameter = ContextualParameters.LastOrDefault();\n                if (lastContextualParameter != null && parameter.Name.Equals(lastContextualParameter, StringComparison.InvariantCultureIgnoreCase))\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2167764022",
    "pr_number": 50890,
    "pr_file": "sdk/tables/Azure.Data.Tables/src/TableErrorCode.cs",
    "created_at": "2025-06-25T22:41:33+00:00",
    "commented_code": "public static bool operator ==(TableErrorCode left, TableErrorCode right) => left.Equals(right);\n        /// <summary> Determines if two <see cref=\"TableErrorCode\"/> values are not the same. </summary>\n        public static bool operator !=(TableErrorCode left, TableErrorCode right) => !left.Equals(right);\n\n        /// <summary> Determines if a <see cref=\"TableErrorCode\"/> and a string are equal. </summary>\n        public static bool operator ==(TableErrorCode code, string value) => value != null && code.Equals(value);",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2167764022",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50890,
        "pr_file": "sdk/tables/Azure.Data.Tables/src/TableErrorCode.cs",
        "discussion_id": "2167764022",
        "commented_code": "@@ -215,6 +215,19 @@ public TableErrorCode(string value)\n         public static bool operator ==(TableErrorCode left, TableErrorCode right) => left.Equals(right);\n         /// <summary> Determines if two <see cref=\"TableErrorCode\"/> values are not the same. </summary>\n         public static bool operator !=(TableErrorCode left, TableErrorCode right) => !left.Equals(right);\n+\n+        /// <summary> Determines if a <see cref=\"TableErrorCode\"/> and a string are equal. </summary>\n+        public static bool operator ==(TableErrorCode code, string value) => value != null && code.Equals(value);",
        "comment_created_at": "2025-06-25T22:41:33+00:00",
        "comment_author": "Copilot",
        "comment_body": "If TableErrorCode can ever be null, consider adding a null check on the 'code' parameter before calling code.Equals(value) to avoid a potential NullReferenceException.\n```suggestion\n        public static bool operator ==(TableErrorCode code, string value) => code != null && value != null && code.Equals(value);\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2156832113",
    "pr_number": 50705,
    "pr_file": "sdk/resourcemanager/Azure.ResourceManager/tests/Unit/JsonAsserts.cs",
    "created_at": "2025-06-19T11:54:22+00:00",
    "commented_code": "Assert.AreEqual(expected, text);\n        }\n\n        public static void AssertConverterSerialization(string expected, object model, JsonSerializerOptions options = default)\n        public static void AssertConverterSerialization<T>(string expected, T model, ModelReaderWriterOptions? options = null)\n        {\n            using var memoryStream = new MemoryStream();\n\n            using (var writer = new Utf8JsonWriter(memoryStream))\n            {\n                JsonSerializer.Serialize(writer, model, options);\n                var jsonModel = model as IJsonModel<T>;\n                jsonModel?.Write(writer, options ?? new ModelReaderWriterOptions(\"W\"));",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2156832113",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50705,
        "pr_file": "sdk/resourcemanager/Azure.ResourceManager/tests/Unit/JsonAsserts.cs",
        "discussion_id": "2156832113",
        "commented_code": "@@ -22,13 +25,14 @@ public static void AssertSerialization(string expected, IUtf8JsonSerializable se\n             Assert.AreEqual(expected, text);\n         }\n \n-        public static void AssertConverterSerialization(string expected, object model, JsonSerializerOptions options = default)\n+        public static void AssertConverterSerialization<T>(string expected, T model, ModelReaderWriterOptions? options = null)\n         {\n             using var memoryStream = new MemoryStream();\n \n             using (var writer = new Utf8JsonWriter(memoryStream))\n             {\n-                JsonSerializer.Serialize(writer, model, options);\n+                var jsonModel = model as IJsonModel<T>;\n+                jsonModel?.Write(writer, options ?? new ModelReaderWriterOptions(\"W\"));",
        "comment_created_at": "2025-06-19T11:54:22+00:00",
        "comment_author": "Copilot",
        "comment_body": "[nitpick] If the cast to IJsonModel<T> fails (resulting in jsonModel being null), the subsequent call to Write may silently be skipped; consider adding an assertion or fallback to handle unexpected types.\n```suggestion\n                if (jsonModel == null)\n                {\n                    throw new InvalidOperationException($\"The provided model is not of type {typeof(IJsonModel<T>)}.\");\n                }\n                jsonModel.Write(writer, options ?? new ModelReaderWriterOptions(\"W\"));\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2141812407",
    "pr_number": 50568,
    "pr_file": "eng/packages/http-client-csharp-mgmt/generator/Azure.Generator.Management/src/Providers/ResourceClientProvider.cs",
    "created_at": "2025-06-12T06:25:42+00:00",
    "commented_code": "if (convenienceMethod != null)\n                    {\n                        var resource = convenienceMethod.Signature.Parameters\n                            .Single(p => p.Type.Equals(ResourceData.Type));\n                            .Single(p => p.Type.Equals(ResourceData.Type) || p.Type.Equals(typeof(RequestContent)));\n                        arguments.Add(resource);",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2141812407",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50568,
        "pr_file": "eng/packages/http-client-csharp-mgmt/generator/Azure.Generator.Management/src/Providers/ResourceClientProvider.cs",
        "discussion_id": "2141812407",
        "commented_code": "@@ -335,7 +330,7 @@ public ValueExpression[] PopulateArguments(\n                     if (convenienceMethod != null)\n                     {\n                         var resource = convenienceMethod.Signature.Parameters\n-                            .Single(p => p.Type.Equals(ResourceData.Type));\n+                            .Single(p => p.Type.Equals(ResourceData.Type) || p.Type.Equals(typeof(RequestContent)));\n                         arguments.Add(resource);",
        "comment_created_at": "2025-06-12T06:25:42+00:00",
        "comment_author": "Copilot",
        "comment_body": "Using `Single(...)` will throw if multiple parameters match or none match. Consider using `FirstOrDefault(...)` and handling a null result explicitly.\n```suggestion\n                            .FirstOrDefault(p => p.Type.Equals(ResourceData.Type) || p.Type.Equals(typeof(RequestContent)));\n                        if (resource != null)\n                        {\n                            arguments.Add(resource);\n                        }\n                        else\n                        {\n                            // Handle the case where no matching parameter is found\n                            throw new InvalidOperationException(\"No matching parameter found for ResourceData.Type or RequestContent.\");\n                        }\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2141812419",
    "pr_number": 50568,
    "pr_file": "eng/packages/http-client-csharp-mgmt/generator/Azure.Generator.Management/src/Providers/OperationMethodProviders/ResourceOperationMethodProvider.cs",
    "created_at": "2025-06-12T06:25:42+00:00",
    "commented_code": "private TryExpression BuildTryExpression()\n        {\n            var cancellationTokenParameter = _convenienceMethod.Signature.Parameters.Single(p => p.Type.Equals(typeof(CancellationToken)));\n\n            var cancellationTokenParameter = _convenienceMethod.Signature.Parameters.FirstOrDefault(p => p.Type.Equals(typeof(CancellationToken)));\n            var requestMethod = _resourceClientProvider.GetClientProvider().GetRequestMethodByOperation(_serviceMethod.Operation);\n\n            var tryStatements = new List<MethodBodyStatement>\n            var tryStatements = new List<MethodBodyStatement>();\n            VariableExpression contextVariable;\n\n            // If the cancellation token parameter is not provided, we create a default one otherwise we use the provided one.\n            // This is to ensure that the RequestContext is always created with a cancellation token.\n            if (cancellationTokenParameter != null)\n            {\n                ResourceMethodSnippets.CreateRequestContext(cancellationTokenParameter, out var contextVariable)\n            };\n                tryStatements.Add(ResourceMethodSnippets.CreateRequestContext(cancellationTokenParameter, out contextVariable));\n            }\n            else\n            {\n                contextVariable = _convenienceMethod.Signature.Parameters.Single(p => p.Type.Equals(typeof(RequestContext))).AsExpression();",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2141812419",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50568,
        "pr_file": "eng/packages/http-client-csharp-mgmt/generator/Azure.Generator.Management/src/Providers/OperationMethodProviders/ResourceOperationMethodProvider.cs",
        "discussion_id": "2141812419",
        "commented_code": "@@ -87,14 +87,22 @@ protected virtual MethodSignature CreateSignature()\n \n         private TryExpression BuildTryExpression()\n         {\n-            var cancellationTokenParameter = _convenienceMethod.Signature.Parameters.Single(p => p.Type.Equals(typeof(CancellationToken)));\n-\n+            var cancellationTokenParameter = _convenienceMethod.Signature.Parameters.FirstOrDefault(p => p.Type.Equals(typeof(CancellationToken)));\n             var requestMethod = _resourceClientProvider.GetClientProvider().GetRequestMethodByOperation(_serviceMethod.Operation);\n \n-            var tryStatements = new List<MethodBodyStatement>\n+            var tryStatements = new List<MethodBodyStatement>();\n+            VariableExpression contextVariable;\n+\n+            // If the cancellation token parameter is not provided, we create a default one otherwise we use the provided one.\n+            // This is to ensure that the RequestContext is always created with a cancellation token.\n+            if (cancellationTokenParameter != null)\n             {\n-                ResourceMethodSnippets.CreateRequestContext(cancellationTokenParameter, out var contextVariable)\n-            };\n+                tryStatements.Add(ResourceMethodSnippets.CreateRequestContext(cancellationTokenParameter, out contextVariable));\n+            }\n+            else\n+            {\n+                contextVariable = _convenienceMethod.Signature.Parameters.Single(p => p.Type.Equals(typeof(RequestContext))).AsExpression();",
        "comment_created_at": "2025-06-12T06:25:42+00:00",
        "comment_author": "Copilot",
        "comment_body": "This `Single(...)` will throw if the `RequestContext` parameter is missing. Consider using `FirstOrDefault(...)` with a fallback or validating existence before calling `Single`.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2124906481",
    "pr_number": 50391,
    "pr_file": "sdk/ai/Azure.AI.Agents.Persistent/src/Custom/UploadFileRequest.Serialization.cs",
    "created_at": "2025-06-03T20:52:54+00:00",
    "commented_code": "internal virtual MultipartFormDataRequestContent ToMultipartRequestContent()\n    {\n        MultipartFormDataRequestContent content = new();\n        content.Add(Data, \"file\", Filename);\n        ContentDispositionHeaderValue header = new(\"form-data\") { Name = \"file\"};\n        var _dataStream = new StreamContent(Data);\n        if (System.Linq.Enumerable.Any(Filename, c => c > 127))\n        {\n            header.FileNameStar = Filename;\n        }\n        else\n        {\n            header.FileName = Filename;\n        }\n        _dataStream.Headers.ContentDisposition = header;\n        (content.HttpContent as System.Net.Http.MultipartFormDataContent).Add(_dataStream, \"file\");",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2124906481",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50391,
        "pr_file": "sdk/ai/Azure.AI.Agents.Persistent/src/Custom/UploadFileRequest.Serialization.cs",
        "discussion_id": "2124906481",
        "commented_code": "@@ -19,7 +21,18 @@ internal partial class UploadFileRequest : IUtf8JsonSerializable\n     internal virtual MultipartFormDataRequestContent ToMultipartRequestContent()\n     {\n         MultipartFormDataRequestContent content = new();\n-        content.Add(Data, \"file\", Filename);\n+        ContentDispositionHeaderValue header = new(\"form-data\") { Name = \"file\"};\n+        var _dataStream = new StreamContent(Data);\n+        if (System.Linq.Enumerable.Any(Filename, c => c > 127))\n+        {\n+            header.FileNameStar = Filename;\n+        }\n+        else\n+        {\n+            header.FileName = Filename;\n+        }\n+        _dataStream.Headers.ContentDisposition = header;\n+        (content.HttpContent as System.Net.Http.MultipartFormDataContent).Add(_dataStream, \"file\");",
        "comment_created_at": "2025-06-03T20:52:54+00:00",
        "comment_author": "Copilot",
        "comment_body": "Using an 'as' cast here can yield null and lead to a NullReferenceException. Consider using a direct cast or checking for null before calling Add(), or refactor to expose the underlying MultipartFormDataContent safely.\n```suggestion\n        ((System.Net.Http.MultipartFormDataContent)content.HttpContent).Add(_dataStream, \"file\");\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2108313204",
    "pr_number": 50274,
    "pr_file": "eng/packages/http-client-csharp-mgmt/generator/Azure.Generator.Management/src/Extensions/ClientProviderExtensions.cs",
    "created_at": "2025-05-27T06:40:48+00:00",
    "commented_code": "\ufeff// Copyright (c) Microsoft Corporation. All rights reserved.\n// Licensed under the MIT License.\n\nusing Microsoft.TypeSpec.Generator.ClientModel.Providers;\nusing Microsoft.TypeSpec.Generator.Input;\nusing Microsoft.TypeSpec.Generator.Providers;\n\nnamespace Azure.Generator.Management.Extensions\n{\n    internal static class ClientProviderExtensions\n    {\n        public static MethodProvider GetConvenienceMethodByOperation(this ClientProvider clientProvider, InputOperation operation, bool isAsync)\n        {\n            var methods = clientProvider.GetMethodCollectionByOperation(operation);\n            return isAsync ? methods[^1] : methods[^2];",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2108313204",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50274,
        "pr_file": "eng/packages/http-client-csharp-mgmt/generator/Azure.Generator.Management/src/Extensions/ClientProviderExtensions.cs",
        "discussion_id": "2108313204",
        "commented_code": "@@ -0,0 +1,18 @@\n+\ufeff// Copyright (c) Microsoft Corporation. All rights reserved.\n+// Licensed under the MIT License.\n+\n+using Microsoft.TypeSpec.Generator.ClientModel.Providers;\n+using Microsoft.TypeSpec.Generator.Input;\n+using Microsoft.TypeSpec.Generator.Providers;\n+\n+namespace Azure.Generator.Management.Extensions\n+{\n+    internal static class ClientProviderExtensions\n+    {\n+        public static MethodProvider GetConvenienceMethodByOperation(this ClientProvider clientProvider, InputOperation operation, bool isAsync)\n+        {\n+            var methods = clientProvider.GetMethodCollectionByOperation(operation);\n+            return isAsync ? methods[^1] : methods[^2];",
        "comment_created_at": "2025-05-27T06:40:48+00:00",
        "comment_author": "Copilot",
        "comment_body": "Consider adding a guard check to ensure the 'methods' collection has at least two elements before indexing; this will prevent potential runtime errors if the collection contains fewer items than expected.",
        "pr_file_module": null
      }
    ]
  }
]
