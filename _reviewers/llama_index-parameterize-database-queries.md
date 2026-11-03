---
title: Parameterize database queries
description: Never build database or query-language strings by interpolating variables
  (f-strings, string concatenation) directly into SQL/NoSQL query text. Untrusted
  or user-supplied values such as document IDs, filter values, `WHERE`/`OFFSET-LIMIT`
  clauses, or metadata values must be passed as bound parameters so the underlying
  driver escapes them and the query...
repository: run-llama/llama_index
label: Security
language: Python
comments_count: 5
repository_stars: 52785
---

Never build database or query-language strings by interpolating variables (f-strings, string concatenation) directly into SQL/NoSQL query text. Untrusted or user-supplied values such as document IDs, filter values, `WHERE`/`OFFSET-LIMIT` clauses, or metadata values must be passed as bound parameters so the underlying driver escapes them and the query structure cannot be altered.

For example, instead of:
```python
query = f"SELECT * FROM c WHERE c.ref_doc_id = '{ref_doc_id}'"
```
use parameter binding:
```python
query = "SELECT * FROM c WHERE c.ref_doc_id = @ref_doc_id"
parameters = [{"name": "@ref_doc_id", "value": ref_doc_id}]
```
The same applies to custom filter-building code (e.g., metadata filters in vector stores) — route every value through a shared escaping/quoting helper rather than re-implementing ad-hoc interpolation in each branch, so a value containing quotes or special characters can't break or hijack the query.

When a value genuinely cannot be parameterized (e.g., DDL statements, table/column names, identifiers, or clauses like `OFFSET n LIMIT n` that must be inlined), do not accept it as free-form raw text. Instead:
- Strictly validate the value against an expected format (e.g., regex `^OFFSET\s+\d+\s+LIMIT\s+\d+$`, or a whitelist of allowed characters/identifiers) before interpolating it.
- Document clearly in the API that such parameters accept raw query syntax and must never contain untrusted/user input.

Apply this consistently across all query-construction code paths (inserts, deletes, selects, filters) in a given store, not just the ones flagged in review — a fix in one method (e.g., `delete()`) should be mirrored in sibling methods (e.g., `_query()`, `_to_filter()`) that build similar queries.