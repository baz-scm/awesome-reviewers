---
title: Externalize configuration parameters
description: Create configurations that can be easily managed outside your application
  code. Design configuration parameters to be externalized through appropriate mechanisms
  like environment variables, config files, or Kubernetes custom resources (CRs).
  This improves manageability, enables GitOps workflows, and supports different deployment
  environments.
repository: kubeflow/kubeflow
label: Configurations
language: Markdown
comments_count: 4
repository_stars: 15064
---

Create configurations that can be easily managed outside your application code. Design configuration parameters to be externalized through appropriate mechanisms like environment variables, config files, or Kubernetes custom resources (CRs). This improves manageability, enables GitOps workflows, and supports different deployment environments.

For Kubernetes-based applications, consider using Custom Resources to abstract complex configurations:

```yaml
# Example: Using a custom resource for simplified configuration
apiVersion: kubeflow.org/v2
kind: Profile
metadata:
  name: ml
spec:
  resourceQuotaSpec:
    hard:
      cpu: "2"
      memory: 2Gi
      requests.nvidia.com/gpu: "1"
      persistentvolumeclaims: "1"
      requests.storage: "5Gi"
  # Optional: Add LimitRange configurations here
```

Key practices:
- Make configuration parameters like namespaces configurable rather than hardcoded
- Document the implications of configuration choices, especially when they affect data persistence
- Consider how configurations interact with mounted volumes or other external systems
- Prefer configuration mechanisms that support auditability and automated deployment
- Add ownership relationships to resources created from configurations to enable proper cleanup

When handling package installation in environments like notebooks, be aware of how configuration choices affect persistence across restarts and different environments.
