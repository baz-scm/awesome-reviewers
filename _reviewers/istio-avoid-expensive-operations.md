---
title: Avoid expensive operations
description: Identify and eliminate computationally expensive operations in frequently
  executed code paths. Common expensive operations include repeated computations,
  unbounded API calls, inefficient string operations, and operations that don't scale
  with data size.
repository: istio/istio
label: Performance Optimization
language: Go
comments_count: 6
repository_stars: 37192
---

Identify and eliminate computationally expensive operations in frequently executed code paths. Common expensive operations include repeated computations, unbounded API calls, inefficient string operations, and operations that don't scale with data size.

Key strategies to avoid expensive operations:
- Use cached data (informers, listers) instead of direct API calls
- Precompute values once rather than recalculating repeatedly  
- Avoid operations like config_dump outside debugging contexts
- Replace inefficient string operations with optimized alternatives
- Minimize unnecessary iterations over large collections

Example optimization for string building:
```go
// Expensive: fmt.Sprintf with multiple allocations (317ns, 5 allocs)
func getEndpointKey(portName string, portNum int32, ips []string) string {
    ipString := strings.Join(ips, ", ")
    return fmt.Sprintf("%s-%s-%d", ipString, portName, portNum)
}

// Optimized: strings.Builder with fewer allocations (75ns, 2 allocs)  
func getEndpointKey(portName string, portNum int32, ips []string) string {
    var b strings.Builder
    for k, ip := range ips {
        if k > 0 {
            b.WriteString(", ")
        }
        b.WriteString(ip)
    }
    b.WriteString("-")
    b.WriteString(portName) 
    b.WriteString("-")
    b.WriteString(strconv.Itoa(int(portNum)))
    return b.String()
}
```

Always consider the performance impact of operations in hot paths and prefer efficient alternatives that scale well with system load.