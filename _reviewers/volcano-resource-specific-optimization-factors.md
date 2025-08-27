---
title: Resource-specific optimization factors
description: Configure different optimization parameters for different resource types
  (CPU, memory, GPU) rather than applying uniform settings across all resources. Different
  resources have distinct characteristics and usage patterns that require tailored
  optimization strategies for maximum performance and utilization.
repository: volcano-sh/volcano
label: Performance Optimization
language: Markdown
comments_count: 2
repository_stars: 4899
---

Configure different optimization parameters for different resource types (CPU, memory, GPU) rather than applying uniform settings across all resources. Different resources have distinct characteristics and usage patterns that require tailored optimization strategies for maximum performance and utilization.

For example, when implementing overcommit functionality, break down generic factors into resource-specific components:

```yaml
- plugins:
  - name: overcommit
    arguments:
      cpu-overcommit-factor: 1.2
      mem-overcommit-factor: 1.0  
      other-overcommit-factor: 1.2
```

Similarly, for GPU scheduling, consider CPU, memory, and GPU memory together with different weights and strategies:

```yaml
- plugins:
  - name: binpack
    arguments:
      binpack.cpu: 5
      binpack.memory: 1
      binpack.resources.nvidia.com/gpu: 2
```

This approach prevents suboptimal resource allocation that occurs when treating all resources uniformly, such as over-provisioning incompressible resources or under-utilizing resources with different performance characteristics. Always analyze the specific behavior and constraints of each resource type before applying optimization parameters.