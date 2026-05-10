---
title: Transactional delete and upsert
description: For database writes that can partially succeed (multi-step deletes/updates,
  bulk upserts with conflict handling), enforce invariants with **atomic transactions**,
  **explicit outcome validation**, and **engine-specific SQL encapsulation**.
repository: infiniflow/ragflow
label: Database
language: Python
comments_count: 3
repository_stars: 80174
---

For database writes that can partially succeed (multi-step deletes/updates, bulk upserts with conflict handling), enforce invariants with **atomic transactions**, **explicit outcome validation**, and **engine-specific SQL encapsulation**.

Apply this standard:
- Wrap helper methods that perform writes in `@DB.atomic()` (or an equivalent transaction boundary).
- After deletes/updates, validate affected-row counts against the expected scope (e.g., dedupe ids and check counts). If partial success breaks invariants, use a clearly justified compensating action.
- When supporting multiple DB engines, don’t assume identical upsert/conflict syntax—branch or adapterize the conflict resolution configuration, but keep the same invariant checks and error handling.

Example (pattern):
```python
@classmethod
@DB.atomic()
def delete_chunks(cls, chunk_ids, doc_id, kb_id):
    # dedupe inputs to make expected counts deterministic
    unique_ids = list(dict.fromkeys(chunk_ids or []))
    if not unique_ids:
        return 0

    condition = {"id": unique_ids, "doc_id": doc_id}
    try:
        deleted_count = settings.docStoreConn.delete(
            condition,
            search.index_name(DocumentService.get_tenant_id(doc_id)),
            kb_id,
        )
    except Exception:
        return 0

    # If partial deletion happened, restore consistency deterministically.
    if deleted_count == 0:
        raise ValueError("chunk deleting failure")
    if deleted_count < len(unique_ids):
        return settings.docStoreConn.delete(
            {"doc_id": doc_id},
            search.index_name(DocumentService.get_tenant_id(doc_id)),
            kb_id,
        )

    return deleted_count
```

Also ensure bulk upsert/bulk insert logic handles DB-specific conflict semantics (e.g., Postgres vs MySQL) inside the DB utility layer, while still using the same atomicity and validation rules at the call site.