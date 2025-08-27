---
title: Justify default enablement
description: When adding new configuration options, carefully consider whether features
  should be enabled by default. Require explicit justification for default enablement,
  weighing functionality benefits against compatibility risks and user impact.
repository: volcano-sh/volcano
label: Configurations
language: Yaml
comments_count: 3
repository_stars: 4899
---

When adding new configuration options, carefully consider whether features should be enabled by default. Require explicit justification for default enablement, weighing functionality benefits against compatibility risks and user impact.

Key considerations:
- **Compatibility**: Will default enablement break existing deployments or require newer system versions?
- **User necessity**: Is this feature essential for basic functionality or an optional enhancement?
- **Override complexity**: How difficult is it for users to change the default if needed?

Example from Helm values configuration:
```yaml
custom:
  # Don't enable by default - requires k8s v1.31+ APIs
  # feature_gates: DynamicResourceAllocation=true
  feature_gates: ""
  
  # Enable capability by default - core functionality
  root_queue:
    capability: true
```

When in doubt, prefer conservative defaults that maintain backward compatibility, and provide clear documentation on how users can enable advanced features when needed.