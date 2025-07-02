---
title: Specific exceptions for clarity
description: Use specific exception types with meaningful error messages rather than
  generic exceptions to improve error handling, debugging, and API usability. This
  allows callers to distinguish between different error conditions and respond appropriately.
repository: Azure/azure-sdk-for-net
label: Error Handling
language: C#
comments_count: 5
repository_stars: 5809
---

Use specific exception types with meaningful error messages rather than generic exceptions to improve error handling, debugging, and API usability. This allows callers to distinguish between different error conditions and respond appropriately.

Instead of:
```csharp
if (string.IsNullOrEmpty(serviceEndpoint))
    throw new Exception("Invalid service endpoint");
```

Prefer:
```csharp
if (string.IsNullOrEmpty(serviceEndpoint))
    throw new ArgumentException("The service endpoint must be a valid URL", nameof(serviceEndpoint));
```

Key practices:
1. Match exception types to error conditions: Use `ArgumentException` for invalid arguments, `InvalidOperationException` for improper state, and `NotSupportedException` instead of `NotImplementedException` for unsupported operations.

2. Include actionable details in error messages: Specify what went wrong and how to fix it.

3. Use reliable error detection: Check specific exception properties or error codes rather than string matching:
```csharp
// Instead of: 
catch (Exception ex) when (ex.Message.Contains("timed out"))

// Prefer:
catch (RequestFailedException ex) when (ex.Status == 408)
```

4. Validate assumptions explicitly: Check for null or invalid values before operations that assume they exist.
```csharp
// Instead of:
arguments.Add(methodParameters.Single(p => p.Name == parameter.Name));

// Prefer:
var matchingParameter = methodParameters.SingleOrDefault(p => p.Name == parameter.Name);
if (matchingParameter == null)
{
    throw new InvalidOperationException($"No matching parameter found for '{parameter.Name}' in methodParameters.");
}
arguments.Add(matchingParameter);
```


