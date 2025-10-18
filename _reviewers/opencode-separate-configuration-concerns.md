---
title: Separate configuration concerns
description: Keep persistent user configuration separate from transient state, setup
  flags, and derived values. Persistent configuration should only contain user-defined
  settings that need to be saved across sessions. Transient state like cached detection
  results, setup completion flags, or runtime-derived values should be stored separately
  using dedicated state...
repository: sst/opencode
label: Configurations
language: Go
comments_count: 2
repository_stars: 28213
---

Keep persistent user configuration separate from transient state, setup flags, and derived values. Persistent configuration should only contain user-defined settings that need to be saved across sessions. Transient state like cached detection results, setup completion flags, or runtime-derived values should be stored separately using dedicated state management or separate files.

For example, instead of adding setup state to the main config:
```go
type Config struct {
    Providers     map[models.ModelProvider]Provider `json:"providers,omitempty"`
    Agents        map[AgentName]Agent               `json:"agents,omitempty"`
    SetupComplete bool                              `json:"setupComplete,omit"` // ❌ Don't mix setup state with config
}
```

Extract setup functionality into its own module or store in app state:
```go
// ✅ Keep config clean of transient state
type Config struct {
    Providers map[models.ModelProvider]Provider `json:"providers,omitempty"`
    Agents    map[AgentName]Agent               `json:"agents,omitempty"`
}

// ✅ Store transient state separately
type AppState struct {
    detectedTimeFormat *bool // cached detection result
    setupComplete      bool  // setup state
}
```

This separation improves maintainability, prevents config bloat, and makes it clear which data persists vs which is computed or temporary.