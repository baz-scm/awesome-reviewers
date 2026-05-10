---
title: Documentation Precision
description: All documentation must accurately reflect product/API behavior, use exact
  feature names, and be unambiguous about constraints, defaults, and unsupported scenarios.
  Also ensure Markdown renders cleanly.
repository: infiniflow/ragflow
label: Documentation
language: Markdown
comments_count: 8
repository_stars: 80174
---

All documentation must accurately reflect product/API behavior, use exact feature names, and be unambiguous about constraints, defaults, and unsupported scenarios. Also ensure Markdown renders cleanly.

Apply this when editing or adding docs:
- **Match exact product/UI terminology**: use the same feature names as the product (e.g., “File” vs “File Management”) everywhere.
- **State exact behavior for edge cases**: if the UI allows non-integers, document how values are handled (e.g., rounding).
- **Fully define parameters and semantics**:
  - For API pagination, describe what `page` and `page_size` mean (offset/limit vs “records per page”) and keep parameter names typo-free.
- **Document defaults and constraints** (ranges, enable/disable conditions) and **include failure/unsupported cases** when a feature can’t be used as a retrieval source.
- **Keep Markdown clean and consistent**: remove unnecessary escaping (e.g., don’t escape `@` in normal Markdown) and standardize spacing/punctuation in READMEs.

Example (API param + constraint precision):
```md
## List files
**GET** `/api/v1/dataset/{dataset_id}/documents?keywords={keyword}&page={page}&page_size={page_size}`

- `page`: 0-based page index.
- `page_size`: number of records returned per page.

## Page rank
- Value type: integer
- Non-integers are rounded down.
- Range: [0, 100]
```