---
title: API examples completeness
description: Ensure all API code examples include all required parameters with correct
  placeholder values. Incomplete examples lead to user confusion and implementation
  errors when developers copy-paste documentation snippets.
repository: Unstructured-IO/unstructured
label: API
language: Other
comments_count: 3
repository_stars: 12117
---

Ensure all API code examples include all required parameters with correct placeholder values. Incomplete examples lead to user confusion and implementation errors when developers copy-paste documentation snippets.

When documenting API usage, always include:
- All required parameters, not just the most obvious ones
- Correct placeholder formats (e.g., use `<<REPLACE WITH YOUR API KEY>>` for keys, not URLs)
- Clear distinction between different parameter types (URLs vs keys vs other values)

Example of complete API documentation:

```python
elements = partition_via_api(
    filename=filename,
    api_key="<<REPLACE WITH YOUR API KEY>>",
    api_url="https://<<REPLACE WITH YOUR API URL>>/general/v0/general"
)
```

Rather than incomplete examples missing the `api_key` parameter or using incorrect placeholder values. Consider providing separate examples for different usage scenarios (SaaS vs self-hosted) when the parameter requirements differ significantly.