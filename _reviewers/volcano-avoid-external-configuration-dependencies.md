---
title: Avoid external configuration dependencies
description: When designing configuration management systems, avoid strong dependencies
  on external projects for configuration logic and data structures. External projects
  may not evolve at the same pace as your codebase, creating maintenance burdens and
  potential compatibility issues.
repository: volcano-sh/volcano
label: Configurations
language: Other
comments_count: 2
repository_stars: 4899
---

When designing configuration management systems, avoid strong dependencies on external projects for configuration logic and data structures. External projects may not evolve at the same pace as your codebase, creating maintenance burdens and potential compatibility issues.

Instead of relying on external configuration frameworks, internalize critical configuration components within your project. This includes rewriting essential configuration handlers, defining custom resource definitions (CRDs) for complex configuration data, and consolidating scattered configuration annotations into structured formats.

For example, rather than using multiple annotation entries for configuration state:
```
# Avoid: Multiple scattered annotations from external projects
annotations:
  nos.io/mig-profile-1: "free"
  nos.io/mig-profile-2: "used" 
  nos.io/pod-request-1: "profile-x"
```

Consolidate into a single, well-structured configuration:
```
# Prefer: Single consolidated configuration structure
annotations:
  volcano.sh/gpu-config: |
    {
      "migProfiles": [
        {"name": "profile-1", "status": "free"},
        {"name": "profile-2", "status": "used"}
      ],
      "requests": [{"profile": "profile-x"}]
    }
```

This approach ensures configuration evolution remains under your control and reduces external dependency risks.