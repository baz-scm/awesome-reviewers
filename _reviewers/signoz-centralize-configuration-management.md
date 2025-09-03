---
title: Centralize configuration management
description: Consolidate configuration parameters into centralized config structures
  instead of using scattered options structs or hardcoded values. Configuration should
  be owned and controlled by the appropriate component, with all related settings
  grouped together in well-organized config files.
repository: SigNoz/signoz
label: Configurations
language: Go
comments_count: 5
repository_stars: 23369
---

Consolidate configuration parameters into centralized config structures instead of using scattered options structs or hardcoded values. Configuration should be owned and controlled by the appropriate component, with all related settings grouped together in well-organized config files.

**Key principles:**
- Replace options structs with direct config parameter passing
- Move hardcoded values to configurable settings
- Group related configuration in single files that can handle multiple providers
- Ensure the controlling component manages its own configuration

**Example transformation:**
```go
// Before: Scattered options struct
type ServerOptions struct {
    FluxInterval               string
    FluxIntervalForTraceDetail string
    HTTPHostPort               string
    // ... many scattered options
}

func NewServer(serverOptions *ServerOptions) (*Server, error) {
    // Complex parsing and handling
}

// After: Centralized config with direct parameters
func NewServer(config signoz.Config, signoz *signoz.SigNoz, jwt *authtypes.JWT) (*Server, error) {
    // Direct access to organized config
    reader := clickhouseReader.NewReader(
        signoz.SQLStore,
        signoz.TelemetryStore,
        config.Querier.FluxInterval, // Controlled by the right component
        // ...
    )
}
```

This approach improves maintainability, reduces configuration drift, and ensures that components have proper ownership of their settings. Avoid hardcoded constants like timeout values or version strings - make them configurable through the centralized config system.