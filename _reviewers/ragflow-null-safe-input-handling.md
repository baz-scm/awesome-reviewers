---
title: Null-safe input handling
description: 'Apply null-safety consistently for request payloads, optional dict keys,
  and nullable fields. Specifically:


  - Guard `None` before doing comparisons/logic that assumes a value exists.'
repository: infiniflow/ragflow
label: Null Handling
language: Python
comments_count: 6
repository_stars: 80174
---

Apply null-safety consistently for request payloads, optional dict keys, and nullable fields. Specifically:

- Guard `None` before doing comparisons/logic that assumes a value exists.
- Don’t index dict keys that may be missing; use `dict.get(..., default)` (and prefer early returns).
- When building strings for output/storage, normalize nullable values to empty strings (avoid turning `None` into the literal "None").
- When merging/extending lists, extend with a default empty list if the source may be missing/nullable.

Example pattern:
```python
# 1) Guard None before comparisons
batch_size = max(1, int(os.getenv("PDF_PARSER_PAGE_BATCH_SIZE", "50")))
if total_pages is None or total_pages <= batch_size:
    run_single_pass()

# 2) Safe dict key access
content = chunk.get("content")
if not content:
    content = chunk.get("content_with_content") or ""

# 3) Avoid serializing None -> "None"
text = str(item.get("text") or "").strip()
if text:
    lines.append({"text": text})

# 4) Safe list merge
node0_attrs.setdefault("source_id", [])
node0_attrs["source_id"].extend(node1_attrs.get("source_id", []) or [])
node0_attrs["source_id"] = sorted(set(node0_attrs["source_id"]))
```

This prevents null-reference crashes and stops incorrect downstream data (like literal "None" strings) from being stored or emitted.