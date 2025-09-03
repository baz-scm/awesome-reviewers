---
title: Database session lifecycle
description: Ensure all database operations and access to database objects occur within
  the appropriate session scope. Database objects become invalid once their session
  is closed, leading to runtime errors when accessed later.
repository: langflow-ai/langflow
label: Database
language: Python
comments_count: 2
repository_stars: 111046
---

Ensure all database operations and access to database objects occur within the appropriate session scope. Database objects become invalid once their session is closed, leading to runtime errors when accessed later.

Always perform database queries and access object attributes within the same session context. If you need to use database object attributes after the session, extract the needed values while the session is still active.

Example of the problem:
```python
async def update_build_config(self, build_config, field_value, field_name=None):
    if field_name == "knowledge_base":
        async with session_scope() as db:
            current_user = await get_user_by_id(db, self.user_id)
        # BAD: Accessing current_user.username after session is closed
        kb_user = current_user.username
```

Correct approach:
```python
async def update_build_config(self, build_config, field_value, field_name=None):
    if field_name == "knowledge_base":
        async with session_scope() as db:
            current_user = await get_user_by_id(db, self.user_id)
            # GOOD: Access attributes within session scope
            kb_user = current_user.username
```

Additionally, consider the timing of database availability checks. Operations that verify database state (like table existence) should occur after initialization is complete, not during the initial setup phase.