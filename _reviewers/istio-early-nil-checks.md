---
title: Early nil checks
description: Add nil and empty checks at the beginning of functions to prevent downstream
  issues and avoid unnecessary processing. This pattern improves code safety and performance
  by failing fast when inputs are invalid or empty.
repository: istio/istio
label: Null Handling
language: Go
comments_count: 3
repository_stars: 37192
---

Add nil and empty checks at the beginning of functions to prevent downstream issues and avoid unnecessary processing. This pattern improves code safety and performance by failing fast when inputs are invalid or empty.

Key practices:
- Check for nil parameters before using them
- Validate empty collections before iteration or processing
- Return early when inputs are nil to avoid complex nested logic
- Use short-circuit evaluation to clean up code structure

Example:
```go
func buildInitialMetadata(metadata []*meshconfig.MeshConfig_ExtensionProvider_HttpHeader) []*core.HeaderValue {
    if metadata == nil { 
        return nil 
    }
    target := make([]*core.HeaderValue, 0, len(metadata))
    // ... rest of processing
}

// Check collection length before operations
if len(ipRange) > 0 {
    chains = append(chains, directChain)
    // ... process ipRange
}

// Short-circuit nil checks to clean up nested logic
if wh.nodes == nil {
    // handle nil case early
    return
}
```

This approach prevents null pointer exceptions, reduces cognitive complexity, and makes code more maintainable by handling edge cases upfront rather than deep within the logic.