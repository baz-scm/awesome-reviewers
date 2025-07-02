---
title: Document code meaningfully
description: 'Provide meaningful documentation that enhances code maintainability
  and understanding. Follow these practices:


  1. **Explain the "why"** - Document complex or non-obvious code behavior with comments
  that explain reasoning, not just functionality:'
repository: dotnet/runtime
label: Documentation
language: C#
comments_count: 5
repository_stars: 16578
---

Provide meaningful documentation that enhances code maintainability and understanding. Follow these practices:

1. **Explain the "why"** - Document complex or non-obvious code behavior with comments that explain reasoning, not just functionality:
```csharp
// Checking HasNewValue ensures the property setter is called even with null values,
// as setters may contain important initialization logic that should not be bypassed
if (bindingPoint.HasNewValue || bindingPoint.Value != null)
```

2. **Track TODOs properly** - Replace generic TODO comments with specific GitHub issue references:
```csharp
// TODO: Implement caching mechanism (see issue #1234)
```

3. **Attribute borrowed code** - When adapting code from external sources, include clear attribution with links and license information:
```csharp
// These definitions are derived from CDDL-licensed source code.
// Original source: https://src.illumos.org/source/xref/illumos-gate/usr/src/uts/common/sys/procfs.h
```

4. **Document APIs with XML comments** - Use XML documentation for public, internal, and significant private APIs to explain their purpose, parameters, and usage patterns, even for parameterless constructors that seed documentation.

5. **Keep documentation readable** - Ensure comments are concise, valuable, and formatted to avoid requiring horizontal scrolling.

Following these practices helps both current and future developers understand code intent, origin, and pending work, significantly reducing maintenance costs.


