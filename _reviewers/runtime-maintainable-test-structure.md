---
title: Maintainable test structure
description: 'Write tests that are maintainable, self-documenting, and that promote
  good testing practices:


  1. **Use proper assertion mechanisms**: Prefer modern assertion patterns over legacy
  approaches. Use built-in assertion methods that clearly indicate what is being tested.'
repository: dotnet/runtime
label: Testing
language: C#
comments_count: 5
repository_stars: 16578
---

Write tests that are maintainable, self-documenting, and that promote good testing practices:

1. **Use proper assertion mechanisms**: Prefer modern assertion patterns over legacy approaches. Use built-in assertion methods that clearly indicate what is being tested.
   ```csharp
   // Bad: Custom test logic with manual exception checking
   bool canceled = false;
   try {
       await GetAsync(useVersion, testAsync, uri, cts.Token);
   } catch (TaskCanceledException) {
       canceled = true;
   }
   Assert.True(canceled);
   
   // Good: Use built-in assertion methods
   await Assert.ThrowsAsync<TaskCanceledException>(() => 
       GetAsync(useVersion, testAsync, uri, cts.Token));
   ```

2. **Create reusable test helpers** for common operations instead of duplicating test code. This improves maintainability and readability while reducing the chance of inconsistencies.

3. **Use modern test patterns**: Replace legacy patterns like "return 100 == success" with proper Assert-based validation that clearly communicates test expectations and failures.

4. **Remove commented-out or dead test code** that doesn't contribute to validation. Keep tests clean and focused on what's actually being tested.

5. **Use appropriate conditional attributes** to ensure tests properly convert Debug.Assert failures to test failures and run only when the tested functionality is supported.


