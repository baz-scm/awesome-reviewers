---
title: Document configuration intent
description: Configuration settings should be self-documenting with clear intent.
  When adding temporary workarounds, conditional flags, or platform-specific settings,
  include descriptive comments explaining their purpose, limitations, and lifecycle.
  Use TODO comments with issue references for temporary configurations, and choose
  clear, descriptive names for all...
repository: dotnet/runtime
label: Configurations
language: Other
comments_count: 6
repository_stars: 16578
---

Configuration settings should be self-documenting with clear intent. When adding temporary workarounds, conditional flags, or platform-specific settings, include descriptive comments explaining their purpose, limitations, and lifecycle. Use TODO comments with issue references for temporary configurations, and choose clear, descriptive names for all configuration properties. This practice helps future developers understand why certain configurations exist and when they can be modified or removed.

Examples:
1. For temporary workarounds:
```xml
<!-- TODO: Remove this workaround once https://github.com/dotnet/runtime/issues/116929 is fixed -->
<_Crossgen2Supported Condition="'$(TargetOS)' != 'illumos' and '$(TargetOS)' != 'solaris'">true</_Crossgen2Supported>
```

2. For feature flags with specific scope:
```xml
<FeatureJavaMarshal Condition="'$(Configuration)' == 'Debug' or '$(Configuration)' == 'Checked' or '$(TargetOS)' == 'Android'">true</FeatureJavaMarshal>
```

3. For clear, descriptive naming:
```xml
<!-- Prefer clear names that indicate purpose -->
<WasmEnableEventPipe>true</WasmEnableEventPipe>
<!-- Instead of ambiguous names -->
<WasmPerfTracing>true</WasmPerfTracing>
```
