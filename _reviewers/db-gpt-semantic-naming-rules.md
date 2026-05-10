---
title: Semantic Naming Rules
description: 'Use names that accurately reflect meaning, scope (internal vs external),
  and responsibility—and keep them consistent with existing/base APIs.


  Apply these rules:'
repository: eosphoros-ai/DB-GPT
label: Naming Conventions
language: Python
comments_count: 8
repository_stars: 18703
---

Use names that accurately reflect meaning, scope (internal vs external), and responsibility—and keep them consistent with existing/base APIs.

Apply these rules:
1) **Internal fields vs user-visible concepts**: If a property is implicit/internal, name it consistently with an underscore prefix and ensure all relevant types expose it.
   - Example: store internal vectors on the graph vertex as `_embedding` (not `embedding`) and ensure `ParagraphChunk` provides `_embedding`.

2) **Match the data type/role to the identifier**: Don’t call vectors “keywords” or “text” if the value is embeddings.
   - Rename patterns: `keywords: List[List[float]]` → `subs` or `embeddings`.

3) **Responsibility-revealing function names**: The function name must describe what it actually does.
   - Example: if the function constructs and persists a document graph, prefer something like `def _load_doc_graph(self, chunks: List[Chunk]):` over `_parse_chunks`.

4) **Avoid duplicate/conflicting base names**: Don’t introduce new variants of fields already defined by base classes.
   - Example: remove redundant `_metadata` if `Knowledge` already owns the metadata concept.

5) **Avoid ambiguous configuration parameter names**: Prefer names that won’t be mistaken for other common concepts.
   - Example: use `model_alias` instead of `version` when the field is an alias used for registration.

6) **Use pythonic module/file naming**: Ensure filenames follow standard Python conventions (lowercase with underscores, no camel-case file names).

If you’re unsure, ask: “Can another developer infer the value’s meaning and the function’s side effects from the name alone?” If not, rename it.