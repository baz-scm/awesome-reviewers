---
title: Enable configurable instrumentation
description: Always provide configurable options for performance instrumentation and
  hardware acceleration in your codebase. These options should be clearly documented
  and defaulted appropriately for common scenarios.
repository: dotnet/runtime
label: Performance Optimization
language: Other
comments_count: 2
repository_stars: 16578
---

Always provide configurable options for performance instrumentation and hardware acceleration in your codebase. These options should be clearly documented and defaulted appropriately for common scenarios.

For hardware optimizations:
- Ensure feature flags are available to enable/disable specific hardware acceleration capabilities
- Document precisely which technology variant each flag controls
- Set sensible defaults that enable optimizations for common hardware but don't break compatibility

```c++
// Good example:
RETAIL_CONFIG_DWORD_INFO(EXTERNAL_EnableAVXVNNIINT8, W("EnableAVXVNNIINT8"), 1, "Allows AVXVNNI8+ hardware intrinsics to be disabled")
```

For performance measurement:
- Include build properties that can toggle instrumentation capabilities
- Make instrumentation switchable to avoid performance overhead in production
- Provide sufficient options to cover different performance analysis needs

```xml
<NestedBuildProperty Include="WasmEnableEventPipe" />
<NestedBuildProperty Include="WasmPerformanceInstrumentation" />
```

Implementing configurable performance options allows teams to make data-driven optimization decisions and tailor application behavior to specific deployment environments.


[
  {
    "discussion_id": "2112558911",
    "pr_number": 113956,
    "pr_file": "src/coreclr/inc/clrconfigvalues.h",
    "created_at": "2025-05-28T18:58:24+00:00",
    "commented_code": "RETAIL_CONFIG_DWORD_INFO(EXTERNAL_EnableAVX10v1,                W(\"EnableAVX10v1\"),             1, \"Allows AVX10v1+ hardware intrinsics to be disabled\")\nRETAIL_CONFIG_DWORD_INFO(EXTERNAL_EnableAVX10v2,                W(\"EnableAVX10v2\"),             0, \"Allows AVX10v2+ hardware intrinsics to be disabled\")\nRETAIL_CONFIG_DWORD_INFO(EXTERNAL_EnableAVXVNNI,                W(\"EnableAVXVNNI\"),             1, \"Allows AVXVNNI+ hardware intrinsics to be disabled\")\nRETAIL_CONFIG_DWORD_INFO(EXTERNAL_EnableAVXVNNIINT8,            W(\"EnableAVXVNNIINT8\"),         1, \"Allows AVXVNNI+ hardware intrinsics to be disabled\")\nRETAIL_CONFIG_DWORD_INFO(EXTERNAL_EnableAVXVNNIINT16,           W(\"EnableAVXVNNIINT16\"),        1, \"Allows AVXVNNI+ hardware intrinsics to be disabled\")",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2112558911",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 113956,
        "pr_file": "src/coreclr/inc/clrconfigvalues.h",
        "discussion_id": "2112558911",
        "commented_code": "@@ -695,6 +695,8 @@ RETAIL_CONFIG_DWORD_INFO(EXTERNAL_EnableAVX512VBMI_VL,          W(\"EnableAVX512V\n RETAIL_CONFIG_DWORD_INFO(EXTERNAL_EnableAVX10v1,                W(\"EnableAVX10v1\"),             1, \"Allows AVX10v1+ hardware intrinsics to be disabled\")\n RETAIL_CONFIG_DWORD_INFO(EXTERNAL_EnableAVX10v2,                W(\"EnableAVX10v2\"),             0, \"Allows AVX10v2+ hardware intrinsics to be disabled\")\n RETAIL_CONFIG_DWORD_INFO(EXTERNAL_EnableAVXVNNI,                W(\"EnableAVXVNNI\"),             1, \"Allows AVXVNNI+ hardware intrinsics to be disabled\")\n+RETAIL_CONFIG_DWORD_INFO(EXTERNAL_EnableAVXVNNIINT8,            W(\"EnableAVXVNNIINT8\"),         1, \"Allows AVXVNNI+ hardware intrinsics to be disabled\")\n+RETAIL_CONFIG_DWORD_INFO(EXTERNAL_EnableAVXVNNIINT16,           W(\"EnableAVXVNNIINT16\"),        1, \"Allows AVXVNNI+ hardware intrinsics to be disabled\")",
        "comment_created_at": "2025-05-28T18:58:24+00:00",
        "comment_author": "tannergooding",
        "comment_body": "```suggestion\r\nRETAIL_CONFIG_DWORD_INFO(EXTERNAL_EnableAVXVNNIINT8,            W(\"EnableAVXVNNIINT8\"),         1, \"Allows AVXVNNI8+ hardware intrinsics to be disabled\")\r\nRETAIL_CONFIG_DWORD_INFO(EXTERNAL_EnableAVXVNNIINT16,           W(\"EnableAVXVNNIINT16\"),        1, \"Allows AVXVNNI16+ hardware intrinsics to be disabled\")\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2103967515",
    "pr_number": 115927,
    "pr_file": "src/mono/sample/wasm/Directory.Build.targets",
    "created_at": "2025-05-23T07:17:54+00:00",
    "commented_code": "<NestedBuildProperty Include=\"WasmEmitSourceMap\" />\n    <NestedBuildProperty Include=\"WasmEmitSymbolMap\" />\n    <NestedBuildProperty Include=\"WasmEnableThreads\" />\n    <NestedBuildProperty Include=\"WasmPerfTracing\" />\n    <NestedBuildProperty Include=\"WasmEnableEventPipe\" />",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2103967515",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 115927,
        "pr_file": "src/mono/sample/wasm/Directory.Build.targets",
        "discussion_id": "2103967515",
        "commented_code": "@@ -34,7 +34,7 @@\n     <NestedBuildProperty Include=\"WasmEmitSourceMap\" />\n     <NestedBuildProperty Include=\"WasmEmitSymbolMap\" />\n     <NestedBuildProperty Include=\"WasmEnableThreads\" />\n-    <NestedBuildProperty Include=\"WasmPerfTracing\" />\n+    <NestedBuildProperty Include=\"WasmEnableEventPipe\" />",
        "comment_created_at": "2025-05-23T07:17:54+00:00",
        "comment_author": "pavelsavara",
        "comment_body": "@copilot add `WasmPerformanceInstrumentation` into this list",
        "pr_file_module": null
      },
      {
        "comment_id": "2103980068",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 115927,
        "pr_file": "src/mono/sample/wasm/Directory.Build.targets",
        "discussion_id": "2103967515",
        "commented_code": "@@ -34,7 +34,7 @@\n     <NestedBuildProperty Include=\"WasmEmitSourceMap\" />\n     <NestedBuildProperty Include=\"WasmEmitSymbolMap\" />\n     <NestedBuildProperty Include=\"WasmEnableThreads\" />\n-    <NestedBuildProperty Include=\"WasmPerfTracing\" />\n+    <NestedBuildProperty Include=\"WasmEnableEventPipe\" />",
        "comment_created_at": "2025-05-23T07:25:27+00:00",
        "comment_author": "Copilot",
        "comment_body": "I've added `WasmPerformanceInstrumentation` to the list of nested build properties in src/mono/sample/wasm/Directory.Build.targets in commit 110386f.",
        "pr_file_module": null
      }
    ]
  }
]
