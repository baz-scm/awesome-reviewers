---
title: Permission hierarchy awareness
description: When implementing permission checks, understand the hierarchical nature
  of permissions and avoid redundant checks. Higher-level permissions typically include
  lower-level ones. Ensure your authorization logic accounts for permission relationships
  to maintain security while keeping code efficient.
repository: vitejs/vite
label: Security
language: Yaml
comments_count: 1
repository_stars: 74031
---

When implementing permission checks, understand the hierarchical nature of permissions and avoid redundant checks. Higher-level permissions typically include lower-level ones. Ensure your authorization logic accounts for permission relationships to maintain security while keeping code efficient.

Example:
```javascript
// Inefficient - checks each permission separately
const hasAccess = data.user.permissions.triage || 
                 data.user.permissions.write || 
                 data.user.permissions.admin;

// Better - understands permission hierarchy
const hasAccess = ['triage', 'write', 'admin'].some(p => data.user.permissions[p]);

// Most efficient - if you know the hierarchy (write and admin include triage)
const hasAccess = data.user.permissions.triage || 
                 data.user.permissions.write || 
                 data.user.permissions.admin;
```

The most appropriate implementation depends on the system's permission model and whether permission hierarchies are guaranteed to remain consistent over time.