[
  {
    "discussion_id": "2176080203",
    "pr_number": 116659,
    "pr_file": "src/installer/tests/Microsoft.NET.HostModel.Tests/Bundle/BundlerConsistencyTests.cs",
    "created_at": "2025-06-30T22:31:20+00:00",
    "commented_code": "Assert.True((file.Type != FileType.Assembly) || (file.Offset % alignment == 0)));\n        }\n\n        [Fact]\n        [Conditional(\"DEBUG\")] // Relies on debug asserts in product code\n        public void LongFileNames()\n        {\n            var app = sharedTestState.App;\n            List<FileSpec> fileSpecs = new List<FileSpec>\n            {\n                new FileSpec(Binaries.AppHost.FilePath, BundlerHostName),\n                new FileSpec(app.AppDll, Path.Join(\n                    Path.GetDirectoryName(Path.GetRelativePath(app.Location, app.AppDll)),\n                    Path.GetFileNameWithoutExtension(app.AppDll) + new string('a', 260) + Path.GetExtension(app.AppDll))),\n            };\n\n            fileSpecs.AddRange(SingleFileTestApp.GetRuntimeFilesToBundle());\n            Bundler bundler = CreateBundlerInstance();\n            // Debug asserts in the Manifest and Bundler should catch size calculation issues related to long file names",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2176080203",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116659,
        "pr_file": "src/installer/tests/Microsoft.NET.HostModel.Tests/Bundle/BundlerConsistencyTests.cs",
        "discussion_id": "2176080203",
        "commented_code": "@@ -314,6 +315,34 @@ public void AssemblyAlignment()\n                 Assert.True((file.Type != FileType.Assembly) || (file.Offset % alignment == 0)));\n         }\n \n+        [Fact]\n+        [Conditional(\"DEBUG\")] // Relies on debug asserts in product code\n+        public void LongFileNames()\n+        {\n+            var app = sharedTestState.App;\n+            List<FileSpec> fileSpecs = new List<FileSpec>\n+            {\n+                new FileSpec(Binaries.AppHost.FilePath, BundlerHostName),\n+                new FileSpec(app.AppDll, Path.Join(\n+                    Path.GetDirectoryName(Path.GetRelativePath(app.Location, app.AppDll)),\n+                    Path.GetFileNameWithoutExtension(app.AppDll) + new string('a', 260) + Path.GetExtension(app.AppDll))),\n+            };\n+\n+            fileSpecs.AddRange(SingleFileTestApp.GetRuntimeFilesToBundle());\n+            Bundler bundler = CreateBundlerInstance();\n+            // Debug asserts in the Manifest and Bundler should catch size calculation issues related to long file names",
        "comment_created_at": "2025-06-30T22:31:20+00:00",
        "comment_author": "elinor-fung",
        "comment_body": "I think I'm missing how the debug asserts interact here - if this path intentionally triggering debug asserts, won't the test show a dialog / require interaction to continue?",
        "pr_file_module": null
      },
      {
        "comment_id": "2178095933",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116659,
        "pr_file": "src/installer/tests/Microsoft.NET.HostModel.Tests/Bundle/BundlerConsistencyTests.cs",
        "discussion_id": "2176080203",
        "commented_code": "@@ -314,6 +315,34 @@ public void AssemblyAlignment()\n                 Assert.True((file.Type != FileType.Assembly) || (file.Offset % alignment == 0)));\n         }\n \n+        [Fact]\n+        [Conditional(\"DEBUG\")] // Relies on debug asserts in product code\n+        public void LongFileNames()\n+        {\n+            var app = sharedTestState.App;\n+            List<FileSpec> fileSpecs = new List<FileSpec>\n+            {\n+                new FileSpec(Binaries.AppHost.FilePath, BundlerHostName),\n+                new FileSpec(app.AppDll, Path.Join(\n+                    Path.GetDirectoryName(Path.GetRelativePath(app.Location, app.AppDll)),\n+                    Path.GetFileNameWithoutExtension(app.AppDll) + new string('a', 260) + Path.GetExtension(app.AppDll))),\n+            };\n+\n+            fileSpecs.AddRange(SingleFileTestApp.GetRuntimeFilesToBundle());\n+            Bundler bundler = CreateBundlerInstance();\n+            // Debug asserts in the Manifest and Bundler should catch size calculation issues related to long file names",
        "comment_created_at": "2025-07-01T16:57:47+00:00",
        "comment_author": "jtschuster",
        "comment_body": "If everything works correctly, this test shouldn't trigger any Debug.Asserts. There are a few asserts in the Manifest code that ensure the actual written size is the same size that is allocated for the manifest. If a Debug.Assert fails won't it just fail the test rather than show a dialog?",
        "pr_file_module": null
      },
      {
        "comment_id": "2178639898",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116659,
        "pr_file": "src/installer/tests/Microsoft.NET.HostModel.Tests/Bundle/BundlerConsistencyTests.cs",
        "discussion_id": "2176080203",
        "commented_code": "@@ -314,6 +315,34 @@ public void AssemblyAlignment()\n                 Assert.True((file.Type != FileType.Assembly) || (file.Offset % alignment == 0)));\n         }\n \n+        [Fact]\n+        [Conditional(\"DEBUG\")] // Relies on debug asserts in product code\n+        public void LongFileNames()\n+        {\n+            var app = sharedTestState.App;\n+            List<FileSpec> fileSpecs = new List<FileSpec>\n+            {\n+                new FileSpec(Binaries.AppHost.FilePath, BundlerHostName),\n+                new FileSpec(app.AppDll, Path.Join(\n+                    Path.GetDirectoryName(Path.GetRelativePath(app.Location, app.AppDll)),\n+                    Path.GetFileNameWithoutExtension(app.AppDll) + new string('a', 260) + Path.GetExtension(app.AppDll))),\n+            };\n+\n+            fileSpecs.AddRange(SingleFileTestApp.GetRuntimeFilesToBundle());\n+            Bundler bundler = CreateBundlerInstance();\n+            // Debug asserts in the Manifest and Bundler should catch size calculation issues related to long file names",
        "comment_created_at": "2025-07-01T22:26:27+00:00",
        "comment_author": "agocke",
        "comment_body": "iirc xunit installs a handler for debug assert that turns it into a test failure. Either that or the proc panics.",
        "pr_file_module": null
      },
      {
        "comment_id": "2178802171",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116659,
        "pr_file": "src/installer/tests/Microsoft.NET.HostModel.Tests/Bundle/BundlerConsistencyTests.cs",
        "discussion_id": "2176080203",
        "commented_code": "@@ -314,6 +315,34 @@ public void AssemblyAlignment()\n                 Assert.True((file.Type != FileType.Assembly) || (file.Offset % alignment == 0)));\n         }\n \n+        [Fact]\n+        [Conditional(\"DEBUG\")] // Relies on debug asserts in product code\n+        public void LongFileNames()\n+        {\n+            var app = sharedTestState.App;\n+            List<FileSpec> fileSpecs = new List<FileSpec>\n+            {\n+                new FileSpec(Binaries.AppHost.FilePath, BundlerHostName),\n+                new FileSpec(app.AppDll, Path.Join(\n+                    Path.GetDirectoryName(Path.GetRelativePath(app.Location, app.AppDll)),\n+                    Path.GetFileNameWithoutExtension(app.AppDll) + new string('a', 260) + Path.GetExtension(app.AppDll))),\n+            };\n+\n+            fileSpecs.AddRange(SingleFileTestApp.GetRuntimeFilesToBundle());\n+            Bundler bundler = CreateBundlerInstance();\n+            // Debug asserts in the Manifest and Bundler should catch size calculation issues related to long file names",
        "comment_created_at": "2025-07-02T01:24:30+00:00",
        "comment_author": "elinor-fung",
        "comment_body": "Ah, right, Debug.Assert should translate to a failure.\r\n\r\n> If everything works correctly, this test shouldn't trigger any Debug.Asserts\r\n\r\nThe test should still be valid in Release then, right? Do we actually need\r\n```\r\n[Conditional(\"DEBUG\")] // Relies on debug asserts in product code\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "2180344542",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116659,
        "pr_file": "src/installer/tests/Microsoft.NET.HostModel.Tests/Bundle/BundlerConsistencyTests.cs",
        "discussion_id": "2176080203",
        "commented_code": "@@ -314,6 +315,34 @@ public void AssemblyAlignment()\n                 Assert.True((file.Type != FileType.Assembly) || (file.Offset % alignment == 0)));\n         }\n \n+        [Fact]\n+        [Conditional(\"DEBUG\")] // Relies on debug asserts in product code\n+        public void LongFileNames()\n+        {\n+            var app = sharedTestState.App;\n+            List<FileSpec> fileSpecs = new List<FileSpec>\n+            {\n+                new FileSpec(Binaries.AppHost.FilePath, BundlerHostName),\n+                new FileSpec(app.AppDll, Path.Join(\n+                    Path.GetDirectoryName(Path.GetRelativePath(app.Location, app.AppDll)),\n+                    Path.GetFileNameWithoutExtension(app.AppDll) + new string('a', 260) + Path.GetExtension(app.AppDll))),\n+            };\n+\n+            fileSpecs.AddRange(SingleFileTestApp.GetRuntimeFilesToBundle());\n+            Bundler bundler = CreateBundlerInstance();\n+            // Debug asserts in the Manifest and Bundler should catch size calculation issues related to long file names",
        "comment_created_at": "2025-07-02T15:19:48+00:00",
        "comment_author": "jtschuster",
        "comment_body": "It won't trigger the size calculation checks in Release, but it probably would be worth it to check the other parts of the test and make sure it doesn't crash somehow in Release. I'll remove the ConditionalAttribute.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2176126144",
    "pr_number": 116659,
    "pr_file": "src/installer/tests/Microsoft.NET.HostModel.Tests/AppHost/CreateAppHost.cs",
    "created_at": "2025-06-30T23:11:47+00:00",
    "commented_code": "}\n        }\n\n        [Theory]\n        [InlineData(\"\")]\n        [InlineData(\"dir with spaces\")]\n        [PlatformSpecific(TestPlatforms.OSX)]\n        public void SigningExistingAppHostCreatesNewInode(string subdir)\n        {\n            using (TestArtifact artifact = CreateTestDirectory())\n            {\n                string testDirectory = Path.Combine(artifact.Location, subdir);\n                Directory.CreateDirectory(testDirectory);\n                string sourceAppHostMock = Binaries.AppHost.FilePath;\n                string destinationFilePath = Path.Combine(testDirectory, Binaries.AppHost.FileName);\n                string appBinaryFilePath = \"Test/App/Binary/Path.dll\";\n                HostWriter.CreateAppHost(\n                   sourceAppHostMock,\n                   destinationFilePath,\n                   appBinaryFilePath,\n                   windowsGraphicalUserInterface: false,\n                   enableMacOSCodeSign: true);\n                var firstls = Command.Create(\"/bin/ls\", \"-li\", destinationFilePath)",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2176126144",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116659,
        "pr_file": "src/installer/tests/Microsoft.NET.HostModel.Tests/AppHost/CreateAppHost.cs",
        "discussion_id": "2176126144",
        "commented_code": "@@ -285,6 +286,55 @@ public void CodeSignMachOAppHost(string subdir)\n             }\n         }\n \n+        [Theory]\n+        [InlineData(\"\")]\n+        [InlineData(\"dir with spaces\")]\n+        [PlatformSpecific(TestPlatforms.OSX)]\n+        public void SigningExistingAppHostCreatesNewInode(string subdir)\n+        {\n+            using (TestArtifact artifact = CreateTestDirectory())\n+            {\n+                string testDirectory = Path.Combine(artifact.Location, subdir);\n+                Directory.CreateDirectory(testDirectory);\n+                string sourceAppHostMock = Binaries.AppHost.FilePath;\n+                string destinationFilePath = Path.Combine(testDirectory, Binaries.AppHost.FileName);\n+                string appBinaryFilePath = \"Test/App/Binary/Path.dll\";\n+                HostWriter.CreateAppHost(\n+                   sourceAppHostMock,\n+                   destinationFilePath,\n+                   appBinaryFilePath,\n+                   windowsGraphicalUserInterface: false,\n+                   enableMacOSCodeSign: true);\n+                var firstls = Command.Create(\"/bin/ls\", \"-li\", destinationFilePath)",
        "comment_created_at": "2025-06-30T23:11:47+00:00",
        "comment_author": "elinor-fung",
        "comment_body": "Would it make sense to have a test helper for getting the inode of a file?",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2143740941",
    "pr_number": 116310,
    "pr_file": "src/tests/Interop/GCBridge/BridgeTest.cs",
    "created_at": "2025-06-12T22:10:40+00:00",
    "commented_code": null,
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2143740941",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116310,
        "pr_file": "src/tests/Interop/GCBridge/BridgeTest.cs",
        "discussion_id": "2143740941",
        "commented_code": null,
        "comment_created_at": "2025-06-12T22:10:40+00:00",
        "comment_author": "jkoritzinsky",
        "comment_body": "Can we change the tests here to use Asserts and not the legacy \"return 100 == success\" model?",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2178373042",
    "pr_number": 117214,
    "pr_file": "src/libraries/System.Net.Http/tests/FunctionalTests/DiagnosticsTests.cs",
    "created_at": "2025-07-01T19:23:04+00:00",
    "commented_code": "{\n                            uri = new Uri($\"{uri.Scheme}://localhost:{uri.Port}\");\n                        }\n\n                        await Assert.ThrowsAsync<TaskCanceledException>(() => GetAsync(useVersion, testAsync, uri, cts.Token));\n                        bool canceled = false;\n                        //await Assert.ThrowsAsync<TaskCanceledException>(() => GetAsync(useVersion, testAsync, uri, cts.Token));\n                        try\n                        {\n                            await GetAsync(useVersion, testAsync, uri, cts.Token);\n                        }\n                        catch (TaskCanceledException)\n                        {\n                            canceled = true;\n                            // Expected\n                        }\n                        Assert.True(canceled);",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2178373042",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 117214,
        "pr_file": "src/libraries/System.Net.Http/tests/FunctionalTests/DiagnosticsTests.cs",
        "discussion_id": "2178373042",
        "commented_code": "@@ -870,8 +875,18 @@ await GetFactoryForVersion(useVersion).CreateClientAndServerAsync(\n                         {\n                             uri = new Uri($\"{uri.Scheme}://localhost:{uri.Port}\");\n                         }\n-\n-                        await Assert.ThrowsAsync<TaskCanceledException>(() => GetAsync(useVersion, testAsync, uri, cts.Token));\n+                        bool canceled = false;\n+                        //await Assert.ThrowsAsync<TaskCanceledException>(() => GetAsync(useVersion, testAsync, uri, cts.Token));\n+                        try\n+                        {\n+                            await GetAsync(useVersion, testAsync, uri, cts.Token);\n+                        }\n+                        catch (TaskCanceledException)\n+                        {\n+                            canceled = true;\n+                            // Expected\n+                        }\n+                        Assert.True(canceled);",
        "comment_created_at": "2025-07-01T19:23:04+00:00",
        "comment_author": "Copilot",
        "comment_body": "Remove this commented-out `Assert.ThrowsAsync` call to clean up dead code, or restore it if you prefer built-in assertion semantics.\n```suggestion\n                        await Assert.ThrowsAsync<TaskCanceledException>(() => GetAsync(useVersion, testAsync, uri, cts.Token));\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2144147364",
    "pr_number": 113956,
    "pr_file": "src/tests/JIT/HardwareIntrinsics/X86_AvxVnniInt16/AvxVnniInt16/AvxVnniInt16SampleTest.cs",
    "created_at": "2025-06-13T03:44:23+00:00",
    "commented_code": "// Licensed to the .NET Foundation under one or more agreements.\n// The .NET Foundation licenses this file to you under the MIT license.\n//\n\nusing System;\nusing System.Runtime.CompilerServices;\nusing System.Runtime.InteropServices;\nusing System.Runtime.Intrinsics.X86;\nusing System.Runtime.Intrinsics;\nusing Xunit;\n\nnamespace IntelHardwareIntrinsicTest._AvxVnniInt16",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2144147364",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 113956,
        "pr_file": "src/tests/JIT/HardwareIntrinsics/X86_AvxVnniInt16/AvxVnniInt16/AvxVnniInt16SampleTest.cs",
        "discussion_id": "2144147364",
        "commented_code": "@@ -0,0 +1,50 @@\n+// Licensed to the .NET Foundation under one or more agreements.\n+// The .NET Foundation licenses this file to you under the MIT license.\n+//\n+\n+using System;\n+using System.Runtime.CompilerServices;\n+using System.Runtime.InteropServices;\n+using System.Runtime.Intrinsics.X86;\n+using System.Runtime.Intrinsics;\n+using Xunit;\n+\n+namespace IntelHardwareIntrinsicTest._AvxVnniInt16",
        "comment_created_at": "2025-06-13T03:44:23+00:00",
        "comment_author": "tannergooding",
        "comment_body": "Were these intentionally added? They look to have dead code and aren't actually testing the APIs in question.\r\n\r\nWe have other tests which cover the CPUID checks",
        "pr_file_module": null
      },
      {
        "comment_id": "2146441207",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 113956,
        "pr_file": "src/tests/JIT/HardwareIntrinsics/X86_AvxVnniInt16/AvxVnniInt16/AvxVnniInt16SampleTest.cs",
        "discussion_id": "2144147364",
        "commented_code": "@@ -0,0 +1,50 @@\n+// Licensed to the .NET Foundation under one or more agreements.\n+// The .NET Foundation licenses this file to you under the MIT license.\n+//\n+\n+using System;\n+using System.Runtime.CompilerServices;\n+using System.Runtime.InteropServices;\n+using System.Runtime.Intrinsics.X86;\n+using System.Runtime.Intrinsics;\n+using Xunit;\n+\n+namespace IntelHardwareIntrinsicTest._AvxVnniInt16",
        "comment_created_at": "2025-06-14T04:55:19+00:00",
        "comment_author": "khushal1996",
        "comment_body": "Yeah right now I have added them to check the support on different hardware. I will remove them now since I have confirmed in the SDE tests that all combinations work fine now.",
        "pr_file_module": null
      }
    ]
  }
]
