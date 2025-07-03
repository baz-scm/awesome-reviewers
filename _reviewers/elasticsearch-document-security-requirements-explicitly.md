---
title: Document security requirements explicitly
description: 'Always document security-related configurations, permissions, and behaviors
  explicitly and comprehensively. When documenting security features:


  1. Clearly specify required permissions and roles'
repository: elastic/elasticsearch
label: Security
language: Other
comments_count: 2
repository_stars: 73104
---

Always document security-related configurations, permissions, and behaviors explicitly and comprehensively. When documenting security features:

1. Clearly specify required permissions and roles
2. Note version-specific security behavior changes 
3. Explicitly state configuration inheritance rules and exceptions
4. Highlight security-critical settings with warnings or notes

For example, when documenting an API that interacts with protected resources:

```
IMPORTANT: This action requires specific permissions. In {es} 8.1 and later, the superuser 
role doesn't have write access to system indices. If you execute this request as a 
user with the superuser role, you must have an additional role with the 
`allow_restricted_indices` privilege set to `true` to delete system indices.
```

For configuration documentation:

```
NOTE: Transport profiles do not inherit TLS/SSL settings from the default transport.
The `xpack.security.transport.ssl.enabled` setting is an exception that controls
SSL for both default transport and any transport profiles.
```

Clear and complete security documentation prevents misconfigurations that could lead to vulnerabilities or access issues.
