---
title: Enforce least privilege
description: Always assign the minimum permissions necessary for functionality when
  implementing role-based access controls. This fundamental security principle reduces
  the potential attack surface and minimizes the impact of compromised accounts.
repository: elastic/elasticsearch
label: Security
language: Java
comments_count: 1
repository_stars: 73104
---

Always assign the minimum permissions necessary for functionality when implementing role-based access controls. This fundamental security principle reduces the potential attack surface and minimizes the impact of compromised accounts.

Key practices:
1. Start with read-only permissions by default and add specific write permissions only where justified
2. Question and verify any broad write access permissions during code reviews
3. Separate read and write privileges in role definitions to make access patterns explicit
4. Regularly audit existing role permissions against actual usage needs

Example:
```java
// Good: Explicit, minimal permissions
RoleDescriptor.IndicesPrivileges.builder()
    .indices(ReservedRolesStore.ENTITY_STORE_V1_LATEST_INDEX)
    .privileges("read", "view_index_metadata")
    .build()

// Avoid: Unnecessarily broad permissions
RoleDescriptor.IndicesPrivileges.builder()
    .indices(ReservedRolesStore.ENTITY_STORE_V1_LATEST_INDEX)
    .privileges("read", "view_index_metadata", "write", "maintenance")
    .build()
```

When in doubt, start with more restrictive permissions and expand only when necessary based on functional requirements. Challenge assumptions about permission needs during code reviews, as shown in the discussion where write access was initially questioned and determined to be unnecessary.
