---
title: Enforce scope boundaries
description: When implementing hierarchical permission systems with scopes, ensure
  that permissions granted at a specific scope cannot be used to access resources
  or escalate privileges outside that scope's boundaries. This prevents lateral movement
  and privilege escalation attacks.
repository: gravitational/teleport
label: Security
language: Markdown
comments_count: 13
repository_stars: 19109
---

When implementing hierarchical permission systems with scopes, ensure that permissions granted at a specific scope cannot be used to access resources or escalate privileges outside that scope's boundaries. This prevents lateral movement and privilege escalation attacks.

Key validation requirements:
- Permissions within a scope must only apply to resources in the same scope or descendant scopes
- Resources created within a scope must have scope constraints equal to or more restrictive than their parent scope
- Administrative operations must be constrained to the scope where the role was granted
- Self-assignment of scope membership should be prevented or strictly validated

Example implementation:
```yaml
# Secure: Role created in /dev/lab scope with proper constraints
kind: role
metadata:
  name: lab-admin
spec:
  grantable_scopes: ['/dev/lab']  # Cannot grant broader than creation scope
  parent_resource_group: /dev/lab
  allow:
    rules:
    - resources: [node, app]
      verbs: [create, read, update, delete]
      # Implicitly scoped to /dev/lab and descendants only

# Insecure: Would allow privilege escalation
kind: role
spec:
  grantable_scopes: ['/']  # Broader than creation scope - should be rejected
  parent_resource_group: /dev/lab
```

This principle ensures that compromised credentials or roles cannot be used to affect resources outside their intended domain, maintaining proper security boundaries in multi-tenant or hierarchical systems.