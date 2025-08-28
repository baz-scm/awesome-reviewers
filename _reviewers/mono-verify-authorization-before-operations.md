---
title: verify authorization before operations
description: Always verify that users have proper authorization to access and modify
  resources before performing any data operations. This prevents privilege escalation
  attacks and unauthorized data access.
repository: rocicorp/mono
label: Security
language: TypeScript
comments_count: 4
repository_stars: 2091
---

Always verify that users have proper authorization to access and modify resources before performing any data operations. This prevents privilege escalation attacks and unauthorized data access.

Key principles:
1. **Check visibility first**: Ensure users can see/access the resource before allowing any operations on it
2. **Validate operation permissions**: Verify the user has specific permissions for the intended operation (read, write, delete)
3. **Prevent impersonation**: Never allow users to change ownership or creator fields to other users, as this constitutes impersonation

Example implementation:
```typescript
async update(tx, change: UpdateValue<typeof schema.tables.issue>) {
  // First verify user can access the resource
  await assertIsAdminOrCreator(tx, tx.query.issue, change.id);
  
  // Then perform the operation
  await tx.mutate.issue.update(change);
}

// In permissions schema
select: [
  (authData, {exists}) =>
    exists('issue', q => q.where(eb => canSeeIssue(authData, eb))),
]
```

This pattern prevents scenarios where users could perform operations on resources they cannot see due to permission changes, and ensures consistent security enforcement across all data access patterns.