---
title: Complete API parameter documentation
description: 'API endpoints must include comprehensive documentation for all parameters.
  For each parameter, clearly specify:


  1. Whether it''s required or optional

  2. The data type and format'
repository: elastic/elasticsearch
label: API
language: Other
comments_count: 2
repository_stars: 73104
---

API endpoints must include comprehensive documentation for all parameters. For each parameter, clearly specify:

1. Whether it's required or optional
2. The data type and format
3. Default values when omitted
4. Validation rules and constraints (e.g., maximum values, character limits)
5. Accepted formats and encoding requirements
6. Behavior details (exact matching vs pattern matching)

This ensures consistency between API implementation and documentation, prevents integration issues, and improves developer experience.

Example:
```
`connector_name`::
(Optional, string) A comma-separated list of connector names, used to filter search results.
Default: Returns all connectors if omitted.
Maximum: 100 connector names.
Format: Exact matches only, URL-encoded values required for special characters.
Validation: Names must follow the same validation rules as defined in the creation API.
```

When updating APIs, ensure that parameter behavior aligns with UI expectations and vice versa to prevent disconnects between API functionality and user experience.
