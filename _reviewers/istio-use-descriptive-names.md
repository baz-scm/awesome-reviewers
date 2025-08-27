---
title: Use descriptive names
description: Names should accurately reflect their actual functionality and behavior.
  Avoid misleading or vague identifiers that don't match what the code actually does.
repository: istio/istio
label: Naming Conventions
language: Go
comments_count: 12
repository_stars: 37192
---

Names should accurately reflect their actual functionality and behavior. Avoid misleading or vague identifiers that don't match what the code actually does.

Key principles:
- **Accuracy over brevity**: Choose names that clearly indicate the actual behavior, even if longer (e.g., `allowOverwrite` instead of `Rotation` when not doing true rotation)
- **Be specific about behavior**: Use precise terms that distinguish between similar concepts (e.g., `IsNetworkGateway` instead of `IsGateway` to differentiate from other gateway types)
- **Method names should reflect purpose**: If a method doesn't mutate, use names like `WithService` instead of `AddService`; if it updates cache, name it accordingly rather than `GetPublicKey`
- **Avoid redundant context**: Don't repeat information already available (e.g., `Key()` instead of `GetIstioEndpointKey()` when called on an IstioEndpoint)
- **Use meaningful variables**: Replace single-letter variables with descriptive names (e.g., `clt.Config().Service()` instead of `"a"`)
- **Follow Go conventions**: Avoid prefixes like `k` in variable names (`annotation` instead of `kAnnotation`)

Example:
```go
// Poor: misleading name
func (ep *IstioEndpoint) GetIstioEndpointKey() string { ... }

// Better: concise and clear
func (ep *IstioEndpoint) Key() string { ... }

// Poor: doesn't reflect actual behavior  
func AddService(service *Service) WasmPluginListenerInfo { ... }

// Better: indicates non-mutating operation
func WithService(service *Service) WasmPluginListenerInfo { ... }
```