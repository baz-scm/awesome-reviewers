---
title: Enforce least privilege
description: 'Configure all systems with the minimum permissions required to function.
  For Kubernetes deployments, use security contexts that prevent privilege escalation
  and running as root:'
repository: kubeflow/kubeflow
label: Security
language: Yaml
comments_count: 2
repository_stars: 15064
---

Configure all systems with the minimum permissions required to function. For Kubernetes deployments, use security contexts that prevent privilege escalation and running as root:

```yaml
securityContext:
  runAsNonRoot: true
  allowPrivilegeEscalation: false
  runAsUser: 65532  # Use specific non-root UID matching Dockerfile
```

For RBAC permissions, regularly audit and remove unnecessary permissions. Test thoroughly after removing permissions to ensure the application still functions correctly. When introducing new permissions, document their purpose and limit their scope as much as possible. Following this principle reduces attack surface and minimizes potential damage from compromised components.
