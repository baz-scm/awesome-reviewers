---
title: Harden container security
description: 'When building container images, ensure they''re compatible with restricted
  Kubernetes security contexts. Use numeric UIDs instead of symbolic usernames, and
  test compatibility with the following security constraints:'
repository: kubeflow/kubeflow
label: Security
language: Dockerfile
comments_count: 1
repository_stars: 15064
---

When building container images, ensure they're compatible with restricted Kubernetes security contexts. Use numeric UIDs instead of symbolic usernames, and test compatibility with the following security constraints:

```yaml
securityContext:
  runAsNonRoot: true
  allowPrivilegeEscalation: false
  capabilities:
    drop:
      - ALL
```

This approach prevents privilege escalation attacks and follows the principle of least privilege. For example, in a Dockerfile, prefer `USER 1000` over `USER jovyan` to ensure compatibility with security contexts that enforce non-root execution. This practice enhances security in various Kubernetes environments, including those that don't automatically apply these restrictions.
