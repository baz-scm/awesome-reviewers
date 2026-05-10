---
title: Api examples clarity
description: 'API docs and interface examples must be unambiguous and cover defaults.


  Apply this standard when writing or updating API documentation:

  - **Validate example syntax**: For query strings, use **one** `?` to start the query
  and **`&`** for every additional parameter. Avoid ambiguous/incorrect examples like
  multiple `?` in the same query string.'
repository: celery/celery
label: API
language: Other
comments_count: 2
repository_stars: 28464
---

API docs and interface examples must be unambiguous and cover defaults.

Apply this standard when writing or updating API documentation:
- **Validate example syntax**: For query strings, use **one** `?` to start the query and **`&`** for every additional parameter. Avoid ambiguous/incorrect examples like multiple `?` in the same query string.
- **Show default behavior**: Provide at least one example demonstrating what the API does with default settings.
- **Demonstrate common conflicts/overrides**: If the API uses keys/slots where repeated inputs can collide (e.g., stamping the same key), include an example showing the resulting behavior.

Example (query param clarity):
```text
# Correct: one '?' then '&' for subsequent params
result_backend = 'gs://mybucket/some-prefix?gcs_project=myproject&firestore_project=myproject2&ttl=600'

# Wrong/ambiguous: multiple '?'
# result_backend = 'gs://...?...?firestore_project=...'
```

Example (default + collision behavior):
```py
sig = add.si(2, 2)
g = group(sig, add.si(3, 3))

# Show default stamping behavior (no custom stamp)
# g.stamp(...)

# Show repeated-key behavior explicitly
g.stamp(stamp='your_custom_stamp')
meta = sig.freeze()._get_task_meta()
```

This reduces user confusion and support load by ensuring examples match actual API semantics and defaults.