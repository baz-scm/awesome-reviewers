---
title: Use descriptive names
description: Choose names that clearly express the purpose, behavior, or semantic
  meaning of variables, functions, and types. Avoid ambiguous or generic names that
  require additional context to understand their role.
repository: traefik/traefik
label: Naming Conventions
language: Go
comments_count: 7
repository_stars: 55772
---

Choose names that clearly express the purpose, behavior, or semantic meaning of variables, functions, and types. Avoid ambiguous or generic names that require additional context to understand their role.

Key principles:
- Make boolean nature explicit: `regex` → `isRegex`
- Describe actual functionality: `ParseDomainsAndRegex` → `ParseHostMatchers`
- Clarify behavior over generic terms: `CustomResponseWriter` → `StatusRecorder`
- Distinguish between similar concepts: `FailTimeout` → `FailureWindow` (time window vs timeout duration)
- Be explicit about quantities: `MaxFails` → `MaxFailedAttempts`
- Align with actual logic: `down` → `up` when variable represents "up" status
- Use explicit constants over magic values: `defaultCacheDuration` instead of `cache.DefaultExpiration`

Example:
```go
// Ambiguous - what kind of timeout?
type PassiveHealthCheck struct {
    FailTimeout ptypes.Duration
    MaxFails    int
}

// Clear - describes the time window and explicit count
type PassiveHealthCheck struct {
    FailureWindow      ptypes.Duration
    MaxFailedAttempts  int
}
```

This approach reduces cognitive load, prevents misunderstandings, and makes code self-documenting.