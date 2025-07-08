---
title: Feature flag implementation
description: 'When implementing feature flags, ensure consistency between runtime
  and compiled scenarios. Feature switches marked with `FeatureSwitchDefinition` must
  properly return the AppContext switch value when defined:'
repository: dotnet/runtime
label: Configurations
language: C#
comments_count: 2
repository_stars: 16578
---

When implementing feature flags, ensure consistency between runtime and compiled scenarios. Feature switches marked with `FeatureSwitchDefinition` must properly return the AppContext switch value when defined:

```csharp
// INCORRECT implementation
[FeatureSwitchDefinition("System.Net.SocketsHttpHandler.Http3Support")]
public static bool IsHttp3Supported => SomeDefaultLogic();

// CORRECT implementation - must use the AppContext switch value
[FeatureSwitchDefinition("System.Net.SocketsHttpHandler.Http3Support")]
public static bool IsHttp3Supported => 
    AppContext.TryGetSwitch("System.Net.SocketsHttpHandler.Http3Support", out var ret) ? ret : SomeDefaultLogic();
```

Consider dead code elimination implications when designing feature flags for AOT scenarios, as behavior differences may arise between `dotnet run` and `dotnet publish`. Avoid adding configuration switches preemptively - only introduce them when there's a demonstrated need from users. For platform-specific features, ensure configuration is properly respected across all supported environments.
