---
title: Configuration documentation standards
description: Ensure all user-configurable options are properly documented and discoverable,
  while keeping configuration files clean and focused. Configuration files serve as
  APIs that users rely on to understand available options.
repository: istio/istio
label: Configurations
language: Yaml
comments_count: 3
repository_stars: 37192
---

Ensure all user-configurable options are properly documented and discoverable, while keeping configuration files clean and focused. Configuration files serve as APIs that users rely on to understand available options.

Key principles:
1. **Document all settable values**: If a configuration can be set at the chart level, it must be defined in `values.yaml` with clear documentation
2. **Minimize noise**: Only include required and non-default values to reduce confusion about what is actually needed
3. **Distinguish internal vs user-facing**: Add comments to clarify when configuration options are for internal usage only
4. **Provide clear descriptions**: Use descriptive comments that explain the purpose and expected values

Example from Helm values:
```yaml
# values.yaml
global:
  # Labels to apply to all resources
  # Set this if you need custom labels on all chart resources
  customLabels: {}
  
  # Internal usage only - controls API version selection
  # Users should not modify this directly
  autoscalingv2API: true

# Avoid unnecessary defaults like:
# test_pod:
#   enabled: false  # Don't include if not needed
#   image: bats/bats:v1.1.0  # Don't include if disabled
```

This ensures users can easily discover configuration options while maintaining clean, focused configuration files that don't overwhelm with unnecessary details.