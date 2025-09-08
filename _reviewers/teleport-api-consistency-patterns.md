---
title: API consistency patterns
description: Maintain consistent API patterns and structures across different resource
  types and access methods within the same system. When designing new API fields or
  resources, follow established patterns from existing similar functionality rather
  than creating divergent approaches.
repository: gravitational/teleport
label: API
language: Markdown
comments_count: 5
repository_stars: 19109
---

Maintain consistent API patterns and structures across different resource types and access methods within the same system. When designing new API fields or resources, follow established patterns from existing similar functionality rather than creating divergent approaches.

For example, when adding Kubernetes access controls, follow the same pattern used for SSH access with `logins` traits and wildcard selectors, rather than creating Kubernetes-specific preset roles:

```yaml
# Consistent pattern - reuse existing access role with traits
tctl users add hugo --logins root --kubernetes-group teleport:preset:editor --roles=access

# Instead of creating new kube-specific roles
roles: [kube-access, kube-editor, kube-auditor]
```

Similarly, when extending existing resources, prefer embedding or reusing established field structures over creating entirely new schemas. If you must create new structures, ensure they follow the same naming conventions, required/optional field patterns, and default value behaviors as existing APIs.

This approach reduces cognitive load for users, ensures feature parity across interfaces (CLI, Web UI, API), and maintains a cohesive system architecture. Always check if similar functionality already exists before designing new API patterns.