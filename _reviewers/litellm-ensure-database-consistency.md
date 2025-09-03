---
title: Ensure database consistency
description: Maintain data consistency by using appropriate database operations and
  ensuring transactional integrity when updating related fields. Choose the right
  ORM methods (upsert vs create) to handle potential duplicates, and ensure that updates
  to related fields across multiple tables happen atomically to prevent data drift.
repository: BerriAI/litellm
label: Database
language: Python
comments_count: 3
repository_stars: 28310
---

Maintain data consistency by using appropriate database operations and ensuring transactional integrity when updating related fields. Choose the right ORM methods (upsert vs create) to handle potential duplicates, and ensure that updates to related fields across multiple tables happen atomically to prevent data drift.

Key practices:
1. Use `upsert()` instead of `create()` when records might already exist to avoid UniqueViolationError
2. When updating related fields across multiple tables (like user.teams and team.members_with_roles), ensure both updates succeed or fail together
3. Use correct schema field names in ORM include/select operations

Example of proper upsert usage:
```python
# Instead of create() which can fail on duplicates
await self.prisma_client.db.litellm_managedobjecttable.upsert(
    where={"object_id": object_id},
    data=data,
    create=data
)

# Correct schema field names in includes
include={"end_users": True}  # Not "litellm_endusertable"
```

This prevents UniqueViolationError exceptions and maintains referential integrity across related database entities.