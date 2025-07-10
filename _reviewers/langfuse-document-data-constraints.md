---
title: Document data constraints
description: Explicitly document all input and output constraints directly in API
  definitions. For inputs, specify validation rules such as length limits, character
  restrictions, and value ranges. For outputs, detail the exact format of returned
  data structures, including array ordering, boundary conditions (inclusive/exclusive),
  and semantic meanings of values. This...
repository: langfuse/langfuse
label: API
language: Yaml
comments_count: 3
repository_stars: 13574
---

Explicitly document all input and output constraints directly in API definitions. For inputs, specify validation rules such as length limits, character restrictions, and value ranges. For outputs, detail the exact format of returned data structures, including array ordering, boundary conditions (inclusive/exclusive), and semantic meanings of values. This practice improves API clarity and reduces integration errors.

Example (for API responses):
```yaml
metrics:
  properties:
    data:
      type: array<array<number>>
      docs: |
        Histograms will return an array with [lower, upper, height] tuples, 
        where lower is inclusive, upper is exclusive, and bins are sorted by lower bound.
```

Example (for API requests):
```yaml
request:
  body:
    properties:
      name:
        type: string
        docs: Project name (must be between 3-30 characters)
```