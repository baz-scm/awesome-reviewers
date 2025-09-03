---
title: Design extensible permission systems
description: When implementing authorization features, design permission systems that
  can accommodate future security requirements rather than adding permissions directly
  to existing tables. Create dedicated permission tables with proper relationships
  to entity tables to ensure authorization can be properly enforced.
repository: BerriAI/litellm
label: Security
language: Prisma
comments_count: 1
repository_stars: 28310
---

When implementing authorization features, design permission systems that can accommodate future security requirements rather than adding permissions directly to existing tables. Create dedicated permission tables with proper relationships to entity tables to ensure authorization can be properly enforced.

Instead of adding permission arrays directly to existing tables:
```prisma
model LiteLLM_TeamTable {
    // ... other fields
    mcp_servers String[] @default([])  // Avoid this approach
}
```

Create extensible permission tables with proper relationships:
```prisma
model LiteLLM_ObjectPermissionTable {
  permission_id  String         @id @default(uuid())
  mcp_servers    String[]       @default([])
  // Future permissions can be added here
}

model LiteLLM_VerificationToken {
  // ... other fields
  permission_id     String?
  object_permission LiteLLM_ObjectPermissionTable? @relation(fields: [permission_id], references: [permission_id])
}
```

This approach ensures that permission enforcement logic has a clear structure to work with and can be extended as new authorization requirements emerge without requiring schema migrations to core entity tables.