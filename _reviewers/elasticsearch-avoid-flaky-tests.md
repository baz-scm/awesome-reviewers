---
title: Avoid flaky tests
description: Design tests to be deterministic and reliable across different environments.
  Tests that occasionally fail due to timing, race conditions, or environmental differences
  waste development time and reduce confidence in the test suite.
repository: elastic/elasticsearch
label: Testing
language: Yaml
comments_count: 2
repository_stars: 73104
---

Design tests to be deterministic and reliable across different environments. Tests that occasionally fail due to timing, race conditions, or environmental differences waste development time and reduce confidence in the test suite.

When testing values that may vary based on environment conditions (like scores influenced by shard counts), use relative comparisons, before/after validations, or approximation matchers rather than exact values:

```yaml
# Instead of relying on exact scores which can vary:
- match: { hits.hits.0._score: 1.8918664 }

# Better - validate scores are different before/after modification:
- do:
    search:
      index: test-index
      body:
        query:
          match:
            field: "query text"
- set: { hits.hits.0._score: base_score }

- do:
    search:
      index: test-index
      body:
        query:
          match:
            field: 
              query: "query text"
              boost: 5.0
- gt: { hits.hits.0._score: $base_score }
```

Avoid "hacky" approaches that depend on timing. Instead, focus on testing that functionality exists without creating timing dependencies:

```yaml
# Avoid unreliable wait mechanisms:
- do:
    catch: request_timeout
    cluster.health:
      wait_for_nodes: 10
      timeout: "2s"

# Better - verify functionality exists without timing dependencies:
- do:
    cat.shards:
      index: foo
      h: refresh.is_search_idle
- match:
    $body: /^(false|true)\s*\n?$/
```
