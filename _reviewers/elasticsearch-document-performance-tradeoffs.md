---
title: Document performance tradeoffs
description: 'Always explicitly document the performance implications of API parameters,
  limit changes, and features that could significantly impact resource usage. When
  introducing functionality that offers a tradeoff between capabilities and performance,
  provide clear warnings and specific details about:'
repository: elastic/elasticsearch
label: Performance Optimization
language: Other
comments_count: 2
repository_stars: 73104
---

Always explicitly document the performance implications of API parameters, limit changes, and features that could significantly impact resource usage. When introducing functionality that offers a tradeoff between capabilities and performance, provide clear warnings and specific details about:

1. Memory consumption impacts
2. Response time implications
3. Scaling considerations for different cluster sizes

For example:

```asciidoc
`include_empty_fields`::
  (Optional, Boolean) If `false`, fields that never had a value in any shards are not included in the response.
  *WARNING*: Setting this parameter to `false` may significantly increase response times on large datasets due to
  additional field existence checks across all documents. Consider using the default value in performance-sensitive
  applications.
```

or

```asciidoc
NOTE: Synonyms sets consume heap memory proportional to their size. While the system supports up to 100,000 
synonym rules per set, large synonym sets may impact query performance and memory usage, especially on smaller
clusters. Monitor heap usage when working with large synonym sets.
```

This practice helps users make informed decisions about performance-sensitive configurations and prevents unexpected resource usage issues in production environments.