[
  {
    "discussion_id": "1713165765",
    "pr_number": 105403,
    "pr_file": "src/libraries/System.Diagnostics.Process/src/System/Diagnostics/Process.SunOS.cs",
    "created_at": "2024-08-12T04:45:33+00:00",
    "commented_code": "// Licensed to the .NET Foundation under one or more agreements.\n// The .NET Foundation licenses this file to you under the MIT license.\n\nusing System;\nusing System.Buffers;\nusing System.Collections.Generic;\nusing System.ComponentModel;\nusing System.Globalization;\nusing System.IO;\nusing System.Runtime.InteropServices;\nusing System.Runtime.Versioning;\nusing System.Text;\nusing System.Threading;\n\n// TODO: remove",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "1713165765",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 105403,
        "pr_file": "src/libraries/System.Diagnostics.Process/src/System/Diagnostics/Process.SunOS.cs",
        "discussion_id": "1713165765",
        "commented_code": "@@ -0,0 +1,143 @@\n+// Licensed to the .NET Foundation under one or more agreements.\n+// The .NET Foundation licenses this file to you under the MIT license.\n+\n+using System;\n+using System.Buffers;\n+using System.Collections.Generic;\n+using System.ComponentModel;\n+using System.Globalization;\n+using System.IO;\n+using System.Runtime.InteropServices;\n+using System.Runtime.Versioning;\n+using System.Text;\n+using System.Threading;\n+\n+// TODO: remove",
        "comment_created_at": "2024-08-12T04:45:33+00:00",
        "comment_author": "AustinWise",
        "comment_body": "If there is remaining work to be done related to this TODO, it could be helpful to file a GitHub issue and include a link here. (same with the comment in `EnsureHandleCountPopulated` later in this file). That way the remaining work is tracked somewhere. This convention that I've seen used in this repo.",
        "pr_file_module": null
      },
      {
        "comment_id": "1720079106",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 105403,
        "pr_file": "src/libraries/System.Diagnostics.Process/src/System/Diagnostics/Process.SunOS.cs",
        "discussion_id": "1713165765",
        "commented_code": "@@ -0,0 +1,143 @@\n+// Licensed to the .NET Foundation under one or more agreements.\n+// The .NET Foundation licenses this file to you under the MIT license.\n+\n+using System;\n+using System.Buffers;\n+using System.Collections.Generic;\n+using System.ComponentModel;\n+using System.Globalization;\n+using System.IO;\n+using System.Runtime.InteropServices;\n+using System.Runtime.Versioning;\n+using System.Text;\n+using System.Threading;\n+\n+// TODO: remove",
        "comment_created_at": "2024-08-16T16:45:25+00:00",
        "comment_author": "gwr",
        "comment_body": "I cleaned up the TODO's",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2166583031",
    "pr_number": 105403,
    "pr_file": "src/libraries/Common/src/Interop/SunOS/procfs/Interop.ProcFs.Definitions.cs",
    "created_at": "2025-06-25T12:21:32+00:00",
    "commented_code": "// Licensed to the .NET Foundation under one or more agreements.\n// The .NET Foundation licenses this file to you under the MIT license.\n\nusing System;\nusing System.Runtime.InteropServices;\n\n// C# equivalents for <sys/procfs.h> structures. See: struct lwpsinfo, struct psinfo.\n// We read directly onto these from procfs, so the layouts and sizes of these structures\n// must _exactly_ match those in <sys/procfs.h>\n\n// analyzer incorrectly flags fixed buffer length const\n// (https://github.com/dotnet/roslyn/issues/37593)\n#pragma warning disable CA1823\n\ninternal static partial class Interop\n{\n    internal static partial class @procfs\n    {\n        internal const string RootPath = \"/proc/\";\n        private const string psinfoFileName = \"/psinfo\";\n        private const string lwpDirName = \"/lwp\";\n        private const string lwpsinfoFileName = \"/lwpsinfo\";\n\n        // Constants from sys/procfs.h\n        private const int PRARGSZ = 80;\n        private const int PRCLSZ = 8;\n        private const int PRFNSZ = 16;\n\n        [StructLayout(LayoutKind.Sequential)]\n        internal struct @timestruc_t\n        {\n            public long tv_sec;\n            public long tv_nsec;\n        }\n\n        // lwp ps(1) information file.  /proc/<pid>/lwp/<lwpid>/lwpsinfo\n        // Equivalent to sys/procfs.h struct lwpsinfo\n        // \"unsafe\" because it has fixed sized arrays.\n        [StructLayout(LayoutKind.Sequential)]\n        internal unsafe struct @lwpsinfo\n        {\n            private     int     pr_flag;        /* lwp flags (DEPRECATED; do not use) */",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2166583031",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 105403,
        "pr_file": "src/libraries/Common/src/Interop/SunOS/procfs/Interop.ProcFs.Definitions.cs",
        "discussion_id": "2166583031",
        "commented_code": "@@ -0,0 +1,155 @@\n+// Licensed to the .NET Foundation under one or more agreements.\n+// The .NET Foundation licenses this file to you under the MIT license.\n+\n+using System;\n+using System.Runtime.InteropServices;\n+\n+// C# equivalents for <sys/procfs.h> structures. See: struct lwpsinfo, struct psinfo.\n+// We read directly onto these from procfs, so the layouts and sizes of these structures\n+// must _exactly_ match those in <sys/procfs.h>\n+\n+// analyzer incorrectly flags fixed buffer length const\n+// (https://github.com/dotnet/roslyn/issues/37593)\n+#pragma warning disable CA1823\n+\n+internal static partial class Interop\n+{\n+    internal static partial class @procfs\n+    {\n+        internal const string RootPath = \"/proc/\";\n+        private const string psinfoFileName = \"/psinfo\";\n+        private const string lwpDirName = \"/lwp\";\n+        private const string lwpsinfoFileName = \"/lwpsinfo\";\n+\n+        // Constants from sys/procfs.h\n+        private const int PRARGSZ = 80;\n+        private const int PRCLSZ = 8;\n+        private const int PRFNSZ = 16;\n+\n+        [StructLayout(LayoutKind.Sequential)]\n+        internal struct @timestruc_t\n+        {\n+            public long tv_sec;\n+            public long tv_nsec;\n+        }\n+\n+        // lwp ps(1) information file.  /proc/<pid>/lwp/<lwpid>/lwpsinfo\n+        // Equivalent to sys/procfs.h struct lwpsinfo\n+        // \"unsafe\" because it has fixed sized arrays.\n+        [StructLayout(LayoutKind.Sequential)]\n+        internal unsafe struct @lwpsinfo\n+        {\n+            private     int     pr_flag;        /* lwp flags (DEPRECATED; do not use) */",
        "comment_created_at": "2025-06-25T12:21:32+00:00",
        "comment_author": "jkotas",
        "comment_body": "What's the license on the file that this was copied from?",
        "pr_file_module": null
      },
      {
        "comment_id": "2166610410",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 105403,
        "pr_file": "src/libraries/Common/src/Interop/SunOS/procfs/Interop.ProcFs.Definitions.cs",
        "discussion_id": "2166583031",
        "commented_code": "@@ -0,0 +1,155 @@\n+// Licensed to the .NET Foundation under one or more agreements.\n+// The .NET Foundation licenses this file to you under the MIT license.\n+\n+using System;\n+using System.Runtime.InteropServices;\n+\n+// C# equivalents for <sys/procfs.h> structures. See: struct lwpsinfo, struct psinfo.\n+// We read directly onto these from procfs, so the layouts and sizes of these structures\n+// must _exactly_ match those in <sys/procfs.h>\n+\n+// analyzer incorrectly flags fixed buffer length const\n+// (https://github.com/dotnet/roslyn/issues/37593)\n+#pragma warning disable CA1823\n+\n+internal static partial class Interop\n+{\n+    internal static partial class @procfs\n+    {\n+        internal const string RootPath = \"/proc/\";\n+        private const string psinfoFileName = \"/psinfo\";\n+        private const string lwpDirName = \"/lwp\";\n+        private const string lwpsinfoFileName = \"/lwpsinfo\";\n+\n+        // Constants from sys/procfs.h\n+        private const int PRARGSZ = 80;\n+        private const int PRCLSZ = 8;\n+        private const int PRFNSZ = 16;\n+\n+        [StructLayout(LayoutKind.Sequential)]\n+        internal struct @timestruc_t\n+        {\n+            public long tv_sec;\n+            public long tv_nsec;\n+        }\n+\n+        // lwp ps(1) information file.  /proc/<pid>/lwp/<lwpid>/lwpsinfo\n+        // Equivalent to sys/procfs.h struct lwpsinfo\n+        // \"unsafe\" because it has fixed sized arrays.\n+        [StructLayout(LayoutKind.Sequential)]\n+        internal unsafe struct @lwpsinfo\n+        {\n+            private     int     pr_flag;        /* lwp flags (DEPRECATED; do not use) */",
        "comment_created_at": "2025-06-25T12:35:25+00:00",
        "comment_author": "am11",
        "comment_body": "https://illumos.org/license/CDDL\r\n\r\nhttps://en.wikipedia.org/wiki/Common_Development_and_Distribution_License#Terms suggests source (not binary) should maintain a copy of the license. We can add it to https://github.com/dotnet/runtime/blob/main/THIRD-PARTY-NOTICES.TXT.",
        "pr_file_module": null
      },
      {
        "comment_id": "2166717529",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 105403,
        "pr_file": "src/libraries/Common/src/Interop/SunOS/procfs/Interop.ProcFs.Definitions.cs",
        "discussion_id": "2166583031",
        "commented_code": "@@ -0,0 +1,155 @@\n+// Licensed to the .NET Foundation under one or more agreements.\n+// The .NET Foundation licenses this file to you under the MIT license.\n+\n+using System;\n+using System.Runtime.InteropServices;\n+\n+// C# equivalents for <sys/procfs.h> structures. See: struct lwpsinfo, struct psinfo.\n+// We read directly onto these from procfs, so the layouts and sizes of these structures\n+// must _exactly_ match those in <sys/procfs.h>\n+\n+// analyzer incorrectly flags fixed buffer length const\n+// (https://github.com/dotnet/roslyn/issues/37593)\n+#pragma warning disable CA1823\n+\n+internal static partial class Interop\n+{\n+    internal static partial class @procfs\n+    {\n+        internal const string RootPath = \"/proc/\";\n+        private const string psinfoFileName = \"/psinfo\";\n+        private const string lwpDirName = \"/lwp\";\n+        private const string lwpsinfoFileName = \"/lwpsinfo\";\n+\n+        // Constants from sys/procfs.h\n+        private const int PRARGSZ = 80;\n+        private const int PRCLSZ = 8;\n+        private const int PRFNSZ = 16;\n+\n+        [StructLayout(LayoutKind.Sequential)]\n+        internal struct @timestruc_t\n+        {\n+            public long tv_sec;\n+            public long tv_nsec;\n+        }\n+\n+        // lwp ps(1) information file.  /proc/<pid>/lwp/<lwpid>/lwpsinfo\n+        // Equivalent to sys/procfs.h struct lwpsinfo\n+        // \"unsafe\" because it has fixed sized arrays.\n+        [StructLayout(LayoutKind.Sequential)]\n+        internal unsafe struct @lwpsinfo\n+        {\n+            private     int     pr_flag;        /* lwp flags (DEPRECATED; do not use) */",
        "comment_created_at": "2025-06-25T13:26:23+00:00",
        "comment_author": "gwr",
        "comment_body": "https://src.illumos.org/source/xref/illumos-gate/usr/src/uts/common/sys/procfs.h\r\nIt's a published interface.",
        "pr_file_module": null
      },
      {
        "comment_id": "2166753814",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 105403,
        "pr_file": "src/libraries/Common/src/Interop/SunOS/procfs/Interop.ProcFs.Definitions.cs",
        "discussion_id": "2166583031",
        "commented_code": "@@ -0,0 +1,155 @@\n+// Licensed to the .NET Foundation under one or more agreements.\n+// The .NET Foundation licenses this file to you under the MIT license.\n+\n+using System;\n+using System.Runtime.InteropServices;\n+\n+// C# equivalents for <sys/procfs.h> structures. See: struct lwpsinfo, struct psinfo.\n+// We read directly onto these from procfs, so the layouts and sizes of these structures\n+// must _exactly_ match those in <sys/procfs.h>\n+\n+// analyzer incorrectly flags fixed buffer length const\n+// (https://github.com/dotnet/roslyn/issues/37593)\n+#pragma warning disable CA1823\n+\n+internal static partial class Interop\n+{\n+    internal static partial class @procfs\n+    {\n+        internal const string RootPath = \"/proc/\";\n+        private const string psinfoFileName = \"/psinfo\";\n+        private const string lwpDirName = \"/lwp\";\n+        private const string lwpsinfoFileName = \"/lwpsinfo\";\n+\n+        // Constants from sys/procfs.h\n+        private const int PRARGSZ = 80;\n+        private const int PRCLSZ = 8;\n+        private const int PRFNSZ = 16;\n+\n+        [StructLayout(LayoutKind.Sequential)]\n+        internal struct @timestruc_t\n+        {\n+            public long tv_sec;\n+            public long tv_nsec;\n+        }\n+\n+        // lwp ps(1) information file.  /proc/<pid>/lwp/<lwpid>/lwpsinfo\n+        // Equivalent to sys/procfs.h struct lwpsinfo\n+        // \"unsafe\" because it has fixed sized arrays.\n+        [StructLayout(LayoutKind.Sequential)]\n+        internal unsafe struct @lwpsinfo\n+        {\n+            private     int     pr_flag;        /* lwp flags (DEPRECATED; do not use) */",
        "comment_created_at": "2025-06-25T13:41:54+00:00",
        "comment_author": "am11",
        "comment_body": "Yea it's fine. Struct definitions and constants usually don't trigger license restrictions. We are doing the same in linux interop code and CDDL is less restrictive than GPL.",
        "pr_file_module": null
      },
      {
        "comment_id": "2167370427",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 105403,
        "pr_file": "src/libraries/Common/src/Interop/SunOS/procfs/Interop.ProcFs.Definitions.cs",
        "discussion_id": "2166583031",
        "commented_code": "@@ -0,0 +1,155 @@\n+// Licensed to the .NET Foundation under one or more agreements.\n+// The .NET Foundation licenses this file to you under the MIT license.\n+\n+using System;\n+using System.Runtime.InteropServices;\n+\n+// C# equivalents for <sys/procfs.h> structures. See: struct lwpsinfo, struct psinfo.\n+// We read directly onto these from procfs, so the layouts and sizes of these structures\n+// must _exactly_ match those in <sys/procfs.h>\n+\n+// analyzer incorrectly flags fixed buffer length const\n+// (https://github.com/dotnet/roslyn/issues/37593)\n+#pragma warning disable CA1823\n+\n+internal static partial class Interop\n+{\n+    internal static partial class @procfs\n+    {\n+        internal const string RootPath = \"/proc/\";\n+        private const string psinfoFileName = \"/psinfo\";\n+        private const string lwpDirName = \"/lwp\";\n+        private const string lwpsinfoFileName = \"/lwpsinfo\";\n+\n+        // Constants from sys/procfs.h\n+        private const int PRARGSZ = 80;\n+        private const int PRCLSZ = 8;\n+        private const int PRFNSZ = 16;\n+\n+        [StructLayout(LayoutKind.Sequential)]\n+        internal struct @timestruc_t\n+        {\n+            public long tv_sec;\n+            public long tv_nsec;\n+        }\n+\n+        // lwp ps(1) information file.  /proc/<pid>/lwp/<lwpid>/lwpsinfo\n+        // Equivalent to sys/procfs.h struct lwpsinfo\n+        // \"unsafe\" because it has fixed sized arrays.\n+        [StructLayout(LayoutKind.Sequential)]\n+        internal unsafe struct @lwpsinfo\n+        {\n+            private     int     pr_flag;        /* lwp flags (DEPRECATED; do not use) */",
        "comment_created_at": "2025-06-25T18:39:04+00:00",
        "comment_author": "jkotas",
        "comment_body": "We prefer to err on the side of doing more attribution.\r\n\r\nThis is more than 100 lines copied nearly verbatim, including docs. I think it is above the threshold.",
        "pr_file_module": null
      },
      {
        "comment_id": "2167388247",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 105403,
        "pr_file": "src/libraries/Common/src/Interop/SunOS/procfs/Interop.ProcFs.Definitions.cs",
        "discussion_id": "2166583031",
        "commented_code": "@@ -0,0 +1,155 @@\n+// Licensed to the .NET Foundation under one or more agreements.\n+// The .NET Foundation licenses this file to you under the MIT license.\n+\n+using System;\n+using System.Runtime.InteropServices;\n+\n+// C# equivalents for <sys/procfs.h> structures. See: struct lwpsinfo, struct psinfo.\n+// We read directly onto these from procfs, so the layouts and sizes of these structures\n+// must _exactly_ match those in <sys/procfs.h>\n+\n+// analyzer incorrectly flags fixed buffer length const\n+// (https://github.com/dotnet/roslyn/issues/37593)\n+#pragma warning disable CA1823\n+\n+internal static partial class Interop\n+{\n+    internal static partial class @procfs\n+    {\n+        internal const string RootPath = \"/proc/\";\n+        private const string psinfoFileName = \"/psinfo\";\n+        private const string lwpDirName = \"/lwp\";\n+        private const string lwpsinfoFileName = \"/lwpsinfo\";\n+\n+        // Constants from sys/procfs.h\n+        private const int PRARGSZ = 80;\n+        private const int PRCLSZ = 8;\n+        private const int PRFNSZ = 16;\n+\n+        [StructLayout(LayoutKind.Sequential)]\n+        internal struct @timestruc_t\n+        {\n+            public long tv_sec;\n+            public long tv_nsec;\n+        }\n+\n+        // lwp ps(1) information file.  /proc/<pid>/lwp/<lwpid>/lwpsinfo\n+        // Equivalent to sys/procfs.h struct lwpsinfo\n+        // \"unsafe\" because it has fixed sized arrays.\n+        [StructLayout(LayoutKind.Sequential)]\n+        internal unsafe struct @lwpsinfo\n+        {\n+            private     int     pr_flag;        /* lwp flags (DEPRECATED; do not use) */",
        "comment_created_at": "2025-06-25T18:48:46+00:00",
        "comment_author": "gwr",
        "comment_body": "OK, should I just copy the top matter from the illumos procfs.h header?\r\nOr what should the updated top matter look like?  Thanks.",
        "pr_file_module": null
      },
      {
        "comment_id": "2167436518",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 105403,
        "pr_file": "src/libraries/Common/src/Interop/SunOS/procfs/Interop.ProcFs.Definitions.cs",
        "discussion_id": "2166583031",
        "commented_code": "@@ -0,0 +1,155 @@\n+// Licensed to the .NET Foundation under one or more agreements.\n+// The .NET Foundation licenses this file to you under the MIT license.\n+\n+using System;\n+using System.Runtime.InteropServices;\n+\n+// C# equivalents for <sys/procfs.h> structures. See: struct lwpsinfo, struct psinfo.\n+// We read directly onto these from procfs, so the layouts and sizes of these structures\n+// must _exactly_ match those in <sys/procfs.h>\n+\n+// analyzer incorrectly flags fixed buffer length const\n+// (https://github.com/dotnet/roslyn/issues/37593)\n+#pragma warning disable CA1823\n+\n+internal static partial class Interop\n+{\n+    internal static partial class @procfs\n+    {\n+        internal const string RootPath = \"/proc/\";\n+        private const string psinfoFileName = \"/psinfo\";\n+        private const string lwpDirName = \"/lwp\";\n+        private const string lwpsinfoFileName = \"/lwpsinfo\";\n+\n+        // Constants from sys/procfs.h\n+        private const int PRARGSZ = 80;\n+        private const int PRCLSZ = 8;\n+        private const int PRFNSZ = 16;\n+\n+        [StructLayout(LayoutKind.Sequential)]\n+        internal struct @timestruc_t\n+        {\n+            public long tv_sec;\n+            public long tv_nsec;\n+        }\n+\n+        // lwp ps(1) information file.  /proc/<pid>/lwp/<lwpid>/lwpsinfo\n+        // Equivalent to sys/procfs.h struct lwpsinfo\n+        // \"unsafe\" because it has fixed sized arrays.\n+        [StructLayout(LayoutKind.Sequential)]\n+        internal unsafe struct @lwpsinfo\n+        {\n+            private     int     pr_flag;        /* lwp flags (DEPRECATED; do not use) */",
        "comment_created_at": "2025-06-25T19:12:02+00:00",
        "comment_author": "gwr",
        "comment_body": "BTW, the ideas (and maybe some code) were borrowed from the following files under `src/libraries/Common/src/Interop/`\r\nOSX/Interop.libproc.GetProcessInfoById.cs\r\nLinux/procfs/Interop.ProcFsStat.TryReadStatusFile.cs\r\n\r\nI've tried to follow what other platform files looked like.\r\nI don't see an example of an attribution to copy.\r\nThe OSX code is the closest, if that helps.\r\n\r\nWould something like this suffice?\r\n```\r\ndiff --git a/src/libraries/Common/src/Interop/SunOS/procfs/Interop.ProcFs.Definitions.cs b/src/libraries/Common/src/Interop/SunOS/procfs/Interop.ProcFs.Definitions.cs\r\nindex 7e7a98bda7c..ec65abb5ee9 100644\r\n--- a/src/libraries/Common/src/Interop/SunOS/procfs/Interop.ProcFs.Definitions.cs\r\n+++ b/src/libraries/Common/src/Interop/SunOS/procfs/Interop.ProcFs.Definitions.cs\r\n@@ -6,7 +6,8 @@\r\n \r\n // C# equivalents for <sys/procfs.h> structures. See: struct lwpsinfo, struct psinfo.\r\n // We read directly onto these from procfs, so the layouts and sizes of these structures\r\n-// must _exactly_ match those in <sys/procfs.h>\r\n+// must _exactly_ match those in the illumos <sys/procfs.h> header. The original is:\r\n+// https://src.illumos.org/source/xref/illumos-gate/usr/src/uts/common/sys/procfs.h\r\n \r\n // analyzer incorrectly flags fixed buffer length const\r\n // (https://github.com/dotnet/roslyn/issues/37593)\r\n```\r\nThe copied (really derived) parts are the two structs:\r\n```\r\n        internal unsafe struct @lwpsinfo {  ... 23 members... }\r\n        internal unsafe struct @psinfo  { ... 36 members... }\r\n```\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "2167639987",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 105403,
        "pr_file": "src/libraries/Common/src/Interop/SunOS/procfs/Interop.ProcFs.Definitions.cs",
        "discussion_id": "2166583031",
        "commented_code": "@@ -0,0 +1,155 @@\n+// Licensed to the .NET Foundation under one or more agreements.\n+// The .NET Foundation licenses this file to you under the MIT license.\n+\n+using System;\n+using System.Runtime.InteropServices;\n+\n+// C# equivalents for <sys/procfs.h> structures. See: struct lwpsinfo, struct psinfo.\n+// We read directly onto these from procfs, so the layouts and sizes of these structures\n+// must _exactly_ match those in <sys/procfs.h>\n+\n+// analyzer incorrectly flags fixed buffer length const\n+// (https://github.com/dotnet/roslyn/issues/37593)\n+#pragma warning disable CA1823\n+\n+internal static partial class Interop\n+{\n+    internal static partial class @procfs\n+    {\n+        internal const string RootPath = \"/proc/\";\n+        private const string psinfoFileName = \"/psinfo\";\n+        private const string lwpDirName = \"/lwp\";\n+        private const string lwpsinfoFileName = \"/lwpsinfo\";\n+\n+        // Constants from sys/procfs.h\n+        private const int PRARGSZ = 80;\n+        private const int PRCLSZ = 8;\n+        private const int PRFNSZ = 16;\n+\n+        [StructLayout(LayoutKind.Sequential)]\n+        internal struct @timestruc_t\n+        {\n+            public long tv_sec;\n+            public long tv_nsec;\n+        }\n+\n+        // lwp ps(1) information file.  /proc/<pid>/lwp/<lwpid>/lwpsinfo\n+        // Equivalent to sys/procfs.h struct lwpsinfo\n+        // \"unsafe\" because it has fixed sized arrays.\n+        [StructLayout(LayoutKind.Sequential)]\n+        internal unsafe struct @lwpsinfo\n+        {\n+            private     int     pr_flag;        /* lwp flags (DEPRECATED; do not use) */",
        "comment_created_at": "2025-06-25T21:09:46+00:00",
        "comment_author": "gwr",
        "comment_body": "We could also consider going back to using (a pair of) SystemNative_... functions, one each to read the lwpsinfo and psinfo, which has the advantage that those can be simply C code that uses the actual system header for these (and converts to C# form).\r\nThere are pros and cons both ways.  I kinda like what's here now, but I'd be open to trying it the other way if reviewers like that better.",
        "pr_file_module": null
      },
      {
        "comment_id": "2172789620",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 105403,
        "pr_file": "src/libraries/Common/src/Interop/SunOS/procfs/Interop.ProcFs.Definitions.cs",
        "discussion_id": "2166583031",
        "commented_code": "@@ -0,0 +1,155 @@\n+// Licensed to the .NET Foundation under one or more agreements.\n+// The .NET Foundation licenses this file to you under the MIT license.\n+\n+using System;\n+using System.Runtime.InteropServices;\n+\n+// C# equivalents for <sys/procfs.h> structures. See: struct lwpsinfo, struct psinfo.\n+// We read directly onto these from procfs, so the layouts and sizes of these structures\n+// must _exactly_ match those in <sys/procfs.h>\n+\n+// analyzer incorrectly flags fixed buffer length const\n+// (https://github.com/dotnet/roslyn/issues/37593)\n+#pragma warning disable CA1823\n+\n+internal static partial class Interop\n+{\n+    internal static partial class @procfs\n+    {\n+        internal const string RootPath = \"/proc/\";\n+        private const string psinfoFileName = \"/psinfo\";\n+        private const string lwpDirName = \"/lwp\";\n+        private const string lwpsinfoFileName = \"/lwpsinfo\";\n+\n+        // Constants from sys/procfs.h\n+        private const int PRARGSZ = 80;\n+        private const int PRCLSZ = 8;\n+        private const int PRFNSZ = 16;\n+\n+        [StructLayout(LayoutKind.Sequential)]\n+        internal struct @timestruc_t\n+        {\n+            public long tv_sec;\n+            public long tv_nsec;\n+        }\n+\n+        // lwp ps(1) information file.  /proc/<pid>/lwp/<lwpid>/lwpsinfo\n+        // Equivalent to sys/procfs.h struct lwpsinfo\n+        // \"unsafe\" because it has fixed sized arrays.\n+        [StructLayout(LayoutKind.Sequential)]\n+        internal unsafe struct @lwpsinfo\n+        {\n+            private     int     pr_flag;        /* lwp flags (DEPRECATED; do not use) */",
        "comment_created_at": "2025-06-27T20:00:16+00:00",
        "comment_author": "gwr",
        "comment_body": "I took a stab at the approach using C functions in `src/native/libs/System.Native/pal_io.c` to read the data.\r\nSee:  https://github.com/dotnet/runtime/pull/117098\r\nThat avoids the C# code having to \"know\" details of the procfs structs.\r\nBetter?\r\n\r\nBTW, I'm having trouble getting the System.Diagnostics.Process.Tests installed.\r\nThe xunit.console.dll is missing ... (found. needed to ./build.sh libs.test ...)\r\nThanks again.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2168972517",
    "pr_number": 105403,
    "pr_file": "src/libraries/Common/src/Interop/SunOS/procfs/Interop.ProcFs.Definitions.cs",
    "created_at": "2025-06-26T12:39:29+00:00",
    "commented_code": "// Licensed to the .NET Foundation under one or more agreements.\n// The .NET Foundation licenses this file to you under the MIT license.\n\nusing System;\nusing System.Runtime.InteropServices;\n\n// C# equivalents for <sys/procfs.h> structures. See: struct lwpsinfo, struct psinfo.\n// We read directly onto these from procfs, so the layouts and sizes of these structures\n// must _exactly_ match those in <sys/procfs.h>",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2168972517",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 105403,
        "pr_file": "src/libraries/Common/src/Interop/SunOS/procfs/Interop.ProcFs.Definitions.cs",
        "discussion_id": "2168972517",
        "commented_code": "@@ -0,0 +1,155 @@\n+// Licensed to the .NET Foundation under one or more agreements.\n+// The .NET Foundation licenses this file to you under the MIT license.\n+\n+using System;\n+using System.Runtime.InteropServices;\n+\n+// C# equivalents for <sys/procfs.h> structures. See: struct lwpsinfo, struct psinfo.\n+// We read directly onto these from procfs, so the layouts and sizes of these structures\n+// must _exactly_ match those in <sys/procfs.h>",
        "comment_created_at": "2025-06-26T12:39:29+00:00",
        "comment_author": "am11",
        "comment_body": "```suggestion\r\n// C# equivalents for <sys/procfs.h> structures {lwpsinfo, psinfo}.\r\n// We read directly onto these from procfs, so the layouts and sizes of these structures\r\n// must _exactly_ match those in the illumos <sys/procfs.h> header. The original is:\r\n// https://src.illumos.org/source/xref/illumos-gate/usr/src/uts/common/sys/procfs.h\r\n//\r\n// These definitions are derived from CDDL-licensed source code (Common Development and Distribution License).\r\n// Use is limited to structure layout reproduction for binary compatibility purposes.\r\n```\r\n\r\n@jkotas, is the attribution in the source comments sufficient, or should we also include a copy of the CDDL license in https://github.com/dotnet/runtime/blob/main/THIRD-PARTY-NOTICES.TXT?",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2111594220",
    "pr_number": 116065,
    "pr_file": "src/coreclr/tools/Common/CommandLineHelpers.cs",
    "created_at": "2025-05-28T11:16:33+00:00",
    "commented_code": "newTokens = null;\n            return false;\n        }\n\n        private sealed class CustomizedHelpAction : SynchronousCommandLineAction\n        {\n            private readonly HelpAction _helpAction;\n            private readonly Action<ParseResult> _customizer;\n\n            public CustomizedHelpAction(HelpOption helpOption, Action<ParseResult> customizer)\n            {\n                _helpAction = (HelpAction)helpOption.Action;\n                _customizer = customizer;\n            }",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2111594220",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116065,
        "pr_file": "src/coreclr/tools/Common/CommandLineHelpers.cs",
        "discussion_id": "2111594220",
        "commented_code": "@@ -427,5 +426,26 @@ public static bool TryReadResponseFile(string filePath, out IReadOnlyList<string\n             newTokens = null;\n             return false;\n         }\n+\n+        private sealed class CustomizedHelpAction : SynchronousCommandLineAction\n+        {\n+            private readonly HelpAction _helpAction;\n+            private readonly Action<ParseResult> _customizer;\n+\n+            public CustomizedHelpAction(HelpOption helpOption, Action<ParseResult> customizer)\n+            {\n+                _helpAction = (HelpAction)helpOption.Action;\n+                _customizer = customizer;\n+            }\n+",
        "comment_created_at": "2025-05-28T11:16:33+00:00",
        "comment_author": "Copilot",
        "comment_body": "Public or internal APIs like `CustomizedHelpAction` would benefit from XML doc comments to explain its purpose and usage.\n```suggestion\n\n        /// <summary>\n        /// Represents a customized help action that modifies the behavior of the default help action.\n        /// </summary>\n        /// <remarks>\n        /// This class wraps the default <see cref=\"HelpAction\"/> and allows additional customization\n        /// of the help output by invoking a user-defined action after the default help action is executed.\n        /// </remarks>\n        private sealed class CustomizedHelpAction : SynchronousCommandLineAction\n        {\n            private readonly HelpAction _helpAction;\n            private readonly Action<ParseResult> _customizer;\n\n            /// <summary>\n            /// Initializes a new instance of the <see cref=\"CustomizedHelpAction\"/> class.\n            /// </summary>\n            /// <param name=\"helpOption\">The help option whose action is being customized.</param>\n            /// <param name=\"customizer\">An action to further customize the help output.</param>\n            public CustomizedHelpAction(HelpOption helpOption, Action<ParseResult> customizer)\n            {\n                _helpAction = (HelpAction)helpOption.Action;\n                _customizer = customizer;\n            }\n\n            /// <summary>\n            /// Invokes the customized help action.\n            /// </summary>\n            /// <param name=\"parseResult\">The result of parsing the command line arguments.</param>\n            /// <returns>The result code of the help action.</returns>\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "2111596281",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116065,
        "pr_file": "src/coreclr/tools/Common/CommandLineHelpers.cs",
        "discussion_id": "2111594220",
        "commented_code": "@@ -427,5 +426,26 @@ public static bool TryReadResponseFile(string filePath, out IReadOnlyList<string\n             newTokens = null;\n             return false;\n         }\n+\n+        private sealed class CustomizedHelpAction : SynchronousCommandLineAction\n+        {\n+            private readonly HelpAction _helpAction;\n+            private readonly Action<ParseResult> _customizer;\n+\n+            public CustomizedHelpAction(HelpOption helpOption, Action<ParseResult> customizer)\n+            {\n+                _helpAction = (HelpAction)helpOption.Action;\n+                _customizer = customizer;\n+            }\n+",
        "comment_created_at": "2025-05-28T11:17:51+00:00",
        "comment_author": "adamsitnik",
        "comment_body": "It's neither public or internal, it's private and I don't feel like adding comments for something self-explaining is worth it.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2155184053",
    "pr_number": 116677,
    "pr_file": "src/libraries/Microsoft.Extensions.Configuration.Binder/src/ConfigurationBinder.cs",
    "created_at": "2025-06-18T17:51:47+00:00",
    "commented_code": "// For property binding, there are some cases when HasNewValue is not set in BindingPoint while a non-null Value inside that object can be retrieved from the property getter.\n            // As example, when binding a property which not having a configuration entry matching this property and the getter can initialize the Value.\n            // It is important to call the property setter as the setters can have a logic adjusting the Value.",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2155184053",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116677,
        "pr_file": "src/libraries/Microsoft.Extensions.Configuration.Binder/src/ConfigurationBinder.cs",
        "discussion_id": "2155184053",
        "commented_code": "@@ -311,7 +311,7 @@ private static void BindProperty(PropertyInfo property, object instance, IConfig\n             // For property binding, there are some cases when HasNewValue is not set in BindingPoint while a non-null Value inside that object can be retrieved from the property getter.\n             // As example, when binding a property which not having a configuration entry matching this property and the getter can initialize the Value.\n             // It is important to call the property setter as the setters can have a logic adjusting the Value.",
        "comment_created_at": "2025-06-18T17:51:47+00:00",
        "comment_author": "Copilot",
        "comment_body": "Consider adding a comment explaining why checking 'HasNewValue' is necessary here, to aid future maintainers in understanding the change in binding behavior.\n```suggestion\n            // For example, when binding a property that does not have a matching configuration entry, the getter might initialize the Value.\n            // Additionally, HasNewValue is checked to ensure that the property setter is called even if the Value is null, as the setter might contain logic to adjust or initialize the value.\n            // It is important to call the property setter in these cases to preserve the intended behavior of the property.\n```",
        "pr_file_module": null
      }
    ]
  }
]
