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
