---
title: Feature gate configuration management
description: Ensure feature gates are properly managed across all configuration files
  and contexts. Feature-specific permissions, settings, and resources should be conditionally
  included based on appropriate feature gate guards rather than being present in default
  configurations. Avoid manually adding feature gates to configuration files when
  they are automatically...
repository: kubernetes/kubernetes
label: Configurations
language: Yaml
comments_count: 4
repository_stars: 116489
---

Ensure feature gates are properly managed across all configuration files and contexts. Feature-specific permissions, settings, and resources should be conditionally included based on appropriate feature gate guards rather than being present in default configurations. Avoid manually adding feature gates to configuration files when they are automatically managed by the system, as this can interfere with jobs that need to run with different feature combinations.

For beta and GA features, follow established patterns: beta features should typically be enabled by default, while alpha features remain disabled. When feature gates eventually get removed for GA features, replace feature gate references in test names and descriptions with plain text equivalents.

Example of proper feature gate guarding:
```yaml
# Good: Guard DRA-specific permissions behind feature gate
- apiGroups:
  - resource.k8s.io
  resources:
  - devicetaintrules
  verbs: [get, list, watch]
  # This should be guarded on DRADeviceTaints feature

# Avoid: Don't manually add feature gates when auto-managed
featureGates:
  DynamicResourceAllocation: true
  # DRAExtendedResource: true  # Let alpha job add this automatically
```

This ensures configurations remain clean, maintainable, and compatible with different deployment scenarios while preventing conflicts between manual and automatic feature gate management.