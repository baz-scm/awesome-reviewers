---
title: SQLAlchemy 2.0 patterns
description: 'Migrate from legacy SQLAlchemy 1.x query patterns to modern 2.0 style
  for better performance, clarity, and future compatibility. This involves several
  key transformations:'
repository: langgenius/dify
label: Database
language: Python
comments_count: 14
repository_stars: 114231
---

Migrate from legacy SQLAlchemy 1.x query patterns to modern 2.0 style for better performance, clarity, and future compatibility. This involves several key transformations:

**Query Construction:**
- Use `select()` instead of `session.query()`
- Use `where()` instead of `filter()`

**Result Retrieval:**
- Use `session.scalar(stmt)` instead of `session.execute(stmt).scalars().first()`
- Use `session.scalars(stmt)` instead of `session.execute(stmt).scalars()`
- Be careful with column-specific queries - they require `session.execute(stmt)` not `session.scalars(stmt)`

**Example transformations:**

```python
# Legacy 1.x style
user = db.session.query(User).filter(User.id == user_id).first()
users = db.session.query(User).filter(User.active == True).all()

# Modern 2.0 style  
stmt = select(User).where(User.id == user_id)
user = db.session.scalar(stmt)

stmt = select(User).where(User.active.is_(True))
users = db.session.scalars(stmt).all()

# Column-specific queries (note: use execute, not scalars)
stmt = select(User.id, User.name).where(User.active.is_(True))
results = db.session.execute(stmt).all()
```

**Boolean Comparisons:**
Use `.is_(True)` or `.is_(False)` instead of `== True/False` for explicit boolean comparisons.

This migration improves code maintainability, leverages SQLAlchemy's latest optimizations, and ensures compatibility with future versions.