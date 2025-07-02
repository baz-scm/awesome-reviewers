---
title: Maintain clean code structure
description: "Keep code clean and well-organized by:\n1. Removing unnecessary elements:\n\
  \   - Delete commented-out code that is no longer needed\n   - Remove unused using\
  \ directives"
repository: Azure/azure-sdk-for-net
label: Code Style
language: C#
comments_count: 5
repository_stars: 5809
---

Keep code clean and well-organized by:
1. Removing unnecessary elements:
   - Delete commented-out code that is no longer needed
   - Remove unused using directives
   - Avoid redundant code blocks

2. Organizing imports properly:
   - Group using directives consistently (System namespaces first)
   - Use clean imports instead of fully qualified names
   - Keep imports ordered alphabetically

Example - Before:
```csharp
using Azure.Core;
using System.Threading;
using System.Linq.Enumerable;
// Old implementation
// public void OldMethod() {
//    // ...
// }
using System;

public class MyClass 
{
    public void ProcessItems()
    {
        if (System.Linq.Enumerable.Any(items)) // Verbose qualification
        {
            // ...
        }
    }
}
```

After:
```csharp
using System;
using System.Linq;
using System.Threading;
using Azure.Core;

public class MyClass
{
    public void ProcessItems() 
    {
        if (items.Any()) // Clean syntax with proper imports
        {
            // ...
        }
    }
}
```


