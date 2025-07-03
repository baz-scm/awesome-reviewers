---
title: Stable configuration management
description: "Always ensure configuration values are managed consistently and sourced\
  \ from stable locations. \n\n1. Use defined constants instead of string literals\
  \ for configuration values to improve maintainability and reduce errors when values\
  \ change"
repository: kubeflow/kubeflow
label: Configurations
language: TSX
comments_count: 2
repository_stars: 15064
---

Always ensure configuration values are managed consistently and sourced from stable locations. 

1. Use defined constants instead of string literals for configuration values to improve maintainability and reduce errors when values change
2. Source configuration files from stable branches or tagged releases rather than potentially unstable sources like master
3. Clearly document when configuration values are environment-specific or will be overridden

Example:
```typescript
// ❌ Poor configuration management
enum ConfigPath {
  V05 = 'v0.5-branch/config/kfctl_config.yaml',
  V06 = 'master/bootstrap/config/kfctl_gcp_iap.yaml'  // Unstable source
}

const versionList = ['v0.7.0', 'v0.6.0'];  // Hard-coded literals

// ✅ Better configuration management
enum Version {
  V05 = 'v0.5.0',
  V06 = 'v0.6.0',
  V07 = 'v0.7.0'
}

enum ConfigPath {
  V05 = 'v0.5-branch/config/kfctl_config.yaml',
  V06 = 'v0.6-branch/config/kfctl_gcp_iap.0.6.yaml'  // Stable source
}

// Use constants and document environment-specific values
const versionList = [
  Version.V07,  // For local testing, will be overwritten by env vars
  Version.V06
];
```
