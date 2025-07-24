---
title: improve code readability
description: Structure code to maximize readability and reduce cognitive load through
  proper formatting and control flow patterns. This includes breaking long function
  signatures across multiple lines, using early returns to reduce nesting levels,
  and extracting complex boolean expressions into well-named functions.
repository: prometheus/prometheus
label: Code Style
language: Go
comments_count: 6
repository_stars: 59616
---

Structure code to maximize readability and reduce cognitive load through proper formatting and control flow patterns. This includes breaking long function signatures across multiple lines, using early returns to reduce nesting levels, and extracting complex boolean expressions into well-named functions.

Key practices:
- Break long function signatures across multiple lines with proper indentation
- Use early returns to avoid deep nesting and improve code flow
- Extract complex boolean conditions into descriptively named functions
- Use named returns for functions with multiple return values to improve clarity
- Avoid unnecessary code changes that reduce readability without providing benefits

Example of improved readability through early returns:
```go
// Instead of:
if t, ok := activeTargets[target.labels.Hash()]; ok {
    // ... log here ...
}

// Prefer:
t, ok := activeTargets[target.labels.Hash()]
if !ok {
    continue
}
// ... log here ...
```

Example of breaking long function signatures:
```go
func NewZookeeperTreeCache(
    conn *zk.Conn, path string, 
    events chan ZookeeperTreeCacheEvent, 
    logger *slog.Logger, 
    failureCounter prometheus.Counter, 
    numWatchers prometheus.Gauge,
) *ZookeeperTreeCache {
```

These practices make code easier to understand, debug, and maintain by reducing visual complexity and making the logical flow more apparent.