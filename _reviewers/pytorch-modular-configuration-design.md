---
title: Modular configuration design
description: 'Configuration systems should be designed with modularity and clarity
  in mind. When creating configuration classes or mechanisms:


  1. **Separate generic from specific configurations**: Organize configuration options
  by their scope and applicability. Use class hierarchies or namespaces to isolate
  domain-specific settings from generic ones.'
repository: pytorch/pytorch
label: Configurations
language: Other
comments_count: 3
repository_stars: 91345
---

Configuration systems should be designed with modularity and clarity in mind. When creating configuration classes or mechanisms:

1. **Separate generic from specific configurations**: Organize configuration options by their scope and applicability. Use class hierarchies or namespaces to isolate domain-specific settings from generic ones.

```cpp
// Good practice - clear separation of concerns
class AcceleratorAllocatorConfig {
  // Common settings applicable to all accelerators
};

class CUDAAllocatorConfig : public AcceleratorAllocatorConfig {
  // CUDA-specific settings
};
```

2. **Use descriptive, consistent naming conventions**: Configuration option names should clearly indicate their purpose and scope.
   - Avoid device-specific terms in generic interfaces (e.g., use `device_malloc` not `cudamalloc`)
   - Use consistent prefixes to group related options (e.g., `pinned_` for pinned memory settings)

3. **Document all configuration options**: Each option should have clear documentation explaining its purpose, valid values, and implications.

4. **Design for extensibility**: Implement hook mechanisms that allow domain-specific configurations to be integrated with generic ones.

5. **Propagate build-time configurations**: When generating configuration files (e.g., from .cmake.in templates), ensure build-time choices are properly encoded for downstream consumers.

These practices improve maintainability by making configuration systems more intuitive, better documented, and easier to extend for new devices or backends.