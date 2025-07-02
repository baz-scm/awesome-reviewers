---
title: Prevent null references
description: "Use defensive coding practices to prevent null reference exceptions\
  \ by properly handling potentially null values throughout your code. \n\n1. **Properly\
  \ initialize objects** instead of using default values when instantiation is needed:"
repository: dotnet/runtime
label: Null Handling
language: C#
comments_count: 5
repository_stars: 16578
---

Use defensive coding practices to prevent null reference exceptions by properly handling potentially null values throughout your code. 

1. **Properly initialize objects** instead of using default values when instantiation is needed:
```csharp
// AVOID: Using default without initialization
ArrayBuilder<ProcessInfo> processes = default; // Could cause NullReferenceException when adding items

// PREFER: Proper instantiation
ArrayBuilder<ProcessInfo> processes = new ArrayBuilder<ProcessInfo>();
```

2. **Capture and check results** of methods that might return null before using them:
```csharp
// AVOID: Potential NullReferenceException if ReadLine() returns null
while (!remoteHandle.Process.StandardOutput.ReadLine().EndsWith(message))
{
    Thread.Sleep(20);
}

// PREFER: Capture and check for null
string? line;
while ((line = remoteHandle.Process.StandardOutput.ReadLine()) != null && 
       !line.EndsWith(message))
{
    Thread.Sleep(20);
}
```

3. **Map null values** to appropriate empty structures to maintain consistent behavior:
```csharp
// AVOID: Will throw if context is null
return SignData(new ReadOnlySpan<byte>(data), destination.AsSpan(), new ReadOnlySpan<byte>(context));

// PREFER: Properly handle null context
return SignData(new ReadOnlySpan<byte>(data), destination.AsSpan(), 
    context == null ? ReadOnlySpan<byte>.Empty : new ReadOnlySpan<byte>(context));
```

4. **Use pattern matching** for more readable and concise null checks:
```csharp
// AVOID: Traditional null check with equality operator
if (setMethod == null || !setMethod.IsPublic)

// PREFER: Modern pattern matching
if (setMethod is null || !setMethod.IsPublic)
```

5. **Combine conditions** using pattern matching for cleaner code:
```csharp
// AVOID: Multiple conditions checked separately
if (changeToken is not null && changeToken is not NullChangeToken)

// PREFER: Combine related checks
if (changeToken is not (null or NullChangeToken))
```

When adding validation in public APIs, favor the built-in helpers like `ArgumentNullException.ThrowIfNull()` over custom throw helpers for better readability and standardization.


