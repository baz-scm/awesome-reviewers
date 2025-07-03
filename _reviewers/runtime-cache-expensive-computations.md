---
title: Cache expensive computations
description: Avoid recomputing expensive operations by caching results when they will
  be used multiple times. This applies to method calls, property access, and static
  property lookups. The performance impact of repeated calculations can be significant,
  especially in hot code paths.
repository: dotnet/runtime
label: Performance Optimization
language: C#
comments_count: 5
repository_stars: 16578
---

Avoid recomputing expensive operations by caching results when they will be used multiple times. This applies to method calls, property access, and static property lookups. The performance impact of repeated calculations can be significant, especially in hot code paths.

Consider these approaches:

1. **Pass computed values as parameters**: When a method needs a value that is expensive to compute, calculate it once and pass it to all methods that need it.

```csharp
// Instead of this:
if (type.GetClassLayout().Kind != MetadataLayoutKind.Auto) { ... }
// And later:
return type.GetClassLayout().Kind switch { ... }

// Do this:
var layout = type.GetClassLayout();
if (layout.Kind != MetadataLayoutKind.Auto) { ... }
// And later:
return layout.Kind switch { ... }
```

2. **Cache static or repeated property lookups**: Store values from static properties or repeated lookups in local variables.

```csharp
// Instead of this:
if (IsHttp3Supported() && GlobalHttpSettings.SocketsHttpHandler.AllowHttp3 && _http3Enabled) { ... }
// And later again:
if (GlobalHttpSettings.SocketsHttpHandler.AllowHttp3) { ... }

// Do this:
bool allowHttp3 = GlobalHttpSettings.SocketsHttpHandler.AllowHttp3;
if (IsHttp3Supported() && allowHttp3 && _http3Enabled) { ... }
// And later:
if (allowHttp3) { ... }
```

3. **Pre-allocate collections with appropriate capacity**: When creating collections that will grow, initialize them with an appropriate capacity to avoid expensive resize operations.

```csharp
// Instead of this:
symbolRemapping = new Dictionary<ISymbolNode, ISymbolNode>();

// Do this:
symbolRemapping = new Dictionary<ISymbolNode, ISymbolNode>(
    (int)(1.05 * (previousSymbolRemapping?.Count ?? 0)));
```

Caching computed values not only improves performance but also makes code more readable by reducing duplication and making dependencies explicit.
