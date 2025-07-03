---
title: Specify explicit REST formats
description: 'Always specify explicit request formats in REST API tests rather than
  relying on default behaviors. This includes:


  1. Set appropriate Content-Type headers (typically application/json for REST APIs) '
repository: elastic/elasticsearch
label: API
language: Yaml
comments_count: 2
repository_stars: 73104
---

Always specify explicit request formats in REST API tests rather than relying on default behaviors. This includes:

1. Set appropriate Content-Type headers (typically application/json for REST APIs) 
2. Define explicit query parameters that clearly test intended functionality

Without proper format specifications, tests may fail unexpectedly or test incorrect behaviors. For example, missing Content-Type headers might cause an endpoint to default to different formats like cbor instead of JSON:

```yaml
- do:
    headers:
      Content-Type: application/json  # Explicitly specify format
    index:
      index: test
      id: 1
      body: { "field": "value" }
```

Similarly, when testing query parameters, be explicit about the expected behavior rather than using generic queries that might not fully test the intended functionality:

```yaml
retriever:
  standard:
    query:
      match_none: {}  # Explicitly testing empty results case
```

This practice improves test reliability and clarity by making the expected request format visible and intentional rather than implicit.
