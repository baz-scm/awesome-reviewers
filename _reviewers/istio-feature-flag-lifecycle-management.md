---
title: Feature flag lifecycle management
description: 'Establish clear guidelines for feature flag creation, default values,
  and removal strategy based on risk assessment and user impact.


  **When to use feature flags:**'
repository: istio/istio
label: Configurations
language: Go
comments_count: 6
repository_stars: 37192
---

Establish clear guidelines for feature flag creation, default values, and removal strategy based on risk assessment and user impact.

**When to use feature flags:**
- Use feature flags for experimental features that need gradual rollout or have unknown risks
- Avoid feature flags for simple internal refactoring that users won't directly interact with
- Consider if the feature needs per-node opt-in/opt-out capabilities for risky changes

**Default value strategy:**
- **Off by default**: For new user-facing features that users will want to opt into, but carry some risk
- **On by default**: For internal improvements or optimizations where you need an escape hatch if something goes wrong
- **No flag needed**: For low-risk internal changes that don't affect user-visible behavior

**Lifecycle management:**
- Plan the removal timeline when creating the flag (e.g., "change default to true in v1.27 and remove in v1.28")
- For experimental features, start off by default, then enable by default after validation
- Remove flags promptly after the deprecation period to avoid accumulating technical debt

**Example pattern:**
```go
// Good: Clear intent and lifecycle plan
NativeMetadataExchange = env.Register("NATIVE_METADATA_EXCHANGE", true,
    "Enable native metadata exchange filter. Default true for escape hatch during rollout.").Get()

// Avoid: Unclear necessity  
SomeInternalRefactor = env.Register("ENABLE_INTERNAL_REFACTOR", false,
    "Enable internal refactoring that users don't interact with").Get()
```

This approach ensures feature flags serve their intended purpose without becoming permanent configuration bloat.