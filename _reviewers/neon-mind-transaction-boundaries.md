---
title: Mind transaction boundaries
description: Be conscious of implicit transaction boundaries when working with databases.
  Programming constructs can create unexpected transaction scopes that affect behavior
  and performance.
repository: neondatabase/neon
label: Database
language: Python
comments_count: 2
repository_stars: 19015
---

Be conscious of implicit transaction boundaries when working with databases. Programming constructs can create unexpected transaction scopes that affect behavior and performance.

For example, in Python, the `with` block for database connections implicitly starts a transaction, causing all operations within the block to execute in a single transaction:

```python
# CAUTION: All operations execute in one transaction
with db.connect() as conn:
    conn.execute("INSERT INTO table1 VALUES (1)")
    conn.execute("INSERT INTO table2 VALUES (2)")
    # Both inserts committed or rolled back together
```

Similarly, be aware of which database commands create transaction boundaries. Commands like `CHECKPOINT` and `COMMIT` flush WAL logs, while others may have different transactional behavior:

```sql
-- Both sufficient to flush current WAL:
CHECKPOINT;
COMMIT;

-- Better than using pg_switch_wal() in many cases:
SELECT pg_current_wal_insert_lsn();
CHECKPOINT;
```

Choosing appropriate transaction boundaries improves reliability, performance, and maintainability of database operations.