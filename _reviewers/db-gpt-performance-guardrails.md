---
title: Performance Guardrails
description: 'When implementing knowledge-graph storage/search, proactively prevent
  expensive work and payload bloat by following these rules:


  1) Minimize returned payloads (especially vectors)'
repository: eosphoros-ai/DB-GPT
label: Performance Optimization
language: Python
comments_count: 5
repository_stars: 18703
---

When implementing knowledge-graph storage/search, proactively prevent expensive work and payload bloat by following these rules:

1) Minimize returned payloads (especially vectors)
- Store large embeddings under a field name that can be excluded via whitelist/filters (e.g., `_embedding` instead of `embedding`) so queries that don’t need vectors don’t fetch them.

2) Make one-time setup idempotent
- Any DDL/index creation that may be triggered by repeated upsert flows must be guarded by a “run once” flag (or persisted state), so SQL executes only once per process/config.

3) Batch compute for similarity search
- Prefer batch embedding APIs for multiple texts/queries instead of per-item embedding calls.

4) Bound expensive retrieval early
- Ensure graph expansion/search is constrained by `topk`/chunk limits during the query/explore step. Avoid relying on later “context trimming” hacks; constrain the result set at the source.

5) Avoid repeated iteration during persistence
- Split insertion/upsert logic by edge/node type to avoid scanning the same data multiple times.

Example (index-create guard pattern):
```python
class Adapter:
    def __init__(self):
        self._chunk_vector_index_created = False
        self._entity_vector_index_created = False

    def upsert_chunks(self, chunks):
        # ... upsert data ...
        if not self._chunk_vector_index_created:
            self._create_chunk_vector_index()
            self._chunk_vector_index_created = True

    def upsert_entities(self, entities):
        # ... upsert data ...
        if not self._entity_vector_index_created:
            self._create_entity_vector_index()
            self._entity_vector_index_created = True
```