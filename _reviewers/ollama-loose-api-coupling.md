---
title: Loose API coupling
description: Maintain a clear separation between API definitions and their implementations
  by avoiding direct passing of API structures to implementation layers. Extract only
  the necessary values from API structures when passing data downstream.
repository: ollama/ollama
label: API
language: Go
comments_count: 4
repository_stars: 145704
---

Maintain a clear separation between API definitions and their implementations by avoiding direct passing of API structures to implementation layers. Extract only the necessary values from API structures when passing data downstream.

This approach has several benefits:
- Improves maintainability as implementation details can evolve independently
- Reduces tight coupling between API contracts and internal code
- Makes testing easier by simplifying dependencies
- Prevents implementation-specific requirements from leaking into the API design

Example of problematic coupling:
```go
// Avoid: Passing entire API structure downstream
sampler := sample.NewSampler(req.Options, grammar)
```

Better approach:
```go
// Better: Extract only needed values
sampler := sample.NewSampler(
    req.Options.Temperature,
    req.Options.TopK,
    req.Options.TopP,
    req.Options.MinP,
    req.Options.Seed,
    grammar,
)
```

Similarly, for transformation pipelines, prefer direct function calls with clear parameters over passing abstract data structures:

```go
// Instead of: Using lists of transforms
transforms := []Transform{topK, topP, softmax}
Weighted(rng, transforms...)

// Better: Use specific function calls in a clear sequence
result := topK(topP(softmax(values)))
```

This principle extends to all layers of your API implementation - keep interfaces clean and pass only what's needed.