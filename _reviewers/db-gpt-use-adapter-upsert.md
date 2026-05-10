---
title: Use Adapter Upsert
description: 'When writing to a database/graph store, make the storage adapter the
  source of truth for schema details and persist data idempotently.


  Apply these rules:'
repository: eosphoros-ai/DB-GPT
label: Database
language: Python
comments_count: 4
repository_stars: 18703
---

When writing to a database/graph store, make the storage adapter the source of truth for schema details and persist data idempotently.

Apply these rules:
- Don’t set storage-specific element metadata (e.g., `vertex_type`, `edge_type`) in business logic. Provide only domain fields; let the adapter derive types from its schema/config.
- Persist through adapter methods (not ad-hoc insert logic). Prefer `upsert*` APIs for vertices/edges/chunks/relations so repeated loads don’t create duplicates.
- Keep DB-wide configuration (charset/collation) at the database level, not per-table.

Example (graph store):
```python
# Bad: callers forcing storage element typing
# graph.upsert_vertex(Vertex(name, description=summary, vertex_type='entity'))

# Good: callers provide only domain data; adapter assigns types
graph.upsert_vertex(Vertex(name, description=summary))

# And when building relations from chunks/documents, route through adapter upsert helpers
graph_adapter.upsert_document_include_chunk(chunk=chunk, doc_vid=doc_vid)
graph_adapter.upsert_chunk_next_chunk(prev_chunk=prev, next_chunk=chunk)
```

Example (DB config principle):
- Set charset/collation when creating/configuring the database, rather than configuring it separately for each table.