[
  {
    "discussion_id": "2128234500",
    "pr_number": 50447,
    "pr_file": "sdk/core/Azure.Core.Expressions.DataFactory/tests/DataFactoryElementTests.cs",
    "created_at": "2025-06-05T08:15:13+00:00",
    "commented_code": "private string GetSerializedString<T>(DataFactoryElement<T> payload)\n        {\n            using var ms = new MemoryStream();\n            using Utf8JsonWriter writer = new Utf8JsonWriter(ms);\n            JsonSerializer.Serialize(writer, payload);\n            writer.Flush();\n            ms.Position = 0;\n            using var sr = new StreamReader(ms);\n            return sr.ReadToEnd();\n            return ((IPersistableModel< DataFactoryElement<T>>)payload).Write(ModelReaderWriterOptions.Json).ToString();\n            //using var ms = new MemoryStream();\n            //using Utf8JsonWriter writer = new Utf8JsonWriter(ms);\n            //JsonSerializer.Serialize(writer, payload);\n            //writer.Flush();\n            //ms.Position = 0;\n            //using var sr = new StreamReader(ms);\n            //return sr.ReadToEnd();",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2128234500",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50447,
        "pr_file": "sdk/core/Azure.Core.Expressions.DataFactory/tests/DataFactoryElementTests.cs",
        "discussion_id": "2128234500",
        "commented_code": "@@ -1086,13 +1087,14 @@ private static void AssertKeyVaultReferenceDfe(DataFactoryElement<string?> dfe)\n \n         private string GetSerializedString<T>(DataFactoryElement<T> payload)\n         {\n-            using var ms = new MemoryStream();\n-            using Utf8JsonWriter writer = new Utf8JsonWriter(ms);\n-            JsonSerializer.Serialize(writer, payload);\n-            writer.Flush();\n-            ms.Position = 0;\n-            using var sr = new StreamReader(ms);\n-            return sr.ReadToEnd();\n+            return ((IPersistableModel< DataFactoryElement<T>>)payload).Write(ModelReaderWriterOptions.Json).ToString();\n+            //using var ms = new MemoryStream();\n+            //using Utf8JsonWriter writer = new Utf8JsonWriter(ms);\n+            //JsonSerializer.Serialize(writer, payload);\n+            //writer.Flush();\n+            //ms.Position = 0;\n+            //using var sr = new StreamReader(ms);\n+            //return sr.ReadToEnd();",
        "comment_created_at": "2025-06-05T08:15:13+00:00",
        "comment_author": "Copilot",
        "comment_body": "[nitpick] There is commented-out legacy code in GetSerializedString; remove these comments if they are no longer needed to improve code maintainability.\n```suggestion\n\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2124906492",
    "pr_number": 50391,
    "pr_file": "sdk/ai/Azure.AI.Agents.Persistent/src/Custom/UploadFileRequest.Serialization.cs",
    "created_at": "2025-06-03T20:52:54+00:00",
    "commented_code": "internal virtual MultipartFormDataRequestContent ToMultipartRequestContent()\n    {\n        MultipartFormDataRequestContent content = new();\n        content.Add(Data, \"file\", Filename);\n        ContentDispositionHeaderValue header = new(\"form-data\") { Name = \"file\"};\n        var _dataStream = new StreamContent(Data);\n        if (System.Linq.Enumerable.Any(Filename, c => c > 127))",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2124906492",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50391,
        "pr_file": "sdk/ai/Azure.AI.Agents.Persistent/src/Custom/UploadFileRequest.Serialization.cs",
        "discussion_id": "2124906492",
        "commented_code": "@@ -19,7 +21,18 @@ internal partial class UploadFileRequest : IUtf8JsonSerializable\n     internal virtual MultipartFormDataRequestContent ToMultipartRequestContent()\n     {\n         MultipartFormDataRequestContent content = new();\n-        content.Add(Data, \"file\", Filename);\n+        ContentDispositionHeaderValue header = new(\"form-data\") { Name = \"file\"};\n+        var _dataStream = new StreamContent(Data);\n+        if (System.Linq.Enumerable.Any(Filename, c => c > 127))",
        "comment_created_at": "2025-06-03T20:52:54+00:00",
        "comment_author": "Copilot",
        "comment_body": "[nitpick] Fully qualifying 'System.Linq.Enumerable.Any' is verbose. Consider adding 'using System.Linq;' and calling 'Filename.Any(c => c > 127)' for readability.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2108103812",
    "pr_number": 50265,
    "pr_file": "sdk/provisioning/Azure.Provisioning/src/BicepDictionaryOfT.cs",
    "created_at": "2025-05-27T03:51:38+00:00",
    "commented_code": "\ufeff// Copyright (c) Microsoft Corporation. All rights reserved.\n// Licensed under the MIT License.\n\nusing System;\nusing System.Collections;\nusing System.Collections.Generic;\nusing System.ComponentModel;\nusing System.Diagnostics.CodeAnalysis;\nusing System.Linq;\nusing System.Reflection;",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2108103812",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50265,
        "pr_file": "sdk/provisioning/Azure.Provisioning/src/BicepDictionaryOfT.cs",
        "discussion_id": "2108103812",
        "commented_code": "@@ -1,11 +1,13 @@\n \ufeff// Copyright (c) Microsoft Corporation. All rights reserved.\n // Licensed under the MIT License.\n \n+using System;\n using System.Collections;\n using System.Collections.Generic;\n using System.ComponentModel;\n using System.Diagnostics.CodeAnalysis;\n using System.Linq;\n+using System.Reflection;",
        "comment_created_at": "2025-05-27T03:51:38+00:00",
        "comment_author": "Copilot",
        "comment_body": "The 'System.Reflection' import is not used in this file; consider removing it to reduce clutter.\n```suggestion\n\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2105455424",
    "pr_number": 50255,
    "pr_file": "sdk/search/Azure.Search.Documents/src/Indexes/Models/SearchIndexerDataSourceConnection.cs",
    "created_at": "2025-05-23T21:38:17+00:00",
    "commented_code": "// Licensed under the MIT License.\n\nusing System;\nusing System.Collections.Generic;",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2105455424",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50255,
        "pr_file": "sdk/search/Azure.Search.Documents/src/Indexes/Models/SearchIndexerDataSourceConnection.cs",
        "discussion_id": "2105455424",
        "commented_code": "@@ -2,6 +2,7 @@\n // Licensed under the MIT License.\n \n using System;\n+using System.Collections.Generic;",
        "comment_created_at": "2025-05-23T21:38:17+00:00",
        "comment_author": "Copilot",
        "comment_body": "[nitpick] The `using` directives are not grouped or ordered consistently. It\u2019s clearer to list `System.*` namespaces first (e.g., `System.Collections.Generic` after `System`) followed by external dependencies.\n```suggestion\nusing System.Collections.Generic;\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2095888075",
    "pr_number": 50017,
    "pr_file": "eng/packages/http-client-csharp/generator/Azure.Generator/src/Providers/CollectionResultDefinition.cs",
    "created_at": "2025-05-19T14:47:38+00:00",
    "commented_code": "? [new CSharpType(typeof(AsyncPageable<>), _itemModelType)]\n                : [new CSharpType(typeof(Pageable<>), _itemModelType)];\n\n        protected override MethodProvider[] BuildMethods()\n        protected override MethodProvider[] BuildMethods() => [BuildAsPagesMethod(), BuildGetNextResponseMethod(), BuildGetResponseMethod()];\n\n        private MethodProvider BuildAsPagesMethod()\n        {\n            return new[]\n            var signature = new MethodSignature(\n                \"AsPages\",\n                $\"Gets the pages of {Name} as an enumerable collection.\",\n                _isAsync\n                    ? MethodSignatureModifiers.Async | MethodSignatureModifiers.Public | MethodSignatureModifiers.Override\n                    : MethodSignatureModifiers.Public | MethodSignatureModifiers.Override,\n                _isAsync ?\n                    new CSharpType(typeof(IAsyncEnumerable<>), new CSharpType(typeof(Page<>), _itemModelType)) :\n                    new CSharpType(typeof(IEnumerable<>), new CSharpType(typeof(Page<>), _itemModelType)),\n                $\"The pages of {Name} as an enumerable collection.\",\n                [NextLinkParameter, PageSizeHintParameter]);\n\n            if (!IsProtocolMethod())\n            {\n                new MethodProvider(\n                    new MethodSignature(\n                    \"AsPages\",\n                    $\"Gets the pages of {Name} as an enumerable collection.\",\n                    MethodSignatureModifiers.Public | MethodSignatureModifiers.Override,\n                    _isAsync ?\n                        new CSharpType(typeof(IAsyncEnumerable<>), new CSharpType(typeof(Page<>), _itemModelType)) :\n                        new CSharpType(typeof(IEnumerable<>), new CSharpType(typeof(Page<>), _itemModelType)),\n                    $\"The pages of {Name} as an enumerable collection.\",\n                    [ContinuationTokenParameter, PageSizeHintParameter]),\n                    ThrowExpression(Null),\n                    this)\n                // Convenience method\n                return new MethodProvider(signature, new MethodBodyStatement[]\n                {\n                    Declare(\"nextLink\", new CSharpType(typeof(string), isNullable: true), NextLinkParameter, out var nextLinkVariableForConvenience),\n                    BuildDoWhileStatementForConvenience(nextLinkVariableForConvenience)\n                }, this);\n            }\n\n            // Protocol method\n            return new MethodProvider(signature, new MethodBodyStatement[]\n                {\n                    Declare(\"nextLink\", new CSharpType(typeof(string), isNullable: true), NextLinkParameter, out var nextLinkVariable),\n                    BuildDoWhileStatementForProtocol(nextLinkVariable)\n                }, this);\n        }\n\n        private DoWhileStatement BuildDoWhileStatementForProtocol(VariableExpression nextLinkVariable)\n        {\n            var doWhileStatement = new DoWhileStatement(Not(Static<string>().Invoke(\"IsNullOrEmpty\", [nextLinkVariable])));\n\n            // Get the response\n            doWhileStatement.Add(Declare(\"response\", new CSharpType(typeof(Response), isNullable: true),\n                This.Invoke(_getNextResponseMethodName, [PageSizeHintParameter, nextLinkVariable], _isAsync),\n                out var responseVariable));\n\n            // Early exit if response is null\n            doWhileStatement.Add(new IfStatement(responseVariable.Is(Null)) { new YieldBreakStatement() });\n\n            // Parse response content as JsonDocument\n            doWhileStatement.Add(UsingDeclare(\"jsonDoc\", typeof(JsonDocument),\n                Static<JsonDocument>().Invoke(\"Parse\", [responseVariable.Property(\"Content\").Invoke(\"ToString\")]),\n                out var jsonDocVariable));\n\n            // Get root element\n            doWhileStatement.Add(Declare(\"root\", typeof(JsonElement),\n                jsonDocVariable.Property(\"RootElement\"), out var rootVariable));\n\n            // Extract items array\n            doWhileStatement.Add(Declare(\"items\", new CSharpType(typeof(List<>), _itemModelType),\n                New.Instance(new CSharpType(typeof(List<>), _itemModelType)), out var itemsVariable));\n\n            // Get items array from response\n            var tryGetItems = new IfStatement(rootVariable.Invoke(\"TryGetProperty\", [Literal(_itemsPropertyName), new DeclarationExpression(typeof(JsonElement), \"itemsArray\", out var itemsArrayVariable, isOut: true)]));\n\n            // Parse items\n            var foreachItems = new ForeachStatement(\"item\", itemsArrayVariable.Invoke(\"EnumerateArray\").As<IEnumerable<KeyValuePair<string, object>>>(), out var itemVariable);\n            //var foreachItems = new ForEachStatement(\"item\", itemsArrayVariable.Invoke(\"EnumerateArray\"), out var itemVarialble);\n            foreachItems.Add(itemsVariable.Invoke(\"Add\", [Static<BinaryData>().Invoke(\"FromString\", [itemVariable.Invoke(\"ToString\")])]).Terminate());\n\n            tryGetItems.Add(foreachItems);\n            doWhileStatement.Add(tryGetItems);\n\n            // Extract next link\n            if (_nextPageLocation == InputResponseLocation.Body && _nextLinkPropertyName != null)\n            {\n                doWhileStatement.Add(nextLinkVariable.Assign(new BinaryOperatorExpression(\":\",\n                    new BinaryOperatorExpression(\"?\",\n                    rootVariable.Invoke(\"TryGetProperty\", [Literal(_nextLinkPropertyName), new DeclarationExpression(typeof(JsonElement), \"value\", out var nextLinkValue, isOut: true)]),\n                    nextLinkValue.Invoke(\"GetString\")), Null)).Terminate());\n            }\n            else if (_nextPageLocation == InputResponseLocation.Header && _nextLinkPropertyName != null)\n            {\n                doWhileStatement.Add(nextLinkVariable.Assign(new BinaryOperatorExpression(\":\",\n                    new BinaryOperatorExpression(\"?\",\n                        responseVariable.Property(\"Headers\").Invoke(\"TryGetValue\",[Literal(_nextLinkPropertyName), new DeclarationExpression(typeof(string), \"value\", out var nextLinkHeader, isOut: true)]).As<bool>(),nextLinkHeader),\n                        Null)).Terminate());\n            }\n\n            // Create and yield the page\n            doWhileStatement.Add(new YieldReturnStatement(\n                Static(new CSharpType(typeof(Page<>), [_itemModelType]))\n                    .Invoke(\"FromValues\", [itemsVariable, nextLinkVariable, responseVariable])));\n\n            return doWhileStatement;\n        }\n\n        private ValueExpression BuildGetNextLinkForProtocol(VariableExpression nextLinkVariable, VariableExpression rootVariable, VariableExpression responseVariable)\n        {\n            if (_nextLinkPropertyName is null)\n            {\n                return Null;\n            }\n\n            switch (_nextPageLocation)\n            {\n                case InputResponseLocation.Body:\n                    return new BinaryOperatorExpression(\":\",\n                    new BinaryOperatorExpression(\"?\",\n                    rootVariable.Invoke(\"TryGetProperty\", [Literal(_nextLinkPropertyName), new DeclarationExpression(typeof(JsonElement), \"value\", out var nextLinkValue, isOut: true)]),\n                    nextLinkValue.Invoke(\"GetString\")), Null);\n                case InputResponseLocation.Header:\n                    return new BinaryOperatorExpression(\":\",\n                        new BinaryOperatorExpression(\"?\",\n                            responseVariable.Property(\"Headers\").Invoke(\"TryGetValue\", [Literal(_nextLinkPropertyName), new DeclarationExpression(typeof(string), \"value\", out var nextLinkHeader, isOut: true)]).As<bool>(), nextLinkHeader),\n                            Null);\n                default:\n                    return Null;\n            }\n        }\n\n        private DoWhileStatement BuildDoWhileStatementForConvenience(VariableExpression nextLinkVariable)\n        {\n            var doWhileStatement = new DoWhileStatement(Not(Static<string>().Invoke(\"IsNullOrEmpty\", [nextLinkVariable])));\n            doWhileStatement.Add(Declare(\"response\", new CSharpType(typeof(Response), isNullable: true), This.Invoke(_getNextResponseMethodName, [PageSizeHintParameter, nextLinkVariable], _isAsync), out var responseVariable));\n            doWhileStatement.Add(new IfStatement(responseVariable.Is(Null)) { new YieldBreakStatement() });\n            doWhileStatement.Add(Declare(\"items\", _responseType, responseVariable.CastTo(_responseType), out var itemsVariable));\n            doWhileStatement.Add(nextLinkVariable.Assign(_nextLinkPropertyName is null ? Null : BuildGetNextLinkMethodBodyForConvenience(itemsVariable, responseVariable).Invoke(\"ToString\")).Terminate());\n            doWhileStatement.Add(new YieldReturnStatement(Static(new CSharpType(typeof(Page<>), [_itemModelType])).Invoke(\"FromValues\", [itemsVariable.Property(_itemsPropertyName).CastTo(new CSharpType(typeof(IReadOnlyList<>), _itemModelType))/*.Invoke(\"AsReadOnly\")*/, nextLinkVariable, responseVariable])));",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2095888075",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50017,
        "pr_file": "eng/packages/http-client-csharp/generator/Azure.Generator/src/Providers/CollectionResultDefinition.cs",
        "discussion_id": "2095888075",
        "commented_code": "@@ -53,23 +132,250 @@ protected override CSharpType[] BuildImplements() =>\n                 ? [new CSharpType(typeof(AsyncPageable<>), _itemModelType)]\n                 : [new CSharpType(typeof(Pageable<>), _itemModelType)];\n \n-        protected override MethodProvider[] BuildMethods()\n+        protected override MethodProvider[] BuildMethods() => [BuildAsPagesMethod(), BuildGetNextResponseMethod(), BuildGetResponseMethod()];\n+\n+        private MethodProvider BuildAsPagesMethod()\n         {\n-            return new[]\n+            var signature = new MethodSignature(\n+                \"AsPages\",\n+                $\"Gets the pages of {Name} as an enumerable collection.\",\n+                _isAsync\n+                    ? MethodSignatureModifiers.Async | MethodSignatureModifiers.Public | MethodSignatureModifiers.Override\n+                    : MethodSignatureModifiers.Public | MethodSignatureModifiers.Override,\n+                _isAsync ?\n+                    new CSharpType(typeof(IAsyncEnumerable<>), new CSharpType(typeof(Page<>), _itemModelType)) :\n+                    new CSharpType(typeof(IEnumerable<>), new CSharpType(typeof(Page<>), _itemModelType)),\n+                $\"The pages of {Name} as an enumerable collection.\",\n+                [NextLinkParameter, PageSizeHintParameter]);\n+\n+            if (!IsProtocolMethod())\n             {\n-                new MethodProvider(\n-                    new MethodSignature(\n-                    \"AsPages\",\n-                    $\"Gets the pages of {Name} as an enumerable collection.\",\n-                    MethodSignatureModifiers.Public | MethodSignatureModifiers.Override,\n-                    _isAsync ?\n-                        new CSharpType(typeof(IAsyncEnumerable<>), new CSharpType(typeof(Page<>), _itemModelType)) :\n-                        new CSharpType(typeof(IEnumerable<>), new CSharpType(typeof(Page<>), _itemModelType)),\n-                    $\"The pages of {Name} as an enumerable collection.\",\n-                    [ContinuationTokenParameter, PageSizeHintParameter]),\n-                    ThrowExpression(Null),\n-                    this)\n+                // Convenience method\n+                return new MethodProvider(signature, new MethodBodyStatement[]\n+                {\n+                    Declare(\"nextLink\", new CSharpType(typeof(string), isNullable: true), NextLinkParameter, out var nextLinkVariableForConvenience),\n+                    BuildDoWhileStatementForConvenience(nextLinkVariableForConvenience)\n+                }, this);\n+            }\n+\n+            // Protocol method\n+            return new MethodProvider(signature, new MethodBodyStatement[]\n+                {\n+                    Declare(\"nextLink\", new CSharpType(typeof(string), isNullable: true), NextLinkParameter, out var nextLinkVariable),\n+                    BuildDoWhileStatementForProtocol(nextLinkVariable)\n+                }, this);\n+        }\n+\n+        private DoWhileStatement BuildDoWhileStatementForProtocol(VariableExpression nextLinkVariable)\n+        {\n+            var doWhileStatement = new DoWhileStatement(Not(Static<string>().Invoke(\"IsNullOrEmpty\", [nextLinkVariable])));\n+\n+            // Get the response\n+            doWhileStatement.Add(Declare(\"response\", new CSharpType(typeof(Response), isNullable: true),\n+                This.Invoke(_getNextResponseMethodName, [PageSizeHintParameter, nextLinkVariable], _isAsync),\n+                out var responseVariable));\n+\n+            // Early exit if response is null\n+            doWhileStatement.Add(new IfStatement(responseVariable.Is(Null)) { new YieldBreakStatement() });\n+\n+            // Parse response content as JsonDocument\n+            doWhileStatement.Add(UsingDeclare(\"jsonDoc\", typeof(JsonDocument),\n+                Static<JsonDocument>().Invoke(\"Parse\", [responseVariable.Property(\"Content\").Invoke(\"ToString\")]),\n+                out var jsonDocVariable));\n+\n+            // Get root element\n+            doWhileStatement.Add(Declare(\"root\", typeof(JsonElement),\n+                jsonDocVariable.Property(\"RootElement\"), out var rootVariable));\n+\n+            // Extract items array\n+            doWhileStatement.Add(Declare(\"items\", new CSharpType(typeof(List<>), _itemModelType),\n+                New.Instance(new CSharpType(typeof(List<>), _itemModelType)), out var itemsVariable));\n+\n+            // Get items array from response\n+            var tryGetItems = new IfStatement(rootVariable.Invoke(\"TryGetProperty\", [Literal(_itemsPropertyName), new DeclarationExpression(typeof(JsonElement), \"itemsArray\", out var itemsArrayVariable, isOut: true)]));\n+\n+            // Parse items\n+            var foreachItems = new ForeachStatement(\"item\", itemsArrayVariable.Invoke(\"EnumerateArray\").As<IEnumerable<KeyValuePair<string, object>>>(), out var itemVariable);\n+            //var foreachItems = new ForEachStatement(\"item\", itemsArrayVariable.Invoke(\"EnumerateArray\"), out var itemVarialble);\n+            foreachItems.Add(itemsVariable.Invoke(\"Add\", [Static<BinaryData>().Invoke(\"FromString\", [itemVariable.Invoke(\"ToString\")])]).Terminate());\n+\n+            tryGetItems.Add(foreachItems);\n+            doWhileStatement.Add(tryGetItems);\n+\n+            // Extract next link\n+            if (_nextPageLocation == InputResponseLocation.Body && _nextLinkPropertyName != null)\n+            {\n+                doWhileStatement.Add(nextLinkVariable.Assign(new BinaryOperatorExpression(\":\",\n+                    new BinaryOperatorExpression(\"?\",\n+                    rootVariable.Invoke(\"TryGetProperty\", [Literal(_nextLinkPropertyName), new DeclarationExpression(typeof(JsonElement), \"value\", out var nextLinkValue, isOut: true)]),\n+                    nextLinkValue.Invoke(\"GetString\")), Null)).Terminate());\n+            }\n+            else if (_nextPageLocation == InputResponseLocation.Header && _nextLinkPropertyName != null)\n+            {\n+                doWhileStatement.Add(nextLinkVariable.Assign(new BinaryOperatorExpression(\":\",\n+                    new BinaryOperatorExpression(\"?\",\n+                        responseVariable.Property(\"Headers\").Invoke(\"TryGetValue\",[Literal(_nextLinkPropertyName), new DeclarationExpression(typeof(string), \"value\", out var nextLinkHeader, isOut: true)]).As<bool>(),nextLinkHeader),\n+                        Null)).Terminate());\n+            }\n+\n+            // Create and yield the page\n+            doWhileStatement.Add(new YieldReturnStatement(\n+                Static(new CSharpType(typeof(Page<>), [_itemModelType]))\n+                    .Invoke(\"FromValues\", [itemsVariable, nextLinkVariable, responseVariable])));\n+\n+            return doWhileStatement;\n+        }\n+\n+        private ValueExpression BuildGetNextLinkForProtocol(VariableExpression nextLinkVariable, VariableExpression rootVariable, VariableExpression responseVariable)\n+        {\n+            if (_nextLinkPropertyName is null)\n+            {\n+                return Null;\n+            }\n+\n+            switch (_nextPageLocation)\n+            {\n+                case InputResponseLocation.Body:\n+                    return new BinaryOperatorExpression(\":\",\n+                    new BinaryOperatorExpression(\"?\",\n+                    rootVariable.Invoke(\"TryGetProperty\", [Literal(_nextLinkPropertyName), new DeclarationExpression(typeof(JsonElement), \"value\", out var nextLinkValue, isOut: true)]),\n+                    nextLinkValue.Invoke(\"GetString\")), Null);\n+                case InputResponseLocation.Header:\n+                    return new BinaryOperatorExpression(\":\",\n+                        new BinaryOperatorExpression(\"?\",\n+                            responseVariable.Property(\"Headers\").Invoke(\"TryGetValue\", [Literal(_nextLinkPropertyName), new DeclarationExpression(typeof(string), \"value\", out var nextLinkHeader, isOut: true)]).As<bool>(), nextLinkHeader),\n+                            Null);\n+                default:\n+                    return Null;\n+            }\n+        }\n+\n+        private DoWhileStatement BuildDoWhileStatementForConvenience(VariableExpression nextLinkVariable)\n+        {\n+            var doWhileStatement = new DoWhileStatement(Not(Static<string>().Invoke(\"IsNullOrEmpty\", [nextLinkVariable])));\n+            doWhileStatement.Add(Declare(\"response\", new CSharpType(typeof(Response), isNullable: true), This.Invoke(_getNextResponseMethodName, [PageSizeHintParameter, nextLinkVariable], _isAsync), out var responseVariable));\n+            doWhileStatement.Add(new IfStatement(responseVariable.Is(Null)) { new YieldBreakStatement() });\n+            doWhileStatement.Add(Declare(\"items\", _responseType, responseVariable.CastTo(_responseType), out var itemsVariable));\n+            doWhileStatement.Add(nextLinkVariable.Assign(_nextLinkPropertyName is null ? Null : BuildGetNextLinkMethodBodyForConvenience(itemsVariable, responseVariable).Invoke(\"ToString\")).Terminate());\n+            doWhileStatement.Add(new YieldReturnStatement(Static(new CSharpType(typeof(Page<>), [_itemModelType])).Invoke(\"FromValues\", [itemsVariable.Property(_itemsPropertyName).CastTo(new CSharpType(typeof(IReadOnlyList<>), _itemModelType))/*.Invoke(\"AsReadOnly\")*/, nextLinkVariable, responseVariable])));",
        "comment_created_at": "2025-05-19T14:47:38+00:00",
        "comment_author": "JoshLove-msft",
        "comment_body": "nit: remove commented code",
        "pr_file_module": null
      }
    ]
  }
]
