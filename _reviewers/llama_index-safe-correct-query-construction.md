---
title: Safe correct query construction
description: 'When building dynamic database queries, prioritize safety, correctness,
  and efficiency:


  1. **Parameterize values, never interpolate identifiers.** Bind parameters (`:param`,
  `?`) are only valid for literal values, not for table/column names, which the engine
  must resolve at parse/compile time. Table or column names coming from user input
  must be validated...'
repository: run-llama/llama_index
label: Database
language: Python
comments_count: 4
repository_stars: 52785
---

When building dynamic database queries, prioritize safety, correctness, and efficiency:

1. **Parameterize values, never interpolate identifiers.** Bind parameters (`:param`, `?`) are only valid for literal values, not for table/column names, which the engine must resolve at parse/compile time. Table or column names coming from user input must be validated against an allow-list or safely quoted — never passed through an f-string alongside bound value parameters as if they were interchangeable.
   ```python
   # Bad: table name interpolated, no validation
   stmt = f"SELECT * FROM `{table_name}` WHERE node_id IN :node_ids"

   # Good: validate/sanitize identifiers separately from bound values
   if not re.match(r"^[A-Za-z0-9_]+$", table_name):
       raise ValueError("Invalid table name")
   stmt = f"SELECT * FROM `{table_name}` WHERE node_id IN :node_ids"
   connection.execute(sqlalchemy.text(stmt), {"node_ids": tuple(node_ids)})
   ```

2. **Don't let query-building branches silently produce incorrect or vacuous results.** If a filter, threshold, or ordering clause isn't actually wired up for a given query mode (e.g., a similarity threshold that is never projected/applied for hybrid search), either implement it correctly or raise an explicit error/warning. Never let unsupported option combinations pass through quietly with no effect — add a test that actually exercises the failure case (e.g., `threshold > 0`, not just `threshold == 0.0`).

3. **Preserve required ordering/filtering semantics when allowing query customization.** When exposing hooks like `customize_query_fn` that let callers extend a generated query, apply the primary ordering/ranking clause (e.g., distance-based `ORDER BY`) before any user-supplied customization, so user extensions compose with (rather than silently override) the core ranking logic.

4. **Avoid pulling entire result sets into memory for operations that only need a projection.** When an operation only needs certain fields (e.g., IDs and metadata to perform a bulk update), request just those fields via the driver's projection/include mechanism instead of fetching full records, and use bulk update APIs rather than looping with full objects. This keeps the data layer scalable for larger collections.
   ```python
   # Bad: loads every full record into memory
   all_nodes = collection.get(where={"__index_id__": from_index_id})

   # Good: only fetch what's needed, then bulk update
   all_metadatas = collection.get(where={"__index_id__": from_index_id}, include=["metadatas"])
   ids = all_metadatas["ids"]
   updated = [{**m, "__index_id__": to_index_id} for m in all_metadatas["metadatas"]]
   collection.update(ids, metadatas=updated)
   ```

Apply these checks whenever adding or modifying query-building code, index/filter logic, or custom query hooks in any vector store, ORM, or raw SQL/NoSQL integration.