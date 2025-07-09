---
title: Consistent code organization
description: Maintain consistent patterns when organizing code elements within schema
  files. Place standard fields (like IDs and timestamps) first in all models to establish
  a predictable structure. Group similar elements together and position enum definitions
  at the bottom of schema files.
repository: elie222/inbox-zero
label: Code Style
language: Prisma
comments_count: 2
repository_stars: 8267
---

Maintain consistent patterns when organizing code elements within schema files. Place standard fields (like IDs and timestamps) first in all models to establish a predictable structure. Group similar elements together and position enum definitions at the bottom of schema files.

Example:
```prisma
model SomeModel {
  // Standard fields first
  id        String   @id @default(cuid())
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  
  // Model-specific fields next
  name      String
  status    Status
  
  // Relations last
  relatedItems RelatedItem[]
}

// Enums at the bottom of the file
enum Status {
  ACTIVE
  INACTIVE
}
```

This organization pattern improves code readability, makes navigation easier across the codebase, and helps team members quickly understand the structure of each schema file.