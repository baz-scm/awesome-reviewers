---
title: avoid repeated expensive operations
description: Avoid performing expensive computational operations repeatedly when the
  same result can be achieved through better algorithm design or data structure choices.
  This includes avoiding sorting on each access, repeated string parsing, or complex
  comparisons that could be precomputed or cached.
repository: istio/istio
label: Algorithms
language: Go
comments_count: 3
repository_stars: 37192
---

Avoid performing expensive computational operations repeatedly when the same result can be achieved through better algorithm design or data structure choices. This includes avoiding sorting on each access, repeated string parsing, or complex comparisons that could be precomputed or cached.

Key principles:
- **Sort once, not on each access**: Instead of sorting data every time it's compared or accessed, sort during creation or maintain sorted order
- **Use appropriate data structures**: Choose data structures that naturally support your access patterns rather than forcing expensive operations on simpler structures
- **Precompute when possible**: For operations that will be repeated, consider precomputing results or using indexing

Example from the codebase:
```go
// Bad: Sorting on each equality check
func WorkloadInstancesEqual(first, second *WorkloadInstance) bool {
    firtAddrs := first.Endpoint.SortIstioEndpointByAddresses() // Mutates and sorts every time
    // ... comparison logic
}

// Better: Use a more efficient comparison or maintain sorted order
func WorkloadInstancesEqual(first, second *WorkloadInstance) bool {
    return IsAddrsEqualIstioEndpoint(first.Endpoint, second.Endpoint) // Efficient comparison without sorting
}
```

Another example:
```go
// Bad: String concatenation and splitting for indexing
workloadNetworkServiceIndex := krt.NewIndex[string, model.WorkloadInfo](GlobalWorkloads, "network;service", func(o model.WorkloadInfo) []string {
    // Later requires: parts := strings.Split(i.Key, ";")
})

// Better: Use a proper struct for composite keys
type NetworkServiceKey struct {
    Network string
    Service string
}
```

This approach reduces computational complexity, improves performance, and makes code more maintainable by choosing algorithms and data structures that match the usage patterns.