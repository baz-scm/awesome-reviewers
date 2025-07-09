---
title: Dynamic configuration needs validation
description: 'When implementing dynamic configuration options, validate that the system
  actually supports runtime changes for that setting. A configuration should only
  be marked as dynamic if:'
repository: vitessio/vitess
label: Configurations
language: Go
comments_count: 7
repository_stars: 19815
---

When implementing dynamic configuration options, validate that the system actually supports runtime changes for that setting. A configuration should only be marked as dynamic if:

1. The code actively monitors for changes to this value
2. The system can safely handle runtime updates
3. Changes are properly persisted according to configuration
4. Backwards compatibility is maintained

Example of proper dynamic config implementation:

```go
// Good: Dynamic config that's actually monitored
allowRecovery = viperutil.Configure(
    "allow-recovery",
    viperutil.Options[bool]{
        FlagName: "allow-recovery",
        Default:  true,
        Dynamic:  true, // System actively checks this value
    }
)

// Bad: Misleading dynamic flag
discoveryMaxConcurrency = viperutil.Configure(
    "discovery-max-concurrency", 
    viperutil.Options[int]{
        FlagName: "discovery-max-concurrency",
        Default:  300,
        Dynamic:  true, // Wrong! Value only checked during initialization
    }
)
```

For backwards compatibility, carefully consider default values and document any runtime limitations. When in doubt, mark as static rather than potentially misleading users about dynamic capabilities.