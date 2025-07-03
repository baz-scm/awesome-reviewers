---
title: Design for evolution
description: When designing APIs, prioritize flexibility and independent evolution
  of components. Avoid tightly coupling related services or wrapping existing components
  when they might evolve differently over time. Instead, design APIs with extension
  points and loose coupling to accommodate future changes.
repository: elastic/elasticsearch
label: API
language: Java
comments_count: 3
repository_stars: 73104
---

When designing APIs, prioritize flexibility and independent evolution of components. Avoid tightly coupling related services or wrapping existing components when they might evolve differently over time. Instead, design APIs with extension points and loose coupling to accommodate future changes.

For example, when designing request structures that may evolve differently between local and remote contexts:

```java
// Avoid tight coupling with wrapping
public class RemoteClusterStateRequest extends ActionRequest {
    // Duplicating fields to allow independent evolution
    private final String[] indices;
    private final boolean local;
    // other fields...
    
    // Instead of:
    // private final ClusterStateRequest clusterStateRequest;
}
```

For extensible APIs, consider using collections or generic structures that can be extended:

```json
// More extensible API design
"hybrid": {
  "fields": ["content", "content.semantic"],
  "query": "foo",
  "rank_modifiers": [
    {"rule": { ... }},
    {"rerank": { "inference_id": "my-reranker-service", "field": "content" }}
  ]
}

// Rather than fixed structures that are harder to extend:
"hybrid": {
  "fields": ["content", "content.semantic"],
  "query": "foo",
  "rule": { ... },
  "rerank": { "inference_id": "my-reranker-service", "field": "content" }
}
```

This approach makes APIs more resilient to changing requirements and easier to extend without breaking compatibility.
