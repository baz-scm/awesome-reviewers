---
title: minimize RBAC permissions
description: When defining RBAC rules and authorization policies, grant only the minimum
  necessary permissions required for the intended functionality. Avoid copying broad
  permission sets or including unnecessary verbs that expand the attack surface.
repository: kubernetes/kubernetes
label: Security
language: Yaml
comments_count: 1
repository_stars: 116489
---

When defining RBAC rules and authorization policies, grant only the minimum necessary permissions required for the intended functionality. Avoid copying broad permission sets or including unnecessary verbs that expand the attack surface.

Review authorization configurations to ensure they follow the principle of least privilege. For each resource and verb combination, verify that the permission is actually needed for the component's operation.

Example from Kubernetes RBAC:
```yaml
# Instead of granting multiple unnecessary verbs:
- apiGroups: [""]
  resources: ["pods/finalizers"]
  verbs: ["get", "list", "patch", "update", "watch"]  # Too broad

# Grant only what's actually needed:
- apiGroups: [""]
  resources: ["pods/finalizers"] 
  verbs: ["update"]  # Only what's meaningful for this use case
```

This practice reduces security risk by limiting the scope of potential privilege escalation and ensures that components cannot perform unintended operations even if compromised.