[
  {
    "discussion_id": "2174208183",
    "pr_number": 50936,
    "pr_file": "eng/packages/http-client-csharp-mgmt/generator/Azure.Generator.Management/src/Providers/ResourceClientProvider.cs",
    "created_at": "2025-06-30T04:41:22+00:00",
    "commented_code": "}\n                else if (parameter.Type.Equals(typeof(RequestContent)))\n                {\n                    // If convenience method is provided, find the resource parameter from it\n                    if (convenienceMethod != null)\n                    if (methodParameters.Count > 0)\n                    {\n                        var resource = convenienceMethod.Signature.Parameters\n                            .Single(p => p.Type.Equals(ResourceData.Type) || p.Type.Equals(typeof(RequestContent)));\n                        // Find the content parameter in the method parameters\n                        // TODO: need to revisit the filter here\n                        var contentInputParameter = operation.Parameters.First(p => !ImplicitParameterNames.Contains(p.Name) && p.Kind == InputParameterKind.Method && p.Type is not InputPrimitiveType);\n                        var resource = methodParameters.Single(p => p.Name == \"data\" || p.Name == contentInputParameter.Name);\n                        arguments.Add(resource);\n                    }\n                    else\n                    {\n                        // Otherwise just add the parameter as-is\n                        arguments.Add(parameter);\n                    }\n                }\n                else if (parameter.Type.Equals(typeof(RequestContext)))\n                {\n                    arguments.Add(contextVariable);\n                }\n                else\n                {\n                    arguments.Add(parameter);\n                    arguments.Add(methodParameters.Single(p => p.Name == parameter.Name));",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2174208183",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50936,
        "pr_file": "eng/packages/http-client-csharp-mgmt/generator/Azure.Generator.Management/src/Providers/ResourceClientProvider.cs",
        "discussion_id": "2174208183",
        "commented_code": "@@ -364,26 +373,22 @@ public ValueExpression[] PopulateArguments(\n                 }\n                 else if (parameter.Type.Equals(typeof(RequestContent)))\n                 {\n-                    // If convenience method is provided, find the resource parameter from it\n-                    if (convenienceMethod != null)\n+                    if (methodParameters.Count > 0)\n                     {\n-                        var resource = convenienceMethod.Signature.Parameters\n-                            .Single(p => p.Type.Equals(ResourceData.Type) || p.Type.Equals(typeof(RequestContent)));\n+                        // Find the content parameter in the method parameters\n+                        // TODO: need to revisit the filter here\n+                        var contentInputParameter = operation.Parameters.First(p => !ImplicitParameterNames.Contains(p.Name) && p.Kind == InputParameterKind.Method && p.Type is not InputPrimitiveType);\n+                        var resource = methodParameters.Single(p => p.Name == \"data\" || p.Name == contentInputParameter.Name);\n                         arguments.Add(resource);\n                     }\n-                    else\n-                    {\n-                        // Otherwise just add the parameter as-is\n-                        arguments.Add(parameter);\n-                    }\n                 }\n                 else if (parameter.Type.Equals(typeof(RequestContext)))\n                 {\n                     arguments.Add(contextVariable);\n                 }\n                 else\n                 {\n-                    arguments.Add(parameter);\n+                    arguments.Add(methodParameters.Single(p => p.Name == parameter.Name));",
        "comment_created_at": "2025-06-30T04:41:22+00:00",
        "comment_author": "Copilot",
        "comment_body": "[nitpick] The use of Single() assumes that exactly one matching parameter exists. It may be safer to validate the existence of a match or provide a clearer error message if the match is not found.\n```suggestion\n                    var matchingParameter = methodParameters.SingleOrDefault(p => p.Name == parameter.Name);\n                    if (matchingParameter == null)\n                    {\n                        throw new InvalidOperationException($\"No matching parameter found for '{parameter.Name}' in methodParameters.\");\n                    }\n                    arguments.Add(matchingParameter);\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2058868488",
    "pr_number": 49293,
    "pr_file": "sdk/ai/Azure.AI.Projects/src/Custom/Agent/ToolCallsResolver.cs",
    "created_at": "2025-04-24T16:53:55+00:00",
    "commented_code": "\ufeff// Copyright (c) Microsoft Corporation. All rights reserved.\n// Licensed under the MIT License.\nusing System;\nusing System.Collections;\nusing System.Collections.Generic;\nusing System.Reflection;\nusing System.Text.Json;\nusing System.Xml.Linq;\n\nnamespace Azure.AI.Projects.Custom.Agent\n{\n    /// <summary>\n    /// ToolCallsResolver is used to resolve tool calls in the streaming API.\n    /// </summary>\n    public class ToolCallsResolver\n    {\n        private readonly Dictionary<string, Delegate> _delegates = new();\n\n        internal ToolCallsResolver(Dictionary<string, Delegate> delegates)\n        {\n            _delegates = delegates;\n        }\n\n        /// <summary>\n        /// Indicates whether auto tool calls are enabled.\n        /// </summary>\n        internal bool EnableAutoToolCalls => _delegates.Count > 0;\n\n        /// <summary>\n        /// Resolves the tool call by invoking the delegate associated with the function name.\n        /// It casts the function arguments to the appropriate types based on the delegate's parameters.\n        /// without knowing the answer.\n        /// </summary>\n        internal ToolOutput GetResolvedToolOutput(string functionName, string toolCallId, string functionArguments)\n        {\n            if (!_delegates.TryGetValue(functionName, out var func))\n            {\n                string error = $\"Function {functionName} not found.\";\n                throw new MissingMethodException(error);",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2058868488",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 49293,
        "pr_file": "sdk/ai/Azure.AI.Projects/src/Custom/Agent/ToolCallsResolver.cs",
        "discussion_id": "2058868488",
        "commented_code": "@@ -0,0 +1,214 @@\n+\ufeff// Copyright (c) Microsoft Corporation. All rights reserved.\n+// Licensed under the MIT License.\n+using System;\n+using System.Collections;\n+using System.Collections.Generic;\n+using System.Reflection;\n+using System.Text.Json;\n+using System.Xml.Linq;\n+\n+namespace Azure.AI.Projects.Custom.Agent\n+{\n+    /// <summary>\n+    /// ToolCallsResolver is used to resolve tool calls in the streaming API.\n+    /// </summary>\n+    public class ToolCallsResolver\n+    {\n+        private readonly Dictionary<string, Delegate> _delegates = new();\n+\n+        internal ToolCallsResolver(Dictionary<string, Delegate> delegates)\n+        {\n+            _delegates = delegates;\n+        }\n+\n+        /// <summary>\n+        /// Indicates whether auto tool calls are enabled.\n+        /// </summary>\n+        internal bool EnableAutoToolCalls => _delegates.Count > 0;\n+\n+        /// <summary>\n+        /// Resolves the tool call by invoking the delegate associated with the function name.\n+        /// It casts the function arguments to the appropriate types based on the delegate's parameters.\n+        /// without knowing the answer.\n+        /// </summary>\n+        internal ToolOutput GetResolvedToolOutput(string functionName, string toolCallId, string functionArguments)\n+        {\n+            if (!_delegates.TryGetValue(functionName, out var func))\n+            {\n+                string error = $\"Function {functionName} not found.\";\n+                throw new MissingMethodException(error);",
        "comment_created_at": "2025-04-24T16:53:55+00:00",
        "comment_author": "KrzysztofCwalina",
        "comment_body": "will it be retried?",
        "pr_file_module": null
      },
      {
        "comment_id": "2058998727",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 49293,
        "pr_file": "sdk/ai/Azure.AI.Projects/src/Custom/Agent/ToolCallsResolver.cs",
        "discussion_id": "2058868488",
        "commented_code": "@@ -0,0 +1,214 @@\n+\ufeff// Copyright (c) Microsoft Corporation. All rights reserved.\n+// Licensed under the MIT License.\n+using System;\n+using System.Collections;\n+using System.Collections.Generic;\n+using System.Reflection;\n+using System.Text.Json;\n+using System.Xml.Linq;\n+\n+namespace Azure.AI.Projects.Custom.Agent\n+{\n+    /// <summary>\n+    /// ToolCallsResolver is used to resolve tool calls in the streaming API.\n+    /// </summary>\n+    public class ToolCallsResolver\n+    {\n+        private readonly Dictionary<string, Delegate> _delegates = new();\n+\n+        internal ToolCallsResolver(Dictionary<string, Delegate> delegates)\n+        {\n+            _delegates = delegates;\n+        }\n+\n+        /// <summary>\n+        /// Indicates whether auto tool calls are enabled.\n+        /// </summary>\n+        internal bool EnableAutoToolCalls => _delegates.Count > 0;\n+\n+        /// <summary>\n+        /// Resolves the tool call by invoking the delegate associated with the function name.\n+        /// It casts the function arguments to the appropriate types based on the delegate's parameters.\n+        /// without knowing the answer.\n+        /// </summary>\n+        internal ToolOutput GetResolvedToolOutput(string functionName, string toolCallId, string functionArguments)\n+        {\n+            if (!_delegates.TryGetValue(functionName, out var func))\n+            {\n+                string error = $\"Function {functionName} not found.\";\n+                throw new MissingMethodException(error);",
        "comment_created_at": "2025-04-24T18:18:40+00:00",
        "comment_author": "howieleung",
        "comment_body": "Yes.   I did lot of experiments.   Depends on the question, if we submit this error to the model, the model might try to figure out the answer with its knowledge or memory.   It might raise the same function call again.   Or it might give up and say it doesn't have the information.",
        "pr_file_module": null
      },
      {
        "comment_id": "2059171479",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 49293,
        "pr_file": "sdk/ai/Azure.AI.Projects/src/Custom/Agent/ToolCallsResolver.cs",
        "discussion_id": "2058868488",
        "commented_code": "@@ -0,0 +1,214 @@\n+\ufeff// Copyright (c) Microsoft Corporation. All rights reserved.\n+// Licensed under the MIT License.\n+using System;\n+using System.Collections;\n+using System.Collections.Generic;\n+using System.Reflection;\n+using System.Text.Json;\n+using System.Xml.Linq;\n+\n+namespace Azure.AI.Projects.Custom.Agent\n+{\n+    /// <summary>\n+    /// ToolCallsResolver is used to resolve tool calls in the streaming API.\n+    /// </summary>\n+    public class ToolCallsResolver\n+    {\n+        private readonly Dictionary<string, Delegate> _delegates = new();\n+\n+        internal ToolCallsResolver(Dictionary<string, Delegate> delegates)\n+        {\n+            _delegates = delegates;\n+        }\n+\n+        /// <summary>\n+        /// Indicates whether auto tool calls are enabled.\n+        /// </summary>\n+        internal bool EnableAutoToolCalls => _delegates.Count > 0;\n+\n+        /// <summary>\n+        /// Resolves the tool call by invoking the delegate associated with the function name.\n+        /// It casts the function arguments to the appropriate types based on the delegate's parameters.\n+        /// without knowing the answer.\n+        /// </summary>\n+        internal ToolOutput GetResolvedToolOutput(string functionName, string toolCallId, string functionArguments)\n+        {\n+            if (!_delegates.TryGetValue(functionName, out var func))\n+            {\n+                string error = $\"Function {functionName} not found.\";\n+                throw new MissingMethodException(error);",
        "comment_created_at": "2025-04-24T20:24:59+00:00",
        "comment_author": "KrzysztofCwalina",
        "comment_body": "Don't we need two exceptions for this to work well. If the model passes a wrong argument, it might indeed retry successfully. But why would the modle give us a wrong function name? We gave it an explicit list of functions that we support",
        "pr_file_module": null
      },
      {
        "comment_id": "2060960574",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 49293,
        "pr_file": "sdk/ai/Azure.AI.Projects/src/Custom/Agent/ToolCallsResolver.cs",
        "discussion_id": "2058868488",
        "commented_code": "@@ -0,0 +1,214 @@\n+\ufeff// Copyright (c) Microsoft Corporation. All rights reserved.\n+// Licensed under the MIT License.\n+using System;\n+using System.Collections;\n+using System.Collections.Generic;\n+using System.Reflection;\n+using System.Text.Json;\n+using System.Xml.Linq;\n+\n+namespace Azure.AI.Projects.Custom.Agent\n+{\n+    /// <summary>\n+    /// ToolCallsResolver is used to resolve tool calls in the streaming API.\n+    /// </summary>\n+    public class ToolCallsResolver\n+    {\n+        private readonly Dictionary<string, Delegate> _delegates = new();\n+\n+        internal ToolCallsResolver(Dictionary<string, Delegate> delegates)\n+        {\n+            _delegates = delegates;\n+        }\n+\n+        /// <summary>\n+        /// Indicates whether auto tool calls are enabled.\n+        /// </summary>\n+        internal bool EnableAutoToolCalls => _delegates.Count > 0;\n+\n+        /// <summary>\n+        /// Resolves the tool call by invoking the delegate associated with the function name.\n+        /// It casts the function arguments to the appropriate types based on the delegate's parameters.\n+        /// without knowing the answer.\n+        /// </summary>\n+        internal ToolOutput GetResolvedToolOutput(string functionName, string toolCallId, string functionArguments)\n+        {\n+            if (!_delegates.TryGetValue(functionName, out var func))\n+            {\n+                string error = $\"Function {functionName} not found.\";\n+                throw new MissingMethodException(error);",
        "comment_created_at": "2025-04-25T22:23:57+00:00",
        "comment_author": "howieleung",
        "comment_body": "It is possible that the agent is created by Foundary UI or other application.   In their C# app, they call getAgent and attempt to stream.   If this agent has a function tool that isn't in the list of delegate, we want to raise exception.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2156708743",
    "pr_number": 50718,
    "pr_file": "sdk/loadtestservice/Azure.Developer.Playwright/src/Utility/ClientUtilities.cs",
    "created_at": "2025-06-19T10:47:33+00:00",
    "commented_code": "if (string.IsNullOrEmpty(authToken))\n                throw new Exception(Constants.s_no_auth_error);\n            JsonWebToken jsonWebToken = _jsonWebTokenHandler!.ReadJsonWebToken(authToken) ?? throw new Exception(Constants.s_invalid_mpt_pat_error);\n            var tokenWorkspaceId = jsonWebToken.Claims.FirstOrDefault(c => c.Type == \"aid\")?.Value;\n            Match match = Regex.Match(serviceEndpoint, @\"wss://(?<region>[\\w-]+)\\.api\\.(?<domain>playwright(?:-test|-int)?\\.io|playwright\\.microsoft\\.com)/accounts/(?<workspaceId>[\\w-]+)/\");\n            var tokenWorkspaceId = jsonWebToken.Claims.FirstOrDefault(c => c.Type == \"pwid\")?.Value;\n            Match match = Regex.Match(serviceEndpoint, @\"wss://(?<region>[\\w-]+)\\.api\\.(?<domain>playwright(?:-test|-int)?\\.io|playwright\\.microsoft\\.com)/playwrightworkspaces/(?<workspaceId>[\\w-]+)/\");\n            if (!match.Success)\n                throw new Exception(Constants.s_invalid_service_endpoint_error_message);",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2156708743",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50718,
        "pr_file": "sdk/loadtestservice/Azure.Developer.Playwright/src/Utility/ClientUtilities.cs",
        "discussion_id": "2156708743",
        "commented_code": "@@ -60,8 +60,8 @@ internal void ValidateMptPAT(string? authToken, string serviceEndpoint)\n             if (string.IsNullOrEmpty(authToken))\n                 throw new Exception(Constants.s_no_auth_error);\n             JsonWebToken jsonWebToken = _jsonWebTokenHandler!.ReadJsonWebToken(authToken) ?? throw new Exception(Constants.s_invalid_mpt_pat_error);\n-            var tokenWorkspaceId = jsonWebToken.Claims.FirstOrDefault(c => c.Type == \"aid\")?.Value;\n-            Match match = Regex.Match(serviceEndpoint, @\"wss://(?<region>[\\w-]+)\\.api\\.(?<domain>playwright(?:-test|-int)?\\.io|playwright\\.microsoft\\.com)/accounts/(?<workspaceId>[\\w-]+)/\");\n+            var tokenWorkspaceId = jsonWebToken.Claims.FirstOrDefault(c => c.Type == \"pwid\")?.Value;\n+            Match match = Regex.Match(serviceEndpoint, @\"wss://(?<region>[\\w-]+)\\.api\\.(?<domain>playwright(?:-test|-int)?\\.io|playwright\\.microsoft\\.com)/playwrightworkspaces/(?<workspaceId>[\\w-]+)/\");\n             if (!match.Success)\n                 throw new Exception(Constants.s_invalid_service_endpoint_error_message);",
        "comment_created_at": "2025-06-19T10:47:33+00:00",
        "comment_author": "Copilot",
        "comment_body": "Throwing a generic Exception makes it harder for callers to distinguish error types; consider using a more specific exception (e.g., ArgumentException) for an invalid service endpoint.\n```suggestion\n                throw new ArgumentException(Constants.s_invalid_service_endpoint_error_message);\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2128234472",
    "pr_number": 50447,
    "pr_file": "sdk/core/Azure.Core.Expressions.DataFactory/src/DataFactoryElementJsonConverter.cs",
    "created_at": "2025-06-05T08:15:12+00:00",
    "commented_code": "return element != null;\n        }\n\n        public override void Write(Utf8JsonWriter writer, object? value, JsonSerializerOptions options)\n        {\n            throw new NotImplementedException();",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2128234472",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50447,
        "pr_file": "sdk/core/Azure.Core.Expressions.DataFactory/src/DataFactoryElementJsonConverter.cs",
        "discussion_id": "2128234472",
        "commented_code": "@@ -399,5 +222,10 @@ private static bool TryGetNonLiteral<T>(JsonElement json, out DataFactoryElement\n \n             return element != null;\n         }\n+\n+        public override void Write(Utf8JsonWriter writer, object? value, JsonSerializerOptions options)\n+        {\n+            throw new NotImplementedException();",
        "comment_created_at": "2025-06-05T08:15:12+00:00",
        "comment_author": "Copilot",
        "comment_body": "The Write override now throws a NotImplementedException, which may cause runtime errors if this converter is used unexpectedly. Consider providing an implementation or documenting that this converter should not be invoked in AOT scenarios.\n```suggestion\n        /// <summary>\n        /// Serialization is not supported for DataFactoryElementJsonConverter.\n        /// </summary>\n        /// <exception cref=\"NotSupportedException\">Thrown when attempting to serialize an object.</exception>\n        public override void Write(Utf8JsonWriter writer, object? value, JsonSerializerOptions options)\n        {\n            throw new NotSupportedException(\"Serialization is not supported for DataFactoryElementJsonConverter.\");\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2130443163",
    "pr_number": 50458,
    "pr_file": "sdk/identity/Azure.Identity/src/ManagedIdentityClient.cs",
    "created_at": "2025-06-05T21:22:48+00:00",
    "commented_code": "return await tokenExchangeManagedIdentitySource.AuthenticateAsync(async, context, cancellationToken).ConfigureAwait(false);\n            }\n\n            // The default case is to use the MSAL implementation, which does no probing of the IMDS endpoint.\n            result = async ?\n                await _msalManagedIdentityClient.AcquireTokenForManagedIdentityAsync(context, cancellationToken).ConfigureAwait(false) :\n                _msalManagedIdentityClient.AcquireTokenForManagedIdentity(context, cancellationToken);\n            try\n            {\n                // The default case is to use the MSAL implementation, which does no probing of the IMDS endpoint.\n                result = async ?\n                    await _msalManagedIdentityClient.AcquireTokenForManagedIdentityAsync(context, cancellationToken).ConfigureAwait(false) :\n                    _msalManagedIdentityClient.AcquireTokenForManagedIdentity(context, cancellationToken);\n            }\n            // If the IMDS endpoint is not available, we will throw a CredentialUnavailableException.\n            catch (MsalServiceException ex) when (HasInnerExceptionMatching(ex, e => e is RequestFailedException && e.Message.Contains(\"timed out\")))",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2130443163",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50458,
        "pr_file": "sdk/identity/Azure.Identity/src/ManagedIdentityClient.cs",
        "discussion_id": "2130443163",
        "commented_code": "@@ -87,10 +87,19 @@ public async ValueTask<AccessToken> AuthenticateAsync(bool async, TokenRequestCo\n                 return await tokenExchangeManagedIdentitySource.AuthenticateAsync(async, context, cancellationToken).ConfigureAwait(false);\n             }\n \n-            // The default case is to use the MSAL implementation, which does no probing of the IMDS endpoint.\n-            result = async ?\n-                await _msalManagedIdentityClient.AcquireTokenForManagedIdentityAsync(context, cancellationToken).ConfigureAwait(false) :\n-                _msalManagedIdentityClient.AcquireTokenForManagedIdentity(context, cancellationToken);\n+            try\n+            {\n+                // The default case is to use the MSAL implementation, which does no probing of the IMDS endpoint.\n+                result = async ?\n+                    await _msalManagedIdentityClient.AcquireTokenForManagedIdentityAsync(context, cancellationToken).ConfigureAwait(false) :\n+                    _msalManagedIdentityClient.AcquireTokenForManagedIdentity(context, cancellationToken);\n+            }\n+            // If the IMDS endpoint is not available, we will throw a CredentialUnavailableException.\n+            catch (MsalServiceException ex) when (HasInnerExceptionMatching(ex, e => e is RequestFailedException && e.Message.Contains(\"timed out\")))",
        "comment_created_at": "2025-06-05T21:22:48+00:00",
        "comment_author": "Copilot",
        "comment_body": "[nitpick] Relying on a string match for \"timed out\" in the exception message is brittle. Consider checking a specific exception property or error code on RequestFailedException instead of matching the message text.\n```suggestion\n            catch (MsalServiceException ex) when (HasInnerExceptionMatching(ex, e => e is RequestFailedException requestFailedEx && requestFailedEx.Status == 408))\n```",
        "pr_file_module": null
      }
    ]
  }
]
