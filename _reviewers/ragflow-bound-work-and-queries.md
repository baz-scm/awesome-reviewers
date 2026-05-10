---
title: Bound Work and Queries
description: When improving performance, make sure code neither (a) fetches too much
  data, nor (b) does the same expensive work repeatedly, nor (c) runs unbounded workloads.
repository: infiniflow/ragflow
label: Performance Optimization
language: Python
comments_count: 9
repository_stars: 80174
---

When improving performance, make sure code neither (a) fetches too much data, nor (b) does the same expensive work repeatedly, nor (c) runs unbounded workloads.

**Practical rules**
1. **Target by primary keys / narrow filters**: Prefer `get_by_id`-style lookups over broad tenant-scoped queries when you already have the identifier.
2. **Push filtering to the datastore**: If you currently fetch large result sets and filter in Python (or run many queries), move the filter into the ES/DB/search criteria (e.g., include `doc_id` / `source_id` in the search condition).
3. **Bound user-controlled heavy parameters**: Add upper bounds for things like `top_k` so a bad request can’t trigger massive retrieval.
4. **Batch/chunk heavy processing**: For page/document loops, use page batches to control memory/CPU and keep progress reporting accurate.
5. **Avoid repeated expensive work**: Hoist invariant computations out of inner loops, and run file-level expensive steps once (not per sheet/per iteration).
6. **Resource-heavy ops must be policy-driven**: If you unload/reload models or enable tracing, ensure it’s safe under concurrency (don’t unload while tasks run) and avoid enabling heavy instrumentation by default.

**Examples**
- Bound retrieval:
```python
top = int(req.get("top_k", 1024))
top = min(top, 200)  # cap user input
results = SearchService.search(..., top_k=top)
```
- Chunk heavy page processing:
```python
batch_size = max(1, int(os.getenv("PDF_PARSER_PAGE_BATCH_SIZE", "50")))
for page_from in range(from_page, to_page, batch_size):
    page_to = min(page_from + batch_size, to_page)
    __images__(fnm, page_from=page_from, page_to=page_to)
    chunk_boxes = parse_window_into_boxes()
    all_boxes.extend(to_global(chunk_boxes))
```
- Push doc_id/source_id filtering into search:
```python
# include source_id/doc_id in the search condition so the store filters
cond = {"source_id": [doc_id], **other_filters}
res = SearchService.search(dataset_id=dataset_id, condition=cond, limit=1)
```