[
  {
    "discussion_id": "2009265886",
    "pr_number": 105403,
    "pr_file": "src/libraries/System.Diagnostics.Process/src/System/Diagnostics/ProcessManager.SunOS.cs",
    "created_at": "2025-03-23T21:50:39+00:00",
    "commented_code": "// Licensed to the .NET Foundation under one or more agreements.\n// The .NET Foundation licenses this file to you under the MIT license.\n\nusing System.Collections.Generic;\nusing System.Globalization;\nusing System.IO;\nusing System.Runtime.InteropServices;\n\nnamespace System.Diagnostics\n{\n    internal static partial class ProcessManager\n    {\n        /// <summary>Gets the IDs of all processes on the current machine.</summary>\n        public static int[] GetProcessIds()\n        {\n            IEnumerable<int> pids = EnumerateProcessIds();\n            return new List<int>(pids).ToArray();\n        }\n\n        /// <summary>Gets process infos for each process on the specified machine.</summary>\n        /// <param name=\"processNameFilter\">Optional process name to use as an inclusion filter.</param>\n        /// <param name=\"machineName\">The target machine.</param>\n        /// <returns>An array of process infos, one per found process.</returns>\n        public static ProcessInfo[] GetProcessInfos(string? processNameFilter, string machineName)\n        {\n            ThrowIfRemoteMachine(machineName);\n\n            // Iterate through all process IDs to load information about each process\n            IEnumerable<int> pids = EnumerateProcessIds();\n            ArrayBuilder<ProcessInfo> processes = default;",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2009265886",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 105403,
        "pr_file": "src/libraries/System.Diagnostics.Process/src/System/Diagnostics/ProcessManager.SunOS.cs",
        "discussion_id": "2009265886",
        "commented_code": "@@ -0,0 +1,244 @@\n+// Licensed to the .NET Foundation under one or more agreements.\n+// The .NET Foundation licenses this file to you under the MIT license.\n+\n+using System.Collections.Generic;\n+using System.Globalization;\n+using System.IO;\n+using System.Runtime.InteropServices;\n+\n+namespace System.Diagnostics\n+{\n+    internal static partial class ProcessManager\n+    {\n+        /// <summary>Gets the IDs of all processes on the current machine.</summary>\n+        public static int[] GetProcessIds()\n+        {\n+            IEnumerable<int> pids = EnumerateProcessIds();\n+            return new List<int>(pids).ToArray();\n+        }\n+\n+        /// <summary>Gets process infos for each process on the specified machine.</summary>\n+        /// <param name=\"processNameFilter\">Optional process name to use as an inclusion filter.</param>\n+        /// <param name=\"machineName\">The target machine.</param>\n+        /// <returns>An array of process infos, one per found process.</returns>\n+        public static ProcessInfo[] GetProcessInfos(string? processNameFilter, string machineName)\n+        {\n+            ThrowIfRemoteMachine(machineName);\n+\n+            // Iterate through all process IDs to load information about each process\n+            IEnumerable<int> pids = EnumerateProcessIds();\n+            ArrayBuilder<ProcessInfo> processes = default;",
        "comment_created_at": "2025-03-23T21:50:39+00:00",
        "comment_author": "Copilot",
        "comment_body": "Ensure that ArrayBuilder is properly instantiated instead of using the default value to prevent potential NullReferenceExceptions when adding items.\n```suggestion\n            ArrayBuilder<ProcessInfo> processes = new ArrayBuilder<ProcessInfo>();\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2178380994",
    "pr_number": 117105,
    "pr_file": "src/libraries/System.Diagnostics.Process/tests/ProcessTests.cs",
    "created_at": "2025-07-01T19:29:25+00:00",
    "commented_code": "}\n        }\n\n        [ConditionalTheory(typeof(RemoteExecutor), nameof(RemoteExecutor.IsSupported))]\n        [InlineData(PosixSignal.SIGTSTP)]\n        [InlineData(PosixSignal.SIGTTOU)]\n        [InlineData(PosixSignal.SIGTTIN)]\n        [InlineData(PosixSignal.SIGWINCH)]\n        [InlineData(PosixSignal.SIGCONT)]\n        [InlineData(PosixSignal.SIGCHLD)]\n        [InlineData(PosixSignal.SIGTERM)]\n        [InlineData(PosixSignal.SIGQUIT)]\n        [InlineData(PosixSignal.SIGINT)]\n        [InlineData(PosixSignal.SIGHUP)]\n        [InlineData((PosixSignal)3)] // SIGQUIT\n        [InlineData((PosixSignal)15)] // SIGTERM\n        public void TestCreateNewProcessGroup_HandlerReceivesExpectedSignal(PosixSignal signal)\n        {\n            const string PosixSignalRegistrationCreatedMessage = \"PosixSignalRegistration created...\";\n\n            if (OperatingSystem.IsWindows() && signal is not (PosixSignal.SIGINT or PosixSignal.SIGQUIT))\n            {\n                throw new SkipTestException(\"GenerateConsoleCtrlEvent does not support sending this signal.\");\n            }\n\n            var remoteInvokeOptions = new RemoteInvokeOptions { CheckExitCode = false };\n            remoteInvokeOptions.StartInfo.RedirectStandardOutput = true;\n            if (OperatingSystem.IsWindows())\n            {\n                remoteInvokeOptions.StartInfo.CreateNewProcessGroup = true;\n            }\n\n            using RemoteInvokeHandle remoteHandle = RemoteExecutor.Invoke(\n                (signalStr) =>\n                {\n                    PosixSignal expectedSignal = Enum.Parse<PosixSignal>(signalStr);\n                    bool receivedSignal = false;\n                    ReEnableCtrlCHandlerIfNeeded(expectedSignal);\n\n                    using PosixSignalRegistration p = PosixSignalRegistration.Create(expectedSignal, (ctx) =>\n                    {\n                        Assert.Equal(expectedSignal, ctx.Signal);\n                        receivedSignal = true;\n                        ctx.Cancel = true;\n                    });\n\n                    Console.WriteLine(PosixSignalRegistrationCreatedMessage);\n\n                    while (!receivedSignal) ;\n\n                    return 0;\n                },\n                arg: $\"{signal}\",\n                remoteInvokeOptions);\n\n            while (!remoteHandle.Process.StandardOutput.ReadLine().EndsWith(PosixSignalRegistrationCreatedMessage))\n            {\n                Thread.Sleep(20);\n            }",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2178380994",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 117105,
        "pr_file": "src/libraries/System.Diagnostics.Process/tests/ProcessTests.cs",
        "discussion_id": "2178380994",
        "commented_code": "@@ -80,6 +81,69 @@ private void AssertNonZeroAllZeroDarwin(long value)\n             }\n         }\n \n+        [ConditionalTheory(typeof(RemoteExecutor), nameof(RemoteExecutor.IsSupported))]\n+        [InlineData(PosixSignal.SIGTSTP)]\n+        [InlineData(PosixSignal.SIGTTOU)]\n+        [InlineData(PosixSignal.SIGTTIN)]\n+        [InlineData(PosixSignal.SIGWINCH)]\n+        [InlineData(PosixSignal.SIGCONT)]\n+        [InlineData(PosixSignal.SIGCHLD)]\n+        [InlineData(PosixSignal.SIGTERM)]\n+        [InlineData(PosixSignal.SIGQUIT)]\n+        [InlineData(PosixSignal.SIGINT)]\n+        [InlineData(PosixSignal.SIGHUP)]\n+        [InlineData((PosixSignal)3)] // SIGQUIT\n+        [InlineData((PosixSignal)15)] // SIGTERM\n+        public void TestCreateNewProcessGroup_HandlerReceivesExpectedSignal(PosixSignal signal)\n+        {\n+            const string PosixSignalRegistrationCreatedMessage = \"PosixSignalRegistration created...\";\n+\n+            if (OperatingSystem.IsWindows() && signal is not (PosixSignal.SIGINT or PosixSignal.SIGQUIT))\n+            {\n+                throw new SkipTestException(\"GenerateConsoleCtrlEvent does not support sending this signal.\");\n+            }\n+\n+            var remoteInvokeOptions = new RemoteInvokeOptions { CheckExitCode = false };\n+            remoteInvokeOptions.StartInfo.RedirectStandardOutput = true;\n+            if (OperatingSystem.IsWindows())\n+            {\n+                remoteInvokeOptions.StartInfo.CreateNewProcessGroup = true;\n+            }\n+\n+            using RemoteInvokeHandle remoteHandle = RemoteExecutor.Invoke(\n+                (signalStr) =>\n+                {\n+                    PosixSignal expectedSignal = Enum.Parse<PosixSignal>(signalStr);\n+                    bool receivedSignal = false;\n+                    ReEnableCtrlCHandlerIfNeeded(expectedSignal);\n+\n+                    using PosixSignalRegistration p = PosixSignalRegistration.Create(expectedSignal, (ctx) =>\n+                    {\n+                        Assert.Equal(expectedSignal, ctx.Signal);\n+                        receivedSignal = true;\n+                        ctx.Cancel = true;\n+                    });\n+\n+                    Console.WriteLine(PosixSignalRegistrationCreatedMessage);\n+\n+                    while (!receivedSignal) ;\n+\n+                    return 0;\n+                },\n+                arg: $\"{signal}\",\n+                remoteInvokeOptions);\n+\n+            while (!remoteHandle.Process.StandardOutput.ReadLine().EndsWith(PosixSignalRegistrationCreatedMessage))\n+            {\n+                Thread.Sleep(20);\n+            }\n+",
        "comment_created_at": "2025-07-01T19:29:25+00:00",
        "comment_author": "Copilot",
        "comment_body": "Calling `EndsWith` on the result of `ReadLine()` can throw if `ReadLine()` returns null. Capture the line in a variable, check for null, and then call `EndsWith` to avoid potential `NullReferenceException`.\n```suggestion\n            string? line;\n            while ((line = remoteHandle.Process.StandardOutput.ReadLine()) != null && \n                   !line.EndsWith(PosixSignalRegistrationCreatedMessage))\n            {\n                Thread.Sleep(20);\n            }\n\n            if (line == null)\n            {\n                throw new InvalidOperationException(\"Unexpected end of stream while waiting for the signal registration message.\");\n            }\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2168704810",
    "pr_number": 117044,
    "pr_file": "src/libraries/Common/src/System/Security/Cryptography/MLDsa.cs",
    "created_at": "2025-06-26T10:08:02+00:00",
    "commented_code": "SR.Argument_SignatureContextTooLong255);\n            }\n\n            if (destination.Length < Algorithm.SignatureSizeInBytes)\n            {\n                throw new ArgumentException(SR.Argument_DestinationTooShort, nameof(destination));\n            }\n\n            ThrowIfDisposed();\n            SignDataCore(data, context, destination.Slice(0, Algorithm.SignatureSizeInBytes));\n            return Algorithm.SignatureSizeInBytes;\n            SignDataCore(data, context, destination);\n        }\n\n        /// <summary>\n        ///   Signs the specified data.\n        /// </summary>\n        /// <param name=\"data\">\n        ///   The data to sign.\n        /// </param>\n        /// <param name=\"context\">\n        ///   An optional context-specific value to limit the scope of the signature.\n        ///   The default value is <see langword=\"null\" />.\n        /// </param>\n        /// <exception cref=\"ArgumentNullException\">\n        ///   <paramref name=\"data\"/> is <see langword=\"null\"/>.\n        /// </exception>\n        /// <exception cref=\"ArgumentOutOfRangeException\">\n        ///   <paramref name=\"context\"/> has a length in excess of 255 bytes.\n        /// </exception>\n        /// <exception cref=\"ObjectDisposedException\">\n        ///   This instance has been disposed.\n        /// </exception>\n        /// <exception cref=\"CryptographicException\">\n        ///   <para>The instance represents only a public key.</para>\n        ///   <para>-or-</para>\n        ///   <para>An error occurred while signing the data.</para>\n        /// </exception>\n        /// <remarks>\n        ///   A <see langword=\"null\" /> context is treated as empty.\n        /// </remarks>\n        public byte[] SignData(byte[] data, byte[]? context = default)\n        {\n            ArgumentNullException.ThrowIfNull(data);\n\n            byte[] destination = new byte[Algorithm.SignatureSizeInBytes];\n            SignData(new ReadOnlySpan<byte>(data), destination.AsSpan(), new ReadOnlySpan<byte>(context));",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2168704810",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 117044,
        "pr_file": "src/libraries/Common/src/System/Security/Cryptography/MLDsa.cs",
        "discussion_id": "2168704810",
        "commented_code": "@@ -119,14 +126,44 @@ public int SignData(ReadOnlySpan<byte> data, Span<byte> destination, ReadOnlySpa\n                     SR.Argument_SignatureContextTooLong255);\n             }\n \n-            if (destination.Length < Algorithm.SignatureSizeInBytes)\n-            {\n-                throw new ArgumentException(SR.Argument_DestinationTooShort, nameof(destination));\n-            }\n-\n             ThrowIfDisposed();\n-            SignDataCore(data, context, destination.Slice(0, Algorithm.SignatureSizeInBytes));\n-            return Algorithm.SignatureSizeInBytes;\n+            SignDataCore(data, context, destination);\n+        }\n+\n+        /// <summary>\n+        ///   Signs the specified data.\n+        /// </summary>\n+        /// <param name=\"data\">\n+        ///   The data to sign.\n+        /// </param>\n+        /// <param name=\"context\">\n+        ///   An optional context-specific value to limit the scope of the signature.\n+        ///   The default value is <see langword=\"null\" />.\n+        /// </param>\n+        /// <exception cref=\"ArgumentNullException\">\n+        ///   <paramref name=\"data\"/> is <see langword=\"null\"/>.\n+        /// </exception>\n+        /// <exception cref=\"ArgumentOutOfRangeException\">\n+        ///   <paramref name=\"context\"/> has a length in excess of 255 bytes.\n+        /// </exception>\n+        /// <exception cref=\"ObjectDisposedException\">\n+        ///   This instance has been disposed.\n+        /// </exception>\n+        /// <exception cref=\"CryptographicException\">\n+        ///   <para>The instance represents only a public key.</para>\n+        ///   <para>-or-</para>\n+        ///   <para>An error occurred while signing the data.</para>\n+        /// </exception>\n+        /// <remarks>\n+        ///   A <see langword=\"null\" /> context is treated as empty.\n+        /// </remarks>\n+        public byte[] SignData(byte[] data, byte[]? context = default)\n+        {\n+            ArgumentNullException.ThrowIfNull(data);\n+\n+            byte[] destination = new byte[Algorithm.SignatureSizeInBytes];\n+            SignData(new ReadOnlySpan<byte>(data), destination.AsSpan(), new ReadOnlySpan<byte>(context));",
        "comment_created_at": "2025-06-26T10:08:02+00:00",
        "comment_author": "Copilot",
        "comment_body": "The byte[] overload of SignData treats a null context incorrectly: new ReadOnlySpan<byte>(context) will throw if context is null. To align with the XML remarks that null is treated as empty, map a null context to ReadOnlySpan<byte>.Empty before calling the span-based overload.\n```suggestion\n            SignData(new ReadOnlySpan<byte>(data), destination.AsSpan(), context == null ? ReadOnlySpan<byte>.Empty : new ReadOnlySpan<byte>(context));\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "2169375771",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 117044,
        "pr_file": "src/libraries/Common/src/System/Security/Cryptography/MLDsa.cs",
        "discussion_id": "2168704810",
        "commented_code": "@@ -119,14 +126,44 @@ public int SignData(ReadOnlySpan<byte> data, Span<byte> destination, ReadOnlySpa\n                     SR.Argument_SignatureContextTooLong255);\n             }\n \n-            if (destination.Length < Algorithm.SignatureSizeInBytes)\n-            {\n-                throw new ArgumentException(SR.Argument_DestinationTooShort, nameof(destination));\n-            }\n-\n             ThrowIfDisposed();\n-            SignDataCore(data, context, destination.Slice(0, Algorithm.SignatureSizeInBytes));\n-            return Algorithm.SignatureSizeInBytes;\n+            SignDataCore(data, context, destination);\n+        }\n+\n+        /// <summary>\n+        ///   Signs the specified data.\n+        /// </summary>\n+        /// <param name=\"data\">\n+        ///   The data to sign.\n+        /// </param>\n+        /// <param name=\"context\">\n+        ///   An optional context-specific value to limit the scope of the signature.\n+        ///   The default value is <see langword=\"null\" />.\n+        /// </param>\n+        /// <exception cref=\"ArgumentNullException\">\n+        ///   <paramref name=\"data\"/> is <see langword=\"null\"/>.\n+        /// </exception>\n+        /// <exception cref=\"ArgumentOutOfRangeException\">\n+        ///   <paramref name=\"context\"/> has a length in excess of 255 bytes.\n+        /// </exception>\n+        /// <exception cref=\"ObjectDisposedException\">\n+        ///   This instance has been disposed.\n+        /// </exception>\n+        /// <exception cref=\"CryptographicException\">\n+        ///   <para>The instance represents only a public key.</para>\n+        ///   <para>-or-</para>\n+        ///   <para>An error occurred while signing the data.</para>\n+        /// </exception>\n+        /// <remarks>\n+        ///   A <see langword=\"null\" /> context is treated as empty.\n+        /// </remarks>\n+        public byte[] SignData(byte[] data, byte[]? context = default)\n+        {\n+            ArgumentNullException.ThrowIfNull(data);\n+\n+            byte[] destination = new byte[Algorithm.SignatureSizeInBytes];\n+            SignData(new ReadOnlySpan<byte>(data), destination.AsSpan(), new ReadOnlySpan<byte>(context));",
        "comment_created_at": "2025-06-26T15:45:35+00:00",
        "comment_author": "krwq",
        "comment_body": "same as https://github.com/dotnet/runtime/pull/117044#discussion_r2168991551",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1897437891",
    "pr_number": 110945,
    "pr_file": "src/coreclr/System.Private.CoreLib/src/System/Reflection/RuntimeCustomAttributeData.cs",
    "created_at": "2024-12-25T17:49:56+00:00",
    "commented_code": "RuntimeMethodInfo setMethod = property.GetSetMethod(true)!;\n\n                            // Public properties may have non-public setter methods\n                            if (!setMethod.IsPublic)\n                            if (setMethod == null || !setMethod.IsPublic)",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "1897437891",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 110945,
        "pr_file": "src/coreclr/System.Private.CoreLib/src/System/Reflection/RuntimeCustomAttributeData.cs",
        "discussion_id": "1897437891",
        "commented_code": "@@ -1580,7 +1580,7 @@ private static void AddCustomAttributes(\n                             RuntimeMethodInfo setMethod = property.GetSetMethod(true)!;\n \n                             // Public properties may have non-public setter methods\n-                            if (!setMethod.IsPublic)\n+                            if (setMethod == null || !setMethod.IsPublic)",
        "comment_created_at": "2024-12-25T17:49:56+00:00",
        "comment_author": "huoyaoyuan",
        "comment_body": "`is null` to avoid unnecessary comparison operator",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2094247389",
    "pr_number": 115684,
    "pr_file": "src/libraries/Microsoft.Extensions.FileProviders.Composite/src/CompositeFileProvider.cs",
    "created_at": "2025-05-18T00:07:26+00:00",
    "commented_code": "foreach (IFileProvider fileProvider in _fileProviders)\n            {\n                IChangeToken changeToken = fileProvider.Watch(pattern);\n                if (changeToken != null)\n                if (changeToken is not null && changeToken is not NullChangeToken)",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2094247389",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 115684,
        "pr_file": "src/libraries/Microsoft.Extensions.FileProviders.Composite/src/CompositeFileProvider.cs",
        "discussion_id": "2094247389",
        "commented_code": "@@ -80,19 +80,18 @@ public IChangeToken Watch(string pattern)\n             foreach (IFileProvider fileProvider in _fileProviders)\n             {\n                 IChangeToken changeToken = fileProvider.Watch(pattern);\n-                if (changeToken != null)\n+                if (changeToken is not null && changeToken is not NullChangeToken)",
        "comment_created_at": "2025-05-18T00:07:26+00:00",
        "comment_author": "teo-tsirpanis",
        "comment_body": "```suggestion\r\n                if (changeToken is not (null or NullChangeToken))\r\n```",
        "pr_file_module": null
      }
    ]
  }
]
