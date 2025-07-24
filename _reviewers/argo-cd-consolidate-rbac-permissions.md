---
title: consolidate RBAC permissions
description: Avoid duplicating RBAC permissions across different deployment configurations
  or installation modes. When the same service or controller needs permissions in
  multiple contexts (e.g., cluster-wide vs namespace-scoped deployments), consolidate
  these permissions into a unified, well-defined role structure rather than maintaining
  separate, potentially...
repository: argoproj/argo-cd
label: Security
language: Yaml
comments_count: 1
repository_stars: 20149
---

Avoid duplicating RBAC permissions across different deployment configurations or installation modes. When the same service or controller needs permissions in multiple contexts (e.g., cluster-wide vs namespace-scoped deployments), consolidate these permissions into a unified, well-defined role structure rather than maintaining separate, potentially inconsistent permission sets.

This practice ensures:
- Consistent security controls across deployment modes
- Reduced maintenance overhead and configuration drift
- Clearer permission auditing and review processes
- Prevention of over-privileged or under-privileged access scenarios

For example, instead of maintaining separate cluster roles and namespace roles with overlapping permissions, create a comprehensive role definition that can be appropriately scoped based on the deployment context:

```yaml
# Consolidated approach - single source of truth for permissions
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["create", "update"]
  - apiGroups: ["coordination.k8s.io"]  
    resources: ["leases"]
    verbs: ["create", "update"]
```

Review existing RBAC configurations to identify and eliminate permission duplication, ensuring that authorization controls remain consistent and maintainable across different deployment scenarios.